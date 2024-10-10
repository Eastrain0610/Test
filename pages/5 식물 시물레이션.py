import streamlit as st
from PIL import Image
from io import BytesIO
import requests

# Streamlit 앱 제목
st.title("식물 성장 시뮬레이션")

# 식물 성장 조건 설정
st.header("식물 성장 조건 설정")

# 온도 설정
temperature = st.slider("온도 (°C)", -30, 50, 20)
# 수분 공급량 설정
water_supply = st.slider("수분 공급량 (1: 적음, 10: 많음)", 1, 10, 5)
# 햇빛 노출 시간 설정
sunlight = st.slider("햇빛 노출 시간 (시간)", 0, 24, 12)
# CO2 농도 설정
co2_level = st.slider("CO2 농도 (ppm)", 100, 1000, 400)

# 선택된 성장 조건에 따른 설명 제공
st.subheader("선택한 성장 조건")
st.write(f"온도: {temperature}°C")
st.write(f"수분 공급량: {water_supply}")
st.write(f"햇빛 노출 시간: {sunlight}시간")
st.write(f"CO2 농도: {co2_level} ppm")

# 조건에 따른 식물 특성 설명 제공
st.subheader("조건에 따른 식물의 특성")

# 다양한 성장 조건에 따른 결과 설정
def determine_plant_characteristics(temperature, water_supply, sunlight, co2_level):
    characteristics = {
        "잎 크기": "중간",
        "뿌리 크기": "중간",
        "꽃 크기": "없음",
        "열매 상태": "없음"
    }

    # 조건에 따른 잎 크기 결정
    if temperature > 30 and water_supply < 5:
        characteristics["잎 크기"] = "작음 (수분 손실 최소화)"
    elif temperature < 0:
        characteristics["잎 크기"] = "두껍고 작음 (추위 보호)"
    elif co2_level > 600:
        characteristics["잎 크기"] = "매우 큼 (광합성 촉진)"
    else:
        characteristics["잎 크기"] = "중간"

    # 조건에 따른 뿌리 크기 결정
    if water_supply < 3:
        characteristics["뿌리 크기"] = "깊음 (물을 찾기 위해)"
    elif water_supply > 7:
        characteristics["뿌리 크기"] = "얕음 (수분이 충분함)"
    else:
        characteristics["뿌리 크기"] = "중간"

    # 조건에 따른 꽃 크기 결정
    if temperature > 20 and sunlight > 10 and co2_level > 500:
        characteristics["꽃 크기"] = "큼 (성장에 적합한 조건)"
    elif temperature < 10 or sunlight < 5:
        characteristics["꽃 크기"] = "없음 (불리한 조건)"
    else:
        characteristics["꽃 크기"] = "중간"

    # 조건에 따른 열매 상태 결정
    if temperature > 25 and water_supply > 5 and co2_level > 400:
        characteristics["열매 상태"] = "잘 자람"
    elif temperature < 15 or water_supply < 4:
        characteristics["열매 상태"] = "없음 (불리한 조건)"
    else:
        characteristics["열매 상태"] = "중간"

    return characteristics

# 식물의 특성 결정
plant_characteristics = determine_plant_characteristics(temperature, water_supply, sunlight, co2_level)

# 결과 출력
st.write(f"잎 크기: {plant_characteristics['잎 크기']}")
st.write(f"뿌리 크기: {plant_characteristics['뿌리 크기']}")
st.write(f"꽃 크기: {plant_characteristics['꽃 크기']}")
st.write(f"열매 상태: {plant_characteristics['열매 상태']}")

# 식물 이미지 생성 (OpenAI API 사용하지 않음)
st.subheader("식물 이미지 (예시)")

# 기본 예시 이미지 표시
st.image("https://via.placeholder.com/512x512.png?text=식물+이미지+예시", caption="식물 이미지 (예시)")