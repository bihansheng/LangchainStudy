import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# .env文件读取
load_dotenv()

llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3",
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url="https://api.siliconflow.cn/v1",
)
messages = [
    {"role": "system", "content": "你是一个有用的助手"},
    {"role": "user", "content": "你好，请介绍一下你自己"},
]

respone = llm.invoke(messages)
print(llm.__dict__)
print(respone)
print(respone.content)
