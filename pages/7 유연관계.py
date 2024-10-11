import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import sys
import os
import matplotlib.font_manager as fm
from Bio import Entrez, SeqIO

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

# 사용자가 선택할 수 있는 동물 옵션
animal_options = ['침팬지', '고릴라', '쥐', '소', '돼지']
selected_animal = st.selectbox('비교할 동물을 선택하세요:', animal_options)

# NCBI에서 사이토크롬 C 서열 가져오기 함수
Entrez.email = "dws0610@naver.com"  # 여기에 자신의 이메일 주소를 입력하세요.

def fetch_cytochrome_c_sequence(organism_name):
    search_term = f"{organism_name}[Organism] AND cytochrome c"
    handle = Entrez.esearch(db="nucleotide", term=search_term, retmax=1)
    record = Entrez.read(handle)
    handle.close()
    if record["IdList"]:
        seq_id = record["IdList"][0]
        handle = Entrez.efetch(db="nucleotide", id=seq_id, rettype="gb", retmode="text")
        seq_record = SeqIO.read(handle, "genbank")
        handle.close()
        return seq_record.seq
    return None

# 사람과 사용자가 선택한 동물의 사이토크롬 C 서열 가져오기
st.write("사이토크롬 C 서열을 가져오는 중입니다...")

human_seq = fetch_cytochrome_c_sequence("Homo sapiens")
animal_seq = fetch_cytochrome_c_sequence(selected_animal)

# 서열 비교 및 결과 출력
def compare_sequences(seq1, seq2):
    if not seq1 or not seq2:
        return None, "서열을 가져오지 못했습니다. 다시 시도해 주세요."
    
    # 간단한 서열 비교: 동일한 염기 수와 비율 계산
    min_len = min(len(seq1), len(seq2))
    matches = sum(1 for i in range(min_len) if seq1[i] == seq2[i])
    similarity_percentage = (matches / min_len) * 100
    return similarity_percentage, f"유사도: {similarity_percentage:.2f}%"

similarity, message = compare_sequences(human_seq, animal_seq)

if similarity is not None:
    st.write(message)
else:
    st.write("서열 비교에 실패했습니다. 다시 시도해 주세요.")

# 그래프 시각화
if similarity is not None:
    fig, ax = plt.subplots()
    ax.bar(['사람', selected_animal], [len(human_seq), len(animal_seq)], color=['blue', 'green'])
    ax.set_ylabel('서열 길이', fontproperties=fontprop if fontprop else None)
    ax.set_title('사이토크롬 C 서열 길이 비교', fontproperties=fontprop if fontprop else None)
    st.pyplot(fig)

# 사용자가 서열을 보고 싶을 경우 출력
if st.checkbox('사이토크롬 C 서열 보기'):
    st.subheader('사람 사이토크롬 C 서열')
    st.text(str(human_seq))

    st.subheader(f'{selected_animal} 사이토크롬 C 서열')
    st.text(str(animal_seq))