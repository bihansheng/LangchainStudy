import asyncio

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

"""
    模型调用方法有
    1、invoke: 普通调用，处理单条输入，等待LLM完全推理完成后再返回调用结果
    2、ainvoke 在 异步环境（async/await） 调用
    3、stream: 流式调用 ，流式响应，是一种逐步返回大模型生成结果的技术，生成一点返回一点，允许服务器将响应内容分批次实时传输给客户端，而不是等待全部内容生成完毕后再一次性返回
    4、astream ：异步流式响应
    5、batch:批处理，处理批量输入，一次性向模型提交多个输入并并行处理，从而显著提升吞吐量
    6、abatch: 异步处理批量输入
"""


# .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
load_dotenv(encoding="utf-8")

model = ChatDeepSeek(model="deepseek-chat")


print("======== 3、stream   ===========")
print(model.stream("你是谁"))


print("======== ainvoke  异步环境调用===========")

"""
LangChain 提供 ainvoke() 异步调用接口，用于在 异步环境（async/await） 中高效并行地执行模型推理。
它的核心作用是：让你同时调用多个模型请求而不阻塞主线程 —— 特别适合大批量请求或 Web 服务场景（如 FastAPI）
"""


async def main():
    # 异步调用一条请求
    response = await model.ainvoke("解释一下LangChain是什么，简洁回答100字以内")
    print(f"响应类型：{type(response)}")
    print(response.content_blocks)


# 4.运行异步函数
if __name__ == "__main__":
    asyncio.run(main())


print("======== batch  批量调用===========")

# 问题列表
questions = [
    "什么是redis?简洁回答，字数控制在100以内",
    "Python的生成器是做什么的？简洁回答，字数控制在100以内",
    "解释一下Docker和Kubernetes的关系?简洁回答，字数控制在100以内",
]

# 批量调用大模型 model.batch()
response = model.batch(questions)
print(f"响应类型：{type(response)}")
print()
for q, r in zip(questions, response):
    print(f"问题：{q}\n回答：{r.content}\n")


print("======== abatch  异步批量调用===========")

# 问题列表
questions = [
    "什么是redis?简洁回答，字数控制在100以内",
    "Python的生成器是做什么的？简洁回答，字数控制在100以内",
    "解释一下Docker和Kubernetes的关系?简洁回答，字数控制在100以内",
]


async def main2():
    # 批量调用大模型 model.batch()
    response = await model.abatch(questions)
    print(f"响应类型：{type(response)}")
    print()
    for q, r in zip(questions, response):
        print(f"问题：{q}\n回答：{r.content}\n")


# 4.运行异步函数
if __name__ == "__main__":
    asyncio.run(main2())
