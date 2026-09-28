# 使用本地大模型
# pip install -qU langchain-ollama
# pip install -U ollama

from langchain_ollama import ChatOllama

# 设置本地模型，不使用深度思考
# 默认的本地地址是  http://localhost:11434 ，model是本地安装了的地址
model = ChatOllama(
    base_url="http://localhost:11434", model="deepseek-r1:14b", reasoning=False
)
# 打印结果，
print(model.invoke("什么是LangChain，100字以内回答"))
