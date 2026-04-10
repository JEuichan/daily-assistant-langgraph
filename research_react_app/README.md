# 리서치 ReAct (LangGraph + Serper)

Ouroboros 시드(`research_react_app/.ouroboros/seed.yaml`)에 맞춘 워크플로입니다.  
저장소 루트의 `daily_assistant_core.py`를 import 하므로 **루트에서** 의존성 설치 후 실행하세요.

## 실행

```bash
# 저장소 루트에서
pip install -r requirements.txt
streamlit run research_react_app/streamlit_research_agent.py
```

## Streamlit Cloud

- **GitHub 레포**: 이 프로젝트 **전체** (`requirements.txt`가 루트에 있는 레포). 파일만 따로 올린 레포는 `langchain_core` 미설치 오류가 납니다.
- 브랜치: **`main`** 또는 **`master`**
- 엔트리: **`research_react_app/streamlit_research_agent.py`**
- Secrets: `OPENAI_API_KEY`, `SERPER_API_KEY`
- 의존성: 기본 **루트 `requirements.txt`**. 고급에서 경로를 바꿨다면 `requirements.txt` 또는 `research_react_app/requirements.txt` 중 하나로 맞추기.

## 구성

- `research_workflow.py` — LangGraph 그래프, Serper·스텁 도구
- `streamlit_research_agent.py` — Streamlit UI
- `reports/seed_report.html` — 시드 정리 보고서
- `.ouroboros/seed.yaml` — 요구사항 시드
