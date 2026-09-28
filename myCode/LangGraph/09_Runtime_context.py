# 创建图时，可以指定运行时上下文，将上下文信息（不属于图状态的信息）传递给节点，以便节点中使用，例如模型名称或数据库连接等。
# 使用 context_schema 的优势：
# （1）分离关注点：将运行时配置与图状态分离，保持状态的纯净性
# （2）类型安全：通过定义数据类，提供类型检查和 IDE 自动补全支持
# （3）易于管理：统一管理运行时依赖，如数据库连接、API密钥等

# 类似微服务的YML文件，配置和代码分离，信息从配置文件读取

# 使用方式
# Context Schema（上下文结构） :使用 @dataclass 定义了一个 ContextSchema类，定义的内容不属于图的状态，但在运行时需要被节点访问
# 节点函数定义 :节点函数接收两个参数：state（图的状态）和 runtime（运行时上下文）,通过 runtime.context 访问上下文信息，如 runtime.context.model_name
# 图的创建和执行 :创建 StateGraph 时传入 context_schema=ContextSchema 参数,调用 graph.invoke() 时通过 context 参数传递上下文数据
#
#

"""
RuntimeContextDemo.py

LangGraph Context Schema 演示

演示如何在 LangGraph 1.0 中使用 context_schema 向节点传递不属于图表状态的信息。
这在传递模型名称、数据库连接等依赖项时非常有用。
"""

from dataclasses import dataclass
from typing import Annotated

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.runtime import Runtime
from typing_extensions import TypedDict


# 定义状态结构
class AgentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]
    response: str


# 定义上下文结构
@dataclass
class ContextSchema:
    model_name: str
    db_connection: str
    api_key: str


# 节点函数：处理用户消息
def process_message(state: AgentState, runtime: Runtime[ContextSchema]) -> dict:
    """处理用户消息的节点，使用context中的信息"""
    print("执行节点: process_message")

    # 获取最新的用户消息
    last_message = state["messages"][-1].content if state["messages"] else ""
    print(f"用户消息: {last_message}")
    print("=========以下是从RuntimeContext中获得信息=========")
    # 使用runtime.context中的信息
    model_name = runtime.context.model_name
    db_connection = runtime.context.db_connection
    api_key = runtime.context.api_key

    print(f"使用的模型: {model_name}")
    print(f"数据库连接: {db_connection}")
    print(f"API密钥前缀: {api_key[:5]}***")  # 只显示前5位，隐藏其余部分

    # 模拟使用这些信息处理请求
    response = f"使用 {model_name} 处理了您的请求，已连接到 {db_connection}"

    return {"messages": [AIMessage(content=response)], "response": response}


# 节点函数：生成最终响应
def generate_response(state: AgentState, runtime: Runtime[ContextSchema]) -> dict:
    """生成最终响应的节点"""
    print("执行节点: generate_response")

    # 使用runtime.context中的信息
    model_name = runtime.context.model_name
    print(f"使用模型 {model_name} 生成最终响应")

    # 获取之前的结果
    previous_response = state["response"]

    # 生成更详细的响应
    final_response = f"{previous_response}\n\n这是使用 {model_name} 生成的完整响应。"

    return {"messages": [AIMessage(content=final_response)], "response": final_response}


def main():
    """演示 context_schema 的使用"""
    print("=== Context Schema 演示 ===\n")

    # 定义上下文
    context = ContextSchema(
        model_name="gpt-4-turbo",
        db_connection="postgresql://user:pass@localhost:5432/orders_db",
        api_key="sk-abcdefghijklmnopqrstuvwxyz123456",
    )

    # 创建图，指定state_schema和context_schema
    builder = StateGraph(AgentState, context_schema=ContextSchema)

    # 添加节点
    builder.add_node("process_message", process_message)
    builder.add_node("generate_response", generate_response)

    # 添加边
    builder.add_edge(START, "process_message")
    builder.add_edge("process_message", "generate_response")
    builder.add_edge("generate_response", END)

    # 编译图
    graph = builder.compile()

    # 定义初始状态
    initial_state = {
        "messages": [HumanMessage(content="请帮我查询最新的订单信息")],
        "response": "",
    }

    print("初始状态:", initial_state)
    print()
    print(
        "上下文信息:\n",
        {
            "model_name": context.model_name,
            "db_connection": context.db_connection,
            "api_key": f"{context.api_key[:5]}***",
        },
    )
    print("\n" + "-" * 50 + "\n")

    # 执行图，通过context参数传递上下文
    result = graph.invoke(initial_state, context=context)

    print("\n" + "=" * 50)
    print("最终状态:", result)
    print("\n最终响应:")
    print(result["response"])


if __name__ == "__main__":
    main()
