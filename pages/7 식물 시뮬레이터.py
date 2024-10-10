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

    # 식물의 특성 결정 및 분석 결과 생성
    plant_characteristics = {
        "잎 크기": "중간",
        "뿌리 크기": "중간",
        "꽃 크기": "없음",
        "열매 상태": "없음"
    }

    if temperature > 30 and water_supply < 5:
        plant_characteristics["잎 크기"] = "작음 (수분 손실 최소화)"
    elif temperature < 0:
        plant_characteristics["잎 크기"] = "두껍고 작음 (추위 보호)"
    elif co2_level > 600:
        plant_characteristics["잎 크기"] = "매우 큼 (광합성 촉진)"
    
    if water_supply < 3:
        plant_characteristics["뿌리 크기"] = "깊음 (물을 찾기 위해)"
    elif water_supply > 7:
        plant_characteristics["뿌리 크기"] = "얕음 (수분이 충분함)"
    
    if temperature > 20 and sunlight > 10 and co2_level > 500:
        plant_characteristics["꽃 크기"] = "큼 (성장에 적합한 조건)"
    elif temperature < 10 or sunlight < 5:
        plant_characteristics["꽃 크기"] = "없음 (불리한 조건)"
    
    if temperature > 25 and water_supply > 5 and co2_level > 400:
        plant_characteristics["열매 상태"] = "잘 자람"
    elif temperature < 15 or water_supply < 4:
        plant_characteristics["열매 상태"] = "없음 (불리한 조건)"

    # 빛의 파장에 따른 특성 결정
    if light_wavelength == "청색광 (400-500 nm)":
        plant_characteristics["잎 크기"] = "두껍고 건강함 (청색광에 의한 잎 성장 촉진)"
    elif light_wavelength == "적색광 (600-700 nm)":
        plant_characteristics["꽃 크기"] = "큼 (적색광에 의한 개화 촉진)"
    elif light_wavelength == "혼합광 (청색 + 적색)":
        plant_characteristics["잎 크기"] = "크고 건강함"
        plant_characteristics["꽃 크기"] = "큼 (청색 및 적색광의 조화로 전체적인 성장 촉진)"

    # 분석 내용 생성 및 형식화
    analysis = """
    ### 1. 분석 결과 요약
    - **온도 조건**:
      - 30°C 이상일 때: 잎의 크기가 작아져 수분 손실을 줄임.
      - 0°C 이하일 때: 잎이 두껍고 작아져 추위에 대한 저항력 증가.
      - 20°C 이상, 햇빛 10시간 이상, CO₂ 500 ppm 이상일 때: 꽃이 크게 자람.

    - **수분 공급량**:
      - 수분이 부족할 때(3 이하): 뿌리가 깊어져 물을 찾으려 함.
      - 수분이 충분할 때(7 이상): 뿌리가 얕아짐, 물을 쉽게 흡수.

    - **햇빛 노출 시간**:
      - 10시간 이상의 햇빛: 성장에 필요한 에너지를 충분히 공급.

    - **CO₂ 농도**:
      - 600 ppm 이상일 때: 광합성이 활발해져 잎의 크기가 커짐.
    
    - **빛의 파장**:
      - 청색광: 잎의 성장을 촉진하여 두껍고 건강한 잎을 만듦.
      - 적색광: 꽃의 성장을 촉진하여 더 크고 화려한 꽃을 피움.
      - 혼합광: 전체적인 성장에 도움이 됨.

    ### 2. 조건에 따른 식물 사례
    - **높은 온도(30°C 이상)와 낮은 수분 공급(수분 공급량 5 이하)**:
      - **선인장**: 고온과 건조한 환경에서 잘 자라며, 잎이 작고 두꺼워 수분 손실을 줄임.
    - **낮은 온도(0°C 이하)와 적절한 수분 공급**:
      - **겨울나무**: 추운 기후에 적응하여 잎이 두껍고 추위를 견딤.
    - **높은 CO₂ 농도(600 ppm 이상)와 충분한 햇빛**:
      - **토마토**: CO₂가 많을 때 광합성이 활발하여 잎이 크고 성장 속도가 빠름.
    - **혼합광(청색광 + 적색광)과 적절한 수분 공급**:
      - **상추**: 혼합광을 통해 잎의 성장이 촉진되며, 상추와 같은 잎채소에 적합함.
    """

    # OpenAI GPT-3.5-turbo 사용하여 분석 요청 및 처리
    openai.api_key = openai_api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that provides explanations in Korean about plant growth based on specific conditions."},
                {"role": "user", "content": f"다음은 식물 성장 조건입니다:\n{analysis}\n이 조건들이 식물 성장에 미치는 영향을 자세하게 설명하고, 이 조건들에 맞는 식물의 실제 사례를 한국어로 작성해 주세요. 문장을 자연스럽게 연결하여 하나의 완성된 문단으로 작성해 주세요."}
            ],
            max_tokens=1000,
            temperature=0.6
        )
        content = response['choices'][0]['message']['content'].strip()
        st.markdown(content)
    except Exception as e:
        st.write(f"API 요청 중 오류가 발생했습니다: {e}")
