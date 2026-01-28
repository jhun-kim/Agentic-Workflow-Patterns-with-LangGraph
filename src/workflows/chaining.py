import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_upstage import ChatUpstage

llm = ChatUpstage(model="solar-pro2")

class ChainState(TypedDict):
    topic: str
    outline: str
    content: str

def generate_outline(state: ChainState):
    res = llm.invoke(f"{state['topic']}에 대한 3단계 개요를 작성하세요.")
    return {"outline": res.content}

def write_content(state: ChainState):
    res = llm.invoke(f"다음 개요를 바탕으로 본문을 작성하세요: {state['outline']}")
    return {"content": res.content}

# Graph Construction
builder = StateGraph(ChainState)
builder.add_node("planner", generate_outline)
builder.add_node("writer", write_content)
builder.add_edge(START, "planner")
builder.add_edge("planner", "writer")
builder.add_edge("writer", END)

chain_app = builder.compile()