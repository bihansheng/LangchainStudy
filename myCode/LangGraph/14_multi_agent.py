# 多智能体 (Multi-Agent)

# 在AI技术快速发展的今天，两个关键协议正在重塑我们构建智能系统的方式：
# Google的Agent-to-Agent协议(A2A)和Model Context Protocol(MCP)。
# 这两个协议代表了AI架构发展的不同维度，但它们共同指向一个未来：我们正从确定性编程转向自主协作系统


# 协议的本质区别：工具vs代理
# 1、 MCP（Model Context Protocol）
#       本质上是关于工具访问的协议。它定义了大语言模型如何与各种工具、数据和资源交互的标准方式。
#       简单来说，MCP让AI能够使用各种功能，就像程序员调用函数一样。
# 2、A2A（Agent-to-Agent Protocol）
#      则专注于代理协作。
#      它建立了智能代理之间相互发现、交流和合作的方式，使得不同的AI系统能够像人类团队一样协同工作。
#
# MCP是工具车间
#   它让工人（AI模型）知道每个工具（API、函数）的位置、用途和使用方法，但不指导工人之间如何合作。
# A2A是会议室
#   它让不同专业人士（专业AI代理）能坐在一起，理解彼此的专长，并协调如何共同完成复杂任务。


# 常见的连接智能体的方式
# 1、Network（网络型）：
#      多个智能体平等存在，每个 Agent 可以和其他 Agent 通信，类似“去中心化网络”
# 2、Supervisor（监督者型）
#      一个主控 Agent（Supervisor），调度其他 Agent子 Agent 只负责各自领域
# 3、Supervisor (as tools)（监督者作为工具）
#      一个 LLM 可以直接调用不同的“子智能体”当作工具，子智能体更像是 专业插件
# 4、Hierarchical（层级型）
#     多层次的监督者，顶层 Supervisor 分配任务给子 Supervisor，子 Supervisor 再调度子 Agent
# 5、Custom（自定义混合型）
#     根据业务需要自由组合（路由 + 协作 + 监督 + HITL）图结构灵活，不一定规则
#
#
#
#
#
# ==================================== 案例01：supervisor（主管）===========================================

# LangGraph提供了专门的Supervisor Python库
# pip install langgraph-supervisor

# import re

# from dotenv import load_dotenv
# from langchain.agents import create_agent
# from langchain_deepseek import ChatDeepSeek
# from langgraph_supervisor import create_supervisor

# # .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
# load_dotenv(encoding="utf-8")


# # 1. 初始化大语言模型
# def init_llm_model() -> ChatDeepSeek:
#     return ChatDeepSeek(model="deepseek-chat")


# # 2. Tools（必须有 docstring）
# def book_flight(from_airport: str, to_airport: str) -> str:
#     """预订航班工具。根据出发机场和到达机场预订一张机票，并返回预订结果。"""
#     return f"✅ 成功预订了从 {from_airport} 到 {to_airport} 的航班"


# def book_hotel(hotel_name: str) -> str:
#     """预订酒店工具。根据酒店名称完成酒店预订，并返回预订结果。"""
#     return f"✅ 成功预订了 {hotel_name} 的住宿"


# # 3. 子 Agent
# flight_assistant = create_agent(
#     model=init_llm_model(), tools=[book_flight], name="flight_assistant"
# )

# hotel_assistant = create_agent(
#     model=init_llm_model(), tools=[book_hotel], name="hotel_assistant"
# )

# # 4. 创建 Supervisor，协调者主管
# supervisor = create_supervisor(
#     agents=[flight_assistant, hotel_assistant],
#     model=init_llm_model(),
#     prompt=(
#         "你是旅行预订系统的调度主管，负责协调航班预订和酒店预订。\n\n"
#         "当用户提出航班和酒店预订请求时，你的工作流程是：\n"
#         "1. 首先调用flight_assistant来预订航班\n"
#         "2. 然后调用hotel_assistant来预订酒店\n"
#         "3. 收到两个助手的结果后，汇总并向用户报告\n"
#         "4. 完成后结束对话\n\n"
#         "重要规则：\n"
#         "- 每个助手只能调用一次\n"
#         "- 不要重复任何内容\n"
#         "- 不要输出任何英文\n"
#         "- 所有通信都使用中文\n"
#     ),
# ).compile()


# # 5. 消息过滤器，就是一个工具类，处理大模型返回的重复废话，直接用可以不看
# def filter_messages(chunk: dict) -> str:
#     """提取并过滤消息，只返回中文内容，去除重复和英文"""
#     output = ""

#     if isinstance(chunk, dict):
#         for role, payload in chunk.items():
#             if isinstance(payload, dict) and "messages" in payload:
#                 for msg in payload["messages"]:
#                     if hasattr(msg, "content") and msg.content:
#                         content = msg.content.strip()

#                         # 过滤英文系统消息
#                         if (
#                             content
#                             and not content.startswith("Successfully")
#                             and not content.startswith("Transferring")
#                             and "Successfully transferred" not in content
#                             and "transferred back to" not in content
#                             and not content.startswith("帮我预订从")
#                         ):
#                             # 只保留中文内容
#                             chinese_content = re.sub(
#                                 r'[^\u4e00-\u9fff，。！？：；""、\s\d✅]', "", content
#                             )
#                             if chinese_content and len(chinese_content.strip()) > 5:
#                                 output += f"{role}: {chinese_content.strip()}\n"

#     return output


# # 6. 主程序
# def main():
#     print("=" * 60)
#     print(
#         "智能旅行预订系统，由于大模型每次调用，可能出现预定不成功情况，这是正常反馈,主要是2026.2.8千问赠送奶茶活动，调用失败"
#     )
#     print("=" * 60)
#     print()

#     # 收集用户信息
#     print("请按顺序提供以下信息：")
#     print("-" * 40)

#     # 1. 询问出发机场
#     from_airport = input("1. 您的出发机场是哪里？: ").strip()
#     while not from_airport:
#         print("请输入有效的出发机场名称")
#         from_airport = input("1. 您的出发机场是哪里？: ").strip()

#     # 2. 询问到达机场
#     to_airport = input("\n2. 您的到达机场是哪里？: ").strip()
#     while not to_airport:
#         print("请输入有效的到达机场名称")
#         to_airport = input("2. 您的到达机场是哪里？: ").strip()

#     # 3. 询问酒店名称
#     hotel_name = input("\n3. 您要预订的酒店名称是什么？: ").strip()
#     while not hotel_name:
#         print("请输入有效的酒店名称")
#         hotel_name = input("3. 您要预订的酒店名称是什么？: ").strip()

#     # 构造更明确的用户请求
#     user_request = (
#         f"请帮我预订以下旅行安排：\n"
#         f"1. 航班：从 {from_airport} 飞往 {to_airport}\n"
#         f"2. 酒店：{hotel_name}\n"
#         f"请完成这两个预订。"
#     )

#     print("\n" + "=" * 60)
#     print("正在处理您的预订请求...")
#     print("=" * 60)
#     print()

#     # 准备输入数据
#     # 创建一个字典，包含一个messages键
#     # messages是一个列表，包含一个消息字典
#     # 每个消息字典包含role（角色）和content（内容）字段
#     input_data = {"messages": [{"role": "user", "content": user_request}]}

#     # 使用流式处理
#     try:
#         # 创建一个空集合，用于记录已经打印过的消息内容，避免重复显示
#         seen_contents = set()

#         for chunk in supervisor.stream(input_data):
#             # 调用filter_messages函数处理当前chunk，提取并过滤其中的消息
#             filtered_output = filter_messages(chunk)
#             # 如果filtered_output不为空（即有过滤后的消息内容）
#             if filtered_output:
#                 # 将过滤后的输出按行分割成列表 strip() 去除首尾空白字符，split('\n') 按换行符分割
#                 lines = filtered_output.strip().split("\n")
#                 # 遍历每一行
#                 for line in lines:
#                     # 检查该行是否非空且不在已见过内容的集合中
#                     if line and line not in seen_contents:
#                         print(line)
#                         # 将该行内容添加到已见过集合中，确保不会重复打印
#                         seen_contents.add(line)

#         # 如果输出太少，显示总结信息
#         if len(seen_contents) < 2:
#             print("\n" + "=" * 60)
#             print("预订已完成！")
#             print(f"航班：从 {from_airport} 到 {to_airport}")
#             print(f"酒店：{hotel_name}")
#             print("=" * 60)
#     except Exception as e:
#         print(f"\n处理过程中出现错误: {e}")
#         # 如果出错，直接调用工具
#         print("\n正在直接执行预订...")
#         flight_result = book_flight(from_airport, to_airport)
#         hotel_result = book_hotel(hotel_name)
#         print(flight_result)
#         print(hotel_result)

#     print("\n感谢使用智能旅行预订系统！")


# # 7. 运行主程序
# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\n程序被用户中断。")
#     except Exception as e:
#         print(f"\n系统出现错误: {e}")


"""
运行结果如下：

============================================================
智能旅行预订系统，由于大模型每次调用，可能出现预定不成功情况，这是正常反馈
============================================================

请按顺序提供以下信息：
----------------------------------------
1. 您的出发机场是哪里？: 北京首都

2. 您的到达机场是哪里？: 深圳宝安

3. 您要预订的酒店名称是什么？: 深圳希尔顿

============================================================
正在处理您的预订请求...
============================================================

supervisor: 请帮我预订以下旅行安排：
1 航班：从 北京首都 飞往 深圳宝安
2 酒店：深圳希尔顿
请完成这两个预订。
flight_assistant: 航班已成功预订！接下来，我将为您预订深圳希尔顿酒店。由于当前工具仅支持航班预订，我需要切换到酒店预订助手来完成此任务。
正在为您转接到酒店预订助手
supervisor: 航班已成功预订！接下来，我将为您预订深圳希尔顿酒店。由于当前工具仅支持航班预订，我需要切换到酒店预订助手来完成此任务。
hotel_assistant: ✅ 您的旅行安排已全部完成：
1 航班：已成功预订，从北京首都机场飞往深圳宝安机场由航班助手完成。
2 酒店：已成功预订 深圳希尔顿由酒店助手完成。
如有其他需求如接送、餐饮、景点门票等，欢迎随时告诉我！祝您旅途愉快！
supervisor: ✅ 您的旅行安排已全部完成：
1 航班：已成功预订，从北京首都机场飞往深圳宝安机场。
2 酒店：已成功预订深圳希尔顿酒店。
所有预订均已确认，祝您旅途愉快！

感谢使用智能旅行预订系统！
"""


# ======================================= 案例02：handoffs（交接） ===========================

# handoffs 指的是一个智能体将控制权交接给另一个智能体，handoffs需要包含两个最基本的要素：
# 目的地：下一个智能体
# State：传递给下一个智能体的信息
# Supervisor都默认使用了create_handoff_tool移交工具，我们也可以自己实现交接函数

from typing import Annotated

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import START, StateGraph
from langgraph.graph.message import MessagesState
from langgraph.prebuilt.tool_node import InjectedState
from langgraph.types import Command, Send

# .env文件读取 这里会读取 .env 文件，并将其中的键值对写入系统的环境变量中
load_dotenv(encoding="utf-8")


# ===============================
# 1. 初始化大语言模型
# ===============================
def init_llm_model() -> ChatDeepSeek:
    return ChatDeepSeek(model="deepseek-chat")


model = init_llm_model()


# ===============================
# 2. 通用 Handoff 工具工厂
# ===============================
def create_task_description_handoff_tool(
    *, agent_name: str, description: str | None = None
):
    name = f"transfer_to_{agent_name}"
    description = description or f"移交给 {agent_name}"

    @tool(name, description=description)
    def handoff_tool(
        task_description: Annotated[
            str, "描述下一个 Agent 应该做什么，包括所有必要信息"
        ],
        state: Annotated[MessagesState, InjectedState],
    ) -> Command:
        task_description_message = {
            "role": "user",
            "content": task_description,
        }
        agent_input = {
            **state,
            "messages": [task_description_message],
        }

        return Command(
            goto=[Send(agent_name, agent_input)],
            graph=Command.PARENT,
        )

    return handoff_tool


# ===============================
# 3. 业务工具（必须有 docstring）
# ===============================
@tool("book_flight")
def book_flight(from_airport: str, to_airport: str) -> str:
    """预订航班，根据出发地和目的地完成机票预订"""
    print(f"✅ 成功预订了从 {from_airport} 到 {to_airport} 的航班")
    return f"成功预订了从 {from_airport} 到 {to_airport} 的航班。"


@tool("book_hotel")
def book_hotel(hotel_name: str) -> str:
    """预订酒店，根据酒店名称完成预订"""
    print(f"✅ 成功预订了 {hotel_name} 的住宿")
    return f"成功预订了 {hotel_name} 的住宿。"


# ===============================
# 4. Handoff 工具
# ===============================
transfer_to_flight_assistant = create_task_description_handoff_tool(
    agent_name="flight_assistant",
    description="将任务移交给航班预订助手",
)

transfer_to_hotel_assistant = create_task_description_handoff_tool(
    agent_name="hotel_assistant",
    description="将任务移交给酒店预订助手",
)


# ===============================
# 5. 定义 Agent（create_agent 新接口）
# create_agent 不再显式接收 prompt，而是：
# 通过 tool schema + tool 名称 + tool docstring
# 通过 graph 上下文（handoff 描述）
# 通过 MessagesState 历史消息
# ===============================
flight_assistant = create_agent(
    model=model,
    tools=[book_flight, transfer_to_hotel_assistant],  # 包含移交工具
    name="flight_assistant",
)

hotel_assistant = create_agent(
    model=model,
    tools=[book_hotel, transfer_to_flight_assistant],  # 包含移交工具
    name="hotel_assistant",
)


# ===============================
# 6. 构建多 Agent Graph
# ===============================
multi_agent_graph = (
    StateGraph(MessagesState)
    .add_node(flight_assistant)
    .add_node(hotel_assistant)
    .add_edge(START, "flight_assistant")
    .compile()
)


# ===============================
# 7. 运行
# ===============================
if __name__ == "__main__":
    result = multi_agent_graph.invoke(
        {
            "messages": [
                HumanMessage(content="帮我预订从北京到上海的航班，并预订如家酒店")
            ]
        }
    )

    print("\n====== 最终对话结果 ======")
    for msg in result["messages"]:
        if msg.type in ("human", "ai"):
            print(msg.content)
