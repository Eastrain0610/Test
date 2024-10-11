import streamlit as st
from Bio.Align import PairwiseAligner

# Streamlit 앱 제목
st.title("사람 사이토크롬 C 유사도 비교")

# 염기서열 입력 섹션
st.header("사이토크롬 C 염기서열 입력")
sequences_input = st.text_area("각 염기서열을 FASTA 형식으로 입력하세요. 여러 서열을 비교하려면 각각을 '>'로 시작하여 구분하세요.", height=200)

# 기본 사람 사이토크롬 C 서열 추가
default_human_cytochrome_c = (">Human Cytochrome C\n"
                              "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLE\n"
                              "NPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE")
sequences_input = default_human_cytochrome_c + "\n" + sequences_input

if sequences_input:
    sequences = []
    current_sequence = ""
    current_id = ""
    for line in sequences_input.splitlines():
        if line.startswith(">"):
            if current_sequence:
                sequences.append((current_id, current_sequence))
            current_id = line[1:].strip()
            current_sequence = ""
        else:
            current_sequence += line.strip()
    if current_sequence:
        sequences.append((current_id, current_sequence))

    # 사이토크롬 C 서열 비교
    if len(sequences) >= 2:
        st.header("서열 간의 유사도 계산")
        aligner = PairwiseAligner()
        aligner.mode = 'global'

        # 두 서열 간의 유사도 계산 및 표시
        for i in range(len(sequences)):
            for j in range(i + 1, len(sequences)):
                alignment = aligner.align(sequences[i][1], sequences[j][1])
                similarity = alignment.score / min(len(sequences[i][1]), len(sequences[j][1])) * 100
                st.write(f"{sequences[i][0]}와 {sequences[j][0]}의 유사도: {similarity:.2f}%")
    else:
        st.warning("두 개 이상의 염기서열을 입력해야 합니다.")
else:
    st.info("염기서열을 입력해 주세요.")