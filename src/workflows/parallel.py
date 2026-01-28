import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_upstage import ChatUpstage

llm = ChatUpstage(model="solar-pro2")

class ParallelState(TypedDict):
    topic: str
    # Annotated와 operator.add를 사용하여 여러 노드의 결과를 리스트로 합칩니다.
    analyses: Annotated[list, operator.add]

def tech_analyst(state: ParallelState):
    res = llm.invoke(f"{state['topic']}에 대한 기술적 관점의 분석을 1문장으로 작성하세요.")
    return {"analyses": [f"기술: {res.content}"]}

def business_analyst(state: ParallelState):
    res = llm.invoke(f"{state['topic']}에 대한 비즈니스 관점의 분석을 1문장으로 작성하세요.")
    return {"analyses": [f"비즈니스: {res.content}"]}

def aggregator(state: ParallelState):
    combined = "\n".join(state["analyses"])
    res = llm.invoke(f"다음 분석 결과들을 종합하여 최종 인사이트를 도출하세요:\n{combined}")
    return {"analyses": [f"--- 최종 종합 ---\n{res.content}"]}

# Graph Construction
builder = StateGraph(ParallelState)
builder.add_node("tech", tech_analyst)
builder.add_node("business", business_analyst)
builder.add_node("aggregate", aggregator)

# 병렬 실행 설정: START에서 두 노드로 동시에 엣지 연결
builder.add_edge(START, "tech")
builder.add_edge(START, "business")
builder.add_edge("tech", "aggregate")
builder.add_edge("business", "aggregate")
builder.add_edge("aggregate", END)

parallel_app = builder.compile()