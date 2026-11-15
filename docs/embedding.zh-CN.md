# 给你的应用加上本地推理

[返回项目介绍](../README.zh-CN.md) · [English](embedding.md) · [示例代码](../examples/README.md)

你可以让自己的程序启动一个专用的 ModelBeans 服务，再通过 HTTP 调用模型。这个服务使用自己的数据目录、动态端口和密钥，不依赖用户打开桌面窗口。

这是子进程嵌入方式：`你的程序 → ModelBeans 服务 → RuntimeShare → 推理后端`。本指南使用应用服务的 HTTP 接口，不直接调用底层 `beansd` 协议，也不要求安装语言专用 SDK。

> 对应的公开服务/运行时开发包尚未发布。以下示例供准备集成和本地试用；需要取得版本匹配的服务与运行时文件后才能实际推理。桌面安装包不应被默认当成完整的嵌入开发包。

## 准备文件

Windows 示例布局：

```text
C:/my-app/bundle/
  modelbeans-app-service.exe
  runtime/                      # 保留发行包中的完整运行时目录布局
    beansd.exe
    ...                         # 所需推理 worker、依赖库和许可文件
C:/my-app/data/                 # 持久数据，放在可升级替换的 bundle 之外
C:/models/example.gguf          # 另外准备的、兼容 CPU 的小型文本模型
```

运行时目录应来自匹配的发行组合。不要只复制 `beansd.exe`，不要打平 DLL 子目录。模型所需的 worker 和依赖库必须存在；不需要的能力可以按开发包说明裁剪。

## 运行完整示例

下载或复制 [examples](../examples/README.md) 中的脚本。Python 需要 3.10+；Node.js 需要 20+，两者都不需要额外安装依赖包。下面的路径是示例，请替换为自己的绝对路径。

先验证启动与退出，任选一种语言：

```powershell
python ./examples/host.py C:/my-app/bundle/modelbeans-app-service.exe C:/my-app/bundle/runtime C:/my-app/data/python
node ./examples/host.mjs C:/my-app/bundle/modelbeans-app-service.exe C:/my-app/bundle/runtime C:/my-app/data/node
```

再增加模型路径，完成导入、CPU 加载与一次问候推理：

```powershell
python ./examples/host.py C:/my-app/bundle/modelbeans-app-service.exe C:/my-app/bundle/runtime C:/my-app/data/python C:/models/example.gguf
node ./examples/host.mjs C:/my-app/bundle/modelbeans-app-service.exe C:/my-app/bundle/runtime C:/my-app/data/node C:/models/example.gguf
```

路径含空格时加引号。示例会复制模型到独立数据目录，保留原文件，因此需要额外磁盘空间。首次导入后，也可以把最后一个参数换成 `embedded-example-model`，复用该数据目录中的模型。不要在同一个数据目录中并行运行多个服务。

预期输出依次是服务就绪地址、健康信息；指定模型时还会输出加载任务结果和模型回复，随后服务退出。没有模型参数时只检查生命周期，不代表真实推理通过。

## 示例做了哪些工作？

1. 生成随机管理密钥，通过环境变量传给子进程；使用 `serve --profile embedded`、独立数据目录和 `--port 0` 启动服务。
2. 等待数据目录中的 `state/endpoint.json`，确认 PID 属于刚启动的进程、地址为本机回环，再请求带认证的 `/ready` 与 `/health`。
3. 指定文件路径时调用 `/models/import`（`copy: true`），轮询 `/tasks`；随后调用 `/models/load`，等待加载完成。
4. 调用 `/v1/chat/completions`，检查回复非空且输出 token 用量大于零。
5. 请求 `/internal/shutdown` 并等待退出；超时只终止自己启动的进程，Windows 下包含其进程树。

启动等待上限为 90 秒；模型任务等待和推理请求上限分别为 5 分钟；正常退出等待 15 秒。超大模型可能需要调整宿主程序的等待策略。这是生命周期示例，不是完整生产宿主。

## 接入自己的业务

在示例的服务就绪后到关闭前之间，替换问候请求为自己的业务调用。常见操作：

| 需求 | HTTP 接口 |
| --- | --- |
| 查看可安装目录 | `GET /models/catalog` |
| 安装目录内模型 | `POST /models/install`，请求体 `{"model":"CATALOG_ID"}` |
| 跟踪安装、导入与加载 | `GET /tasks` |
| 导入本地文件 | `POST /models/import` |
| 加载 / 卸载 | `POST /models/load` / `POST /models/unload` |
| 生成回复 | `POST /v1/chat/completions` |

示例不自动下载模型。卸载释放模型运行资源，不等于删除模型文件。

嵌入配置下所有接口都需要认证。管理密钥由可信宿主持有，不应暴露给不可信网页或渲染进程。`endpoint.json` 用于发现地址，不能替代实时就绪检查。此配置不开放桌面和智能体接口。

升级时替换程序与运行时，保留应用自己的持久数据；先在独立目录验证新组合。不要复用桌面版的数据目录，也不要按可执行文件名批量结束进程。

## 分发给用户

将服务、匹配的 RuntimeShare、所需依赖库、许可证和 NOTICE 一起交付，记录版本对应关系。模型另行下载或分发时，遵守其各自许可和访问条件。

RuntimeShare 二进制的 Apache-2.0 许可允许遵照许可嵌入、商用与再分发；这不替代第三方组件和模型许可。正式开发包发布后，还应按其兼容清单在目标硬件上验证。
