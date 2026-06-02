import streamlit as st
from google import genai

# 페이지 설정
st.set_page_config(
    page_title="연애운 상담소",
    page_icon="💕"
)

st.title("💕 AI 연애운 상담소")
st.caption("오늘의 연애운을 AI가 재미로 봐드립니다.")

# API 키 불러오기
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("GEMINI_API_KEY를 Secrets에 설정해주세요.")
    st.stop()

# 채팅 기록 유지
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요 💕 생년월일, 성별, 현재 연애 상태를 알려주시면 연애운을 재미로 봐드릴게요!"
        }
    ]

# 기존 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 사용자 입력
if prompt := st.chat_input("연애운을 물어보세요"):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    try:
        # 대화 기록 구성
        conversation = "\n".join(
            [
                f"{m['role']}: {m['content']}"
                for m in st.session_state.messages
            ]
        )

        system_prompt = """
        당신은 친절한 연애운 상담가입니다.

        규칙:
        - 사용자의 연애운을 재미있고 긍정적으로 해석한다.
        - 실제 점술가처럼 말하되 과도하게 단정하지 않는다.
        - 300자 내외로 답변한다.
        - 마지막에 연애운 점수(0~100점)를 제공한다.
        - 한국어로 답변한다.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=f"{system_prompt}\n\n{conversation}"
        )

        answer = response.text

    except Exception as e:
        answer = f"오류가 발생했습니다.\n\n{str(e)}"

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.write(answer)
