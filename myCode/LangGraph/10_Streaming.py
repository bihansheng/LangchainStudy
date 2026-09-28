# 是什么
# LangGraph 里的 “流式传输” 功能，核心就是让 AI 应用（比如用大语言模型做的工具、对话机器人）能 “实时输出结果”，不用等整个流程跑完，体验更流畅。
# 用大白话拆解重点：
# 1、大语言模型（LLM）回应通常有点慢，流式传输能让结果 “一点点蹦出来”（比如打字机似的），用户不用干等，体验更好。
# 2、简单说，这功能就是让 LangGraph 做的 AI 应用 “更透明、更流畅”，用户能实时看到进度，开发者也方便调试，还能灵活适配各种需求。


# 能实现啥效果？
# 1、实时看流程状态：比如知道 AI 现在在处理哪个步骤、当前的结果是什么（比如 “正在细化主题”“已生成笑话初稿”）；
# 2、实时看子流程结果：如果你的 AI 流程里嵌套了小流程（子图），也能同步看到子流程的进度；
# 3、实时看 LLM 输出的每一个字：比如 AI 写笑话时，每个词、每句话实时蹦出来，不是最后一次性显示；
# 4、自定义实时消息：比如让 AI 干活时，实时发 “进度 30%”“正在调用工具查数据” 这种自定义提示；
# 5、调试用：能看到流程里的详细细节，方便找问题。


# 怎么用
# 就像选功能开关一样，用的时候指定 “模式” 就行


# ============================= 案例01---流图状态(Stream graph state) ==========================

"""
StreamGraphState.py

流图状态
使用流模式，并在图执行时流式传输其状态。updatesvalues
updates在图的每一步后，将更新流向状态。
values在图的每一步后，流出状态的---->全部值。
"""

# from typing import TypedDict

# from langgraph.graph import END, START, StateGraph


# class AtguiguState(TypedDict):
#     topic: str
#     joke: str


# def refine_topic(state: AtguiguState):
#     return {"topic": state["topic"] + " and cats"}


# def generate_joke(state: AtguiguState):
#     return {"joke": f"This is a joke about {state['topic']}"}


# def main():
#     graph = (
#         StateGraph(AtguiguState)
#         .add_node(refine_topic)
#         .add_node(generate_joke)
#         .add_edge(START, "refine_topic")
#         .add_edge("refine_topic", "generate_joke")
#         .add_edge("generate_joke", END)
#         .compile()
#     )

#     # updates在图的每一步后，将更新流向状态。
#     for chunk in graph.stream({"topic": "ice cream"}, stream_mode="updates"):
#         print(chunk)

#     print()
#     # {'refine_topic': {'topic': 'ice cream and cats'}}
#     # {'generate_joke': {'joke': 'This is a joke about ice cream and cats'}}

#     # values在图的每一步后，流出状态的全部值。
#     for chunk in graph.stream({"topic": "ice cream"}, stream_mode="values"):
#         print(chunk)
#     # {'topic': 'ice cream'}
#     # {'topic': 'ice cream and cats'}
#     # {'topic': 'ice cream and cats', 'joke': 'This is a joke about ice cream and cats'}

# if __name__ == "__main__":
#     main()


# ============================= 案例02---多模式流+debug模式并存(Stream multiple mdes)  ==========================

"""
StreamMultipleModes.py
LangGraph 多模式流式传输演示

将列表作为stream_mode参数传递，以同时流式传输多种模式。

流式输出将是(mode, chunk)形式的元组，其中mode是流模式的名称，chunk是该模式所流式传输的数据。


"""

# from typing import TypedDict

# from langgraph.graph import END, START, StateGraph


# # 定义状态类型
# class AtguiguState(TypedDict):
#     question: str
#     answer: str
#     confidence: float  # 置信度分数
#     steps: list


# def think(state: AtguiguState) -> AtguiguState:
#     """思考节点"""
#     question = state["question"]
#     # 模拟思考过程
#     steps = [f"分析问题: {question}", "检索相关知识", "形成初步答案"]
#     return {"steps": steps}


# def respond(state: AtguiguState) -> AtguiguState:
#     """回应节点"""
#     question = state["question"]
#     # 根据问题生成答案
#     if "天气" in question:
#         answer = "今天天气晴朗"
#         confidence = 0.9
#     elif "时间" in question:
#         answer = "现在是上午10点"
#         confidence = 0.8
#     else:
#         answer = "这是一个很好的问题"
#         confidence = 0.7

#     return {"answer": answer, "confidence": confidence}


# def reflect(state: AtguiguState) -> AtguiguState:
#     """反思节点"""
#     answer = state["answer"]
#     confidence = state["confidence"]
#     steps = state.get("steps", [])

#     steps.append(f"验证答案: {answer}")
#     steps.append(f"置信度评估: {confidence}")

#     if confidence > 0.8:
#         conclusion = "高置信度答案"
#     elif confidence > 0.5:
#         conclusion = "中等置信度答案"
#     else:
#         conclusion = "低置信度答案"

#     steps.append(f"结论: {conclusion}")

#     return {"steps": steps}


# def main():
#     # 构建图
#     builder = StateGraph(AtguiguState)
#     builder.add_node("think", think)
#     builder.add_node("respond", respond)
#     builder.add_node("reflect", reflect)

#     builder.add_edge(START, "think")
#     builder.add_edge("think", "respond")
#     builder.add_edge("respond", "reflect")
#     builder.add_edge("reflect", END)

#     graph = builder.compile()

#     print("=== LangGraph 多模式流式传输演示 ===\n")

#     # 准备输入
#     input_state = {
#         "question": "今天天气怎么样?",
#         "answer": "",
#         "confidence": 0.0,
#         "steps": [],
#     }

#     print("--- 1. 使用 stream_mode='values' 模式 ---")
#     print("显示每一步执行后的完整状态:")
#     for chunk in graph.stream(input_state, stream_mode="values"):
#         print(f"  {chunk}")

#     print("\n" + "=" * 60 + "\n")

#     print("--- 2. 使用 stream_mode='updates' 模式 ---")
#     print("只显示每一步的状态更新:")
#     for chunk in graph.stream(input_state, stream_mode="updates"):
#         print(f"  {chunk}")

#     print("\n" + "=" * 60 + "\n")
#     #
#     print("--- 3. 同时使用stream_mode=[values,updates]多种流模式 ---")
#     print("同时显示完整状态和状态更新:")
#     for mode, chunk in graph.stream(input_state, stream_mode=["values", "updates"]):
#         print(f"  [{mode}]: {chunk}")

#     print("\n" + "=" * 60 + "\n")

#     print("--- 4. 使用 debug 模式 ---")
#     print("显示详细的调试信息:")
#     try:
#         for chunk in graph.stream(input_state, stream_mode="debug"):
#             print(f"  {chunk}")
#     except Exception as e:
#         print(f"  Debug模式可能需要特殊配置: {e}")


# if __name__ == "__main__":
#     main()

#  运行打印的日志
# === LangGraph 多模式流式传输演示 ===

# --- 1. 使用 stream_mode='values' 模式 ---
# 显示每一步执行后的完整状态:
#   {'question': '今天天气怎么样?', 'answer': '', 'confidence': 0.0, 'steps': []}
#   {'question': '今天天气怎么样?', 'answer': '', 'confidence': 0.0, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}
#   {'question': '今天天气怎么样?', 'answer': '今天天气晴朗', 'confidence': 0.9, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}
#   {'question': '今天天气怎么样?', 'answer': '今天天气晴朗', 'confidence': 0.9, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案', '验证答案: 今天天气晴朗', '置信度评估: 0.9', '结论: 高置信度答案']}

# ============================================================

# --- 2. 使用 stream_mode='updates' 模式 ---
# 只显示每一步的状态更新:
#   {'think': {'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}}
#   {'respond': {'answer': '今天天气晴朗', 'confidence': 0.9}}
#   {'reflect': {'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案', '验证答案: 今天天气晴朗', '置信度评估: 0.9', '结论: 高置信度答案']}}

# ============================================================

# --- 3. 同时使用stream_mode=[values,updates]多种流模式 ---
# 同时显示完整状态和状态更新:
#   [values]: {'question': '今天天气怎么样?', 'answer': '', 'confidence': 0.0, 'steps': []}
#   [updates]: {'think': {'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}}
#   [values]: {'question': '今天天气怎么样?', 'answer': '', 'confidence': 0.0, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}
#   [updates]: {'respond': {'answer': '今天天气晴朗', 'confidence': 0.9}}
#   [values]: {'question': '今天天气怎么样?', 'answer': '今天天气晴朗', 'confidence': 0.9, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}
#   [updates]: {'reflect': {'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案', '验证答案: 今天天气晴朗', '置信度评估: 0.9', '结论: 高置信度答案']}}
#   [values]: {'question': '今天天气怎么样?', 'answer': '今天天气晴朗', 'confidence': 0.9, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案', '验证答案: 今天天气晴朗', '置信度评估: 0.9', '结论: 高置信度答案']}

# ============================================================

# --- 4. 使用 debug 模式 ---
# 显示详细的调试信息:
#   {'step': 1, 'timestamp': '2026-09-28T03:25:16.837131+00:00', 'type': 'task', 'payload': {'id': 'e66ab4c8-8da2-cff2-b196-b79f14abfd93', 'name': 'think', 'input': {'question': '今天天气怎么样?', 'answer': '', 'confidence': 0.0, 'steps': []}, 'triggers': ('branch:to:think',)}}
#   {'step': 1, 'timestamp': '2026-09-28T03:25:16.837173+00:00', 'type': 'task_result', 'payload': {'id': 'e66ab4c8-8da2-cff2-b196-b79f14abfd93', 'name': 'think', 'error': None, 'result': {'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}, 'interrupts': []}}
#   {'step': 2, 'timestamp': '2026-09-28T03:25:16.837209+00:00', 'type': 'task', 'payload': {'id': 'f3e7322f-6aa7-474c-05cf-e43b3cb0b802', 'name': 'respond', 'input': {'question': '今天天气怎么样?', 'answer': '', 'confidence': 0.0, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}, 'triggers': ('branch:to:respond',)}}
#   {'step': 2, 'timestamp': '2026-09-28T03:25:16.837257+00:00', 'type': 'task_result', 'payload': {'id': 'f3e7322f-6aa7-474c-05cf-e43b3cb0b802', 'name': 'respond', 'error': None, 'result': {'answer': '今天天气晴朗', 'confidence': 0.9}, 'interrupts': []}}
#   {'step': 3, 'timestamp': '2026-09-28T03:25:16.837295+00:00', 'type': 'task', 'payload': {'id': '7ab8b502-9452-bc58-74fd-120f59aef071', 'name': 'reflect', 'input': {'question': '今天天气怎么样?', 'answer': '今天天气晴朗', 'confidence': 0.9, 'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案']}, 'triggers': ('branch:to:reflect',)}}
#   {'step': 3, 'timestamp': '2026-09-28T03:25:16.837337+00:00', 'type': 'task_result', 'payload': {'id': '7ab8b502-9452-bc58-74fd-120f59aef071', 'name': 'reflect', 'error': None, 'result': {'steps': ['分析问题: 今天天气怎么样?', '检索相关知识', '形成初步答案', '验证答案: 今天天气晴朗', '置信度评估: 0.9', '结论: 高置信度答案']}, 'interrupts': []}}


# ============================= 案例03--- LLM令牌(LLM tokens)  ==========================

"""
StreamLLMTokens.py

使用messages流模式，从图中的任何部分（包括节点、工具、子图或任务）逐token流式传输大型语言模型（LLM）的输出。
messages模式的流式输出是一个元组(message_chunk, metadata)，其中：
	message_chunk：来自大语言模型（LLM）的令牌或消息片段。
	metadata：一个包含图节点和大语言模型调用详情的字典元数据。

"""

# import os
# from typing import TypedDict

# from langchain.chat_models import init_chat_model
# from langgraph.graph import START, StateGraph


# class State(TypedDict):
#     query:str
#     answer:str

# def node(state:State):
#     print("开始调用node节点")

#     model = init_chat_model(model="qwen-plus",
#                             model_provider="openai",
#                             api_key=os.getenv("aliQwen-api"),
#                             base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

#     llm_result = model.invoke( [("user",state["query"])] )
#     print("llm invoke结束",end="\n\n")

#     return {"answer":llm_result}

# def main():
#     graph = (
#         StateGraph(state_schema=State)
#         .add_node(node)
#         .add_edge(START,"node")
#         .compile()
#     )

#     inputs = {"query":"帮我生成一个200字的小学生作文，主题为我的一天"}

#     # stream_mode="messages"从任何调用了大语言模型的图节点流式传输二元组（大语言模型token，元数据）。
#     '''messages模式的流式输出是一个元组(message_chunk, metadata)，其中：
#         message_chunk：来自大语言模型（LLM）的令牌或消息片段。
#         metadata：一个包含图节点和大语言模型调用详情的字典元数据。'''
#     for chunk,meta_data in graph.stream(inputs,stream_mode="messages"):
#         #print(f"type of chunk:{type(chunk)}")#上课时候打开注释
#         print(chunk.content,end="")
#         #print(chunk,end="")

# if __name__ == '__main__':
#     main()


# ============================= 案例04--- 流式传输自定义数据StreamCustomData   1 ==========================

# 要从LangGraph节点或工具内部发送自定义用户定义数据，请遵循以下步骤：
# Ø 使用get_stream_writer访问流写入器并发送自定义数据。
# Ø 调用.stream()或.astream()时，设置stream_mode="custom"以在流中获取自定义数据。你可以组合多种模式（例如["updates", "custom"]），但至少有一种模式必须是"custom"。


"""
StreamCustomDataSimple.py

要从LangGraph节点或工具内部发送自定义用户定义数据，请遵循以下步骤：
	使用get_stream_writer访问流写入器并发送自定义数据。
	调用.stream()或.astream()时，设置stream_mode="custom"以在流中获取自定义数据。
你可以组合多种模式（例如["updates", "custom"]），但至少有一种模式必须是"custom"。

LangGraph 自定义数据流式传输演示
展示如何从节点内部发送自定义用户定义数据
"""

# from typing import TypedDict

# from langgraph.config import get_stream_writer
# from langgraph.graph import END, START, StateGraph


# class State(TypedDict):
#     query: str
#     answer: str

# def node(state: State):
#     # Get the stream writer to send custom data
#     writer = get_stream_writer()
#     # Emit a custom key-value pair (e.g., progress update)
#     writer({"custom_key": "欢迎来到尚硅谷线上Agent班级学习，O(∩_∩)O"})
#     return {"answer": "some data"}

# graph = (
#     StateGraph(State)
#     .add_node(node)
#     .add_edge(START, "node")
#     .add_edge("node",END)
#     .compile()
# )

# # Set stream_mode="custom" to receive the custom data in the stream
# # for chunk in graph.stream({"query": "example"}, stream_mode=["custom"]):
# #     print(chunk)
# #
# # for chunk in graph.stream({"query": "example"}, stream_mode=["updates", "custom"]):
# #     print(chunk)
# #
# for chunk in graph.stream({"query": "example"}, stream_mode=["values", "custom"]):
#     print(chunk)


# ============================= 案例04--- 流式传输自定义数据StreamCustomData   2 ==========================

"""
StreamCustomData.py

要从LangGraph节点或工具内部发送自定义用户定义数据，请遵循以下步骤：
	使用get_stream_writer访问流写入器并发送自定义数据。
	调用.stream()或.astream()时，设置stream_mode="custom"以在流中获取自定义数据。
你可以组合多种模式（例如["updates", "custom"]），但至少有一种模式必须是"custom"。

LangGraph 自定义数据流式传输演示
展示如何从节点内部发送自定义用户定义数据
"""

from typing import TypedDict

from langgraph.config import get_stream_writer
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    query: str
    answer: str
    progress: list


def node_with_custom_streaming(state: State) -> State:
    """带自定义流式传输的节点"""
    # 获取流写入器以发送自定义数据,使用get_stream_writer访问流写入器并发送自定义数据。
    writer = get_stream_writer()

    # 发送自定义数据（例如，进度更新）
    writer({"custom_key": "开始处理查询"})
    writer({"progress": "步骤1: 分析查询内容", "status": "running"})

    query = state["query"]

    writer({"progress": "步骤2: 生成结果", "status": "running"})
    writer({"progress": "步骤3: 完成处理", "status": "completed"})
    writer({"custom_key": "查询处理完成"})

    # 模拟处理过程
    result = f"处理结果: {query.upper()}"
    return {"answer": result, "progress": state.get("progress", []) + ["处理完成"]}


def main():
    print("=== LangGraph 自定义数据流式传输演示 ===\n")

    # 构建图
    graph = (
        StateGraph(State)
        .add_node("node_with_custom_streaming", node_with_custom_streaming)
        .add_edge(START, "node_with_custom_streaming")
        .add_edge("node_with_custom_streaming", END)
        .compile()
    )

    inputs = {"query": "hello world", "answer": "", "progress": []}

    print("--- 1. 单独使用 custom 流模式 ---")
    try:
        # 设置 stream_mode="custom" 以在流中接收自定义数据
        for chunk in graph.stream(inputs, stream_mode="custom"):
            print(f"自定义数据块: {chunk}")
    except Exception as e:
        print(f"错误: {e}")
        print("说明: 在Graph API中，自定义流数据需要在节点中通过特定方式发送")

    print("\n" + "=" * 50 + "\n")

    print("--- 2. 单独使用 updates 流模式 ---")
    for chunk in graph.stream(inputs, stream_mode="updates"):
        print(f"状态更新: {chunk}")

    print("\n" + "=" * 50 + "\n")

    print("--- 3. 同时使用 custom 和 updates 流模式 ---")
    try:
        for mode, chunk in graph.stream(inputs, stream_mode=["custom", "updates"]):
            print(f"[{mode}]: {chunk}")
    except Exception as e:
        print(f"错误: {e}")
        print("说明: 在Graph API中，需要特殊配置才能使用自定义流模式")


if __name__ == "__main__":
    main()
