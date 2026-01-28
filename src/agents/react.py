from langgraph.prebuilt import create_react_agent
from langchain_upstage import ChatUpstage
# 이전에 만든 custom_tools에서 도구를 가져옵니다.
from src.tools.custom_tools import calculator, get_weather

llm = ChatUpstage(model="solar-pro2")
tools = [calculator, get_weather]

# LangGraph의 prebuilt 기능을 사용하여 ReAct 에이전트 생성
# 이 방식은 내부적으로 '생각-도구호출-결과확인-응답'의 루프를 자동 관리합니다.
react_agent = create_react_agent(llm, tools=tools)

def run_agent(query: str):
    print(f"User: {query}")
    inputs = {"messages": [("user", query)]}
    for s in react_agent.stream(inputs, stream_mode="values"):
        message = s["messages"][-1]
        if hasattr(message, "content"):
            print(f"AI: {message.content}")

if __name__ == "__main__":
    run_agent("오늘 서울의 날씨를 알려주고, 123 * 456의 결과를 계산해줘.")