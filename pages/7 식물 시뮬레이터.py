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
if 'analysis_content' not in st.session_state:
    st.session_state.analysis_content = ""

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
        f"- 빛의 파장: {light_wavelength}\n\n"
        "각각의 조건이 식물 성장에 미치는 영향을 한국어로 번역하고 개조식으로 정리해서 설명해줘. "
        "온도가 너무 낮으면 잎사귀, 열매, 식물의 크기 등등을 고려해줘. "
        "예를 들면, 너무 높은 온도와 수분이 없는 조건에서는 잎사귀의 형태가 뾰족하게 자란다와 같은 식의 표현이면 좋겠어. "
        "반드시 성장 조건에 맞는 식물의 사례를 3가지 이상 들어서 설명해줘."
    )

    # OpenAI GPT-3.5-turbo 사용하여 분석 요청
    openai.api_key = openai_api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that provides detailed explanations in Korean about plant growth based on specific conditions."},
                {"role": "user", "content": analysis_prompt}
            ],
            max_tokens=1000,
            temperature=0.6
        )
        st.session_state.analysis_content = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.session_state.analysis_content = f"API 요청 중 오류가 발생했습니다: {e}"

# 분석 내용 출력
if st.session_state.analysis_content:
    st.subheader("내용 분석")
    st.markdown(st.session_state.analysis_content)

# 그림 생성 버튼 (분석 후 표시)
if st.session_state.analysis_content:
    generate_image_button = st.button("그림 생성")

    if generate_image_button:
        st.subheader("그림 생성")

        # 분석 결과에서 식물의 종류 추출
        plant_names = ""
        if "사례" in st.session_state.analysis_content:
            plant_lines = [line for line in st.session_state.analysis_content.split('\n') if "사례" in line]
            if plant_lines:
                plant_names = ", ".join(plant_lines)

        # 그림 생성을 위한 프롬프트 생성
        image_prompt = (
            f"다음 조건에 맞는 식물을 만화 스타일로 그려주세요. 반드시 plant 형태로 그려주세요:
"
            f"- 온도: {temperature}°C\n"
            f"- 수분 공급량: {water_supply} (1: 적음, 10: 많음)\n"
            f"- 햇빛 노출 시간: {sunlight}시간\n"
            f"- CO2 농도: {co2_level} ppm\n"
            f"- 빛의 파장: {light_wavelength}\n"
            f"- 추천된 식물: {plant_names}\n\n"
            "선택한 성장 조건에 맞는 식물의 형태, 잎의 크기, 열매 등을 중심으로 만화 스타일로 그려주세요. 서식지보다는 식물의 모양과 잎의 특성에 집중하여 식물을 표현해 주세요. 그림에 동물이 포함되지 않도록 해주세요."
        )

        # OpenAI의 이미지 생성 모델 사용
        try:
            image_response = openai.Image.create(
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            image_url = image_response['data'][0]['url']
            st.image(image_url, caption="성장 조건에 따른 식물 이미지 (만화 스타일)")
        except Exception as e:
            st.write(f"이미지 생성 중 오류가 발생했습니다: {e}")