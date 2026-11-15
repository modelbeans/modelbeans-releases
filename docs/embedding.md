# Add local inference to your application

[Back to ModelBeans](../README.md) · [简体中文](embedding.zh-CN.md) · [Example code](../examples/README.md)

Your application can start a dedicated ModelBeans service and call models over HTTP. The service owns a separate data directory, dynamic port, and key, without requiring the desktop window to be open.

This is child-process embedding: `Your application → ModelBeans service → RuntimeShare → inference backend`. This guide uses the application service's HTTP interface, rather than the lower-level `beansd` protocol, and requires no language-specific SDK.

> A public service/runtime developer bundle is not available yet. These examples are for integration preparation and local trials; actual inference requires matching service and runtime binaries. Do not assume the desktop installer is a complete embedding bundle.

## Prepare the files

An example Windows layout:

```text
C:/my-app/bundle/
  modelbeans-app-service.exe
  runtime/                      # Preserve the release's complete runtime layout.
    beansd.exe
    ...                         # Required workers, libraries, and license files.
C:/my-app/data/                 # Persistent data, outside the replaceable bundle.
C:/models/example.gguf          # A separately obtained small CPU-compatible text model.
```

Use a runtime directory from a matching release combination. Do not copy only `beansd.exe` or flatten DLL subdirectories. Include the worker and libraries your model needs; omit unused capabilities only as documented by the developer bundle.

## Run a complete example

Copy the scripts from [examples](../examples/README.md). Use Python 3.10+ or Node.js 20+; neither needs extra packages. Replace these sample paths with your own absolute paths.

First check startup and shutdown, using either language:

```powershell
python ./examples/host.py C:/my-app/bundle/modelbeans-app-service.exe C:/my-app/bundle/runtime C:/my-app/data/python
node ./examples/host.mjs C:/my-app/bundle/modelbeans-app-service.exe C:/my-app/bundle/runtime C:/my-app/data/node
```

Add a model path to import it, load it on CPU, and generate a greeting:

```powershell
python ./examples/host.py C:/my-app/bundle/modelbeans-app-service.exe C:/my-app/bundle/runtime C:/my-app/data/python C:/models/example.gguf
node ./examples/host.mjs C:/my-app/bundle/modelbeans-app-service.exe C:/my-app/bundle/runtime C:/my-app/data/node C:/models/example.gguf
```

Quote paths containing spaces. The example copies the model into its private data directory, preserving the original and requiring additional disk space. After the first import, you can use `embedded-example-model` as the last argument to reuse that directory's model. Do not run multiple services concurrently against the same data directory.

Expected output starts with the ready service address and health information. With a model argument, it also includes the load task result and generated reply, followed by service shutdown. A run without a model only checks lifecycle, not real inference.

## What does the example do?

1. Generate a random administrator key, pass it through the environment, and start the child with `serve --profile embedded`, a private data directory, and `--port 0`.
2. Wait for `state/endpoint.json` in that directory, verify that its PID belongs to the child and its host is loopback, then call authenticated `/ready` and `/health`.
3. For a file path, call `/models/import` with `copy: true` and poll `/tasks`. Call `/models/load` and wait for loading to finish.
4. Call `/v1/chat/completions`, checking for a nonempty reply and positive output token usage.
5. Request `/internal/shutdown` and wait for exit. On timeout, terminate only the owned child, including its process tree on Windows.

Startup allows 90 seconds, model task waits and inference requests allow five minutes each, and graceful shutdown allows 15 seconds. Very large models may require a different host timeout policy. This demonstrates lifecycle management; it is not a complete production host.

## Connect your own workflow

Replace the greeting request with your application logic between readiness and shutdown. Common operations include:

| Operation | HTTP interface |
| --- | --- |
| Browse installable models | `GET /models/catalog` |
| Install a catalog model | `POST /models/install`, body `{"model":"CATALOG_ID"}` |
| Track installation, import, and loading | `GET /tasks` |
| Import local files | `POST /models/import` |
| Load / unload | `POST /models/load` / `POST /models/unload` |
| Generate a reply | `POST /v1/chat/completions` |

The examples do not download models automatically. Unloading releases runtime resources; it does not delete model files.

All embedded-profile endpoints require authentication. Keep the administrator key in the trusted host, away from untrusted pages or renderers. `endpoint.json` provides discovery, not proof of live readiness. Desktop and agent routes are not exposed by this profile.

During upgrades, replace the application and runtime while retaining your application's persistent data. Test new combinations in a separate directory first. Do not reuse the desktop application's data directory or terminate processes by executable name.

## Distribute your application

Ship the service, matching RuntimeShare, required libraries, licenses, and NOTICE files together, recording their version compatibility. Separately downloaded or bundled models retain their own license and access conditions.

RuntimeShare's Apache-2.0 binary license permits embedding, commercial use, and redistribution under its terms. It does not replace third-party or model licenses. When the developer bundle is published, also validate against its compatibility matrix on your target hardware.
