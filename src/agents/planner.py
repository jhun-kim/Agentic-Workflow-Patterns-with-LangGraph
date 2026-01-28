from typing import List, TypedDict
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain_upstage import ChatUpstage

class Plan(BaseModel):
    steps: List[str]

llm = ChatUpstage(model="solar-pro2")
planner_llm = llm.with_structured_output(Plan)

class PlanState(TypedDict):
    goal: str
    steps: List[str]
    current_idx: int
    results: List[str]

def planner(state: PlanState):
    plan = planner_llm.invoke(state["goal"])
    return {"steps": plan.steps, "current_idx": 0}

def executor(state: PlanState):
    step = state["steps"][state["current_idx"]]
    res = llm.invoke(f"현재 단계 실행: {step}")
    return {"results": [res.content], "current_idx": state["current_idx"] + 1}

builder = StateGraph(PlanState)
builder.add_node("planner", planner)
builder.add_node("executor", executor)

builder.add_edge(START, "planner")
builder.add_edge("planner", "executor")
builder.add_conditional_edges("executor", lambda x: "next" if x["current_idx"] < len(x["steps"]) else "end", {"next": "executor", "end": END})

plan_app = builder.compile()