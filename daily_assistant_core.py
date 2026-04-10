"""일상 비서 ReAct 에이전트 코어 (노트북 03 Cell 16 스펙). Streamlit 없이 재사용·테스트 가능."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

for _base in (
    Path(__file__).resolve().parent,
    Path.cwd(),
    Path.home() / "Downloads" / "notebooks",
):
    _env = _base / ".env"
    if _env.is_file():
        load_dotenv(_env)
        break
else:
    load_dotenv()


@tool
def translate_text(text: str, target_language: str) -> str:
    """텍스트를 목표 언어로 번역합니다. target_language 예: English, 한국어, 日本語."""
    lang = target_language.lower()
    if "english" in lang or "영어" in target_language:
        return f"[EN] {text} (mock translation to English)"
    if "日本" in target_language or "japanese" in lang:
        return f"[JA] {text}（モック翻訳）"
    return f"[KO] {text} (한국어로 옮긴 결과처럼 보이는 문장입니다.)"


@tool
def get_weather(city: str) -> str:
    """도시 이름으로 현재 날씨를 조회합니다 (시뮬레이션)."""
    mock = {
        "서울": "맑음, 기온 12°C, 미세먼지 보통",
        "부산": "흐림, 기온 15°C, 강한 바람",
        "제주": "비, 기온 18°C, 습도 높음",
    }
    for k, v in mock.items():
        if k in city:
            return f"{city}: {v}"
    return f"{city}: 맑음, 기온 약 14°C (시뮬레이션 결과)"


@tool
def save_note(title: str, body: str) -> str:
    """제목과 본문으로 메모를 저장한 것처럼 확인 문자열을 반환합니다."""
    return f"메모 저장됨 — 제목: «{title[:40]}», 본문 길이: {len(body)}자"


@tool
def word_count(text: str) -> str:
    """공백 기준 단어 수와 글자 수(공백 제외)를 셉니다."""
    words = text.split()
    chars = len(text.replace(" ", ""))
    return f"단어 수: {len(words)}, 공백 제외 글자 수: {chars}"


MY_TOOLS = [translate_text, get_weather, save_note, word_count]

MY_SYSTEM_PROMPT = """당신은 '일상 비서' 역할의 ReAct 에이전트입니다.
- 사용자 질문에 맞게 번역·날씨·메모·글자 수 도구를 골라 사용하세요.
- 도구 결과를 바탕으로 짧고 명확하게 한국어로 답하세요.
- 불필요한 도구 호출은 피하고, 한 번에 해결되면 한 번만 호출하세요."""


def build_llm() -> ChatOpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY가 없습니다.")
    return ChatOpenAI(model="gpt-5-mini", api_key=key)


def build_agent():
    return create_react_agent(build_llm(), MY_TOOLS, prompt=MY_SYSTEM_PROMPT)


class DailyAssistant:
    """대화 히스토리를 유지하는 일상 비서 (노트북 DailyAssistant 패턴)."""

    def __init__(self, agent=None):
        self.agent = agent or build_agent()
        self.history = []

    def chat(self, user_input: str) -> str:
        self.history.append(HumanMessage(content=user_input))
        result = self.agent.invoke({"messages": self.history})
        self.history = list(result["messages"])
        return self.history[-1].content
