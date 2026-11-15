# 0.1.97 preview: compatibility and known limitations

[简体中文](compatibility.zh-CN.md) · [Getting started](getting-started.md)

ModelBeans is developed on Windows PCs with Intel and AMD integrated graphics. The first public preview ships a Windows x64 installer including RuntimeShare; models are downloaded separately. Linux implementation exists, with a release planned after hardware validation. Discrete GPU integration and testing are planned for later.

Results do not transfer automatically between GPUs, drivers, model architectures or quantizations. Final AMD / Strata hardware acceptance for this candidate is still pending. Reports identifying the exact device and model are welcome.

| Backend | Included version | Scope |
| --- | --- | --- |
| llama.cpp | b12359 | CPU / Vulkan; real model generation previously verified on the Intel development machine |
| OpenVINO | Runtime 2026.4.1, GenAI 2026.4.1.0 | Native library loading verified; real OpenVINO model inference not yet validated for this upgrade |
| ONNX | GenAI 0.19.0, ORT DirectML 1.24.4, DirectML 1.15.4 | Small test model generation verified on CPU / DirectML, not universal ONNX model compatibility |
| stable-diffusion.cpp | master-1098-b521db4 | Z-Image Q4_K_M generation previously verified on Intel Vulkan; other combinations need separate validation |
| audio.cpp | 0.9.4 | Experimental; tasks, languages and reference-audio requirements vary by model |
| Strata | Suite 0.2.13, engine 0.1.59 | This Windows bundle uses AMD HIP. It does not run Strata on Intel integrated graphics; other backends remain separate options |

## Installation and resources

- The installer is approximately 629 MiB; the unpacked application and runtime are approximately 2.52 GiB. Shared runtime copies, extraction and temporary files need additional space. Allow at least 10 GiB before model downloads as a practical recommendation, not a measured installation peak or a minimum for every model.
- Model file size is not total inference memory. Context, output size, model components and other applications matter. Integrated GPU shared memory must not be counted again as additional system RAM.
- This preview is unsigned. Windows may show an unknown-publisher or SmartScreen prompt. Check the GitHub download source and SHA256; report the message if execution is blocked. Checksums verify file contents, not publisher identity.
- Download the installer from release **Assets**. GitHub's automatic **Source code** archives contain public documentation, not the application.

## Feature limits

- The agent is evolving. Connectivity and readiness checks do not guarantee success on complex tasks. Start in a disposable workspace, review tool permissions and file changes. Automatic smart routing is not promised in this release.
- The audio studio offers speech generation, voice cloning, song covers, music generation and sound design. Voice cloning requires compatible models and reference audio; quality varies by model, language and inputs.
- Connection entries cover Claude Code, Codex CLI, OpenCode, WorkBuddy, DeepSeek Harness and Marvis. Automated setup varies; Marvis requires manually saving connection details. API compatibility is endpoint-specific.
- Built-in performance and agent-readiness checks help model selection. The full BeansEval application is a separate future release.
- Embedded-service examples demonstrate process-based integration. A standalone RuntimeShare / SDK developer bundle is not yet published; the examples are not a complete SDK distribution.
- Local inference runs on the device. Downloads, configured cloud models and network-enabled tools still use the network.

Please report the version, OS, CPU/GPU, driver, model, backend and reproduction steps. Remove keys, personal paths and private file contents from reports.
