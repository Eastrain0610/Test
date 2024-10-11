import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import sys
import os
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
    plt.rcParams['font.family'] = fontprop.get_name()
else:
    st.warning("NanumGothic.ttf 폰트 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.")
    fontprop = None

# Streamlit 앱 제목 설정
st.title('사이토크롬 C 서열 비교: 사람 vs 다른 동물')

# 학생이 입력한 동물 이름, 학명, 단백질 서열
user_animal_name = st.text_input('비교할 동물의 이름을 입력하세요 (예: 침팬지):')
user_animal_sci_name = st.text_input('비교할 동물의 학명을 입력하세요 (예: Pan troglodytes):')
user_animal_protein_seq = st.text_area('비교할 동물의 사이토크롬 C 단백질 서열을 입력하세요:')

# 사람의 사이토크롬 C 단백질 서열
human_protein_seq = "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE"

# 출석한 학생 데이터를 저장할 리스트 초기화
if 'student_data' not in st.session_state:
    st.session_state['student_data'] = []

# 학명 데이터 추가
if user_animal_name and user_animal_sci_name and user_animal_protein_seq and st.button('제출'):
    st.session_state['student_data'].append({
        '이름': user_animal_name,
        '학명': user_animal_sci_name,
        '서열': user_animal_protein_seq
    })
    st.success('학명 데이터가 성공적으로 정리되었습니다!')

# 저장된 학생 데이터를 데이터프레임으로 변환하여 표시
if st.session_state['student_data']:
    student_df = pd.DataFrame(st.session_state['student_data'])
    st.write("## 학명 데이터:")
    st.dataframe(student_df)

# 서열 비교 및 결과 출력
from Bio import pairwise2
from Bio.pairwise2 import format_alignment

def compare_sequences(seq1, seq2):
    if not seq1 or not seq2:
        return None, "서열을 가져오지 못했습니다. 다시 시도해 주세요."
    
    # BioPython의 pairwise2를 이용한 정렬 및 비교
    alignments = pairwise2.align.globalxx(seq1, seq2)
    best_alignment = alignments[0]
    alignment_str = format_alignment(*best_alignment)

    # Query와 Sbjct 서열을 정렬하여 보기 쉽게 표현
    aligned_seq1, aligned_seq2, score, start, end = best_alignment
    result_str = ""
    line_length = 60
    for i in range(0, len(aligned_seq1), line_length):
        query_line = f"Query {i+1:<5}{aligned_seq1[i:i+line_length]}  {i+line_length}"
        sbjct_line = f"Sbjct {i+1:<5}{aligned_seq2[i:i+line_length]}  {i+line_length}"
        result_str += query_line + "\n" + sbjct_line + "\n\n"
    
    similarity_percentage = (best_alignment.score / min(len(seq1), len(seq2))) * 100
    return similarity_percentage, result_str

if user_animal_protein_seq:
    similarity, alignment_result = compare_sequences(human_protein_seq, user_animal_protein_seq)

    if similarity is not None:
        st.write(f"유사도: {similarity:.2f}%")
        st.text(alignment_result)
    else:
        st.write("서열 비교에 실패했습니다. 다시 시도해 주세요.")

    # 그래프 시각화
    if similarity is not None:
        fig, ax = plt.subplots()
        ax.bar(['사람', user_animal_name], [len(human_protein_seq), len(user_animal_protein_seq)], color=['blue', 'green'])
        ax.set_ylabel('단백질 서열 길이', fontproperties=fontprop if fontprop else None)
        ax.set_title('사이토크롬 C 단백질 서열 길이 비교', fontproperties=fontprop if fontprop else None)
        ax.set_xticklabels(['사람', user_animal_name], fontproperties=fontprop if fontprop else None)
        st.pyplot(fig)

    # 사용자가 서열을 보고 싶을 경우 출력
    if st.checkbox('사이토크롬 C 단백질 서열 보기'):
        st.subheader('사람 사이토크롬 C 단백질 서열')
        st.text(human_protein_seq)

        st.subheader(f'{user_animal_name} ({user_animal_sci_name}) 사이토크롬 C 단백질 서열')
        st.text(user_animal_protein_seq)
else:
    st.write("유효한 동물 이름을 입력하고 서열을 확인하세요.")