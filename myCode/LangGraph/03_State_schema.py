"""'
 Schema  构成三要素 state_schema、input_schema 、output_schema
    1、state_schema  ：图的完整内部状态，包含了所有节点可能读写的字段，必须指定，不能为空
        特点： 是图的"全局状态空间"，所有节点都可以访问和写入这个 schema 中的任何字段
    2、input_schema ：定义图接受什么输入，是 state_schema 的子集
        特点： 可选参数，如果不指定，默认等于 state_schema，限制图的输入接口，只能传入这些字段
    3、output_schema：定义图返回什么输出，是 state_schema 的子集
        特点： 可选参数，如果不指定，默认等于 state_schema。限制图的输出接口，只返回这些字段

State可以是TypedDict类型，也可以是pydantic中的BaseModel类型：
    想要 轻量、无运行时开销、习惯字典写法 → 用 TypedDict
    想要 自动校验、默认值、嵌套结构、字段描述 → 用 pydantic.BaseModel
    两种写法在 LangGraph 里都能一键编译，只需按上例规则声明字段即可

"""

#  ====================== 使用 state 的默认方法  ========================

# from typing import TypedDict

# from langgraph.graph import END, START, StateGraph


# class BasicState(TypedDict):
#     """基本的 State定义"""

#     user_input: str
#     response: str
#     count: int
#     process_data: dict


# # 创建状态图，并指定状态结构
# basicState = StateGraph(BasicState)
# # 添加起始到结束的边（无中间节点）
# basicState.add_edge(START, END)
# # 编译生成计算图
# app = basicState.compile()

# # invoke()方法只接收状态字典作为核心参数
# initial_state = {
#     "user_input": "a",
#     "response": "resp",
#     "count": 25,
#     "process_data": {"k1": "v1"},  # process_data本身是dict类型，需嵌套
# }

# # invoke() 仅接收 1 个核心位置参数（状态字典），可选 1 个配置参数，切勿传入多个独立参数。
# result = app.invoke(initial_state)
# # 打印结果验证
# print("执行结果：", result)

#  =========================== 图输入输出模式和私有状态传递演示 ===========================
"""
LangGraph 图输入输出模式和私有状态传递演示

该演示展示了：
1. 如何定义图的输入和输出模式
"""

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


# 定义输入状态模式
class InputState(TypedDict):
    question: str


# 定义输出状态模式
class OutputState(TypedDict):
    answer: str


# 定义整体状态模式，结合输入和输出
class OverallState(InputState, OutputState):
    pass


# 定义处理节点
def answer_node(state: InputState):
    """
    处理输入并生成答案的节点
    Args:
        state: 输入状态
    Returns:
        dict: 包含答案的字典
    """
    print("执行 answer_node 节点:")
    print(f"  输入: {state}")

    # 示例答案
    answer = "再见" if "bye" in state["question"].lower() else "你好"
    result = {"answer": answer, "question": state["question"]}

    print(f"  输出: {result}")
    return result


def demo_input_output_schema():
    """演示输入输出模式"""
    print("=== 演示输入输出模式 ===")

    # 使用指定的输入和输出模式构建图
    builder = StateGraph(
        OverallState, input_schema=InputState, output_schema=OutputState
    )
    builder.add_edge(START, "answer_node")  # 定义起始边
    builder.add_node("answer_node", answer_node)  # 添加答案节点
    builder.add_edge("answer_node", END)  # 定义结束边
    graph = builder.compile()  # 编译图

    # 使用输入调用图并打印结果
    result = graph.invoke({"question": "你好"})
    print(f"图调用结果: {result}")
    # 打印图的ascii可视化结构
    print(graph.get_graph().print_ascii())
    print()


def main():
    """主函数"""
    print("=== LangGraph 图输入输出模式===\n")

    # 演示输入输出模式
    demo_input_output_schema()

    print("=== 演示完成 ===")


if __name__ == "__main__":
    main()
