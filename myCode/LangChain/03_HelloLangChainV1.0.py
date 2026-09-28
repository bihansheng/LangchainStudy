# LangChain1.0+版本使用方式,目前主流,多模型共存


# 1.导入依赖
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
load_dotenv()

# 2.实例化模型
# model = init_chat_model(
#     model="qwen-plus",
#     model_provider="openai",
#     api_key=os.getenv("QWEN_API_KEY"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )
#
# # 3.调用模型
# print(model.invoke("你是谁").content)
#
# print("*" * 70)

# 4.实例化模型v2
"""
说明：
model="deepseek-chat" 和 base_url="https://api.deepseek.com" 
DeepSeek 是LangChain支持的模型
刚好匹配默认的 model_provider（如 deepseek），因此无需显式传入，函数内部做了智能推导
LangChain ：LangChain 的底层机制会自动尝试去系统的环境变量（os.environ）中寻找预设名称的 API Key。所以这里也没有显示设定
如果切换成其他模型（如 OpenAI），若默认值不匹配，就需要显式指定 model_provider="openai"。
什么是关键字参数  key1 = value1 ,key2 = value2
"""
model = init_chat_model(
    model="deepseek-chat",  # deepseek-chat 对应 DeepSeek-V3.2 的非思考模式
    model_provider="deepseek",
)


# 5.调用模型v2
respone = model.invoke("你是谁")
print(model.__dict__)
print(respone)
print(respone.content)
