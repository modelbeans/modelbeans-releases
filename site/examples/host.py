"""Python 3.10+, standard library only: host.py SERVICE RUNTIME DATA [MODEL]."""
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.request


def main():
    if len(sys.argv) not in (4, 5):
        raise SystemExit(__doc__)
    service, runtime, data = map(lambda value: Path(value).resolve(), sys.argv[1:4])
    data.mkdir(parents=True, exist_ok=True)
    key = secrets.token_hex(32)
    child = subprocess.Popen([
        str(service), "serve", "--profile", "embedded", "--data-dir", str(data),
        "--runtime-dir", str(runtime), "--port", "0",
        "--api-key-env", "MODELBEANS_HOST_KEY", "--parent-pid", str(os.getpid()),
    ], env={**os.environ, "MODELBEANS_HOST_KEY": key}, stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
    base = None
    # Loopback traffic must not go through a host's configured HTTP proxy.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))

    def request(route, body=None, timeout=10):
        req = urllib.request.Request(base + route,
            data=None if body is None else json.dumps(body).encode("utf-8"),
            headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        with opener.open(req, timeout=timeout) as response:
            text = response.read().decode("utf-8")
            return json.loads(text) if response.headers.get_content_type() == "application/json" else text

    try:
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            if child.poll() is not None:
                raise RuntimeError("Service exited before readiness")
            try:
                receipt = json.loads((data / "state" / "endpoint.json").read_text(encoding="utf-8"))
            except FileNotFoundError:
                receipt = None
            if receipt and receipt["pid"] == child.pid and receipt["port"] > 0 and receipt["host"] == "127.0.0.1":
                base = "http://127.0.0.1:" + str(receipt["port"])
                try:
                    request("/ready")
                    break
                except (urllib.error.URLError, TimeoutError):
                    base = None
            time.sleep(0.1)
        if not base:
            raise TimeoutError("Service readiness timed out")
        print("Embedded service ready:", base, flush=True)
        print(request("/health"), flush=True)
        if len(sys.argv) == 5:
            model = sys.argv[4]
            def wait_task(started):
                deadline = time.monotonic() + 300
                while time.monotonic() < deadline:
                    task = next((item for item in request("/tasks")["data"] if item["id"] == started["task_id"]), None)
                    if task and task["status"] == "succeeded":
                        return task
                    if task and task["status"] in ("failed", "cancelled"):
                        raise RuntimeError(json.dumps(task))
                    time.sleep(0.2)
                raise TimeoutError("Task timed out: " + started["task_id"])
            if Path(model).exists():
                imported = request("/models/import", {"path": str(Path(model).resolve()), "id": "embedded-example-model", "copy": True})
                wait_task(imported)
                model = "embedded-example-model"
            print(wait_task(request("/models/load", {"model": model, "device": "cpu"})), flush=True)
            completion = request("/v1/chat/completions", {
                "model": model, "messages": [{"role": "user", "content": "Reply with one short greeting."}],
                "max_tokens": 256, "stream": False,
                "chat_template_kwargs": {"enable_thinking": False},
            }, 300)
            if not completion["choices"][0]["message"].get("content", "").strip():
                raise RuntimeError("Model returned no greeting; finish_reason=" + str(completion["choices"][0].get("finish_reason")))
            if completion.get("usage", {}).get("completion_tokens", 0) <= 0:
                raise RuntimeError("Model returned no usage")
            print(json.dumps(completion, ensure_ascii=False, indent=2), flush=True)
    finally:
        if base and child.poll() is None:
            try:
                request("/internal/shutdown", {})
            except (urllib.error.URLError, TimeoutError) as error:
                print("Graceful shutdown failed:", error, file=sys.stderr)
        try:
            child.wait(timeout=15)
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(child.pid), "/T", "/F"],
                    creationflags=subprocess.CREATE_NO_WINDOW, check=False)
            else:
                child.kill()
            child.wait(timeout=15)
        if child.returncode != 0:
            raise RuntimeError("Service exited with code " + str(child.returncode))


if __name__ == "__main__":
    main()
