import streamlit as st
from PIL import Image
from io import BytesIO
import requests

# Streamlit 앱 제목
st.title("북극여우와 사막여우 시뮬레이션")

# 서식지 선택
environment = st.selectbox("여우의 서식지를 선택하세요", ["사막", "북극"])

# 서식지에 따른 기본 설명 제공
if environment == "사막":
    st.write("사막: 뜨겁고 건조한 환경입니다.")
elif environment == "북극":
    st.write("북극: 매우 추운 툰드라 환경입니다.")

# 신체적 조건 설정
st.header("신체적 조건 설정")

# 귀 크기 설정
ear_size = st.slider("귀 크기 (1: 작은 귀, 10: 큰 귀)", 1, 10, 5)
# 털 두께 설정
fur_thickness = st.slider("털 두께 (1: 얇은 털, 10: 두꺼운 털)", 1, 10, 5)
# 체구 크기 설정
body_size = st.slider("체구 크기 (1: 작은 체구, 10: 큰 체구)", 1, 10, 5)

# 선택된 신체적 조건에 따른 설명 제공
st.subheader("선택한 신체적 조건")
st.write(f"귀 크기: {ear_size}")
if ear_size > 5:
    st.write("큰 귀: 열을 방출하는 데 도움을 주며, 주로 뜨거운 환경에 적합합니다.")
else:
    st.write("작은 귀: 체열 손실을 줄이는 데 도움을 주며, 주로 추운 환경에 적합합니다.")

st.write(f"털 두께: {fur_thickness}")
if fur_thickness > 5:
    st.write("두꺼운 털: 추운 환경에서 체온을 유지하는 데 도움을 줍니다.")
else:
    st.write("얇은 털: 열을 쉽게 방출하며, 더운 환경에 적합합니다.")

st.write(f"체구 크기: {body_size}")
if body_size > 5:
    st.write("큰 체구: 체열을 보존하기 쉬워 추운 환경에서 적응하기 좋습니다.")
else:
    st.write("작은 체구: 체열을 빠르게 방출하며, 주로 더운 환경에서 적응하기 좋습니다.")

# 서식지와 신체적 조건 간의 적합성 평가
st.subheader("서식지와 신체적 조건 간의 적합성")
if environment == "사막":
    if ear_size > 5 and fur_thickness <= 5 and body_size <= 5:
        st.write("사막에 적합한 신체적 조건을 잘 선택하셨습니다.")
    else:
        st.write("선택한 조건들이 사막 환경에 최적화되지 않을 수 있습니다.")
elif environment == "북극":
    if ear_size <= 5 and fur_thickness > 5 and body_size > 5:
        st.write("북극에 적합한 신체적 조건을 잘 선택하셨습니다.")
    else:
        st.write("선택한 조건들이 북극 환경에 최적화되지 않을 수 있습니다.")