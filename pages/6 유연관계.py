import os
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 폰트 파일 경로 설정: 다양한 경로에서 시도해 보기
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
    fontprop = None  # 폰트를 찾지 못했을 경우 기본 폰트를 사용

# Streamlit 웹 페이지 설정
st.set_page_config(page_title="사이토크롬 C 서열 비교: 사람 vs 다른 동물", layout="wide")

# 나눔 고딕 폰트 설정 (CSS를 이용해 전체 텍스트 적용)
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
    plt.rc('font', **{'family': fontprop.get_name()})
plt.rcParams['axes.unicode_minus'] = False

# Streamlit 앱 설명
st.title("사이토크롬 C 서열 비교: 사람 vs 다른 동물")
st.write("이 애플리케이션은 사람과 다른 동물의 사이토크롬 C 서열을 비교합니다. 나눔 고딕 폰트를 사용하여 한글을 지원합니다.")

# 사람의 사이토크롬 C 서열
human_sequence = "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE"

# 사용자 입력을 통한 학명 입력 및 Gemini API 사용
import requests

animal_name = st.text_input("다른 동물의 학명을 입력하세요:", "Animal 1")

# Gemini API를 사용해 학명에 따른 사이토크롬 C 서열 가져오기
if animal_name:
    try:
        response = requests.get(f"https://api.gemini.com/sequence/{animal_name}")
        if response.status_code == 200:
            other_animal_sequence = response.json().get('sequence', "데이터를 찾을 수 없습니다.")
            st.write(f"{animal_name}의 사이토크롬 C 서열:")
            st.text(other_animal_sequence)
        else:
            st.warning("Gemini API에서 데이터를 가져오는 데 실패했습니다. 다른 학명을 입력해보세요.")
    except Exception as e:
        st.error(f"API 요청 중 오류가 발생했습니다: {e}")

# 학명에 따른 사이토크롬 C 서열 예시 데이터
animal_sequences = {
    "Animal 1": "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTAP",
    "Animal 2": "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTAA",
    "Animal 3": "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGP",
    "Animal 4": "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTTG"
}

# 입력된 학명에 해당하는 서열을 가져오기
if animal_name in animal_sequences:
    other_animal_sequence = animal_sequences[animal_name]
    st.write(f"{animal_name}의 사이토크롬 C 서열:")
    st.text(other_animal_sequence)
else:
    st.warning("입력한 학명에 해당하는 서열 데이터가 없습니다. 다른 학명을 입력해보세요.")

# 사용자 입력을 통한 다른 동물의 서열 입력 (최대 2가지 서열 입력)
other_animal_sequences = []
other_animal_names = []
for i in range(1, 3):
    animal_name = st.text_input(f"다른 동물 {i}의 학명을 입력하세요:", f"Animal {i}")
    other_animal_names.append(animal_name)
    other_animal_sequence = st.text_input(f"{animal_name}의 사이토크롬 C 서열을 입력하세요:", f"MGDVEKGKKIFIMKCSQCHTVEKGGKHKTAP")
    other_animal_sequences.append(other_animal_sequence)

# 서열 일치율 계산
def calculate_similarity(seq1, seq2):
    matches = sum(a == b for a, b in zip(seq1, seq2))
    return matches / len(seq1) * 100

# 결과 출력
st.write("사람과 다른 동물들의 사이토크롬 C 서열 일치율:")
similarities = []
for i, (animal_name, other_animal_sequence) in enumerate(zip(other_animal_names[:2], other_animal_sequences[:2])):
    similarity = calculate_similarity(human_sequence, other_animal_sequence)
    similarities.append(similarity)
    st.write(f"사람과 {animal_name}의 서열 일치율: {similarity:.2f}%")

# 서열 데이터 출력
st.subheader("사람의 사이토크롬 C 서열")
st.text(human_sequence[:80] + '\n' + human_sequence[80:])

for i, (animal_name, other_animal_sequence) in enumerate(zip(other_animal_names, other_animal_sequences)):
    st.subheader(f"{animal_name}의 사이토크롬 C 서열")
    st.text(other_animal_sequence)

# 서열 비교 시각화
fig, ax = plt.subplots(figsize=(10, 6))
labels = [f'사람 vs {animal_name}' for animal_name in other_animal_names[:2]]
similarity_values = similarities[:2]
ax.bar(labels, similarity_values, color=['blue'] * len(other_animal_sequences))
ax.set_ylabel('서열 일치율 (%)', fontproperties=fontprop if fontprop else None)
ax.set_title('사이토크롬 C 서열 일치율 비교', fontproperties=fontprop if fontprop else None)
ax.tick_params(axis='x', labelsize=10)
for label in ax.get_xticklabels():
    label.set_fontproperties(fontprop if fontprop else None)

# Streamlit에 그래프 출력
st.pyplot(fig)