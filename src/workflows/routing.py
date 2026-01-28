from typing import Literal, TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_upstage import ChatUpstage

class RouteDecision(BaseModel):
    category: Literal["tech", "billing"] = Field(description="문의 분류")

llm = ChatUpstage(model="solar-pro2")
router_llm = llm.with_structured_output(RouteDecision)

class RouterState(TypedDict):
    query: str
    category: str
    response: str

def classify(state: RouterState):
    decision = router_llm.invoke(state["query"])
    return {"category": decision.category}

def handle_tech(state: RouterState):
    return {"response": "기술 지원팀으로 연결합니다."}

def handle_billing(state: RouterState):
    return {"response": "결제 관리팀으로 연결합니다."}

builder = StateGraph(RouterState)
builder.add_node("classify", classify)
builder.add_node("tech", handle_tech)
builder.add_node("billing", handle_billing)

builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", lambda x: x["category"], {"tech": "tech", "billing": "billing"})
builder.add_edge("tech", END)
builder.add_edge("billing", END)

router_app = builder.compile()