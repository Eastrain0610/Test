import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 사람과 붉은털 원숭이의 사이토크롬 C 서열을 비교하는 코드입니다.

# 서열 정의
human_cytochrome_c = "MGDVEKGKKIFVQKCAQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFAGIKKKTEREDLIAYLKKADEYITNA"
rhesus_cytochrome_c = "MGDVEKGKKIFVQKCAQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFAGIKKKTEREDLIAYLKKADEYIQNA"

# 서열 비교 함수
def compare_sequences(seq1, seq2):
    differences = []
    for i, (residue1, residue2) in enumerate(zip(seq1, seq2)):
        if residue1 != residue2:
            differences.append((i, residue1, residue2))
    return differences

# Streamlit UI
def main():
    st.title("사이토크롬 C 서열 비교: 사람 vs 붉은털 원숭이")
    
    # 서열 비교 수행
    differences = compare_sequences(human_cytochrome_c, rhesus_cytochrome_c)
    
    # 결과 출력
    if differences:
        st.write(f"두 서열 간의 차이점: 총 {len(differences)}개의 차이가 발견되었습니다.")
        for index, human_residue, rhesus_residue in differences:
            st.write(f"위치 {index + 1}: 사람 - {human_residue}, 붉은털 원숭이 - {rhesus_residue}")
    else:
        st.write("두 서열은 동일합니다.")
    
    # 서열 비교 결과 시각화
    diff_indices = [i for i, _, _ in differences]
    sequence_length = len(human_cytochrome_c)
    x = np.arange(1, sequence_length + 1)
    y = [1 if i in diff_indices else 0 for i in range(sequence_length)]
    
    fig, ax = plt.subplots(figsize=(10, 2))
    ax.bar(x, y, color='b')
    ax.set_xlabel('Position in Sequence')
    ax.set_ylabel('Difference (1 = Different, 0 = Same)')
    ax.set_title('Comparison of Human and Rhesus Monkey Cytochrome C Sequences')
    
    # Streamlit을 통해 그래프 표시
    st.pyplot(fig)

if __name__ == "__main__":
    main()