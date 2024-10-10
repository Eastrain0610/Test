import streamlit as st
from PIL import Image
from io import BytesIO
import requests

# Streamlit 앱 제목
st.title("북극과 사막의 식물 시뮬레이션")

# 서식지 선택
environment = st.selectbox("식물의 서식지를 선택하세요", ["사막", "북극"])

# 서식지에 따른 기본 설명 제공
if environment == "사막":
    st.write("사막: 뜨겁고 건조한 환경입니다.")
elif environment == "북극":
    st.write("북극: 매우 추운 툰드라 환경입니다.")

# 식물 성장 조건 설정
st.header("식물 성장 조건 설정")

# 온도 설정
temperature = st.slider("온도 (°C)", -30, 50, 20)
# 수분 공급량 설정
water_supply = st.slider("수분 공급량 (1: 적음, 10: 많음)", 1, 10, 5)
# 햇빛 노출 시간 설정
sunlight = st.slider("햇빛 노출 시간 (시간)", 0, 24, 12)

# 선택된 성장 조건에 따른 설명 제공
st.subheader("선택한 성장 조건")
st.write(f"온도: {temperature}°C")
st.write(f"수분 공급량: {water_supply}")
st.write(f"햇빛 노출 시간: {sunlight}시간")

# 조건에 따른 식물 특성 설명 제공
st.subheader("조건에 따른 식물의 특성")
if environment == "사막":
    if temperature > 30 and water_supply < 5 and sunlight > 12:
        st.write("이 조건에서는 두꺼운 왁스층을 가진 얇은 잎을 가진 식물이 적합합니다. 수분 손실을 최소화합니다.")
    else:
        st.write("이 조건에서는 적당한 크기의 잎과 강한 뿌리를 가진 식물이 적합합니다.")
elif environment == "북극":
    if temperature < 0 and water_supply > 5:
        st.write("이 조건에서는 두꺼운 잎과 낮은 키를 가진 식물이 적합합니다. 추운 환경에서 체온을 유지합니다.")
    else:
        st.write("이 조건에서는 내한성이 강한 식물이 적합합니다.")

# 식물 이미지 생성 (OpenAI API 사용하지 않음)
st.subheader("식물 이미지 (예시)")

# 사막과 북극에 따른 기본 예시 이미지 표시
if environment == "사막":
    st.image("https://via.placeholder.com/512x512.png?text=사막+식물+이미지+예시", caption="사막 식물 이미지 (예시)")
elif environment == "북극":
    st.image("https://via.placeholder.com/512x512.png?text=북극+식물+이미지+예시", caption="북극 식물 이미지 (예시)")