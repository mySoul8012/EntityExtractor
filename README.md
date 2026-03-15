以下是为你的 `app.py` 编写的 `README.md` 文件内容，说明如何运行、部署并使用你的 UIE 推理服务。

---

# UIE 推理服务

这是一个基于 Flask 和 Hugging Face 的 UIE (用户信息提取) 模型的推理服务。该服务提供了一个接口，允许你通过 HTTP 请求进行文本分析和实体抽取。

## 1. 项目介绍

本项目使用 `xusenlin/uie-base` 预训练模型进行实体抽取，并通过 Flask 提供一个简单的 REST API 接口。你可以通过 POST 请求将文本内容和 schema 提交到服务，返回的结果是推理后抽取的实体信息。

## 2. 环境要求

* Python >= 3.7
* `transformers` 库
* `Flask` 库
* `torch`（如果模型使用 PyTorch）

## 3. 安装依赖

首先，确保你已经安装了 Python 和 pip，然后运行以下命令安装项目的依赖：

```bash
pip install -r requirements.txt
```

或者单独安装需要的库：

```bash
pip install flask transformers torch
```

## 4. 项目结构

```plaintext
.
├── app.py          # Flask 服务主程序
├── requirements.txt # 依赖文件
└── README.md        # 本文档
```

## 5. 运行服务

在项目目录下运行以下命令启动 Flask 服务：

```bash
python app.py
```

Flask 服务将默认监听 `5000` 端口。你可以通过 `http://localhost:5000/infer` 访问推理接口。

### 启动日志示例：

```bash
加载 UIE 模型...
模型加载完成
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

## 6. 接口文档

### 请求方式：POST

* **URL**: `/infer`
* **请求体 (JSON)**:

```json
{
  "text": "这是一个测试文本。",
  "schema": ["实体1", "实体2", "实体3"]
}
```

**参数说明**：

* `text`: 需要进行实体抽取的文本内容。
* `schema`: 定义模型识别的实体类型，可以是列表或对象。

### 响应体 (JSON)

* **成功响应**：

```json
{
  "result": {
    "实体1": "识别出的实体内容",
    "实体2": "识别出的实体内容",
    "实体3": "识别出的实体内容"
  }
}
```

* **错误响应**：

如果请求体不符合要求或者推理过程中出现错误，服务将返回相应的错误信息：

```json
{
  "error": "错误信息"
}
```

### 错误代码

* `400`: 请求参数错误（如缺少 `text` 或 `schema`）。
* `500`: 推理过程中出现的服务器错误。

## 7. 测试接口

可以使用 `curl` 或 Postman 等工具来测试接口。

* **使用 curl 测试**：

```bash
curl -X POST http://localhost:5000/infer \
-H "Content-Type: application/json" \
-d '{"text": "这是一个测试文本。", "schema": ["实体1", "实体2"]}'
```

* **使用 Postman**：

  * 选择 POST 请求，设置 URL 为 `http://localhost:5000/infer`。
  * 在 Body 部分选择 raw 和 JSON 格式，输入请求体数据。

## 8. 部署到生产环境

当你准备将该服务部署到生产环境时，建议关闭 Flask 的调试模式，并使用 WSGI 服务器（如 Gunicorn）来运行应用。

### 示例：使用 Gunicorn 部署

首先，安装 Gunicorn：

```bash
pip install gunicorn
```

然后使用 Gunicorn 启动应用：

```bash
gunicorn -w 4 app:app
```

这将使用 4 个工作进程启动 Flask 应用，并且你可以将它部署到生产环境中。

## 9. License

本项目使用 [MIT License](LICENSE) 开源许可证。
