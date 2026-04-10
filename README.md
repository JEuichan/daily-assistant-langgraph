# 일상 비서 (LangGraph ReAct + Streamlit)

`create_react_agent` 기반 ReAct 에이전트와 Streamlit 채팅 UI입니다.

## 준비

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# .env에 OPENAI_API_KEY 설정
```

## 실행

```bash
streamlit run streamlit_daily_assistant.py
```

### 리서치 ReAct (Serper·분기·시드)

저장소 루트에서:

```bash
streamlit run research_react_app/streamlit_research_agent.py
```

상세는 `research_react_app/README.md` 참고.

## 테스트

```bash
python test_daily_assistant.py
```

## 파일

- `daily_assistant_core.py` — 도구, 에이전트, `DailyAssistant` 히스토리
- `streamlit_daily_assistant.py` — Streamlit 앱
- `test_daily_assistant.py` — 다턴 대화 스모크 테스트
- `research_react_app/` — 리서치 ReAct LangGraph·Streamlit·시드·HTML 보고서
