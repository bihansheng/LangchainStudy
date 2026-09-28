# LangGraph
# 基于 LangChain 构建的、面向智能体多轮交互 / 状态持久化 / 分支并行执行的图结构工作流框架
# LangGraph = LangChain + 图编排 + 状态机
# 彻底打破了“链”的束缚，引入了“图”的结构，让构建复杂AI应用的可能性，从一条直线，变成了一张网


# LangGraph是基于LangChain构建的，无论图结构多复杂，单独每个任务执行链路仍然是线性的，
# 其背后仍然是靠着LangChain的Chain来实现的。
# LangGraph是LangChain工作流的高级编排工具，其中“高级”之处就是LangGraph能按照图结构来编排工作流。

#  ==================================== 简单的 LangGraph 示例 ============================
# from typing import TypedDict

# from langgraph.graph import END, START, StateGraph


# # 1．定义State(可选)
# class HelloState(TypedDict):
#     name: str
#     greeting: str


# # 2.定义节点Node
# def greet(helloState: HelloState) -> dict:
#     name = helloState["name"]
#     return {"greeting": f"你好,{name}"}


# def add_emoji(helloState: HelloState) -> dict:
#     greeting = helloState["greeting"]
#     return {"greeting": greeting + "  。。。😄"}


# # 3.构建图graph
# graph = StateGraph(HelloState)

# graph.add_node("greeting", greet)
# graph.add_node("add_emoji", add_emoji)

# graph.add_edge(START, "greeting")
# graph.add_edge("greeting", "add_emoji")
# graph.add_edge("add_emoji", END)


# # 4.编译图
# app = graph.compile()

# # 5.运行
# # invoke()方法只接收状态字典作为核心参数
# result = app.invoke({"name": "z3"})
# print(result)
# print(result["greeting"])


# #
# # #6 打印图的边和节点信息
# # 6.1 打印图的ascii可视化结构
# print(app.get_graph().print_ascii())
# print("=" * 50)
# #
# # #6.2 打印图的Mermaid代码可视化结构并通过https://www.processon.com/mermaid编辑器查看
# print(app.get_graph().draw_mermaid())
# print("=" * 50)


# #
# # #6.3 生成 PNG并写入文件
# # png_bytes = app.get_graph().draw_mermaid_png(max_retries=2,retry_delay=2.0)
# # output_path = "langgraph" + str(uuid.uuid4())[:8] + ".png"
# # with open(output_path, "wb") as f:
# #     f.write(png_bytes)
# # print(f"图片已生成：{output_path}")

# """
# 上面第3种方式，容易bug,时好时坏
# ValueError: Failed to reach https://mermaid.ink  API while trying to render your graph after 1 retries.
# To resolve this issue:
# 1. Check your internet connection and try again
# 2. Try with higher retry settings: `draw_mermaid_png(..., max_retries=5, retry_delay=2.0)`
# 3. Use the Pyppeteer rendering method which will render your graph locally in a browser:
# `draw_mermaid_png(..., draw_method=MermaidDrawMethod.PYPPETEER)`
# """


"""
LangGraph 简单案例HelloWorld：
构建一个最小的有向图，流程是：START → 模型节点 → END

LangGraph的灵魂：State(状态) + Nodes(节点) + Edges(边) + Graph(图)
"""

from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

# .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
load_dotenv(encoding="utf-8")


# ========== 1. 定义状态（State） ==========
# 存储对话消息
class AtguiguState(TypedDict):
    # messages 是一个消息列表，Annotated + add_messages 表示支持自动追加消息
    messages: Annotated[list, add_messages]


# ========== 2. 定义大模型 ==========
llm = ChatDeepSeek(
    model="deepseek-chat",
)


# ========== 3. 定义节点函数 ==========
# 节点：调用大模型，并把回复加入到 state["messages"] 里
def model_node(state: AtguiguState):
    reply = llm.invoke(state["messages"])  # 输入历史消息，调用模型
    return {"messages": [reply]}  # 返回新消息，自动加到 state


# ========== 4. 构建图结构 ==========
graph = StateGraph(AtguiguState)  # 初始化图，指定 State 类型

graph.add_node("model", model_node)  # 添加一个节点，名字叫 "model"

graph.add_edge(START, "model")  # 从 START 到 "model"
graph.add_edge("model", END)  # 从 "model" 到 END
# 打印图的边和节点信息
# print(graph.edges)
print()
# print(graph.nodes)

# ========== 5. 编译==========
app = graph.compile()

# ========== 6. 运行 ==========
# result = app.invoke({"messages": [HumanMessage(content="请用一句话解释什么是 LangGraph。")]})
result = app.invoke({"messages": "请用一句话解释什么是 LangGraph。"})

# 打印模型的最后一条回复
print("模型回答：", result["messages"][-1].content)

print()
# =========================
# 1. 打印图的ascii可视化结构
print(app.get_graph().print_ascii())
print("=" * 50)

# 2. 打印图的Mermaid代码可视化结构并通过https://www.processon.com/mermaid编辑器查看
print(app.get_graph().draw_mermaid())
print("=" * 50)

# 3. 生成 PNG并写入文件
# png_bytes = app.get_graph().draw_mermaid_png()
# output_path = "langgraph" + str(uuid.uuid4())[:8] + ".png"
# with open(output_path, "wb") as f:
#     f.write(png_bytes)
# print(f"图片已生成：{output_path}")
