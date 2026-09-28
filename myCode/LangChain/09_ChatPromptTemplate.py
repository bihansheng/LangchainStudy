# ChatPromptTemplate 是
#  LangChain 中专门用于**结构化聊天对话提示**的核心组件，它比普通 `PromptTemplate` 更适合处理多角色、多轮次的对话场景。为与现代聊天模型的交互提供了一种上下文丰富和会话友好的方式

# 参数类型：列表参数格式是tuple类型（ role :str,content :str 组合最常用）
# 元组的格式为：(role: str | type, content: str | list[dict] | list[object])
# 其中 role 是：字符串（如 “system” 、“human” 、“ai” ）
#
#
#
# System/Human/AIMessage 是 langchain 中用于构建不同角色的一个类。它通常用于创建聊天消息的一部分，特别是当你构建一个多轮对话的 prompt 模板时，区分系统、AI、和人类消息
#
#
# 如果我们不确定消息何时生成，也不确定要插入几条消息，
# 比如在提示词中添加聊天历史记忆这种场景，可以在ChatPromptTemplate添加MessagesPlaceholder占位符，在调用invoke时，在占位符处插入消息


from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_deepseek import ChatDeepSeek

# .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
load_dotenv(encoding="utf-8")

# 创建聊天提示模板，用于构建AI助手的对话上下文


"""
使用ChatPromptTemplate构造方法直接实例化
实例化时需要传入messages: Sequence[MessageLikeRepresentation]
messages 参数支持如下格式：
	tuple 构成的列表，格式为[(role, content)]
	dict 构成的列表，格式为[{“role”:... , “content”:...}]
	Message 类构成的列表
"""
# = = = = = = = = = = = = = = = = = = = = = = 一般通用的格式 （tuple 格式）= = = = = = = = = = = =
# 使用ChatPromptTemplate 创建
chatPromptTemplate = ChatPromptTemplate(
    [
        ("system", "你是一个AI开发工程师，你的名字是{name}。"),
        ("human", "你能帮我做什么?"),
        ("ai", "我能开发很多{thing}。"),
        ("human", "{user_input}"),
    ]
)

prompt = chatPromptTemplate.format_messages(
    name="小谷AI", thing="AI", user_input="7 + 5等于多少"
)
print(prompt)

model = ChatDeepSeek(model="deepseek-chat")
print("======================")

result = model.invoke(prompt)
print(result)
print(result.content)


# = = = = = = = = = = = = = = = = = = = = = = 列表参数格式是dict类型 = = = = = = = = = = = =
# dict 构成的列表，格式为[{“role”:... , “content”:...}]

# 使用 ChatPromptTemplate.from_messages 创建模版 ，模版通过format_messages 创建消息
print("= = = 列表参数格式是dict类型 = = = =")

chat_prompt = ChatPromptTemplate.from_messages(
    [
        {"role": "system", "content": "你是AI助手，你的名字叫{name}。"},
        {"role": "user", "content": "请问：{question}"},
    ]
)

# 格式化聊天提示模板，填充具体的助手名称和问题内容
# 参数name: AI助手的名字
# 参数question: 用户提出的问题
# 返回值: 格式化后的消息列表
message = chat_prompt.format_messages(name="小问", question="什么是LangChain")

# 打印格式化后的消息内容
print(message)


# = = = = = = = = = = = = = = = = = = = = = = message 类型 = = = = = = = = = = = =

"""
message 类型

System/Human/AIMessage 是 langchain 中用于构建不同角色的一个类。它通常用于创建聊天消息的一部分，特别是当你构建一个多轮对话的 prompt 模板时，区分系统、AI、和人类消息
"""
# 使用 ChatPromptTemplate 创建，其中SystemMessage、HumanMessage都是 LangChain 本身的类，帮助构建提示词
# 模版通过format_messages 创建消息
# 该模板包含两个消息：AI助手的自我介绍和用户问题
print("= = = message 类型 = = = =")

chat_prompt = ChatPromptTemplate(
    [
        SystemMessage(content="你是AI助手，你的名字叫{name}。"),
        HumanMessage(content="请问：{question}"),
    ]
)

# 格式化聊天提示模板，填充具体的助手名称和问题内容
# 参数name: AI助手的名字
# 参数question: 用户提出的问题
# 返回值: 格式化后的消息列表
message = chat_prompt.format_messages(name="亮仔", question="什么是LangChain")

# 打印格式化后的消息内容
print(message)


"""
如果我们不确定消息何时生成，也不确定要插入几条消息，比如在提示词中添加聊天历史记忆这种场景，
可以在ChatPromptTemplate添加MessagesPlaceholder占位符，在调用invoke时，在占位符处插入消息。

显式使用MessagesPlaceholder
"""


# = = = = = = = = = = = = = = = = = = = = = = = Message 类构成的列表 = = = = = = = = = = =

# 可以用作 多轮对话传入历史记录
# 构建一个 ChatPromptTemplate，包含多种消息类型：
print("= = = Message 类构成的列表 = = = =")

prompt = ChatPromptTemplate.from_messages(
    [
        # 添加一条系统消息，设定 AI 的角色或行为准则
        (
            "system",
            "你是一个资深的Python应用开发工程师，请认真回答我提出的Python相关的问题",
        ),
        # 插入 memory 占位符，用于填充历史对话记录（如多轮对话上下文）
        MessagesPlaceholder("memory"),
        # 添加一条用户问题消息，用变量 {question} 表示
        ("human", "{question}"),
    ]
)

# 调用 prompt.invoke 来格式化整个 Prompt 模板
# 传入的参数中：
# - memory：是一组历史消息，表示之前的对话内容（多轮上下文）
# - question：是当前用户的问题
prompt_value = prompt.invoke(
    {
        "memory": [
            # 用户第一轮说的话
            HumanMessage("我的名字叫亮仔，是一名程序员111"),
            # AI 第一轮的回应
            AIMessage("好的，亮仔你好222"),
        ],
        # 当前问题：结合上下文，测试模型是否记住了用户名字
        "question": "请问我的名字叫什么？",
    }
)

# 打印生成的完整 prompt 文本，格式化后的聊天记录
print(prompt_value)
