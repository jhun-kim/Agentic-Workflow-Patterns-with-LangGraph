from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """수학 계산을 수행합니다. 예: '123 * 456'"""
    try:
        return f"계산 결과: {eval(expression)}"
    except Exception as e:
        return f"계산 오류: {str(e)}"

@tool
def get_weather(city: str) -> str:
    """특정 도시의 현재 날씨 정보를 조회합니다."""
    # Mock data for demonstration
    weather_map = {"서울": "맑음, 22°C", "부산": "흐림, 20°C", "뉴욕": "비, 15°C"}
    return weather_map.get(city, f"{city}의 날씨 정보를 찾을 수 없습니다.")