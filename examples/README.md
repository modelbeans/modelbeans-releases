# Embedded host examples / 嵌入服务示例

| Language / 语言 | File / 文件 | Requirement / 要求 |
| --- | --- | --- |
| Python | [host.py](host.py) | Python 3.10+, standard library only / 仅标准库 |
| JavaScript | [host.mjs](host.mjs) | Node.js 20+, no third-party packages / 无第三方依赖 |

Follow the [English embedding guide](../docs/embedding.md) or [中文嵌入指南](../docs/embedding.zh-CN.md) for binary prerequisites, commands, expected output, and lifecycle details.

These examples start and stop their own service. They do not connect to an already running desktop instance. Without a model argument they check readiness and shutdown; with a model path or ID they also perform CPU inference. They do not automatically download binaries or models.

示例启动并关闭自己管理的服务，不连接已运行的桌面实例。不传模型参数时检查就绪和退出；传入模型路径或 ID 时增加 CPU 推理。不会自动下载程序或模型。

Public developer bundles are not yet available. Use version-matched service and runtime files, a private data directory, and a compatible model. See the guides before running.

公开开发包尚未提供。运行前需要匹配版本的服务与运行时文件、独立数据目录和兼容模型，请先阅读指南。
