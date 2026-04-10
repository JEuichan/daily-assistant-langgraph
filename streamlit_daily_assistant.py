"""
LangGraph create_react_agent 기반 일상 비서 Streamlit 앱.
03_react_agent.ipynb 마지막 실습 과제와 동일 스펙 — `daily_assistant_core` 사용.
"""

from __future__ import annotations

import streamlit as st
from langchain_core.messages import HumanMessage

from daily_assistant_core import MY_SYSTEM_PROMPT, MY_TOOLS, build_llm

from langgraph.prebuilt import create_react_agent


@st.cache_resource
def get_agent():
    llm = build_llm()
    return create_react_agent(llm, MY_TOOLS, prompt=MY_SYSTEM_PROMPT)


def _message_label(msg) -> str:
    if msg.type == "human":
        return "사용자"
    if msg.type == "ai":
        return "비서"
    if msg.type == "tool":
        return f"도구({getattr(msg, 'name', '')})"
    return msg.type


def _render_message(msg):
    _ = _message_label(msg)
    if msg.type == "human":
        with st.chat_message("user"):
            st.markdown(msg.content)
        return
    if msg.type == "ai":
        with st.chat_message("assistant"):
            if msg.content:
                st.markdown(msg.content)
            if getattr(msg, "tool_calls", None):
                for tc in msg.tool_calls:
                    name = tc.get("name", "?")
                    args = tc.get("args", {})
                    st.caption(f"🔧 `{name}`({args})")
        return
    if msg.type == "tool":
        with st.chat_message("assistant"):
            st.caption(f"📎 도구 결과 ({getattr(msg, 'name', '')})")
            st.text(msg.content[:2000])
        return


def run_agent_turn(history: list, stream_updates: bool) -> list:
    """DailyAssistant와 동일: 전체 히스토리로 실행 후 messages 전체를 교체."""
    agent = get_agent()
    if not stream_updates:
        out = agent.invoke({"messages": history})
        return list(out["messages"])

    placeholder = st.empty()
    lines: list[str] = []
    last_values = None
    for chunk in agent.stream({"messages": history}, stream_mode="values"):
        last_values = chunk
        lines.append(str(chunk)[:500])
        placeholder.code("\n---\n".join(lines[-8:]), language="text")
    placeholder.empty()
    if last_values and "messages" in last_values:
        return list(last_values["messages"])
    out = agent.invoke({"messages": history})
    return list(out["messages"])


def main():
    st.set_page_config(
        page_title="일상 비서 (LangGraph ReAct)",
        page_icon="🤖",
        layout="centered",
    )
    st.title("일상 비서 — LangGraph `create_react_agent`")
    st.caption(
        "번역·날씨·메모·글자 수 도구 | 대화 히스토리 유지 | 노트북 03 실습 과제와 동일 스펙"
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    show_stream = st.sidebar.checkbox("그래프 단계 스트림 미리보기 (values)", value=False)
    if st.sidebar.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

    for msg in st.session_state.messages:
        _render_message(msg)

    user_text = st.chat_input("메시지를 입력하세요…")
    if user_text:
        st.session_state.messages.append(HumanMessage(content=user_text))
        try:
            with st.spinner("ReAct 에이전트 실행 중…"):
                new_messages = run_agent_turn(
                    st.session_state.messages,
                    stream_updates=show_stream,
                )
            st.session_state.messages = new_messages
        except Exception as e:
            st.error(str(e))
            st.session_state.messages.pop()
        st.rerun()


if __name__ == "__main__":
    main()
