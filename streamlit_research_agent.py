"""
리서치 ReAct + Serper + 분기/재시도/사용자 게이트 — `.ouroboros/seed.yaml` 스펙.
실행: `streamlit run streamlit_research_agent.py`
"""

from __future__ import annotations

import streamlit as st
from langchain_core.messages import HumanMessage

from research_workflow import build_research_graph, new_thread_config


@st.cache_resource
def get_graph():
    return build_research_graph()


def _pick_final(values: dict) -> str:
    fa = values.get("final_answer")
    if isinstance(fa, str) and fa.strip():
        return fa.strip()
    da = values.get("draft_answer")
    if isinstance(da, str) and da.strip():
        return da.strip()
    return "(답변 없음)"


def main():
    st.set_page_config(
        page_title="리서치 ReAct (LangGraph)",
        page_icon="🔎",
        layout="wide",
    )
    st.title("리서치 에이전트 — ReAct · Serper · 분기")
    st.caption(
        "gpt-5-mini · Serper 웹검색 + 스텁 도구 · 검증 후 자동 재시도(최대 2회) · "
        "필요 시 계속/중단"
    )

    if "awaiting_user" not in st.session_state:
        st.session_state.awaiting_user = False
    if "pending_config" not in st.session_state:
        st.session_state.pending_config = None
    if "last_branch_reasons" not in st.session_state:
        st.session_state.last_branch_reasons = []
    if "last_values" not in st.session_state:
        st.session_state.last_values = None
    if "last_user_query" not in st.session_state:
        st.session_state.last_user_query = None

    graph = get_graph()

    with st.sidebar:
        st.subheader("세션")
        if st.button("새 스레드 (질문 초기화)"):
            st.session_state.awaiting_user = False
            st.session_state.pending_config = None
            st.session_state.last_branch_reasons = []
            st.session_state.last_values = None
            st.session_state.last_user_query = None
            st.rerun()
        st.markdown(
            "`OPENAI_API_KEY`, `SERPER_API_KEY` 는 환경 변수 또는 `.env` 에 설정하세요."
        )

    col_log, col_chat = st.columns([1, 1])

    with col_log:
        st.subheader("분기 한 줄 로그")
        reasons = st.session_state.last_branch_reasons or []
        if not reasons:
            st.info("아직 분기 기록이 없습니다. 질문을 보내면 여기에 쌓입니다.")
        else:
            for i, r in enumerate(reasons, 1):
                st.markdown(f"{i}. **{r}**")

    with col_chat:
        st.subheader("대화")
        if st.session_state.last_user_query:
            with st.chat_message("user"):
                st.markdown(st.session_state.last_user_query)
        lv = st.session_state.last_values
        if lv and lv.get("final_answer"):
            with st.chat_message("assistant"):
                st.markdown(lv["final_answer"])
        elif lv and st.session_state.awaiting_user and lv.get("draft_answer"):
            with st.chat_message("assistant"):
                st.markdown(lv.get("draft_answer", ""))
                st.caption("위 초안은 검증 후 사용자 확인 단계입니다.")

        if st.session_state.awaiting_user and st.session_state.pending_config:
            st.warning("자동 재시도 한도에 도달했습니다. 추가 조사를 계속할까요?")
            b1, b2 = st.columns(2)
            with b1:
                if st.button("계속 조사", type="primary"):
                    cfg = st.session_state.pending_config
                    try:
                        out = graph.invoke({"user_decision": "continue"}, cfg)
                        snap = graph.get_state(cfg)
                        values = dict(snap.values) if snap and snap.values is not None else out
                        st.session_state.last_values = values
                        st.session_state.last_branch_reasons = list(
                            values.get("branch_reasons") or []
                        )
                        st.session_state.awaiting_user = bool(values.get("awaiting_user"))
                        if not st.session_state.awaiting_user:
                            st.session_state.pending_config = None
                    except Exception as e:
                        st.error(str(e))
                    st.rerun()
            with b2:
                if st.button("중단"):
                    cfg = st.session_state.pending_config
                    try:
                        out = graph.invoke({"user_decision": "stop"}, cfg)
                        snap = graph.get_state(cfg)
                        values = dict(snap.values) if snap and snap.values is not None else out
                        st.session_state.last_values = values
                        st.session_state.last_branch_reasons = list(
                            values.get("branch_reasons") or []
                        )
                        st.session_state.awaiting_user = False
                        st.session_state.pending_config = None
                    except Exception as e:
                        st.error(str(e))
                    st.rerun()

    user_text = st.chat_input(
        "리서치 질문을 입력하세요…",
        disabled=st.session_state.awaiting_user,
    )
    if user_text and not st.session_state.awaiting_user:
        cfg = new_thread_config()
        st.session_state.last_user_query = user_text
        try:
            with st.spinner("그래프 실행 중…"):
                out = graph.invoke(
                    {
                        "messages": [HumanMessage(content=user_text)],
                        "user_query": user_text,
                        "retry_count": 0,
                        "branch_reasons": [],
                    },
                    cfg,
                )
                snap = graph.get_state(cfg)
                values = dict(snap.values) if snap and snap.values is not None else out
                st.session_state.pending_config = cfg
                st.session_state.last_values = values
                st.session_state.last_branch_reasons = list(
                    values.get("branch_reasons") or []
                )
                st.session_state.awaiting_user = bool(values.get("awaiting_user"))
                if not st.session_state.awaiting_user:
                    st.session_state.pending_config = None
        except Exception as e:
            st.error(str(e))
        st.rerun()

    with st.expander("마지막 상태 요약 (디버그)"):
        st.json(
            {
                "awaiting_user": st.session_state.awaiting_user,
                "retry_count": (st.session_state.last_values or {}).get("retry_count"),
                "confidence": (st.session_state.last_values or {}).get("confidence"),
                "sufficient_sources": (st.session_state.last_values or {}).get(
                    "sufficient_sources"
                ),
                "final_preview": _pick_final(st.session_state.last_values or {})[:400],
            }
        )


if __name__ == "__main__":
    main()
