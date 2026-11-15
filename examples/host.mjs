import assert from "node:assert/strict";
import { spawn, spawnSync } from "node:child_process";
import { randomBytes } from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { setTimeout as delay } from "node:timers/promises";

// Node.js 20+. Positional arguments avoid a CLI dependency in this host example.
const [servicePath, runtimePath, dataPath, model] = process.argv.slice(2);
assert.ok(servicePath && runtimePath && dataPath,
  "usage: node host.mjs SERVICE RUNTIME DATA [MODEL_ID_OR_PATH]");
const data = path.resolve(dataPath);
await fs.mkdir(data, { recursive: true });
const key = randomBytes(32).toString("hex");
const child = spawn(path.resolve(servicePath), [
  "serve", "--profile", "embedded", "--data-dir", data,
  "--runtime-dir", path.resolve(runtimePath), "--port", "0",
  "--api-key-env", "MODELBEANS_HOST_KEY", "--parent-pid", String(process.pid),
], {
  windowsHide: true,
  stdio: ["ignore", "inherit", "inherit"],
  env: { ...process.env, MODELBEANS_HOST_KEY: key },
});
let finished = false;
let spawnError;
const exited = new Promise((resolve) => {
  child.once("error", (error) => { spawnError = error; finished = true; resolve({ code: null }); });
  child.once("exit", (code, signal) => { finished = true; resolve({ code, signal }); });
});
let base;
const headers = { authorization: `Bearer ${key}`, "content-type": "application/json" };
const request = async (route, body, timeout = 10000) => {
  const response = await fetch(base + route, {
    method: body === undefined ? "GET" : "POST", headers,
    body: body === undefined ? undefined : JSON.stringify(body),
    signal: AbortSignal.timeout(timeout),
  });
  if (!response.ok) throw new Error(`${route}: HTTP ${response.status}: ${await response.text()}`);
  return response.headers.get("content-type")?.includes("application/json")
    ? response.json() : response.text();
};
try {
  const deadline = Date.now() + 90000;
  while (Date.now() < deadline) {
    if (finished) throw spawnError || new Error("Service exited before readiness");
    try {
      const receipt = JSON.parse(await fs.readFile(path.join(data, "state/endpoint.json"), "utf8"));
      // A killed previous run may leave a receipt. Never connect using that PID.
      if (receipt.pid === child.pid && receipt.port > 0 && receipt.host === "127.0.0.1") {
        base = `http://127.0.0.1:${receipt.port}`;
        try { await request("/ready"); break; } catch { base = undefined; }
      }
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    await delay(100);
  }
  if (!base) throw new Error("Service readiness timed out");
  console.log("Embedded service ready:", base);
  console.log(await request("/health"));
  if (model) {
    const waitTask = async (started) => {
      const deadline = Date.now() + 300000;
      while (Date.now() < deadline) {
        const task = (await request("/tasks")).data.find((task) => task.id === started.task_id);
        if (task?.status === "succeeded") return task;
        if (["failed", "cancelled"].includes(task?.status)) throw new Error(JSON.stringify(task));
        await delay(200);
      }
      throw new Error(`Task timed out: ${started.task_id}`);
    };
    let modelId = model;
    if (await fs.stat(model).then(() => true, (error) => { if (error.code === "ENOENT") return false; throw error; })) {
      modelId = "embedded-example-model";
      await waitTask(await request("/models/import", { path: path.resolve(model), id: modelId, copy: true }));
    }
    console.log(await waitTask(await request("/models/load", { model: modelId, device: "cpu" })));
    const completion = await request("/v1/chat/completions", {
      model: modelId, messages: [{ role: "user", content: "Reply with one short greeting." }],
      max_tokens: 256, stream: false,
      chat_template_kwargs: { enable_thinking: false },
    }, 300000);
    assert.ok(completion.choices?.[0]?.message?.content?.trim(), `Model returned no greeting; finish_reason=${completion.choices?.[0]?.finish_reason}`);
    assert.ok(completion.usage?.completion_tokens > 0, "Model returned no usage");
    console.log(JSON.stringify(completion, null, 2));
  }
} finally {
  if (base && !finished) {
    try { await request("/internal/shutdown", {}); }
    catch (error) { console.error("Graceful shutdown failed:", error.message); }
  }
  const timer = new AbortController();
  try {
    await Promise.race([exited, delay(15000, undefined, { signal: timer.signal })]);
  } finally { timer.abort(); }
  if (!finished && child.pid) {
    // Only the child owned by this host. Never kill by executable name.
    if (process.platform === "win32") {
      spawnSync("taskkill", ["/PID", String(child.pid), "/T", "/F"], { windowsHide: true });
    } else {
      child.kill("SIGKILL");
    }
  }
  const result = await exited;
  if (spawnError) throw spawnError;
  if (result.code !== 0) throw new Error(`Service exit: ${JSON.stringify(result)}`);
}
