# app.py
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModel

app = Flask(__name__)

# ====== 1. 全局加载模型 + Tokenizer ======
print("加载 UIE 模型...")
tokenizer = AutoTokenizer.from_pretrained("xusenlin/uie-base", trust_remote_code=True)
model = AutoModel.from_pretrained("xusenlin/uie-base", trust_remote_code=True)
print("模型加载完成")

# ====== 2. 定义推理 API 路由 ======
@app.route("/infer", methods=["POST"])
def infer():
    """
    接口说明:
    - 输入 JSON: {"text": "文本内容", "schema": [... 或 {...}]}
    - 输出 JSON: {"result": 推理结果}
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求 body 必须为 JSON"}), 400

    text = data.get("text")
    schema = data.get("schema")

    if not text or schema is None:
        return jsonify({"error": "参数 text 和 schema 必须提供"}), 400

    try:
        # 调用 UIE 推理
        res = model.predict(tokenizer, text, schema=schema)
        return jsonify({"result": res})
    except Exception as e:
        # 推理时出错
        return jsonify({"error": str(e)}), 500

# ====== 3. 启动 Flask 服务 ======
if __name__ == "__main__":
    # debug=True 开发模式可见错误信息，部署时建议 False
    app.run(host="0.0.0.0", port=5000, debug=True)