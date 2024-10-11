import os
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 페이지 설정
st.set_page_config(page_title="사이토크롬 C 서열 비교: 사람 vs 다른 동물", layout="wide")

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

# 동물 이름 및 학명, 서열 입력
animal_common_name = st.text_input("비교할 동물의 이름을 작성해 주세요:", "예:침팬지")
animal_name = st.text_input("비교할 동물의 학명을 입력하세요:", "예:Pan troglodytes")
animal_sequence = st.text_area("비교할 동물의 사이토크롬 C의 염기 서열을 작성해주세요:", "예:MGDVEKGKKIFVQKCAQCHTVEKGGKHKTGPNLHGLFRQKTGQAVGFSYTDANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFAGIKKKAEKADLTAYLKKATND")

# 사람의 사이토크롬 C 서열
human_sequence = "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE"

# 서열 일치율 계산 함수
def calculate_similarity(seq1, seq2):
    # 두 서열의 길이가 다를 경우 최소 길이를 기준으로 계산
    min_length = min(len(seq1), len(seq2))
    matches = sum(a == b for a, b in zip(seq1[:min_length], seq2[:min_length]))
    return matches / min_length * 100

# 서열 비교 함수
def align_sequences(query, subject):
    alignment = []
    for i, (q, s) in enumerate(zip(query, subject)):
        if q == s:
            alignment.append(q)
        else:
            alignment.append(' ')  # 빈칸으로 표현해 차이점 구분
    return ''.join(alignment)

# 서열 정렬 및 출력
st.subheader("서열 정렬 결과")
query_aligned = human_sequence
subject_aligned = animal_sequence[:len(human_sequence)]
alignment = align_sequences(query_aligned, subject_aligned)

st.text(f"Query  1    {query_aligned[:60]}  60")
st.text(f"            {alignment[:60]}")
st.text(f"Sbjct  1    {subject_aligned[:60]}  60")

st.text(f"Query  61   {query_aligned[60:]}  105")
st.text(f"            {alignment[60:]}")
st.text(f"Sbjct  61   {subject_aligned[60:]}  105")

# 사람의 서열 출력
st.subheader("사람의 사이토크롬 C 서열")
st.text(human_sequence[:80] + '\n' + human_sequence[80:])

# 일치율 계산 및 출력
similarity = calculate_similarity(human_sequence, animal_sequence)
st.write(f"사람과 {animal_common_name}의 서열 일치율: {similarity:.2f}%")

# 서열 비교 시각화
fig, ax = plt.subplots(figsize=(10, 6))
labels = ['사람', animal_common_name]
similarity_values = [100, similarity]
ax.bar(labels, similarity_values, color=['blue', 'green'])
ax.set_ylabel('서열 일치율 (%)', fontproperties=fontprop if fontprop else None)
ax.set_title('사이토크롬 C 서열 일치율 비교', fontproperties=fontprop if fontprop else None)
ax.tick_params(axis='x', labelsize=10)
for label in ax.get_xticklabels():
    label.set_fontproperties(fontprop if fontprop else None)

# Streamlit에 그래프 출력
st.pyplot(fig)