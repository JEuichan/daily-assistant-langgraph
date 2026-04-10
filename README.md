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

## Streamlit Community Cloud 배포

**Branch 없음 오류**는 보통 Cloud에 설정된 브랜치 이름이 GitHub에 없을 때 납니다. 이 저장소는 **`main`** 과 **`master`**(동일 커밋) 둘 다 있습니다. 앱 설정에서 둘 중 하나를 선택하면 됩니다.

1. [share.streamlit.io](https://share.streamlit.io) → GitHub 연결 → 해당 레포 선택
2. **Branch**: `main` 또는 `master`
3. **Main file path**: `research_react_app/streamlit_research_agent.py`
4. **App settings → Secrets** 에서 예시:

   ```toml
   OPENAI_API_KEY = "sk-..."
   SERPER_API_KEY = "..."
   ```

   로컬 `.env`는 Git에 없으므로 Cloud에서는 Secrets로만 주입됩니다. 앱이 시작될 때 이 값들을 `os.environ`에 옮깁니다.

## 테스트

```bash
python test_daily_assistant.py
```

## 파일

- `daily_assistant_core.py` — 도구, 에이전트, `DailyAssistant` 히스토리
- `streamlit_daily_assistant.py` — Streamlit 앱
- `test_daily_assistant.py` — 다턴 대화 스모크 테스트
- `research_react_app/` — 리서치 ReAct LangGraph·Streamlit·시드·HTML 보고서
