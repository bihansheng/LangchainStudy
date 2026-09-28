# 官网-向量存储(Vector Store)
# 一种专门用于存储、管理和检索向量数据（即高维数值数组）的数据库系统。
# 其核心功能是通过高效的索引结构和相似性计算算法，支持大规模向量数据的快速查询与分析，向量数据库维度越高，查询精准度也越高，查询效果也越好。
# 将文本、图像和视频转换为称为向量（Vectors）的浮点数数组在 VectorStore中，查询与传统关系数据库不同。它们执行相似性搜索，而不是精确匹配。
# 当给定一个向量作为查询时，VectorStore 返回与查询向量“相似”的向量
# 指征特点:
#  1、捕捉复杂的词汇关系（如语义相似性、同义词、多义词）
#  2、向量嵌入为检索增强生成 (RAG) 应用程序提供支持
#
# # 常用的向量数据库 有很多
#   Redis (Vector Search / RedisVL)
#       特点：通过 Redis Search 模块扩展出来的向量数据库功能。
#       优势：如果你本地或线上已经运行了 Redis，无需引入全新组件即可直接兼任 LLM 响应缓存与向量存储。
#
# Redis Stack
# RedisStack = 原生Redis + 搜索 + 图 + 时间序列 + JSON + 概率结构 + 可视化工具 + 开发框架支持
#   是 Redis 官方推出的一套扩展增强版服务软件。
#   它在经典 Redis（单纯的 Key-Value 内存缓存）基础上，通过预装官方的核心模块（Modules），
#   把 Redis 从一个“纯缓存系统”升级成了一个多模态数据平台（Multi-model Data Store）。
# RedisStack核心组件
#       1、 RediSearch：  提供全文搜索能力，支持复杂的文本搜索、聚合和过滤，以及向量数据的存储和检索
#       2、RedisJSON： 原生支持JSON数据的存储、索引I和查询，可高效存储和操作嵌套的JSON文档。
#       3、RedisGraph：支持图数据模型，使用Cypher查询语言进行图遍历查询。
#       4、RedisBloom:支持 Bloom、Cuckoo、Count-Min Sketch等概率数据结构。


# 嵌入模型 (Embedding Model)
# 是将现实世界中的非结构化数据（如文本、图片、文本视频）转换成高维数值向量（Vector / 浮点数数组）的 AI 模型。
# 它是连接自然语言/多媒体与计算机数学计算之间的“翻译官”。
# 代表模型 ：text-embedding-3, bge-m3, CLIP
#
# 在 LangChain 开发中，Embedding 模型是构建 RAG（检索增强生成/知识库问答） 的灵魂:
#  1、构建私有知识库：
#       将你的 Markdown、PDF 或代码文档切成小块，通过 Embedding 模型批量转成向量，存入向量数据库（如 Milvus, Qdrant, Chroma 或 Redis Vector Store）。
#   2、语义搜索 (Semantic Search)：
#       用户提问 Mac 如何清理内存 时，就算知识库里只有 macOS 释放显存与 RAM 的方法，通过计算两者的向量余弦相似度（Cosine Similarity），系统依然能精准匹配到答案（而传统关键字搜索会失效）。
#   3、多模态搜索：
#       输入一段文字 蓝天白云下的海滩，通过对比向量距离，直接在图片/视频库中把符合描述的资源检索出来。
#

# https://bailian.console.aliyun.com/cn-beijing/?productCode=p_efm&tab=doc#/doc/?type=model&url=2842587


"""
https://bailian.console.aliyun.com/cn-beijing/?tab=api#/api/?type=model&url=2587654
pip install langchain-community dashscope
"""

#  =====================================================================  dashscope ==================================


# from langchain_community.embeddings import DashScopeEmbeddings

# embeddings = DashScopeEmbeddings(
#     model="text-embedding-v4",
#     # other params...
# )

# text = "This is a test document."

# query_result = embeddings.embed_query(text)
# print("文本向量长度：", len(query_result), sep='')
# #
# doc_results = embeddings.embed_documents(
#     [
#         "Hi there!",
#         "Oh, hello!",
#         "What's your name?",
#         "My friends call me World",
#         "Hello World!"
#     ])
# print(doc_results)
# print("文本向量数量：", len(doc_results), "，文本向量长度：", len(doc_results[0]), sep='')


#  =====================================================================  openAI ==================================
# import os

# from openai import OpenAI

# input_text = "衣服的质量杠杠的"

# client = OpenAI(
#     # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
#     # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
#     api_key=os.getenv("aliQwen-api"),
#     # 以下是北京地域base-url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
# )

# completion = client.embeddings.create(
#     model="text-embedding-v4",
#     input=input_text
# )

# print(completion.model_dump_json())


#  =====================================================================  dashscope pro ==================================


# import json
# import os
# from http import HTTPStatus

# import dashscope

# # Embedding 文本向量化

# # 调用多模态embedding模型接口进行向量编码
# # https://bailian.console.aliyun.com/?productCode=p_efm&tab=model#/model-market/all?capabilities=ME
# resp = dashscope.MultiModalEmbedding.call(
#     model="tongyi-embedding-vision-plus",  # 支持 v1 或 v2
#     dashscope_api_key=os.getenv("aliQwen-api"),  # 从环境变量读取
#     input=[{"text": "尚硅谷AI"}]
# )

# result = "";

# # 处理模型返回结果，提取关键信息并格式化输出
# if resp.status_code == HTTPStatus.OK:
#     result = {
#         "status_code": resp.status_code,
#         "request_id": getattr(resp, "request_id", ""),
#         "code": getattr(resp, "code", ""),
#         "message": getattr(resp, "message", ""),
#         "output": resp.output,
#         "usage": resp.usage
#     }
#     print(json.dumps(result, ensure_ascii=False, indent=4))

# print("=================================")
# print()

# result 就是你已经拿到的完整 dict
# embedding_values = result["output"]["embeddings"][0]["embedding"]
# print(embedding_values)
# print("=================================")
# print("=================================")
# # 只打印 embedding 数组
# print(json.dumps(embedding_values, ensure_ascii=False))

#  ==================================================================== 计算余弦相似度 ============================
"""
把文本转换成向量有什么用呢？
最核心的作用是可以通过向量之间的计算，来分析文本与文本之间的相似性。
计算的方法有很多种，其中用得最多的是向量余弦相似度。
Python语言中提供了一个库sklearn，可以很方便的计算向量之间的余弦相似度
"""

# import dashscope
# import os
# from http import HTTPStatus
# import numpy as np


# # 准备输入文本数据
# texts = [
#     '我喜欢吃苹果',
#     '苹果是我最喜欢吃的水果',
#     '我喜欢用苹果手机'
# ]

# # 获取每个文本的embedding向量
# embeddings = []
# # 假如要处理图片，请参考https://bailian.console.aliyun.com/cn-beijing/?productCode=p_efm&tab=doc#/doc/?type=model&url=2842587
# for text in texts:
#     input_data = [{'text': text}]
#     resp = dashscope.MultiModalEmbedding.call(
#         model="multimodal-embedding-v1",
#         api_key=os.getenv("aliQwen-api"),
#         base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
#         input=input_data
#     )

#     if resp.status_code == HTTPStatus.OK:
#         embedding = resp.output['embeddings'][0]['embedding']
#         embeddings.append(embedding)

# # 计算余弦相似度
# def cosine_similarity(vec1, vec2):
#     # 计算两个向量的余弦相似度
#     dot_product = np.dot(vec1, vec2)
#     norm_vec1 = np.linalg.norm(vec1)
#     norm_vec2 = np.linalg.norm(vec2)
#     return dot_product / (norm_vec1 * norm_vec2)

# # 比较所有文本之间的相似度
# print("文本相似度比较结果:")
# print("=" * 60)

# for i in range(len(texts)):
#     for j in range(i+1, len(texts)):
#         similarity = cosine_similarity(embeddings[i], embeddings[j])
#         print(f"文本{i+1} vs 文本{j+1}:")
#         print(f"  文本{i+1}: {texts[i]}")
#         print(f"  文本{j+1}: {texts[j]}")
#         print(f"  余弦相似度: {similarity:.4f}")
#         print("-" * 40)


#  ==================================================================== 用redisStack作为向量存储 ============================


# pip install langchain-community dashscope redis redisvl
import os

from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from langchain_core.documents import Document

# .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
load_dotenv(encoding="utf-8")

# 1. 初始化阿里千问 Embedding 模型
embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",  # 支持 v1 或 v2
    dashscope_api_key=os.getenv("ALIQWEN_API"),  # 从环境变量读取
)


# 2. 准备要向量化的文本（Document 列表）
texts = [
    "通义千问是阿里巴巴研发的大语言模型。",
    "Redis 是一个高性能的键值存储系统，支持向量检索。",
    "LangChain 可以轻松集成各种大模型和向量数据库。",
]
documents = [
    Document(page_content=text, metadata={"source": "manual"}) for text in texts
]

# 3. 连接到 Redis 并存入向量（自动调用 embeddings 嵌入）
vector_store = Redis.from_documents(
    documents=documents,
    embedding=embeddings,
    redis_url="redis://localhost:6379",  # 替换为你的 Redis 地址
    index_name="my_index11",  # 向量索引名称
)

# 4. （可选）后续可直接用于检索
retriever = vector_store.as_retriever(search_kwargs={"k": 2})
results = retriever.invoke("LangChain 和 Redis 怎么结合？")
for res in results:
    print(res.page_content)
