import streamlit as st
import openai

# Streamlit 앱 제목
st.title("식물 성장 시뮬레이션")

# 식물 성장 조건 설정
openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")
if not openai_api_key:
    st.warning("API 키를 입력해야 시뮬레이션을 시작할 수 있습니다.")
    st.stop()

st.header("식물 성장 조건 설정")

# 성장 조건 슬라이더 설정
temperature = st.slider("온도 (°C)", -10, 40, 20)
water_supply = st.slider("수분 공급량 (1: 적음, 10: 많음)", 1, 10, 6)
sunlight = st.slider("햇빛 노출 시간 (시간)", 4, 16, 8)
co2_level = st.slider("CO2 농도 (ppm)", 300, 800, 400)
light_wavelength = st.selectbox("빛의 파장 (nm)", ["청색광 (400-500 nm)", "적색광 (600-700 nm)", "혼합광 (청색 + 적색)"])

# 선택한 성장 조건 출력
st.subheader("선택한 성장 조건")
st.write(f"온도: {temperature}°C")
st.write(f"수분 공급량: {water_supply}")
st.write(f"햇빛 노출 시간: {sunlight}시간")
st.write(f"CO2 농도: {co2_level} ppm")
st.write(f"빛의 파장: {light_wavelength}")

# 성장 조건에 따른 식물 분석 버튼
analyze_button = st.button("성장 조건에 따른 식물 분석")

if analyze_button:
    st.subheader("내용 분석")

    # 분석 요청에 사용할 내용 생성
    analysis_prompt = (
        f"현재 식물 성장 조건은 다음과 같습니다:\n"
        f"- 온도: {temperature}°C\n"
        f"- 수분 공급량: {water_supply} (1: 적음, 10: 많음)\n"
        f"- 햇빛 노출 시간: {sunlight}시간\n"
        f"- CO2 농도: {co2_level} ppm\n"
        f"- 빛의 파장: {light_wavelength}\n"
        "이 조건들이 식물의 성장에 미치는 영향을 한국어로 자세히 설명해 주세요. "
        "각 조건이 식물의 생리에 미치는 영향을 설명하고, 이에 맞는 식물의 예시를 제시해 주세요."
    )

    # OpenAI GPT-3.5-turbo 사용하여 분석 요청
    openai.api_key = openai_api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that provides detailed explanations about plant growth in Korean based on specific conditions."},
                {"role": "user", "content": analysis_prompt}
            ],
            max_tokens=1000,
            temperature=0.6
        )
        content = response['choices'][0]['message']['content'].strip()
        st.markdown(content)
    except Exception as e:
        st.write(f"API 요청 중 오류가 발생했습니다: {e}")
