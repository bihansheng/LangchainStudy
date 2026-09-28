# 在LangGraph中，节点(Node)就是是Python函数（可以是同步的，也可以是异步的），它们接受以下参数：
#   Ø state：图的状态
#   Ø config：一个RunnableConfig对象，包含诸如thread_id之类的配置信息以及诸如tags之类的跟踪信息
#   Ø runtime：一个Runtime对象，包含运行时context以及其他信息，如store和stream_writer
#   定义好node函数后，使用add_node方法将这些节点添加到图中。如果在向图中添加节点时未指定名称，系统会为其分配一个与函数名相同的默认名称。
#
#
# Node是LangGraph中的一个基本处理单元，代表工作流中的一个操作步骤，
# 可以是一个Agent、调用大模型、工具或一个函数（说白了就是绑定一个python函数，具体逻辑可以干任何事情）
#
# Node的设计原则
#  1、单一职责原则：每个节点应该只负责一项职责，避免功能过于复杂
#  2、无状态设计：节点本身不应该保存状态，所有数据都通过输入状态传递
#  3、幂等性：相同的输入应该产生相同的输出，确保可重试性
#  4、可测试性：节点逻辑应该易于单元测试
#
#
# 特殊的节点 __START__ （开始节点）和 __END__（结束节点）：
#   __START__节点：开始节点，确定应该首先调用哪些节点
#   __END__节点：终止节点，表示后续没有其他节点可以继续执行了
#
#
# 节点缓存Node Caching
#    LangGraph支持基于节点输入对任务/节点进行缓存。使用缓存的方法如下：
#         1、编译图（或指定入口点）时指定缓存。
#         2、为节点指定缓存策略。每个缓存策略支持：
#            Ø key_func用于根据节点的输入生成缓存键。
#            Ø ttl，即缓存的生存时间（以秒为单位）。如果未指定，缓存将永不过期。
#   缓存键与命中：
#     当一个节点开始执行时，系统会使用其配置的 key_func 根据当前节点的输入数据生成一个唯一的键。LangGraph 会检查缓存中是否存在这个键。
#           如果存在（缓存命中），则直接返回之前存储的结果，跳过该节点的实际执行。
#           如果不存在（缓存未命中），则正常执行节点函数，并将结果与缓存键关联后存入缓存。
#   缓存有效期：
#       ttl 参数能控制缓存的有效期。
#       例如，对于依赖实时数据的天气查询节点，可以设置较短的 ttl（如60秒）。而对于处理静态信息或变化不频繁数据的节点，则可以设置较长的 ttl甚至不设置（None），让缓存永久有效，直到手动清除
#
#
# 错误处理和重试机制
#  LangGraph还提供了错误处理和重试机制来指定重试次数、重试间隔、重试异常等，用于保证系统的可靠性
#   为节点添加重试策略，需要在add_node中设置retry_policy参数。retry_policy参数接受一个RetryPolicy命名元组对象。
#   默认情况下，retry_on参数使用default_retry_on函数，该函数会在遇到任何异常时重试
#
#
#
#
#
#
#

#  ========================================== 默认示例  ========================

# from functools import partial
# from typing import TypedDict

# from langgraph.graph import END, START, StateGraph
# from langgraph.types import RetryPolicy
# from requests import RequestException, Timeout


# # 定义状态
# class GraphState(TypedDict):
#     process_data: dict  # 默认更新策略


# # 定义一个节点，入参为state
# def input_node(state: GraphState) -> GraphState:
#     print(f"input_node收到的初始值:{state}")
#     return {"process_data": {"input": "input_value"}}


# # 定义带参数的node节点
# def process_node(state: dict, param1: int, param2: str) -> dict:
#     print(state, param1, param2)
#     return {"process_data": {"process": "process_value"}}


# # 重试策略,add_node方法时可选
# retry_policy = RetryPolicy(
#     max_attempts=3,  # 最大重试次数
#     initial_interval=1,  # 初始间隔
#     jitter=True,  # 抖动（添加随机性避免重试风暴）
#     backoff_factor=2,  # 退避乘数（每次重试间隔时间的增长倍数）
#     retry_on=[RequestException, Timeout],  # 只重试这些异常
# )


# stateGraph = StateGraph(GraphState)
# # 添加inpu节点
# stateGraph.add_node("input", input_node)
# # 给process_node节点绑定参数
# process_with_params = partial(process_node, param1=100, param2="test")
# # 添加带参数的node节点
# stateGraph.add_node("process", process_with_params, retry=retry_policy)

# # 定义节点之间的执行顺序 edges
# # 设置节点间的依赖关系，形成执行流程图
# stateGraph.add_edge(START, "input")
# stateGraph.add_edge("input", "process")
# stateGraph.add_edge("process", END)

# # 编译图构建器生成计算图
# graph = stateGraph.compile()


# # # 打印图的边和节点信息
# print(stateGraph.edges)
# print(stateGraph.nodes)
# # 打印图的可视化结构
# print(graph.get_graph().print_ascii())

# print()

# # 定义一个初始状态字典，包含键值对"x": 5
# initial_state = {"process_data": 5}
# # 调用graph对象的invoke方法，传入初始状态，执行图计算流程
# result = graph.invoke(initial_state)
# print(f"最后的结果是:{result}")


#  ========================================== 缓存示例  ========================

# import time

# from langgraph.cache.memory import InMemoryCache
# from langgraph.graph import StateGraph
# from langgraph.types import CachePolicy
# from typing_extensions import TypedDict


# # 定义状态类，也就是你的业务实体entity
# class State(TypedDict):
#     x: int
#     result: int

# # 创建图
# builder = StateGraph(State)

# # 定义节点：模拟耗时计算（sleep3秒）
# def expensive_node(state: State) -> dict[str, int]:
#     time.sleep(3)
#     return {"result": state["x"] * 2}

# #     builder.add_node("node1", node_default_1)

# # 添加节点
# builder.add_node(node="expensive_node",action=expensive_node,
#     # 不用传key_fn，底层自动用默认逻辑
#     cache_policy=CachePolicy(ttl=8)
# )

# # 设置入口和出口
# builder.set_entry_point("expensive_node")
# builder.set_finish_point("expensive_node")

# # 编译图，指定内存缓存
# app = builder.compile(cache=InMemoryCache())

# # 第一次执行：耗时3秒（无缓存）
# print("第一次执行（无缓存，耗时3秒）：")
# print(app.invoke({"x": 5}))
# # 第二次执行：瞬间返回（利用缓存，8秒内有效）
# print("\n1111111111111111111111111111")
# print("第二次运行利用缓存并快速返回：")
# print(app.invoke({"x": 5}))

# # 可选：测试8秒后缓存过期（取消注释查看）
# print("\n等待8秒，缓存过期...")
# time.sleep(8)
# print("8秒后第三次执行（重新计算，耗时3秒）：")
# print(app.invoke({"x": 5}))


#  ========================================== 节点重试策略演示  ========================

"""
LangGraph 节点重试策略演示

默认重试策略：max_attempts=5，对Exception重试、对ValueError/TypeError等不重试，异常过滤列表完全相同；
自定义重试策略：max_attempts=5 + custom_retry_on，仅对包含{模拟API调用失败}的异常重试；throw new RuntimeExp("模拟API调用失败")
不可重试测试：ValueError直接抛错，无重试，max_attempts=3
"""

from typing import Any

from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy
from typing_extensions import TypedDict


# 定义状态类型
class AtguiguState(TypedDict):
    result: str


# 全局计数器：记录API尝试次数
attempt_counter = 0


# 工具函数
def build_retry_graph(node_name: str, node_func, retry_policy: RetryPolicy):
    builder = StateGraph(AtguiguState)
    # 为节点添加重试策略，需要在add_node中设置retry_policy参数。
    # retry_policy参数接受一个RetryPolicy命名元组对象。
    # 默认情况下，retry_on参数使用default_retry_on函数，该函数会在遇到任何异常时重试
    builder.add_node(node_name, node_func, retry_policy=retry_policy)
    builder.add_edge(START, node_name)
    builder.add_edge(node_name, END)
    return builder.compile()


# 模拟不稳定的API调用，使用全局变量跟踪尝试次数
def unstable_api_call(state: AtguiguState) -> dict[str, Any]:
    """模拟不稳定API：前2次失败，第3次成功（全局计数器记录尝试次数）"""
    global attempt_counter
    attempt_counter += 1
    # 纯文本打印尝试次数
    print(f"尝试调用API，这是第 {attempt_counter} 次尝试")

    # 模拟失败/成功逻辑：前2次抛异常，第3次返回结果
    if attempt_counter < 3:
        raise Exception(f"模拟API调用失败abcd (尝试 {attempt_counter})")  # noqa: TRY002
    return {"result": f"API调用成功，经过 {attempt_counter} 次尝试"}


# 自定义重试条件判断函数
def custom_retry_on(exception: Exception) -> bool:
    """自定义重试规则：只对包含「模拟API调用失败」的异常重试"""
    print("########################:  " + str(exception))
    err_msg = str(exception)
    if "模拟API调用失败" in err_msg:
        print(f"捕获到可重试异常: {err_msg}")
        return True
    print(f"捕获到不可重试异常: {err_msg}")
    return False


# 模拟抛出 ValueError 的节点
def value_error_call(state: AtguiguState) -> dict[str, Any]:
    """模拟抛出ValueError：默认重试策略对这类异常不重试"""
    print("调用会抛出 ValueError 的节点")
    raise ValueError("模拟 ValueError 异常")


# 测试方法1：默认重试策略
def test_default_retry():
    global attempt_counter
    print("1. 使用默认重试策略:")
    print("   默认策略会对除特定异常外的所有异常进行重试")
    print("   不会重试的异常包括: ValueError, TypeError, ArithmeticError, ImportError,")
    print("                     LookupError, NameError, SyntaxError, RuntimeError,")
    print(
        "                     ReferenceError, StopIteration, StopAsyncIteration, OSError\n"
    )

    print("测试默认重试策略:")
    attempt_counter = 0  # 重置计数器
    default_graph = build_retry_graph(
        node_name="unstable_api",
        node_func=unstable_api_call,
        retry_policy=RetryPolicy(max_attempts=5),  # 最多5次尝试，足够重试成功
    )
    try:
        result = default_graph.invoke({"result": ""})
        print(f"最终结果: {result}\n")
    except Exception as e:  # noqa: BLE001
        print(f"最终失败: {type(e).__name__}: {e}\n")


# 测试方法2：自定义重试策略（输出完全匹配要求）
def test_custom_retry():
    global attempt_counter
    print("2. 使用自定义重试策略:")
    print("   自定义策略只对特定错误进行重试\n")
    print("测试自定义重试策略:")
    attempt_counter = 0  # 重置计数器
    custom_graph = build_retry_graph(
        node_name="custom_retry_api",
        node_func=unstable_api_call,
        retry_policy=RetryPolicy(max_attempts=5, retry_on=custom_retry_on),
    )
    try:
        result = custom_graph.invoke({"result": ""})
        print(f"最终结果: {result}\n")
    except Exception as e:  # noqa: BLE001
        print(f"最终失败: {type(e).__name__}: {e}\n")


# 测试方法3：不可重试异常演示,测试 ValueError（默认策略不会重试）
def test_no_retry_exception():
    print("3. 测试不会重试的异常类型:")
    print("测试 ValueError（默认策略不会重试）:")
    no_retry_graph = build_retry_graph(
        node_name="value_error_node",
        node_func=value_error_call,
        retry_policy=RetryPolicy(max_attempts=3),
    )
    try:
        result = no_retry_graph.invoke({"result": ""})
        print(f"最终结果: {result}\n")
    except Exception as e:  # noqa: BLE001
        print(f"最终失败: {type(e).__name__}: {e}\n")


# 主演示函数
def run_demo():
    print("=== LangGraph 节点重试策略完整演示===")
    print("-" * 80 + "\n")
    # test_default_retry()
    # test_custom_retry()
    test_no_retry_exception()
    print("-" * 80)
    print("=== 演示结束 ===")


# 程序入口
if __name__ == "__main__":
    run_demo()
