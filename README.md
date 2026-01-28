# 🤖 Agentic Workflow & LLM Design Patterns
> **Advanced AI System Orchestration with LangGraph and Upstage Solar-Pro**

단순한 프롬프트 엔지니어링을 넘어, **LangGraph**를 활용하여 복잡한 비즈니스 로직을 자율적 에이전트와 결정론적 워크플로우로 설계하는 아키텍처 패턴 저장소입니다. 2026년 기업용 AI 시스템이 요구하는 **신뢰성(Reliability)**과 **확장성(Scalability)**에 초점을 맞추어 구현되었습니다.

---

## 📑 Overview: Workflow vs Agentic Pattern

현대 AI 시스템 설계의 핵심은 제어 흐름의 주체를 결정하는 것입니다. 이 프로젝트는 다음 두 가지 접근법을 모두 다룹니다.

| 분류 | 특징 | 주요 메커니즘 | 적합한 작업 |
| :--- | :--- | :--- | :--- |
| **Workflow** | 예측 가능한 고정 경로 | DAG (Directed Acyclic Graph) | 고품질 문서 생성, 데이터 파이프라인 |
| **Agentic** | LLM 기반 자율 의사결정 | Cyclic Feedback Loop | 복잡한 문제 해결, 외부 도구 통합 |

---

## 🏗️ Implemented Design Patterns

### 1. Deterministic Workflows
코드 수준에서 흐름을 제어하여 안정성을 극대화한 패턴입니다.

* **Prompt Chaining**: 하위 작업을 순차적으로 연결하여 품질을 점진적으로 개선합니다.
* **Routing**: 입력문의 의도를 분석하여 전문화된 노드(Billing, Tech, General)로 라우팅합니다.
* **Parallelization**: 독립적인 하위 작업을 병렬 실행하여 지연 시간을 단축하고 다각도 분석을 수행합니다.
* **Orchestrator-Worker**: 중앙 노드가 작업을 동적으로 분해하고 `Send()` 함수를 통해 가변적인 수의 Worker를 생성 및 관리합니다.



### 2. Agentic Loops
LLM이 환경과 상호작용하며 최적의 경로를 스스로 찾아가는 패턴입니다.

* **ReAct (Reasoning + Acting)**: `Thought-Action-Observation` 루프를 통해 도구를 자율적으로 선택하고 실행합니다.

* **Evaluator-Optimizer**: 생성-평가-개선 루프를 통해 품질 기준(Threshold)을 만족할 때까지 자기 수정을 반복합니다.

* **Planning Pattern**: 목표 달성을 위해 다단계 계획을 먼저 수립하고, 상태(State)를 누적하며 순차적으로 실행합니다.

---

## 🛠 Tech Stack & Tools

* **Orchestration**: ![LangGraph](https://img.shields.io/badge/LangGraph-232F3E?style=flat-square&logo=langchain&logoColor=white) ![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
* **LLM**: Upstage Solar-Pro (Solar-pro2)
* **Development**: ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white) ![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat-square&logo=pydantic&logoColor=white)
* **Observability**: LangSmith (Tracing & Evaluation)

---

## 🧠 Engineering Key Takeaways

### ✅ State Management (상태 관리)
`TypedDict`와 `Annotated`를 활용하여 노드 간 전역 상태를 안전하게 관리합니다. 특히 `operator.add`를 사용한 리듀서 패턴으로 병렬 실행 결과의 정합성을 보장했습니다.

### ✅ Reliability (신뢰성)
에이전트의 무한 루프를 방지하기 위해 `iteration` 카운터를 도입하고, 특정 점수 이하일 경우에만 재시도하는 `Conditional Edges` 로직을 설계했습니다.

### ✅ Structured Output (구조화된 출력)
Pydantic 모델을 LLM에 바인딩하여(`with_structured_output`), 비정형 텍스트 출력을 시스템이 이해할 수 있는 정형 데이터로 변환하여 라우팅 정확도를 높였습니다.