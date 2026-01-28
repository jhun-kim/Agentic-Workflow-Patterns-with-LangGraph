from typing import List, Annotated, TypedDict
import operator
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_upstage import ChatUpstage

class Section(BaseModel):
    title: str
    description: str

class Plan(BaseModel):
    sections: List[Section]

llm = ChatUpstage(model="solar-pro2")
planner_llm = llm.with_structured_output(Plan)

class OrchestratorState(TypedDict):
    task: str
    sections: List[Section]
    results: Annotated[list, operator.add]

def orchestrator(state: OrchestratorState):
    # 작업을 여러 섹션으로 분할
    plan = planner_llm.invoke(f"'{state['task']}'를 수행하기 위한 상세 목차를 만드세요.")
    return {"sections": plan.sections}

def worker(state: dict):
    # 개별 섹션을 작성하는 일꾼 노드
    section = state["section"]
    res = llm.invoke(f"목차: {section.title}\n내용: {section.description}\n위 내용을 바탕으로 상세 기술을 작성하세요.")
    return {"results": [f"## {section.title}\n{res.content}"]}

def assign_workers(state: OrchestratorState):
    # 각 섹션마다 worker 노드를 동적으로 생성 (Send 활용)
    return [Send("worker", {"section": s}) for s in state["sections"]]

def synthesizer(state: OrchestratorState):
    final_report = "\n\n".join(state["results"])
    return {"results": [f"# 최종 보고서\n\n{final_report}"]}

# Graph Construction
builder = StateGraph(OrchestratorState)
builder.add_node("orchestrator", orchestrator)
builder.add_node("worker", worker)
builder.add_node("synthesizer", synthesizer)

builder.add_edge(START, "orchestrator")
builder.add_conditional_edges("orchestrator", assign_workers, ["worker"])
builder.add_edge("worker", "synthesizer")
builder.add_edge("synthesizer", END)

orchestrator_app = builder.compile()