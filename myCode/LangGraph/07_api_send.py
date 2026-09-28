# Send和Command是两种用于实现高级工作流控制的核心机制，用于支持动态地决定下一步执行哪个节点

# Map-Reduce(映射 - 归约) :将一个「大规模的复杂计算任务」拆解成无数个「小任务」并行处理，最后再把小任务的结果汇总得到最终答案。
#  1、Map 直译是「映射」，核心行为是：「拆分 + 局部处理」
#  2、Reduce 直译是「归约」，核心行为是：「聚合 + 全局计算」
#
# 核心思想：拆分任务 →并行执行 → 统一汇总结果
#
# 为了支持这种设计模式，LangGraph支持从条件边返回 Send 对象
#
#
# Send ：多路并进，汇总规约
#      动态创建多个执行分支，实现并行处理，每个Send对象都指定了一个执行目标节点和传递给该节点的参数，
#      LangGraph会并行执行所有的这些任务,常用在Map-Reduce的场景，并行执行多个子节点并最终汇总到一个总节点。


"""
SendDemo.py
LangGraph Map-Reduce 模式演示
通过使用 Send 对象，LangGraph 提供了一种优雅的方式来实现这种动态图结构，
使得我们可以根据运行时状态来决定执行路径。

解释：
（1）首先执行 generate_subjects主题列表节点，生成主题列表：['猫', '狗', '程序员']
（2）然后通过条件边函数 map_subjects_to_jokes 为每个主题创建一个 Send 对象
（3）make_joke 节点被并行执行3次，每次处理一个主题
（4）最终将所有生成的笑话合并到一个列表中
这种模式非常适合处理动态数量的任务
"""

from typing import Annotated, List  # noqa: UP035

from langgraph.graph import END, START, StateGraph
from langgraph.types import Send
from typing_extensions import TypedDict


# 定义状态
class AtguiguState(TypedDict):
    subjects: list[str]
    jokes: Annotated[list[str], lambda x, y: x + y]  # 使用列表合并的方式


# 第一个节点：生成需要处理的主题列表
def generate_subjects(state: AtguiguState) -> dict:
    """生成需要处理的主题列表"""
    print("执行节点(第一个节点：生成需要处理的主题列表): generate_subjects")
    subjects = ["猫", "狗", "程序员"]
    print(f"生成主题列表: {subjects}")
    return {"subjects": subjects}


# Map节点：为每个主题生成笑话
def make_joke(state: AtguiguState) -> dict:
    """为单个主题生成笑话"""
    subject = state.get("subject", "未知")
    print(f"执行节点: make_joke，处理主题: {subject}")

    # 根据主题生成相应笑话
    jokes_map = {
        "猫": "为什么猫不喜欢在线购物？因为它们更喜欢实体店！",
        "狗": "为什么狗不喜欢计算机？因为它们害怕被鼠标咬！",
        "程序员": "为什么程序员喜欢洗衣服？因为他们在寻找bugs！",
        "未知": "这是一个关于未知主题的神秘笑话。",
    }

    joke = jokes_map.get(subject, f"这是一个关于{subject}的即兴笑话。")
    print(f"生成笑话: {joke}")
    return {"jokes": [joke]}


# 条件边函数：根据主题列表生成Send对象列表
def map_subjects_to_jokes(state: AtguiguState) -> List[Send]:
    """将主题列表映射到joke生成任务"""
    print("执行条件边函数: map_subjects_to_jokes")
    subjects = state["subjects"]
    print(f"映射主题到joke任务: {subjects}")

    # 为每个主题创建一个Send对象，指向make_joke节点
    # 每个Send对象包含节点名称和传递给该节点的状态
    send_list = [Send("make_joke", {"subject": subject}) for subject in subjects]
    print(f"生成Send对象列表: {send_list}")
    return send_list


def main():
    """演示Map-Reduce模式"""
    print("=== Map-Reduce 模式演示 ===\n")

    # 创建图
    builder = StateGraph(AtguiguState)

    # 添加节点
    builder.add_node("generate_subjects", generate_subjects)
    builder.add_node("make_joke", make_joke)

    # 添加边
    builder.add_edge(START, "generate_subjects")

    # 添加条件边，使用Send对象实现map-reduce    相当于并行边
    builder.add_conditional_edges(
        "generate_subjects",  # 源节点
        map_subjects_to_jokes,  # 路由函数，返回Send对象列表
    )

    # 从make_joke到结束
    builder.add_edge("make_joke", END)

    # 编译图
    graph = builder.compile()
    print(graph.get_graph().print_ascii())

    # 执行图
    initial_state = {"subjects": [], "jokes": []}
    print("初始状态:", initial_state)
    print("\n开始执行图...")

    result = graph.invoke(initial_state)
    print(f"\n最终结果: {result}")

    print("\n=== 演示完成 ===")


if __name__ == "__main__":
    main()
