import streamlit as st
import requests
import json
import openai

# Streamlit 앱 제목
st.title("식물 성장 시뮬레이션")

# OpenAI API 키 입력
openai_api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")
if not openai_api_key:
    st.warning("API 키를 입력해야 시뮬레이션을 시작할 수 있습니다.")
    st.stop()

# OpenAI API 설정
openai.api_key = openai_api_key

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

    # 분석 내용 생성
    analysis = "조건에 따른 식물의 특성:\n"
    for key, value in plant_characteristics.items():
        analysis += f"{key}: {value}\n"

    # OpenAI GPT-3를 사용하여 내용 분석 생성
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": analysis}
            ],
            max_tokens=150
        )
        content = response.choices[0].message['content'].strip()
        st.write(f"분석 결과: {content}")
    except Exception as e:
        st.write(f"API 요청 중 오류가 발생했습니다: {e}")

    # OpenAI DALL-E를 사용하여 성장 조건에 따른 이미지 생성
    st.subheader("선택한 성장 조건에 따른 식물 이미지")
    try:
        image_prompt = f"A plant with the following characteristics: {analysis}"
        image_response = openai.Image.create(
            prompt=image_prompt,
            n=1,
            size="512x512",
            response_format="url"
        )
        image_url = image_response['data'][0]['url']
        st.image(image_url, caption="성장 조건에 따른 가상 식물 이미지")
    except Exception as e:
        st.write(f"이미지 생성 중 오류가 발생했습니다: {e}")