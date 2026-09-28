import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI

# .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
load_dotenv(encoding="utf-8")

# ========== ========== ========== ========== ==========  0.3版本的基础写法
"""## 0.3版本的基础写法 ChatOpenAI 支持所有模型的调用 """
chatLLM = ChatOpenAI(
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_URL"),
    model=os.getenv(
        "SILICONFLOW_MODEL"
    ),  # 此处以deepseek为例，您可按需更换模型名称 可以在对应的界面查找
)
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"},
]
response = chatLLM.invoke(messages)
print(f"ChatOpenAI 输出： \n {response.content}")

# ==================================================   1.0 版本的基础写法
"""
    1.0 版本的基础写法  init_chat_model  支持所有模型
    非标准模型需要同时指定model和model_provider
"""
model = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url=os.getenv("ALIQWEN_URL"),
    api_key=os.getenv("ALIQWEN_API"),
)
# 3.调用模型
print(f"init_chat_model 输出： \n {model.invoke('你是谁').content}")


# ==================================================  直接使用DeepSeek方法
"""'
    直接使用DeepSeek方法
    DeepSeek是 LangChain 默认支持的模型，他会自动查找对应的 BASE_URL 和 本地的 API_KEY,可以不用显示的配置,也可以指定
"""
model = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

print(model.invoke("什么是 Langchat？"))


# ==================================================  通义千问（阿里云百炼）
"""
    ChatTongyi已经慢慢废弃了
    后续可以考虑直接使用ChatOpenAI 
"""
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage

# .env文件读取
load_dotenv()

chatLLM = ChatTongyi(
    model="qwen-plus",
    streaming=True,  # 设置为 True 时可直接开启全局流式输出支持
    model_provider="openai",
)
# 打印结果
print(chatLLM.invoke("你是谁"))

print("*" * 60)
# 使用流式打印结果
res = chatLLM.stream([HumanMessage(content="你好，你是谁")], streaming=True)
for r in res:
    print("chat resp:", r.content)


# ==================================================  通义千问（阿里云百炼）
"""
    ChatTongyi已经慢慢废弃了
    后续可以考虑直接使用ChatOpenAI 
"""

from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage

chatLLM = ChatTongyi(
    model="qwen-plus",
    api_key=os.getenv("aliQwen-api"),
    streaming=True,
    # other params...
)
# 打印结果
print(chatLLM.invoke("你是谁"))
