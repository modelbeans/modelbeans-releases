# Getting started

[Back to ModelBeans](../README.md) · [简体中文](getting-started.zh-CN.md)

This guide covers the Windows x64 public preview. Download the installer from [release Assets](https://github.com/modelbeans/modelbeans-releases/releases/tag/v0.1.97-rc.1) and read [compatibility and known limitations](compatibility.md). Models are downloaded separately.

## Run your first model

1. Install and start ModelBeans, then check the inference backend status. If a backend is unavailable, record the error and check the release's runtime and driver requirements.
2. Open the model marketplace and choose Hugging Face or ModelScope. Start with a small compatible text model.
3. Download the model or import an existing file. Downloaded does not mean loaded.
4. Load it from your model library, choosing an available device and a modest context length. Longer contexts consume more memory.
5. Select the model in chat and send a short greeting. Try image or audio features afterward, using the corresponding model and backend.

Model file size is only part of the memory requirement. Context caches, the runtime, and other applications also use memory; an estimate is not a guarantee that loading will succeed.

## Call the local API

Enable the API service in settings and copy its actual address and local API key. The default address, used below, is `http://127.0.0.1:10723`.

| Client setting | Example |
| --- | --- |
| OpenAI-style base URL | `http://127.0.0.1:10723/v1` |
| Ollama-compatible server address | `http://127.0.0.1:10723`; configure authentication as required by the client |
| Anthropic-style base URL | `http://127.0.0.1:10723`; messages use `/v1/messages` |
| API key | The key from ModelBeans local service settings, not a cloud provider key |
| Model | An actual model ID or an alias you have configured |

Compatibility does not mean every upstream feature is implemented. Check the release's compatibility notes for required endpoints and parameters. Changing the port alone does not change protocol compatibility.

For this Windows PowerShell example, supply the local service key through the current process environment variable `MODELBEANS_API_KEY`. Keep it out of shared scripts. Replace the model ID with your actual model and load it first.

```powershell
if (-not $env:MODELBEANS_API_KEY) { throw 'Set MODELBEANS_API_KEY first.' }
$baseUrl = 'http://127.0.0.1:10723'
$headers = @{ Authorization = "Bearer $env:MODELBEANS_API_KEY" }

# List the model identifiers exposed by the service.
Invoke-RestMethod -Uri "$baseUrl/v1/models" -Headers $headers

$body = @{
    model = 'YOUR_MODEL_ID'
    messages = @(@{ role = 'user'; content = 'Reply with a short greeting.' })
    max_tokens = 256
    chat_template_kwargs = @{ enable_thinking = $false }
    stream = $false
} | ConvertTo-Json -Depth 6

$reply = Invoke-RestMethod -Method Post -Uri "$baseUrl/v1/chat/completions" `
    -Headers $headers -ContentType 'application/json' -Body $body
$reply.choices[0].message.content
```

A name such as `code` only works after you configure that alias. A listing in `/v1/models` also does not mean the model is currently resident in memory.

## Connect a coding tool or use the built-in agent

For third-party tools, start with the client setup options available in your version. For manual setup, use the protocol, address, key, and model settings above. Try a simple request before testing tool calls. If basic requests work but tool calls fail, agent-readiness checks can help assess the model.

For the built-in agent, choose a model, workspace, and tool permissions. Start with a small task in a disposable practice directory. Cloud use requires separate provider configuration and data permissions. Smart routing remains under development; do not rely on it as a stable automatic task assignment feature.

## Troubleshooting

| Symptom | Check first |
| --- | --- |
| Connection refused | Service enabled, correct port, startup complete |
| 401 / 403 | Local service key, client authentication method, permissions |
| Model not found | Correct model ID / alias and an existing alias target |
| Out of memory or load failure | Model/backend compatibility, device availability, context length |
| Repeated requests or tool-call failures | Client protocol support, model tool-use ability, context, logs |

`127.0.0.1` always means the machine making the request. Entering it on another computer will not connect to your ModelBeans computer.

Closing the main window may leave the application running in the system tray. Use the tray's quit action to exit completely.

If you are still stuck, [open an issue](https://github.com/modelbeans/modelbeans-releases/issues) with your version, hardware, model, reproduction steps, and redacted logs.

## Verify the installer

Download the EXE and its .sha256 file, then compare the hash below with the file. GitHub Source code ZIPs are not installers.

```powershell
Get-FileHash .\ModelBeans-0.1.97-win-x64.exe -Algorithm SHA256
```
