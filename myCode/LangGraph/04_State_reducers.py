"""'
状态合并策略（Reducers）  : “字段级合并策略”，它让节点只需吐出“增量”，框架负责按规则把增量焊进全局 State

Reducer函数在LangGraph中的作用：
        控制状态更新方式：决定新值如何与现有值合并。
        处理并行更新：当多个节点同时更新同一字段时，确保数据一致性。
        提供灵活性：支持不同的合并策略，如覆盖、追加、相加等。
        增强表达力：允许开发者根据业务需求自定义合并逻辑。
通过合理使用Reducer函数，可以构建更强大和灵活的状态管理机制，特别是在处理复杂工作流和并行执行场景时。

Reducer常用函数有以下几种:
    1、default：未指定Reducer时使用覆盖更新   ----- 主流
    2、add_messages：用于消息列表追加
    3、operator.add：将元素追加到现有元素中，支持列表、字符串、数值类型的追加
    4、operator.mul：用于数值相乘
    5、自定义Reducer：支持用户自定义合并逻辑


"""

#  ============================== 默认Reducer（覆盖更新） =========================================================
"""
如果未明确指定reducer函数，则默认对该键的更新是覆盖行为。
LangGraph Reducer函数演示 - 默认Reducer（覆盖更新）

直接覆盖：
如果没有为状态字段指定 Reducer，默认会覆盖更新。
也就是说，后执行的节点返回的值会直接覆盖先执行节点的值，
即下一个节点的State数据是上一个节点的返回。
"""

# from typing import List

# from langgraph.graph import END, START, StateGraph
# from typing_extensions import TypedDict


# # 1. 默认Reducer（覆盖更新）
# # 未指定合并策略，默认覆盖，上一个节点的返回是下一个节点的值
# class DefaultReducerState(TypedDict):
#     foo: int
#     bar: list[str]


# def node_default_1(state: DefaultReducerState) -> dict:
#     print(state["foo"])
#     print(state["bar"])
#     return {"foo": 22}


# def node_default_2(state: DefaultReducerState) -> dict:
#     print()
#     print(state["foo"])
#     print(state["bar"])
#     return {"bar": ["bye1", "bye2", "bye3"]}


# def main():
#     print("1. 默认Reducer（覆盖更新）演示:\n")
#     builder = StateGraph(DefaultReducerState)

#     builder.add_node("node1", node_default_1)
#     builder.add_node("node2", node_default_2)

#     builder.add_edge(START, "node1")
#     builder.add_edge("node1", "node2")
#     builder.add_edge("node2", END)

#     graph = builder.compile()

#     result = graph.invoke(input={"foo": 1, "bar": ["hi"]})
#     # print(f"初始状态: {{'foo': 1, 'bar': ['hi']}}")
#     print(f"执行结果: {result}\n")


# if __name__ == "__main__":
#     main()


#  ============================== add_messages Reducer（消息列表专用）） =========================================================


# """
# LangGraph Reducer函数演示 - add_messages Reducer（消息列表专用）
# """

# from typing import Annotated

# from langgraph.graph import END, START, StateGraph
# from langgraph.graph.message import add_messages
# from typing_extensions import TypedDict


# # 2. add_messages Reducer（消息列表专用）
# class AddMessagesState(TypedDict):
#     """
#     引入的 Annotated 类型，它允许给类型添加额外的元数据。
#     messages: Annotated[List, add_messages]
#     表示:
#     - messages 我的状态里只有一个字段叫 messages，类型是是 List列表类型,
#     - add_messages  这里的 add_messages 是一个函数，用于修改 messages 列表
#                     每当节点返回对 messages 的“局部更新”时，
#                     请用 add_messages 规约器把它合并到旧列表上（追加，而不是覆盖）
#     总结：
#     节点永远只 return 增量字典，不用手动把旧列表读出来再拼接。
#     add_messages 在后台帮你完成“追加”动作；如果换成默认 reducer，旧消息会被整份替换掉
#     """

#     messages: Annotated[list, add_messages]


# def chat_node_1(state: AddMessagesState) -> dict:
#     return {"messages": [("assistant", "Hello from node 1")]}


# def chat_node_2(state: AddMessagesState) -> dict:
#     return {"messages": [("assistant", "Hello from node 2")]}


# def run_demo():
#     print("2. add_messages Reducer（消息列表专用）演示:")
#     builder = StateGraph(AddMessagesState)
#     builder.add_node("chat1", chat_node_1)
#     builder.add_node("chat2", chat_node_2)

#     builder.add_edge(START, "chat1")
#     builder.add_edge(START, "chat2")  # 并行执行
#     builder.add_edge("chat1", END)
#     builder.add_edge("chat2", END)
#     graph = builder.compile()

#     result = graph.invoke({"messages": [("user", "Hi there!")]})
#     print("初始状态: {'messages': [('user', 'Hi there!')]}")
#     print(f"执行结果: {result}\n")

#     print("*" * 60)

#     # 打印图的ascii可视化结构
#     print(graph.get_graph().print_ascii())


# if __name__ == "__main__":
#     run_demo()


#  ============================== operator.add Reducer（列表追加） =========================================================

# """
# LangGraph Reducer函数演示 - operator.add Reducer（列表追加）
# """

# import operator
# from typing import Annotated

# from langgraph.graph import END, START, StateGraph
# from typing_extensions import TypedDict


# # 3. operator.add Reducer（列表追加）
# class ListAddState(TypedDict):
#     # data: Annotated[List[int], None]  #默认覆盖
#     data: Annotated[list[int], operator.add]  # （列表追加）


# def producer_1(state: ListAddState) -> dict:
#     return {"data": [1, 2]}


# def producer_2(state: ListAddState) -> dict:
#     return {"data": [3, 4]}


# def run_demo():
#     builder = StateGraph(ListAddState)
#     # 注册节点
#     builder.add_node("producer1", producer_1)
#     builder.add_node("producer2", producer_2)
#     # 顺序执行边
#     builder.add_edge(START, "producer1")
#     builder.add_edge("producer1", "producer2")
#     builder.add_edge("producer2", END)

#     graph = builder.compile()
#     result = graph.invoke({"data": [0]})
#     print("初始状态: {'data': [0]}")
#     print(f"执行结果: {result}\n")


# if __name__ == "__main__":
#     run_demo()


#  ============================== operator.add 字符串连接Reducer =========================================================


# """
# LangGraph Reducer函数演示 - 字符串连接Reducer
# """

# import operator
# from typing import Annotated

# from langgraph.graph import END, START, StateGraph
# from typing_extensions import TypedDict


# # 6. 字符串连接Reducer
# class StringConcatState(TypedDict):
#     text: Annotated[str, operator.add]


# def add_text_1(state: StringConcatState) -> dict:
#     return {"text": "Hello "}


# def add_text_2(state: StringConcatState) -> dict:
#     return {"text": "World!"}


# def run_demo():
#     print("3.2 字符串连接Reducer演示:")

#     builder = StateGraph(StringConcatState)

#     builder.add_node("add_text_1", add_text_1)
#     builder.add_node("add_text_2", add_text_2)

#     builder.add_edge(START, "add_text_1")
#     builder.add_edge(START, "add_text_2")  # 并行执行
#     builder.add_edge("add_text_1", END)
#     builder.add_edge("add_text_2", END)

#     graph = builder.compile()

#     result = graph.invoke({"text": "Say: "})
#     print(f"初始状态: {{'text': 'Say: '}}")
#     print(f"执行结果: {result}\n")


# if __name__ == "__main__":
#     run_demo()


#  ============================== operator.add 数值累加Reducer  =========================================================

# """
# LangGraph Reducer函数演示 - 数值累加Reducer
# """

# import operator
# from typing import Annotated

# from langgraph.graph import END, START, StateGraph
# from typing_extensions import TypedDict


# # 7. 数值累加Reducer
# class NumberAddState(TypedDict):
#     count: Annotated[int, operator.add]


# def increment_1(state: NumberAddState) -> dict:
#     return {"count": 5}


# def increment_2(state: NumberAddState) -> dict:
#     return {"count": 3}


# def run_demo():
#     print("3.3 数值累加Reducer演示:")
#     builder = StateGraph(NumberAddState)
#     builder.add_node("increment_1", increment_1)
#     builder.add_node("increment_2", increment_2)
#     # 顺序执行边
#     builder.add_edge(START, "increment_1")
#     builder.add_edge("increment_1", "increment_2")
#     builder.add_edge("increment_2", END)

#     graph = builder.compile()

#     result = graph.invoke({"count": 10})
#     print("初始状态: {'count': 10}")
#     print(f"执行结果: {result}\n")


# if __name__ == "__main__":
#     run_demo()


#  ============================== 自定义 规则  =========================================================

from typing import Annotated

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


def MyOperatorMul(current: float, update: float) -> float:
    """自定义乘法reducer，处理初始值为1.0"""
    # 如果是第一次调用，current会是默认值0.0
    if current == 0.0:
        # 对于乘法，恒等元应该是1.0或者 return 1.0 * update
        print(f"current:{current}")
        print(f"update:{update}")
        return 1.0 * update
    return current * update


class MultiplyState(TypedDict):
    factor: Annotated[float, MyOperatorMul]  # 设置自定义规则


def multiplier(state: MultiplyState) -> dict:
    return {"factor": 2.0}


def run_demo():
    print("使用自定义reducer解决乘法问题:")
    builder = StateGraph(MultiplyState)
    builder.add_node("multiplier", multiplier)
    builder.add_edge(START, "multiplier")
    builder.add_edge("multiplier", END)
    graph = builder.compile()

    result = graph.invoke({"factor": 5.0})
    print("初始状态: {'factor': 5.0}")
    print(f"执行结果: {result}")  # 应该是 {'factor': 10.0}
    print("解释: 5.0 * 2.0 = 10.0\n")


if __name__ == "__main__":
    run_demo()
