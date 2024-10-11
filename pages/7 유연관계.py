import streamlit as st
from Bio import SeqIO
from Bio.Align import PairwiseAligner
import os

# Streamlit 앱 제목
st.title("사람 사이토크롬 C 유사도 비교")

# 파일 업로드 섹션
st.header("FASTA 파일 업로드")
uploaded_files = st.file_uploader("사이토크롬 C 서열이 포함된 두 개 이상의 FASTA 파일을 업로드하세요.", accept_multiple_files=True)

if uploaded_files:
    sequences = []
    for uploaded_file in uploaded_files:
        # FASTA 파일에서 서열 가져오기
        with open(uploaded_file.name, "w") as f:
            f.write(uploaded_file.getvalue().decode("utf-8"))
        for record in SeqIO.parse(uploaded_file.name, "fasta"):
            sequences.append(record)
        os.remove(uploaded_file.name)

    # 사이토크롬 C 서열 비교
    if len(sequences) >= 2:
        st.header("서열 간의 유사도 계산")
        aligner = PairwiseAligner()
        aligner.mode = 'global'

        # 두 서열 간의 유사도 계산 및 표시
        for i in range(len(sequences)):
            for j in range(i + 1, len(sequences)):
                alignment = aligner.align(sequences[i].seq, sequences[j].seq)
                similarity = alignment.score / min(len(sequences[i].seq), len(sequences[j].seq)) * 100
                st.write(f"{sequences[i].id}와 {sequences[j].id}의 유사도: {similarity:.2f}%")
    else:
        st.warning("두 개 이상의 FASTA 서열을 업로드해야 합니다.")
else:
    st.info("FASTA 파일을 업로드해 주세요.")