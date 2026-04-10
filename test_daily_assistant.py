"""노트북과 동일한 4턴 대화로 DailyAssistant + LangGraph 에이전트 스모크 테스트."""

from daily_assistant_core import DailyAssistant


def main():
    assistant = DailyAssistant()

    print("=== 1턴: 날씨 ===")
    print(assistant.chat("서울 날씨 어때?"))
    print()

    print("=== 2턴: 번역 ===")
    print(assistant.chat("방금 말한 날씨 한 줄을 영어로 번역해줘"))
    print()

    print("=== 3턴: 메모 + 글자 수 ===")
    print(
        assistant.chat(
            "제목은 '주말 계획', 본문은 '등산 후 카페'로 메모 저장하고, 본문 글자 수만 알려줘"
        )
    )
    print()

    print("=== 4턴: 후속 질문 ===")
    print(assistant.chat("지금까지 저장한 메모 제목이 뭐였지?"))
    print()

    assert len(assistant.history) >= 8, "히스토리에 사람/AI/도구 메시지가 쌓여야 합니다."
    print("OK: 4턴 대화 및 히스토리 유지 스모크 테스트 통과")


if __name__ == "__main__":
    main()
