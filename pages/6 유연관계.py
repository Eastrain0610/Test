import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 사람, 붉은털 원숭이, 닭의 사이토크롬 C 서열을 비교하는 코드입니다.

# 서열 정의
human_cytochrome_c = "MGDVEKGKKIFVQKCAQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFAGIKKKTEREDLIAYLKKADEYITNA"
rhesus_cytochrome_c = "MGDVEKGKKIFVQKCAQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFAGIKKKTEREDLIAYLKKADEYIQNA"
chicken_cytochrome_c = "MGDVEKGKKIFVQKCAQCHTVEKGGPHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLEDPKDYIPGTKMVFAAMKKKTEREDLIAYLKDATSE"

# 서열 비교 함수
def compare_sequences(seq1, seq2):
    differences = []
    for i, (residue1, residue2) in enumerate(zip(seq1, seq2)):
        if residue1 != residue2:
            differences.append((i, residue1, residue2))
    return differences

# 일치 비율 계산 함수
def calculate_similarity(seq1, seq2):
    matches = sum(1 for a, b in zip(seq1, seq2) if a == b)
    return (matches / len(seq1)) * 100

# Streamlit UI
def main():
    st.title("사이토크롬 C 서열 비교: 사람 vs 붉은털 원숭이 vs 닭")
    
    # 서열 비교 선택
    option = st.selectbox(
        '어떤 두 서열을 비교하시겠습니까?',
        ('사람 vs 붉은털 원숭이', '사람 vs 닭', '붉은털 원숭이 vs 닭')
    )
    
    if option == '사람 vs 붉은털 원숭이':
        seq1 = human_cytochrome_c
        seq2 = rhesus_cytochrome_c
        label1 = '사람'
        label2 = '붉은털 원숭이'
    elif option == '사람 vs 닭':
        seq1 = human_cytochrome_c
        seq2 = chicken_cytochrome_c
        label1 = '사람'
        label2 = '닭'
    else:
        seq1 = rhesus_cytochrome_c
        seq2 = chicken_cytochrome_c
        label1 = '붉은털 원숭이'
        label2 = '닭'
    
    # 서열 비교 수행
    differences = compare_sequences(seq1, seq2)
    similarity = calculate_similarity(seq1, seq2)
    
    # 결과 출력
    st.write(f"두 서열 간의 일치율: {similarity:.2f}%")
    if differences:
        st.write(f"두 서열 간의 차이점: 총 {len(differences)}개의 차이가 발견되었습니다.")
        for index, residue1, residue2 in differences:
            st.write(f"위치 {index + 1}: {label1} - {residue1}, {label2} - {residue2}")
    else:
        st.write("두 서열은 동일합니다.")
    
    # 서열 비교 결과 시각화
    diff_indices = [i for i, _, _ in differences]
    sequence_length = len(seq1)
    x = np.arange(1, sequence_length + 1)
    y = [1 if i in diff_indices else 0 for i in range(sequence_length)]
    
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.bar(x, y, color='b')
    ax.set_xlabel('Position in Sequence')
    ax.set_ylabel('Difference (1 = Different, 0 = Same)')
    ax.set_title(f'Comparison of {label1} and {label2} Cytochrome C Sequences')
    
    # Streamlit을 통해 그래프 표시
    st.pyplot(fig)

if __name__ == "__main__":
    main()