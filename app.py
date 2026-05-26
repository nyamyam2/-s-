import random
import time
import streamlit as st

# -------------------------------------------------
# 페이지 설정
# -------------------------------------------------
st.set_page_config(
    page_title="숫자 야구 게임",
    page_icon="⚾",
    layout="centered"
)

# -------------------------------------------------
# 캐릭터 데이터
# -------------------------------------------------
characters = {
    "🐯 타이거": {
        "emoji": "🐯",
        "color": "#f59e0b",
        "message": "불꽃처럼 강력한 직감!",
        "skill": "🔥 숫자 하나 위치 공개"
    },
    "🦊 여우": {
        "emoji": "🦊",
        "color": "#ef4444",
        "message": "교묘하게 상대를 분석한다!",
        "skill": "🧠 없는 숫자 하나 제거"
    },
    "🐼 판다": {
        "emoji": "🐼",
        "color": "#10b981",
        "message": "차분한 집중력!",
        "skill": "💡 볼 숫자 하나 힌트"
    },
    "🐸 개구리": {
        "emoji": "🐸",
        "color": "#22c55e",
        "message": "점프하듯 빠른 감각!",
        "skill": "⚡ 추가 기회 1회"
    }
}

# -------------------------------------------------
# 배경 파티클 애니메이션
# -------------------------------------------------
particles_html = """
<style>

/* 배경 */
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    overflow: hidden;
}

/* 파티클 */
.particle {
    position: fixed;
    width: 8px;
    height: 8px;
    background: rgba(255,255,255,0.7);
    border-radius: 50%;
    animation: float 20s infinite linear;
}

@keyframes float {
    from {
        transform: translateY(100vh) scale(0);
        opacity: 0;
    }
    20% {
        opacity: 1;
    }
    to {
        transform: translateY(-10vh) scale(1.2);
        opacity: 0;
    }
}

/* 제목 */
.title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: #facc15;
    text-shadow: 0 0 20px #facc15;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from {
        text-shadow: 0 0 10px #facc15;
    }
    to {
        text-shadow: 0 0 25px #f59e0b;
    }
}

.character-card {
    background: rgba(255,255,255,0.08);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 20px;
    backdrop-filter: blur(10px);
}

.skill-box {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 15px;
    margin-top: 10px;
    border-left: 5px solid #facc15;
}

.history-card {
    background: rgba(255,255,255,0.08);
    padding: 12px;
    border-radius: 15px;
    margin-bottom: 10px;
    animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
    border: none;
    font-size: 18px;
    font-weight: bold;
    background: linear-gradient(to right, #f59e0b, #ef4444);
    color: white;
}

.stTextInput input {
    text-align: center;
    font-size: 30px;
    border-radius: 12px;
}

.big-result {
    text-align: center;
    font-size: 34px;
    font-weight: bold;
    animation: pop 0.3s ease;
}

@keyframes pop {
    from {
        transform: scale(0.6);
    }
    to {
        transform: scale(1);
    }
}

</style>

<div class="particle" style="left:10%; animation-duration:18s;"></div>
<div class="particle" style="left:20%; animation-duration:25s;"></div>
<div class="particle" style="left:30%; animation-duration:22s;"></div>
<div class="particle" style="left:40%; animation-duration:19s;"></div>
<div class="particle" style="left:50%; animation-duration:30s;"></div>
<div class="particle" style="left:60%; animation-duration:24s;"></div>
<div class="particle" style="left:70%; animation-duration:17s;"></div>
<div class="particle" style="left:80%; animation-duration:28s;"></div>
<div class="particle" style="left:90%; animation-duration:20s;"></div>
"""

st.markdown(particles_html, unsafe_allow_html=True)

# -------------------------------------------------
# 제목
# -------------------------------------------------
st.markdown(
    '<div class="title">⚾ 숫자 야구 게임 ⚾</div>',
    unsafe_allow_html=True
)

# -------------------------------------------------
# 캐릭터 선택
# -------------------------------------------------
selected_character = st.selectbox(
    "🎮 캐릭터 선택",
    list(characters.keys())
)

char = characters[selected_character]

st.markdown(
    f"""
    <div class="character-card">
        <h1>{char["emoji"]}</h1>
        <h2 style='color:{char["color"]}'>{selected_character}</h2>
        <p>{char["message"]}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# 난이도
# -------------------------------------------------
difficulty = st.radio(
    "🎯 난이도 선택",
    ["쉬움 (3자리)", "보통 (4자리)", "어려움 (5자리)"],
    horizontal=True
)

digit_map = {
    "쉬움 (3자리)": 3,
    "보통 (4자리)": 4,
    "어려움 (5자리)": 5
}

digit_count = digit_map[difficulty]

# -------------------------------------------------
# 숫자 생성
# -------------------------------------------------
def generate_number(count):
    nums = random.sample(range(1, 10), count)
    return "".join(map(str, nums))

# -------------------------------------------------
# 판정 함수
# -------------------------------------------------
def check_guess(secret, guess):

    strike = 0
    ball = 0

    for i in range(len(secret)):

        if guess[i] == secret[i]:
            strike += 1

        elif guess[i] in secret:
            ball += 1

    return strike, ball

# -------------------------------------------------
# 세션 상태
# -------------------------------------------------
if "secret" not in st.session_state:
    st.session_state.secret = generate_number(digit_count)

if "history" not in st.session_state:
    st.session_state.history = []

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "skill_used" not in st.session_state:
    st.session_state.skill_used = False

if "extra_life" not in st.session_state:
    st.session_state.extra_life = False

# -------------------------------------------------
# 난이도 변경 시 초기화
# -------------------------------------------------
if "prev_difficulty" not in st.session_state:
    st.session_state.prev_difficulty = difficulty

if st.session_state.prev_difficulty != difficulty:

    st.session_state.secret = generate_number(digit_count)
    st.session_state.history = []
    st.session_state.game_over = False
    st.session_state.skill_used = False
    st.session_state.extra_life = False
    st.session_state.prev_difficulty = difficulty

# -------------------------------------------------
# 스킬 설명
# -------------------------------------------------
st.markdown(
    f"""
    <div class="skill-box">
        <h4>✨ 캐릭터 스킬</h4>
        <p>{char["skill"]}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# 스킬 버튼
# -------------------------------------------------
if st.button("🪄 스킬 사용"):

    if st.session_state.skill_used:
        st.warning("이미 스킬을 사용했습니다!")

    else:

        secret = st.session_state.secret

        # 타이거
        if selected_character == "🐯 타이거":

            idx = random.randint(0, digit_count - 1)

            st.success(
                f"🔥 힌트! {idx+1}번째 숫자는 {secret[idx]} 입니다!"
            )

        # 여우
        elif selected_character == "🦊 여우":

            nums = [str(i) for i in range(1, 10)]
            fake = [n for n in nums if n not in secret]

            st.success(
                f"🧠 없는 숫자 힌트: {random.choice(fake)} 는 정답에 없습니다!"
            )

        # 판다
        elif selected_character == "🐼 판다":

            ball_num = random.choice(secret)

            st.success(
                f"💡 정답에 포함된 숫자: {ball_num}"
            )

        # 개구리
        elif selected_character == "🐸 개구리":

            st.session_state.extra_life = True

            st.success("⚡ 추가 기회 활성화!")

        st.session_state.skill_used = True

# -------------------------------------------------
# 입력
# -------------------------------------------------
guess = st.text_input(
    f"🔢 {digit_count}자리 숫자 입력",
    max_chars=digit_count
)

# -------------------------------------------------
# 결과 버튼
# -------------------------------------------------
if st.button("⚾ 결과 확인"):

    if st.session_state.game_over:
        st.warning("게임 종료!")

    else:

        if not guess.isdigit():
            st.error("숫자만 입력하세요.")

        elif len(guess) != digit_count:
            st.error(f"{digit_count}자리 숫자를 입력하세요.")

        elif "0" in guess:
            st.error("0은 사용할 수 없습니다.")

        elif len(set(guess)) != digit_count:
            st.error("중복 없는 숫자를 입력하세요.")

        else:

            with st.spinner("🔍 분석 중..."):
                time.sleep(1)

            strike, ball = check_guess(
                st.session_state.secret,
                guess
            )

            st.session_state.history.append({
                "guess": guess,
                "strike": strike,
                "ball": ball
            })

            if strike == digit_count:

                st.markdown(
                    """
                    <div class="big-result" style="color:#4ade80">
                    🎉 HOME RUN 🎉
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.success(
                    f"{char['emoji']} 정답은 {st.session_state.secret}!"
                )

                st.balloons()

                st.session_state.game_over = True

            else:

                st.markdown(
                    f"""
                    <div class="big-result" style="color:#facc15">
                    {strike} STRIKE ⚾ / {ball} BALL
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# -------------------------------------------------
# 기록
# -------------------------------------------------
st.markdown("## 📜 시도 기록")

if st.session_state.history:

    for idx, item in enumerate(
        reversed(st.session_state.history),
        start=1
    ):

        st.markdown(
            f"""
            <div class="history-card">
                <b>#{idx}</b>
                &nbsp;&nbsp;
                🔢 {item["guess"]}
                <br>
                ⚾ {item["strike"]} Strike
                &nbsp;&nbsp;
                🟡 {item["ball"]} Ball
            </div>
            """,
            unsafe_allow_html=True
        )

else:
    st.info("아직 기록이 없습니다!")

# -------------------------------------------------
# 새 게임
# -------------------------------------------------
if st.button("🔄 새 게임 시작"):

    st.session_state.secret = generate_number(digit_count)
    st.session_state.history = []
    st.session_state.game_over = False
    st.session_state.skill_used = False
    st.session_state.extra_life = False

    st.toast("새 게임 시작! 🎮")

    st.rerun()

# -------------------------------------------------
# 개발용 힌트
# -------------------------------------------------
with st.expander("🛠 개발용 힌트"):
    st.write("정답:", st.session_state.secret)
