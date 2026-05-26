import random
import streamlit as st

# -----------------------------
# 숫자 야구 게임
# -----------------------------

st.set_page_config(page_title="숫자 야구", page_icon="⚾")

st.title("⚾ 숫자 야구 게임")
st.write("1~9 사이의 서로 다른 3자리 숫자를 맞혀보세요!")

# 정답 생성 함수
def generate_number():
    nums = random.sample(range(1, 10), 3)
    return "".join(map(str, nums))

# 판정 함수
def check_guess(secret, guess):
    strike = 0
    ball = 0

    for i in range(3):
        if guess[i] == secret[i]:
            strike += 1
        elif guess[i] in secret:
            ball += 1

    return strike, ball

# 세션 상태 초기화
if "secret" not in st.session_state:
    st.session_state.secret = generate_number()

if "history" not in st.session_state:
    st.session_state.history = []

if "game_over" not in st.session_state:
    st.session_state.game_over = False

# 입력
guess = st.text_input("3자리 숫자 입력", max_chars=3)

# 확인 버튼
if st.button("확인"):
    if st.session_state.game_over:
        st.warning("게임이 끝났습니다. 새 게임을 시작하세요.")
    else:
        # 입력 검증
        if not guess.isdigit() or len(guess) != 3:
            st.error("3자리 숫자를 입력하세요.")
        elif "0" in guess:
            st.error("0은 사용할 수 없습니다.")
        elif len(set(guess)) != 3:
            st.error("중복되지 않은 숫자를 입력하세요.")
        else:
            strike, ball = check_guess(st.session_state.secret, guess)

            result = f"{guess} → {strike} 스트라이크 / {ball} 볼"
            st.session_state.history.append(result)

            if strike == 3:
                st.success(f"🎉 정답입니다! 숫자는 {st.session_state.secret}였습니다.")
                st.session_state.game_over = True

# 기록 출력
st.subheader("📜 시도 기록")

if st.session_state.history:
    for item in reversed(st.session_state.history):
        st.write(item)
else:
    st.write("아직 시도한 기록이 없습니다.")

# 새 게임 버튼
if st.button("새 게임"):
    st.session_state.secret = generate_number()
    st.session_state.history = []
    st.session_state.game_over = False
    st.rerun()

# 힌트 (개발용)
with st.expander("🔍 개발용 힌트"):
    st.write("정답:", st.session_state.secret)
