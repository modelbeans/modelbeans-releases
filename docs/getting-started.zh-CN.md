# 快速上手

[返回项目介绍](../README.zh-CN.md) · [English](getting-started.md)

本指南面向 Windows x64 公开预览。从 [Release](https://github.com/modelbeans/modelbeans-releases/releases/tag/v0.1.97-rc.1) 的 Assets 获取安装包，先阅读[兼容范围与已知限制](compatibility.zh-CN.md)。模型另行下载。

## 跑通第一个模型

1. 安装并启动 ModelBeans，确认推理后端状态。若显示不可用，先记录错误信息并检查该发行版的运行时和驱动要求。
2. 打开模型市场，选择 Hugging Face 或魔搭 ModelScope。第一次建议选择内存需求较低、发行说明中验证过的文本模型。
3. 下载模型，或导入已有模型文件。下载完成并不等于已加载。
4. 在模型库中加载模型，选择可用设备和适当的上下文长度。更长上下文会消耗更多内存；先用较小配置跑通。
5. 在对话界面选择模型，发送一句简短问候。成功后再尝试看图、音频等功能，并为这些功能选择对应的模型与后端。

模型文件大小不是全部内存开销。上下文缓存、运行时和其他程序都会占用资源，界面估算也不是一定加载成功的保证。

## 调用本地 API

在 API 服务设置中启用服务，复制实际地址和本地 API Key。默认地址是 `http://127.0.0.1:10723`，以下示例按此地址编写。

| 客户端要求的配置 | 示例 |
| --- | --- |
| OpenAI 风格 Base URL | `http://127.0.0.1:10723/v1` |
| Ollama 兼容服务地址 | `http://127.0.0.1:10723`，按该客户端要求配置认证 |
| Anthropic 风格 Base URL | `http://127.0.0.1:10723`，消息路由为 `/v1/messages` |
| API Key | ModelBeans 本地服务设置中的密钥，不是云端供应商密钥 |
| Model | 实际模型 ID，或你已经配置好的别名 |

兼容接口不代表实现了上游产品的全部功能。若客户端需要特定接口或参数，请以该版本兼容清单为准。把端口改为 `11434` 或 `1234` 也不会自动获得完整的 Ollama 或 LM Studio 行为。

下面是 Windows PowerShell 示例。先将本地服务密钥放入当前进程环境变量 `MODELBEANS_API_KEY`，不要把密钥写进共享脚本；将模型 ID 替换为实际值，并确保已加载该模型。

```powershell
if (-not $env:MODELBEANS_API_KEY) { throw 'Set MODELBEANS_API_KEY first.' }
$baseUrl = 'http://127.0.0.1:10723'
$headers = @{ Authorization = "Bearer $env:MODELBEANS_API_KEY" }

# 查看服务公开的模型标识
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

`code` 之类的名字只有在配置了对应别名后才可使用。`/v1/models` 的列表也不表示每个模型都已经驻留内存。

## 接入编程助手或使用内置智能体

第三方工具：优先使用当前版本提供的客户端接入入口；手动配置时，填写上表中的协议、地址、密钥和模型。先测试一个简单请求，再测试工具调用。连接成功但工具调用失败时，可以运行智能体就绪评测，辅助判断模型能力。

内置智能体：选择模型、工作目录和工具权限，先在可丢弃的练习目录处理一个小任务。要使用云端，需单独配置供应商和数据授权。不要把尚在开发的智能路由视为稳定的自动任务分配功能。

## 常见问题

| 现象 | 先检查 |
| --- | --- |
| 连接被拒绝 | 服务是否启用、端口是否正确、是否仍在启动 |
| 401 / 403 | 本地服务密钥、客户端认证方式和权限 |
| 模型不存在 | 模型 ID / 别名是否正确，别名目标是否存在 |
| 内存不足或加载失败 | 模型与后端是否匹配，设备是否可用，上下文是否过大 |
| 客户端重复请求或工具调用失败 | 客户端协议兼容性、模型工具调用能力、上下文和日志 |

`127.0.0.1` 只指向当前机器。在另一台电脑填写同一地址，并不会连接到这台电脑的 ModelBeans。

关闭主窗口后，程序可能继续留在托盘中；需要完全退出时，请使用托盘的退出操作。

仍然无法解决时，请到 [Issues](https://github.com/modelbeans/modelbeans-releases/issues) 提供版本、硬件、模型、复现步骤和脱敏日志。

## 安装包校验

下载 EXE 及同名 `.sha256` 文件，运行以下命令并逐字比较哈希。GitHub 的 Source code ZIP 不是安装包。

```powershell
Get-FileHash .\ModelBeans-0.1.97-win-x64.exe -Algorithm SHA256
```
