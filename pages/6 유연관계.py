import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import networkx as nx

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
plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# Streamlit 앱 설명
st.title("사이토크롬 C 서열 비교: 사람 vs 다른 동물")
st.write("이 애플리케이션은 사람과 다른 동물의 사이토크롬 C 서열을 비교합니다. 나눔 고딕 폰트를 사용하여 한글을 지원합니다.")

# 서열 데이터 (예시)
human_sequence = "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGP"
other_animal_sequence = "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTAP"

# 서열 일치율 계산
def calculate_similarity(seq1, seq2):
    matches = sum(a == b for a, b in zip(seq1, seq2))
    return matches / len(seq1) * 100

similarity = calculate_similarity(human_sequence, other_animal_sequence)

# 결과 출력
st.write(f"사람과 다른 동물의 사이토크롬 C 서열 일치율: {similarity:.2f}%")

# 서열 비교 시각화
fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(['사람', '다른 동물'], [len(human_sequence), len(other_animal_sequence)], color=['blue', 'green'])
ax.set_ylabel('서열 길이')
ax.set_title('사이토크롬 C 서열 길이 비교')

# Streamlit에 그래프 출력
st.pyplot(fig)