import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import requests

# 사람의 사이토크롬 C 서열을 고정하고, 다른 동물의 서열을 입력하여 비교하는 코드입니다.

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

# 외부 데이터베이스에서 서열 가져오기 함수
def fetch_sequence(animal_name):
    # 여기서는 예시로 NCBI의 API를 사용하여 서열을 가져오는 방법을 보여줍니다.
    # 실제 사용 시에는 적절한 데이터베이스와 API 엔드포인트를 사용해야 합니다.
    url = f"https://api.example.com/get_sequence?animal={animal_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        st.error("서열을 가져오는 데 실패했습니다. 다시 시도하세요.")
        return None

# Streamlit UI
def main():
    st.title("사이토크롬 C 서열 비교: 사람 vs 다른 동물")
    
    # 동물 선택 또는 사용자 입력을 통한 서열 가져오기
    option = st.selectbox(
        '어떤 동물의 서열을 비교하시겠습니까?',
        ('붉은털 원숭이', '닭', '다른 동물 (직접 입력)')
    )
    
    if option == '붉은털 원숭이':
        seq2 = rhesus_cytochrome_c
        label2 = '붉은털 원숭이'
    elif option == '닭':
        seq2 = chicken_cytochrome_c
        label2 = '닭'
    else:
        animal_name = st.text_input("비교할 동물의 이름을 입력하세요:")
        if animal_name:
            seq2 = fetch_sequence(animal_name)
            label2 = animal_name
        else:
            st.stop()
    
    seq1 = human_cytochrome_c
    label1 = '사람'
    
    # 서열 비교 수행
    if seq2:
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