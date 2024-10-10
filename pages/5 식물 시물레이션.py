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

# 만들어진 식물 분석
st.subheader("만들어진 식물 분석")
analysis = "이러한 특성을 가진 식물은 "
if temperature > 30 and water_supply < 5:
    analysis += "건조하고 뜨거운 사막과 같은 환경에서 잘 적응할 수 있습니다. 잎이 작고 수분 손실을 최소화하는 특성을 가지고 있습니다. 대표적인 식물로는 선인장과 같은 다육식물이 있습니다."
elif temperature < 0:
    analysis += "추운 기후의 툰드라 환경에서 잘 살 수 있습니다. 두꺼운 잎과 낮은 키로 추위를 견딜 수 있습니다. 대표적인 식물로는 이끼류와 방울꽃 등이 있습니다."
elif co2_level > 600:
    analysis += "CO2 농도가 높은 환경에서 빠르게 성장할 수 있으며, 광합성이 활발하게 이루어지는 환경에 적합합니다. 이러한 특성을 가진 대표적인 식물로는 고속 성장 나무인 유칼립투스가 있습니다."
else:
    analysis += "온화한 기후에서 적당한 수분과 햇빛을 필요로 하며, 일반적인 환경에서 잘 자랄 수 있습니다. 이러한 특성을 가진 대표적인 식물로는 민들레와 같은 야생화가 있습니다."

st.write(analysis)

# 식물 이미지 생성 (OpenAI API 사용하지 않음)
st.subheader("식물 이미지 (예시)")

# 기본 예시 이미지 표시
st.image("https://via.placeholder.com/512x512.png?text=식물+이미지+예시", caption="식물 이미지 (예시)")