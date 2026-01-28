from typing import TypedDict
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_upstage import ChatUpstage

class Evaluation(BaseModel):
    score: int = Field(description="1-10점 사이의 점수")
    feedback: str = Field(description="개선 피드백")

llm = ChatUpstage(model="solar-pro2")
evaluator_llm = llm.with_structured_output(Evaluation)

class EvalState(TypedDict):
    task: str
    draft: str
    score: int
    feedback: str

def optimizer(state: EvalState):
    prompt = f"태스크: {state['task']}\n피드백: {state.get('feedback', '없음')}\n작성: {state.get('draft', '')}"
    res = llm.invoke(f"피드백을 반영하여 내용을 개선하세요.\n{prompt}")
    return {"draft": res.content}

def evaluator(state: EvalState):
    res = evaluator_llm.invoke(f"다음 결과물을 평가하세요: {state['draft']}")
    return {"score": res.score, "feedback": res.feedback}

builder = StateGraph(EvalState)
builder.add_node("optimizer", optimizer)
builder.add_node("evaluator", evaluator)

builder.add_edge(START, "optimizer")
builder.add_edge("optimizer", "evaluator")
builder.add_conditional_edges("evaluator", lambda x: "end" if x["score"] >= 8 else "retry", {"end": END, "retry": "optimizer"})

eval_app = builder.compile()