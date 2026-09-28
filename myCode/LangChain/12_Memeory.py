# 记忆缓存是聊天系统中的一个重要组件，用于存储和管理对话的上下文信息。它的主要作用是让AI助手能够”记住”之前的对话内容，从而提供连贯和个性化的回复。


"""
BaseChatMessageHistory简介
是用来保存聊天消息历史的抽象基类
    1、messages: List[BaseMessage]：用来接收和读取历史消息的只读属性
    2、add_messages：批量添加消息，默认实现是每个消息都去调用一次add_message
    3、add_message：单独添加消息，实现类必须重写这个方法，否则会抛出异常
    4、clear()：清空所有消息，实现类必须重写这个方法

常用组件
    InMemoryChatMessageHistory      基于内存存储的聊天消息历史组件
    FileChatMessageHistory          基于文件存储的聊天消息历史组件
    RedisChatMessageHistory         基于Redis存储的聊天消息历史组件     最常用
    ElasticsearchChatMessageHistory 基于ES存储的聊天消息历史组件



"""

"""
可持续记忆（RunnableWithMessageHistory）

BaseChatMessageHistory 与 RunnableWithMessageHistory 配合使用

InMemoryChatMessageHistory 创建内存聊天历史记录实例，用于存储对话历史，数据存在内存中，重启系统就会丢失
RunnableWithMessageHistory 创建带消息历史的可运行对象，用于处理带历史记录的对话
在提示词中插入历史消息
prompt = ChatPromptTemplate.from_messages([
    # 用于插入历史消息
    MessagesPlaceholder(variable_name="history"),  # 用于插入历史消息
    ("human", "{input}")
])    
"""

# 版本1 ，基于LangChain 0.3

# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
# from langchain.chat_models import init_chat_model
# from langchain_core.chat_history import InMemoryChatMessageHistory
# from langchain_deepseek import ChatDeepSeek
# from loguru import logger
# import os

# # 设置本地模型
# from dotenv import load_dotenv

# # .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
# load_dotenv(encoding="utf-8")

# llm = ChatDeepSeek(model="deepseek-chat")

# # 定义 Prompt
# prompt = ChatPromptTemplate.from_messages(
#     [
#         # 用于插入历史消息
#         MessagesPlaceholder(variable_name="history"),
#         ("human", "{input}"),
#     ]
# )

# parser = StrOutputParser()
# # 构建处理链：将提示词模板、语言模型和输出解析器组合
# chain = prompt | llm | parser
# # 创建内存聊天历史记录实例，用于存储对话历史
# history = InMemoryChatMessageHistory()
# # 创建带消息历史的可运行对象，用于处理带历史记录的对话
# runnable = RunnableWithMessageHistory(
#     chain,
#     get_session_history=lambda session_id: history,
#     input_messages_key="input",  # 指定输入键
#     history_messages_key="history",  # 指定历史消息键
# )
# # 清空历史记录
# history.clear()
# # 配置运行时参数，设置会话ID
# config = RunnableConfig(configurable={"session_id": "user-001"})
# logger.info(runnable.invoke({"input": "我叫张三，我爱好学习。"}, config))
# logger.info(runnable.invoke({"input": "我叫什么？我的爱好是什么？"}, config))


# """
# 可持续记忆（RunnableWithMessageHistory）

# 版本 2 基于LangChain 1.0，
# 逻辑和版本 1 一致，只是一些方法使用了不同的写法，尤其是 LangChain 本身方法的写法习惯

# """

# from langchain.chat_models import init_chat_model
# from langchain_core.chat_history import InMemoryChatMessageHistory  # 内存型消息记录
# from langchain_core.runnables.history import RunnableWithMessageHistory
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.output_parsers import StrOutputParser
# import os

# # 设置本地模型
# model = init_chat_model(
#     model="qwen-plus",
#     model_provider="openai",
#     base_url=os.getenv("ALIQWEN_URL"),
#     api_key=os.getenv("ALIQWEN_API"),
# )

# # 定义全局的“会话存储”，用来保存每个 session 的聊天历史
# #    （真实项目中可改为 Redis、SQLite 等）
# store = {}

# def get_session_history(session_id: str):
#     """
#     根据 session_id 获取对应的历史消息对象。
#     如果不存在则创建一个新的 InMemoryChatMessageHistory。
#     """
#     if session_id not in store:
#         store[session_id] = InMemoryChatMessageHistory()
#     return store[session_id]


# # 定义 Prompt 模板
# #     - system: 给模型设定角色
# #     - MessagesPlaceholder: 历史消息将注入这里
# #     - human: 当前用户输入
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一个友好的中文助理，会根据上下文回答问题。"),
#     MessagesPlaceholder("history"),
#     ("human", "{question}")
# ])


# #构建基本链：Prompt → LLM → 输出解析
# memory_chain = prompt | llm | StrOutputParser()

# # -----------------------------------------------------
# # 将链包装为支持记忆的版本
# with_history = RunnableWithMessageHistory(
#     memory_chain,              # 原始链
#     get_session_history,       # 获取历史函数
#     input_messages_key="question",  # 对应 prompt 输入的 key
#     history_messages_key="history", # 对应 MessagesPlaceholder 的变量名
# )

# # -----------------------------------------------------
# # 模拟一个会话，用 session_id 区分不同用户
# cfg = {"configurable": {"session_id": "user-001"}}

# # 第一次提问：告诉模型“我叫张三”
# print("用户：我叫张三。")
# print("AI：", with_history.invoke({"question": "我叫张三。"}, cfg))

# # 第二次提问：让模型回忆前面的对话
# print("\n 用户：我叫什么？")
# print("AI：", with_history.invoke({"question": "我叫什么？"}, cfg))


'''
    使用 redis 本地持久化
    
    BaseChatMessageHistory 与 RunnableWithMessageHistory 配合使用

    1、RedisChatMessageHistory 创建内存聊天历史记录实例，用于存储对话历史，数据存在redis 中
        def get_session_history(session_id: str) -> RedisChatMessageHistory:
            """获取或创建会话历史（使用 Redis）"""
            # 创建 Redis 历史对象
            history = RedisChatMessageHistory(
                session_id=session_id,
                url=REDIS_URL,
                # ttl=3600  # 注释：关闭自动过期，避免重启后数据被清理
            )
            return history

    2 、RunnableWithMessageHistory 创建带消息历史的可运行对象，用于处理带历史记录的对话
        chain = RunnableWithMessageHistory(
                    prompt | llm,
                    get_session_history,
                    input_messages_key="question",
                    history_messages_key="history"
                )
    
    3、在提示词中插入历史消息
        prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder("history"),
            ("human", "{question}")
            ])   
    
'''

from langchain.chat_models import init_chat_model
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
import os
import redis  # 导入原生redis库，pip install redis==5.3.1
from loguru import logger

# 设置本地模型
from dotenv import load_dotenv

# .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
load_dotenv(encoding="utf-8")

REDIS_URL = "redis://localhost:6379"
# 创建原生Redis客户端,decode_responses 控制 Redis 返回数据的类型：False 返字节串，True 返字符串
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    base_url=os.getenv("ALIQWEN_URL"),
    api_key=os.getenv("ALIQWEN_API"),
)

# 创建提示模板
prompt = ChatPromptTemplate.from_messages(
    [MessagesPlaceholder("history"), ("human", "{question}")]
)


# 创建 Redis 历史对象
def get_session_history(session_id: str) -> RedisChatMessageHistory:
    """获取或创建会话历史（使用 Redis）"""
    history = RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL,
        # ttl=3600  # 注释：关闭自动过期，避免重启后数据被清理
    )

    return history


# 创建带历史的链
chain = RunnableWithMessageHistory(
    prompt | llm,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

# 配置
# session_id 就是登录大模型的各自帐户，类似登录手机号码，各不相同
config = RunnableConfig(configurable={"session_id": "user-001"})

# 主循环
print("开始对话（输入 'quit' 退出）")
while True:
    question = input("\n输入问题：")
    if question.lower() in ["quit", "exit", "q"]:
        break

    response = chain.invoke({"question": question}, config)
    logger.info(f"AI回答:{response.content}")

    # 等同于redis-cli的SAVE命令，强制写入dump.rdb
    redis_client.save()
