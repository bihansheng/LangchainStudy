# LCEL 是LangChain 表达式语言(LangChain Expression Language)
# 通过 LCEL（| 运算符、RunnableSequence、RunnableParallel 等）快速拼接多个 Runnable 为复杂工作流，支持条件分支、并行执行等

# 什么是 Runnable？
#  - 定位：LangChain 中的抽象基类（ABC）
#  - 目标：为所有可执行组件提供统一的操作接口
#  - 核心理念：一切可执行的对象都应该有统一的调用方式
# Runnable 是 LangChain 核心抽象接口(定义在 langchain_core.runnables)统一组件调用方式，支持 LCEL 组合，适配同步 / 异步、流式、批量等场景，是构建工作流的基础


"""
RunnableLambda-函数链将普通Python函数融入Runnable流程.
｜ 链方法前后的函数都需要实现Runnable这个接口,如 RunnableLambda(MyFunction)


"""

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_deepseek import ChatDeepSeek
from loguru import logger

from dotenv import load_dotenv

# .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
load_dotenv(encoding="utf-8")

model = ChatDeepSeek(model="deepseek-chat")


# 一个简单的打印函数，调试用
def debug_print(x):
    logger.info(f"中间结果:{x}")
    return {"input": x}


# 子链1提示词
prompt1 = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
        ("human", "请简短介绍什么是{topic}"),
    ]
)
# 子链1解析器
parser1 = StrOutputParser()
# 子链1：生成内容
# 这种写法可见将输入模版，模型，解析函数 分开写，但是最终一起调用
chain1 = prompt1 | model | parser1

# 子链2提示词
prompt2 = ChatPromptTemplate.from_messages(
    [("system", "你是一个翻译助手，将用户输入内容翻译成英文"), ("human", "{input}")]
)
# 子链2解析器
parser2 = StrOutputParser()

# 子链2：翻译内容
chain2 = prompt2 | model | parser2
# 创建一个可运行的调试节点，用于打印中间结果
debug_node = RunnableLambda(debug_print)

# 构建完整的处理链，将chain1、调试打印和chain2串联起来
full_chain = chain1 | debug_node | chain2

# 调用复合链
result1 = full_chain.invoke({"topic": "langchain"})
logger.info(f"最终结果111:{result1}")


# # 构建完整的处理链，将chain1、调试打印和chain2串联起来
# full_chain = chain1 | debug_node | chain2

# # 调用复合链  最终执行
# result2 = full_chain.invoke({"topic": "langchain"})
# logger.info(f"最终结果222:{result2}")


"""
    1、RunnableSequence-顺序链 
        如   chat_prompt | model | parser
    2、RunnableBranch-分支链
        如：
        RunnableBranch(
        (lambda x: determine_language(x) == "japanese", japanese_prompt | model | parser),
        (lambda x: determine_language(x) == "korean", korean_prompt | model | parser),
        (english_prompt | model | parser)
        )
    3、RunnableSerializable-串行链  
        如  chain1 | (lambda content: {"input": content}) | chain2
    4、RunnableParallel-并行链
        如：# 创建并行链,用于同时执行多个语言处理链
        parallel_chain = RunnableParallel({
            "chinese": chain1,
            "english": chain2
        })

"""


"""
顺序链
LangChain 的一个典型链条由Prompt、Model、OutputParser （可没有）组成，如（ chain = chat_prompt | model | parser）
然后可以通过 链（Chain） 把它们顺序组合起来，让一个任务的输出成为下一个任务的输入
意思等价于Linux里面的管道符
"""

# from langchain.chat_models import init_chat_model
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from loguru import logger
# import os

# # 创建聊天提示模板，包含系统角色设定和用户问题输入
# chat_prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一个{role}，请简短回答我提出的问题"),
#     ("human", "请回答:{question}")
# ])

# # 使用具体参数实例化提示模板并记录日志
# prompt = chat_prompt.invoke({"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"})
# logger.info(prompt)

# # 初始化模型
# model = init_chat_model(
#     model="qwen-plus",
#     model_provider="openai",
#     api_key=os.getenv("aliQwen-api"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )


# # 调用模型获取原始响应并记录日志
# result = model.invoke(prompt)
# logger.info(f"********>模型原始输出:\n{result}")

# # 创建字符串输出解析器，用于处理模型输出
# parser = StrOutputParser ()

# # 解析模型输出为结构化结果并记录日志
# response = parser.invoke(result)
# logger.info(f"解析后的结构化结果:\n{response}")
# # 记录解析结果的数据类型
# logger.info(f"结果类型: {type(response)}")


# print()
# print("*" * 60)
# print()


# # 构建处理链：提示模板 -> 模型 -> 输出解析器
# chain = chat_prompt | model | parser

# # 执行处理链并记录最终结果及数据类型
# result_chain = chain.invoke({"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"})
# logger.info(f"Chain执行结果:\n {result_chain}")
# logger.info(f"Chain执行结果类型: {type(result_chain)}")

# print()

# print(type(chain))


"""
串行链
RunnableSerializable-串行链 如：chain1 | (lambda content: {"input": content}) | chain2
子链叠加串行，假如我们需要多次调用大模型，将多个步骤串联起来实现功能
"""
# from langchain.chat_models import init_chat_model
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from loguru import logger
# import os

# model = init_chat_model(
#     model="qwen-plus",
#     model_provider="openai",
#     api_key=os.getenv("aliQwen-api"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )


# # 子链1提示词
# prompt1 = ChatPromptTemplate.from_messages([
#     ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
#     ("human", "请简短介绍什么是{topic}")
# ])
# # 子链1解析器
# parser1 = StrOutputParser()
# # 子链1：生成内容
# chain1 = prompt1 | model | parser1

# result1 = chain1.invoke({"topic": "langchain"})
# logger.info(result1)

# # 子链2提示词
# prompt2 = ChatPromptTemplate.from_messages([
#     ("system", "你是一个翻译助手，将用户输入内容翻译成英文"),
#     ("human", "{input}")
# ])
# # 子链2解析器
# parser2 = StrOutputParser()
# # 子链2：翻译内容
# chain2 = prompt2 | model | parser2


# # 组合成一个复合 Chain，使用 lambda 函数将chain1执行结果content内容添加input键作为参数传递给chain2
# full_chain = chain1 | (lambda content: {"input": content}) | chain2

# # 调用复合链
# result = full_chain.invoke({"topic": "langchain"})
# logger.info(result)


"""
分支链
如：
RunnableBranch(
    (lambda x: determine_language(x) == "japanese", japanese_prompt | model | parser),
    (lambda x: determine_language(x) == "korean", korean_prompt | model | parser),
    (english_prompt | model | parser)
)
在LangChain中提供了类RunnableBranch来完成LCEL中的条件分支判断，它可以根据输入的不同采用不同的处理逻辑，
具体示例如下
会根据用户输入中是否包含英语、韩语等关键词，来选择对应的提示词进行处理。根据判断结果，
再执行不同的逻辑分支
"""
# from langchain.chat_models import init_chat_model
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from loguru import logger
# from langchain_core.runnables import RunnableBranch
# import os

# # 构建提示词
# english_prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一个英语翻译专家，你叫小英"),
#     ("human", "{query}")
# ])

# japanese_prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一个日语翻译专家，你叫小日"),
#     ("human", "{query}")
# ])

# korean_prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一个韩语翻译专家，你叫小韩"),
#     ("human", "{query}")
# ])


# def determine_language(inputs):
#     """判断语言种类"""
#     query = inputs["query"]
#     if "日语" in query:
#         return "japanese"
#     elif "韩语" in query:
#         return "korean"
#     else:
#         return "english"


# # 初始化模型
# model = init_chat_model(
#     model="qwen-plus",
#     model_provider="openai",
#     api_key=os.getenv("aliQwen-api"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )

# # 创建字符串输出解析器，用于处理模型输出
# parser = StrOutputParser()
# # 创建一个可运行的分支链，根据输入文本的语言类型选择相应的处理流程
# # 返回值：RunnableBranch对象，可根据输入动态选择执行路径的可运行链
# chain = RunnableBranch(
#     (lambda x: determine_language(x) == "japanese", japanese_prompt | model | parser),
#     (lambda x: determine_language(x) == "korean", korean_prompt | model | parser),
#     (english_prompt | model | parser)
# )

# # 测试查询
# test_queries = [
#     {'query': '请你用韩语翻译这句话:"见到你很高兴"'},
#     {'query': '请你用日语翻译这句话:"见到你很高兴"'},
#     {'query': '请你用英语翻译这句话:"见到你很高兴"'}
# ]

# for query_input in test_queries:

#     # 判断使用哪个提示词
#     lang = determine_language(query_input)
#     logger.info(f"检测到语言类型: {lang}")

#     # 根据语言类型选择对应的提示词并格式化
#     if lang == "japanese":
#         chatPromptTemplate = japanese_prompt
#     elif lang == "korean":
#         chatPromptTemplate = korean_prompt
#     else:
#         chatPromptTemplate = english_prompt

#     #print(query_input) # {'query': '请你用英语翻译这句话:"见到你很高兴"'}

#     # 格式化提示词并打印
#     formatted_messages = chatPromptTemplate.format_messages(**query_input)
#     logger.info("格式化后的提示词:")
#     for msg in formatted_messages:
#         logger.info(f"[{msg.type}]: {msg.content}")

#     # 执行链
#     result = chain.invoke(query_input)
#     logger.info(f"输出结果: {result}\n")


"""
        RunnableParallel-并行链

        在 Langchain 中，创建并行链（Parallel Chains），是指同时运行多个子链（Chain），并在它们都完成后汇总结果。
        **作用**：同时执行多个 Runnable，合并结果
"""
# from langchain.chat_models import init_chat_model
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnableParallel
# from loguru import logger
# import os

# model = init_chat_model(
#     model="qwen-plus",
#     model_provider="openai",
#     api_key=os.getenv("aliQwen-api"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )

# # 并行链1提示词
# prompt1 = ChatPromptTemplate.from_messages([
#     ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
#     ("human", "请简短介绍什么是{topic}")
# ])
# # 并行链1解析器
# parser1 = StrOutputParser()
# # 并行链1：生成中文结果
# chain1 = prompt1 | model | parser1

# # 并行链2提示词
# prompt2 = ChatPromptTemplate.from_messages([
#     ("system", "你是一个知识渊博的计算机专家，请用英文简短回答"),
#     ("human", "请简短介绍什么是{topic}")
# ])
# # 并行链2解析器
# parser2 = StrOutputParser()

# # 并行链2：生成英文结果
# chain2 = prompt2 | model | parser2

# # 创建并行链,用于同时执行多个语言处理链
# parallel_chain = RunnableParallel({
#     "chinese": chain1,
#     "english": chain2
# })

# # 调用复合链
# result = parallel_chain.invoke({"topic": "langchain"})
# logger.info(result)


# # 打印并行链的ASCII图形表示，LangGraph提前预告，不是本节知识点
# parallel_chain.get_graph().print_ascii()


"""
RunnableParallel-并行链

在 Langchain 中，创建并行链（Parallel Chains），是指同时运行多个子链（Chain），并在它们都完成后汇总结果。
**作用**：同时执行多个 Runnable，合并结果
"""
# from langchain.chat_models import init_chat_model
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.runnables import RunnableParallel
# from loguru import logger
# import os

# model = init_chat_model(
#     model="qwen-plus",
#     model_provider="openai",
#     api_key=os.getenv("aliQwen-api"),
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )

# # 并行链1提示词
# prompt1 = ChatPromptTemplate.from_messages([
#     ("system", "你是一个知识渊博的计算机专家，请用中文简短回答"),
#     ("human", "请简短介绍什么是{topic}")
# ])
# # 并行链1解析器
# parser1 = StrOutputParser()
# # 并行链1：生成中文结果
# chain1 = prompt1 | model | parser1

# # 并行链2提示词
# prompt2 = ChatPromptTemplate.from_messages([
#     ("system", "你是一个知识渊博的计算机专家，请用英文简短回答"),
#     ("human", "请简短介绍什么是{topic}")
# ])
# # 并行链2解析器
# parser2 = StrOutputParser()

# # 并行链2：生成英文结果
# chain2 = prompt2 | model | parser2

# # 创建并行链,用于同时执行多个语言处理链
# parallel_chain = RunnableParallel({
#     "chinese": chain1,
#     "english": chain2
# })

# # 调用复合链
# result = parallel_chain.invoke({"topic": "langchain"})
# logger.info(result)


# # 打印并行链的ASCII图形表示，LangGraph提前预告，不是本节知识点
# parallel_chain.get_graph().print_ascii()
