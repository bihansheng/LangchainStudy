# 检索增强生成RAG
# RAG的核心卖点正是让生成模型利用检索到的外部知识再做一次深加工，从而给出连贯、准确且带引用的回答
#
# RAG标准流程
#  1、在RAG准备阶段，LangChain通过文档加载器对各种格式的文档进行加载，转换为LangChain中的文档对象
#  2、对文档对象进行分割，根据分割规则，分割成文档片段
#  3、将文档片段通过文本嵌入模型组件，转换为向量，通过向量数据库组件，保存到向量数据库
#  4、在RAG的使用阶段，用户首先提出问题，使用文本嵌入模型组件，将提问文本转换为向量数据，通过向量数据库检索器组件，进行相似性检索，返回关联的文本片段
#  5、将相关的文档片段内容渲染到提示词模板中，作为提问问题的上下文传递给大模型，在上下文里做“阅读-理解-整合-生成”，最后把整理好的答案返回给用户
#
#
#
# 文档加载器
# 用于将各种格式的文档转换为Document对象
# 常用的LangChain文档加载器
#  1 UnstructuredWordDocumentLoader  ：Word 文档加载
#  2、CSVLoader                      ：csv文档加载
#  3、UnstructuredMarkdownLoader     ：Markdown
#  4、JSONLoader                     ： json 文件
#  5、PyPDFLoader                    ： pdf
#  6、TextLoader                     ：text
#
# 文本分割器
# 为什么分割 ：
#  1、 文档太大，一口吞不下
#  2、文档太大，Token太费钱+有限制
# LangChain提供了多种文本分割器，常用切分策略，主要使用RecursiveCharacterTextSplitter(递归字符文本切分器)
# RecursiveCharacterTextSplitter不仅可以分割纯文本，还可以直接分割Document对象
#
#
#
#
#


# #  ==================================================   Word 文档加载 =======================
# # pip install langchain_community unstructured[docx]
# # pip install -U unstructured
# # pip install python-docx
# # pip install regex==2026.1.14
# from langchain_community.document_loaders import UnstructuredWordDocumentLoader

# docs = UnstructuredWordDocumentLoader(
#     # 文件路径
#     file_path="assets/alibaba-more.docx",
#     # 加载模式:
#     #   single 返回单个Document对象
#     #   elements 按标题等元素切分文档
#     mode="single",
# ).load()

# # print(type(docs))
# print(docs)


# #  ==================================================   JSON 文档加载 =======================

# # pip install jq
# from langchain_community.document_loaders import JSONLoader

# # 提取所有字段
# docs = JSONLoader(
#     file_path="assets/sample.json",  # 文件路径
#     jq_schema=".",  # 提取所有字段
#     text_content=False,  # 提取内容是否为字符串格式
# ).load()

# print(docs)


# #  ==================================================   Markdown 文档加载 =======================

# # pip install langchain_community unstructured[md]
# from langchain_community.document_loaders import UnstructuredMarkdownLoader

# docs = UnstructuredMarkdownLoader(
#     # 文件路径
#     file_path="assets/sample.md",
#     # 加载模式:
#     #   single 返回单个Document对象
#     #   elements 按标题等元素切分文档
#     mode="elements",
# ).load()

# print(docs)


# #  ==================================================   PDF 文档加载 =======================

# # pip install langchain_community
# from langchain_community.document_loaders import PyPDFLoader

# docs = PyPDFLoader(
#     # 文件路径，支持本地文件和在线文件链接，如"https://arxiv.org/pdf/alg-geom/9202012"
#     file_path="assets/sample.pdf",
#     # 提取模式:
#     #   plain 提取文本
#     #   layout 按布局提取
#     extraction_mode="plain",
# ).load()

# print(docs)


# #  ==================================================   Text 文档加载 =======================

# # pip install langchain_community
# from langchain_community.document_loaders import TextLoader

# # 返回List[Document]
# file_path = "assets/sample.txt"  # 文件路径
# encoding = "utf-8"  # 文件编码方式

# docs = TextLoader(file_path, encoding).load()

# print(docs)
# # [Document(metadata={'source': 'asset/sample.txt'}, page_content='...')]


# #  ==================================================   csv 文档加载 =======================

# # pip install langchain_community
# from langchain_community.document_loaders.csv_loader import CSVLoader

# # 加载所有列
# docs = CSVLoader(
#     file_path="assets/sample.csv",  # 文件路径
# ).load()  # 返回List[Document]

# print(docs)

# # 加载部分列
# docs = CSVLoader(
#     file_path="assets/sample.csv",  # 文件路径
#     metadata_columns=["title", "author"],  # 将指定列作为元数据
#     content_columns=["content"],  # 将指定列作为内容
# ).load()  # 返回List[Document]

# print(docs)


# # ==================================== RecursiveCharacterTextSplitter  字符串分割 ========================


# """
# 使用split_text()方法进行文本分割
# RecursiveCharacterTextSplitter中指定的
# chunk_size=100,块大小为100，
# chunk_overlap=30, 片段重叠字符数为30，
# length_function=len，计算长度的函数使用len，# 可选：默认为字符串长度，可自定义函数来实现按 token 数切分
# """
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# # 1.分割文本内容
# content = (
#     "大模型RAG（检索增强生成）是一种结合生成模型与外部知识检索的技术，通过从大规模文档或数据库中检索相关信息，"
#     "辅助生成模型以提升回答的准确性和相关性。其核心流程包括用户输入查询、系统检索相关知识、"
#     "生成模型基于检索结果生成内容，并输出最终答案。RAG的优势在于能够弥补生成模型的知识盲区，"
#     "提供更准确、实时和可解释的输出，广泛应用于问答系统、内容生成、客服、教育和企业领域。"
#     "然而，其也面临依赖高质量知识库、可能的响应延迟、较高的维护成本以及数据隐私等挑战。")


# # 2.定义递归文本分割器
# # 使用RecursiveCharacterTextSplitter创建文本分割器，设置块大小为100，重叠长度为30,
# # length_function=len就是指定使用 Python 内置的len()函数来计算文本长度，也是这个分割器的默认值
# # 比如，print(len("大模型RAG技术"))  # 输出8，因为统计的是字符个数（中文字符、字母、符号各算1个）
# # 遵循 “重叠后向前取有效内容、且不生成过小碎片” 的核心分割逻辑，不会让最后一个片段的有效内容只剩扣除重叠后的少量字符
# # 原始文本 → split_text → 第一次分割成字符串块 → create_documents → 对字符串块二次分割 → 内容丢失有可能
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=30, length_function=len)

# # 3.分割文本
# # 将原始文本内容分割成多个文本块
# splitter_texts = text_splitter.split_text(content)

# # 4.转换为文档对象
# # 将分割后的文本块转换为文档对象列表
# splitter_documents = text_splitter.create_documents(splitter_texts)
# print(f"原始文本大小：{len(content)}")
# print(f"分割文档数量：{len(splitter_documents)}")
# for splitter_document in splitter_documents:
#     print(f"文档片段大小：{len(splitter_document.page_content)},文档内容：{splitter_document.page_content}")

# # # 拼接所有分割后的内容（剔除重叠部分）验证完整性
# # full_content = ""
# # for text in splitter_texts:
# #     if full_content:
# #         full_content += text[30:]  # 剔除重叠的30个字符后拼接
# #     else:
# #         full_content += text


# # ==================================== RecursiveCharacterTextSplitter  文档分割 ========================
# # pip install python-magic
# # pip install langchain-unstructured unstructured
# from pathlib import Path

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_unstructured import UnstructuredLoader

# # 1.创建文档加载器，进行文档加载
# #  获取当前代码文件所在的绝对目录， Python 寻找相对路径时，不是以“代码文件所在目录”为基准，而是以“当前终端执行命令时所在的目录（Working Directory）”为基准。
# current_dir = Path(__file__).parent
# loader = UnstructuredLoader(current_dir / "rag.txt")
# documents = loader.load()

# # 2.定义递归文本分割器
# # 创建RecursiveCharacterTextSplitter实例，用于将文档分割成指定大小的文本块
# # chunk_size: 每个文本块的最大字符数为100
# # chunk_overlap: 相邻文本块之间的重叠字符数为30，一般是chunk_size的 20% - 40%
# # length_function: 使用len函数计算文本长度
# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=100, chunk_overlap=30, length_function=len
# )

# # 3.分割文本
# # 使用文本分割器将加载的文档分割成多个较小的文档片段
# splitter_documents = text_splitter.split_documents(documents)

# # 输出分割后的文档信息
# print(f"分割文档数量：{len(splitter_documents)}")

# for splitter_document in splitter_documents:
#     print(f"文档片段：{splitter_document.page_content}")
#     print(
#         f"文档片段大小：{len(splitter_document.page_content)}, 文档元数据：{splitter_document.metadata}"
#     )


# ====================================  分割字符串 并向量化存储到 redis 中 ========================

import os

from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_redis import RedisConfig, RedisVectorStore

# .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
load_dotenv(encoding="utf-8")

# 初始化 Embedding 模型
# 1. 初始化阿里千问 Embedding 模型
embeddingsModel = DashScopeEmbeddings(
    model="text-embedding-v3",  # 支持 v1 或 v2
    dashscope_api_key=os.getenv("ALIQWEN_API"),  # 从环境变量读取
)

# ========== 存储数据 ==========
# 定义待处理的文本数据列表
texts = [
    "我喜欢吃苹果",
    "苹果是我最喜欢吃的水果",
    "我喜欢用苹果手机",
]
# query_result = embeddings.embed_query(texts)
# print(query_result)


# 获取文本向量
# 使用embedding模型将文本转换为向量表示
embeddings = embeddingsModel.embed_documents(texts)

# 打印结果
# 遍历并打印每个文本及其对应的向量信息
for i, vec in enumerate(embeddings, 1):
    print(f"文本 {i}: {texts[i - 1]}")
    print(f"向量长度: {len(vec)}")
    print(f"前5个向量值: {vec[:10]}\n")

# 定义每条文本对应的元数据信息
metadata = [{"segment_id": "1"}, {"segment_id": "2"}, {"segment_id": "3"}]

# 配置Redis连接参数和索引名称
config = RedisConfig(
    index_name="newsgroups",
    redis_url="redis://localhost:6379",
)

# 创建Redis向量存储实例
vector_store = RedisVectorStore(embeddingsModel, config=config)

# 将文本和元数据添加到向量存储中
ids = vector_store.add_texts(texts, metadata)

# 打印前5个存储记录的ID
print(ids[0:5])
