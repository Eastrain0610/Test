import os
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import requests

# 페이지 설정
st.set_page_config(page_title="사이토크롬 C 서열 비교: 사람 vs 다른 동물", layout="wide")

# Gemini API 키 입력 및 설정
api_key = st.text_input("Gemini API 키를 입력하세요:", type="password")
if not api_key:
    st.error("이 애플리케이션을 사용하려면 유효한 Gemini API 키가 필요합니다.")
    st.stop()

# 폰트 파일 경로 설정
possible_paths = [
    "./fonts/NanumGothic.ttf",
    "../fonts/NanumGothic.ttf",
    "/workspaces/test/fonts/NanumGothic.ttf"
]

font_path = None
for path in possible_paths:
    if os.path.exists(path):
        font_path = path
        break

if font_path:
    fontprop = fm.FontProperties(fname=font_path)
else:
    st.warning("NanumGothic.ttf 폰트 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.")
    fontprop = None

# 나눔 고딕 폰트 설정 (CSS 적용)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Nanum Gothic', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# 나눔 고딕 폰트를 Matplotlib에 설정
if fontprop:
    plt.rc('font', family=fontprop.get_name())
plt.rcParams['axes.unicode_minus'] = False

# 앱 설명
st.title("사이토크롬 C 서열 비교: 사람 vs 다른 동물")

# 학명 입력 및 생물 정보 표시
animal_name = st.text_input("비교할 동물의 학명을 입력하세요:", "Pan troglodytes")

# Gemini API를 사용해 학명에 따른 생물 정보 가져오기
if animal_name:
    try:
        response = requests.get(f"https://api.gemini.com/organism/{animal_name}", headers={"Authorization": f"Bearer {api_key}"})
        if response.status_code == 200:
            organism_info = response.json().get('common_name', "정보를 찾을 수 없습니다.")
            st.write(f"{animal_name}는 {organism_info}입니다.")
        else:
            st.warning("Gemini API에서 생물 정보를 가져오는 데 실패했습니다. 다른 학명을 입력해보세요.")
    except Exception as e:
        st.error(f"API 요청 중 오류가 발생했습니다: {e}")

# 사람의 사이토크롬 C 서열
human_sequence = "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE"

# 서열 일치율 계산 함수
def calculate_similarity(seq1, seq2):
    matches = sum(a == b for a, b in zip(seq1, seq2))
    return matches / len(seq1) * 100

# 사람의 서열 출력
st.subheader("사람의 사이토크롬 C 서열")
st.text(human_sequence[:80] + '\n' + human_sequence[80:])

# 다른 동물의 서열 입력
dog_sequence = st.text_area("비교할 동물의 사이토크롬 C 서열을 입력하세요:", "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTAP")

# 일치율 계산 및 출력
similarity = calculate_similarity(human_sequence, dog_sequence)
st.write(f"사람과 입력된 동물의 서열 일치율: {similarity:.2f}%")

# 서열 비교 시각화
fig, ax = plt.subplots(figsize=(10, 6))
labels = ['사람', '입력된 동물']
similarity_values = [100, similarity]
ax.bar(labels, similarity_values, color=['blue', 'green'])
ax.set_ylabel('서열 일치율 (%)', fontproperties=fontprop if fontprop else None)
ax.set_title('사이토크롬 C 서열 일치율 비교', fontproperties=fontprop if fontprop else None)
ax.tick_params(axis='x', labelsize=10)
for label in ax.get_xticklabels():
    label.set_fontproperties(fontprop if fontprop else None)

# Streamlit에 그래프 출력
st.pyplot(fig)