# 状态持久化
# 指的是在程序运行时将瞬间的状态保存下来，以便后续需要的时候能够重新恢复执行，用于解决因为程序退出、重启等事件而丢失任务。
# 在 LangGraph 如果使用了持久化，工作流执行的每个步骤结束后，系统会自动将当前整个图的状态（包括所有变量、历史消息、下一步要执行的节点等信息）完整地保存下来，
# 这份存档就是一个检查点（Checkpoint），LangGraph支持存储在内存、Redis、DB等存储介质中。

# 检查点通过thread_id（会话id，不是操作系统中的线程id）区分不同的会话，后续重新执行时会使用。
# 使用检查点调用图时，必须在配置的可配置部分指定thread_id。
# {"configurable": {"thread_id": "user-001"}}


# 短期记忆（Checkpointer）

# 载体：Checkpointer（MemorySaver、RedisSaver、PostgresSaver…）
# 作用：把每轮消息 + 工具调用结果序列化成图状态，按 thread_id 持久化；下次传入相同 thread_id 自动续写。
# 原理：
# 每次你调用 graph.invoke(...) 或 graph.stream(...)，LangGraph 都会维护一个状态（state）。
# 如果没有 Checkpointer，这个 state 默认只存在本次调用内，调用结束就丢掉了。
# 如果启用了 Checkpointer，...

# 长期记忆（BaseStore）

# 载体：BaseStore（InMemoryStore、RedisStore、AsyncPostgresStore…）
# 作用：显式保存“用户偏好”“背景事实”等高密度信息，由 LLM 主动读写；Store 支持向量检索，支持命名空间隔离。

# 和 Checkpointer 的区别：
# Checkpointer：保存图的运行状态（短期记忆，主要用于同一个线程连续对话）。
# Store：LangGraph的存储模块提供持久化的键值存储，支持跨线程和会话的长期内存，适用于需持久化数据的复杂工作流。


#   ======================= LangGraph 1.0 持久化存储演示 - 内存存储 (In-Memory) ================================

"""
MemoryPersistence.py
langgraph-checkpoint：检查点保存器（BaseCheckpointSaver）
的基础接口以及序列化/反序列化接口（SerializerProtocol）。
包含用于实验的内存中检查点实现（InMemorySaver）。
LangGraph 已内置 langgraph-checkpoint。



特点：
- 数据暂存于内存，程序关闭后丢失
- 无需额外配置
- 适用于本地测试和临时验证工作流逻辑
"""

# import operator
# from typing import Annotated

# from langgraph.checkpoint.memory import InMemorySaver
# from langgraph.graph import END, START, StateGraph
# from typing_extensions import TypedDict


# # 定义状态
# class PersistenceDemoState(TypedDict):
#     # operator.add：将元素追加到现有元素中，支持列表、字符串、数值类型的追加
#     messages: Annotated[list, operator.add]
#     step_count: Annotated[int, operator.add]


# # 节点函数
# def step_one(state: PersistenceDemoState) -> dict:
#     print("执行步骤 1")
#     return {"messages": ["执行了步骤 1"], "step_count": 1}


# def step_two(state: PersistenceDemoState) -> dict:
#     print("执行步骤 2")
#     return {"messages": ["执行了步骤 2"], "step_count": 1}


# def step_three(state: PersistenceDemoState) -> dict:
#     print("执行步骤 3")
#     return {"messages": ["执行了步骤 3"], "step_count": 1}


# # 构建图
# def create_graph():
#     builder = StateGraph(PersistenceDemoState)

#     builder.add_node("step_one", step_one)
#     builder.add_node("step_two", step_two)
#     builder.add_node("step_three", step_three)

#     builder.add_edge(START, "step_one")
#     builder.add_edge("step_one", "step_two")
#     builder.add_edge("step_two", "step_three")
#     builder.add_edge("step_three", END)

#     return builder


# def main():
#     print("=== LangGraph 1.0 内存持久化存储演示 ===\n")

#     # 编译图并使用内存存储
#     graph = create_graph()
#     app = graph.compile(checkpointer=InMemorySaver())

#     # 配置线程ID用于存储状态
#     config = {"configurable": {"thread_id": "user_13811112222"}}

#     print("1. 首次执行工作流:")
#     result = app.invoke({"messages": ["开始执行"], "step_count": 0}, config)

#     print(f"执行结果result: {result}\n")

#     print("2. 检查存储的状态:")
#     saved_state = app.get_state(config)
#     print(f"保存的状态: {saved_state.values}")
#     print(f"下一个节点: {saved_state.next}\n")

#     # 获取指定线程的完整执行历史（正序：从最早到最晚,第一步在栈底）
#     history = app.get_state_history(config)
#     # 遍历历史中的每一个检查点快照
#     for checkpoint in history:
#         print("=" * 50)
#         # 该时刻的完整State状态（最核心）
#         print(f"当前状态: {checkpoint.values}")

#     print("=" * 80)
#     print("3. 恢复执行工作流:")
#     # 由于工作流已经完成，这里会直接返回最终结果
#     result2 = app.invoke(None, config)
#     print(f"恢复执行结果: {result2}\n")

#     print("=== 演示结束 ===")


# if __name__ == "__main__":
#     main()

#   ======================= 数据库检查点(sqlite)================================

"""
SqlitePersistence.py
在底层，检查点功能由符合BaseCheckpointSaver接口的检查点对象提供支持。
LangGraph提供了多种检查点实现，所有这些实现都通过独立的、可安装的库来完成，数据库类型的有：
	langgraph-checkpoint-sqlite：使用SQLite数据库（SqliteSaver / AsyncSqliteSaver）存储检查点。
非常适合实验和本地工作流程。需要单独安装。
	langgraph-checkpoint-postgres：使用Postgres数据库（PostgresSaver / AsyncPostgresSaver）
存储检查点，用于LangSmith。非常适合在生产环境中使用。需要单独安装。
......

本次案例，安装sqlite所需依赖
pip install langgraph-checkpoint-sqlite

"""

# import operator
# import sqlite3
# from typing import Annotated, TypedDict

# from langgraph.checkpoint.sqlite import SqliteSaver
# from langgraph.graph import END, START, StateGraph


# class MyState(TypedDict):
#     messages:Annotated[list,operator.add]

# def node_1(state:MyState):

#     return {"messages":["abc","def"]}

# def main():
# 	# 数据存储到D:\\44目录下面，需要目录存在
#     conn = sqlite3.connect(database="D:\\44\\sqlite_data.db",check_same_thread=False)
#     sqliteDB = SqliteSaver(conn=conn)

#     builder = StateGraph(MyState)
#     builder.add_node("node_1",node_1)

#     builder.add_edge(START, "node_1")
#     builder.add_edge("node_1", END)

#     graph = builder.compile(checkpointer=sqliteDB)
#     # 同一个用户id下，每次执行都会插入一次新数据，上课时记得修改用户编号或者直接删除D:\\44\\sqlite_data.db
#     config = {"configurable": {"thread_id": "user-001"}}

#     initial_state = graph.get_state(config)
#     print(f"Initial state: {initial_state}")

#     # 执行图
#     result = graph.invoke({"messages":[]}, config)
#     print(f"Result: {result}")

#     print()
#     print("====================查看执行后的状态====================")
#     # 查看执行后的状态
#     final_state = graph.get_state(config)
#     print()
#     print(f"Final state: {final_state}")

#     conn.close()

# if __name__ == '__main__':
#     main()


#   ======================= 预构建 Agent 实现记忆存储 ================================


import os

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

# ==========定义大模型 ==========
llm = init_chat_model(
    model="qwen-plus",
    model_provider="openai",
    api_key=os.getenv("aliQwen-api"),
    temperature=0.0,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 定义短期记忆使用内存（生产可以换 RedisSaver/PostgresSaver）
checkpointer = InMemorySaver()
agent = create_agent(model=llm, checkpointer=checkpointer)
# 多轮对话配置，同一 thread_id 即同一会话
config = {"configurable": {"thread_id": "user-001"}}

msg1 = agent.invoke(
    {"messages": [("user", "你好，我叫张三，喜欢足球，60字内简洁回复")]}, config
)
msg1["messages"][-1].pretty_print()

# 6. 第二轮（继续同一 thread）
msg2 = agent.invoke({"messages": [("user", "我叫什么？我喜欢做什么？")]}, config)
msg2["messages"][-1].pretty_print()
