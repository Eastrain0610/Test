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

# 서열 데이터 (예시)
human_sequence = "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGP"

# 사용자 입력을 통한 다른 동물의 서열 입력
other_animal_sequence = st.text_input("다른 동물의 사이토크롬 C 서열을 입력하세요:", "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTAP")

# 서열 일치율 계산
def calculate_similarity(seq1, seq2):
    matches = sum(a == b for a, b in zip(seq1, seq2))
    return matches / len(seq1) * 100

similarity = calculate_similarity(human_sequence, other_animal_sequence)

# 결과 출력
st.write(f"사람과 다른 동물의 사이토크롬 C 서열 일치율: {similarity:.2f}%")

# 서열 데이터 출력
st.subheader("사람의 사이토크롬 C 서열")
st.text(human_sequence)

st.subheader("다른 동물의 사이토크롬 C 서열")
st.text(other_animal_sequence)

# 서열 비교 시각화
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(['사람', '다른 동물'], [len(human_sequence), len(other_animal_sequence)], color=['blue', 'green'])
ax.set_ylabel('서열 길이', fontproperties=fontprop if fontprop else None)
ax.set_title('사이토크롬 C 서열 길이 비교', fontproperties=fontprop if fontprop else None)
ax.tick_params(axis='x', labelsize=12)
for label in ax.get_xticklabels():
    label.set_fontproperties(fontprop if fontprop else None)

# Streamlit에 그래프 출력
st.pyplot(fig)