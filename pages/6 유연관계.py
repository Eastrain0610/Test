import os
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
import io

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

# 업로드 버튼 추가
if st.button('업로드'):
    if animal_sequence:
        # 사람의 사이토크롬 C 서열
        human_sequence = "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE"

        # 서열 일치율 계산 함수
        def calculate_similarity(seq1, seq2):
            # 두 서열의 길이가 다를 경우 최소 길이를 기준으로 계산
            min_length = min(len(seq1), len(seq2))
            matches = sum(a == b for a, b in zip(seq1[:min_length], seq2[:min_length]))
            return matches / min_length * 100

        # 일치율 계산 및 데이터 정리
        similarity = calculate_similarity(human_sequence, animal_sequence)
        data = {
            '서열 종류': ['사람', animal_common_name],
            '서열 길이': [len(human_sequence), len(animal_sequence)],
            '일치율 (%)': [100, similarity]
        }
        df = pd.DataFrame(data)

        # 내용 정리 표 출력
        st.subheader("내용 정리")
        st.table(df)

        # 엑셀 파일로 데이터 다운로드
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='서열 비교 결과')
            writer.close()
            processed_data = output.getvalue()

        st.download_button(label='엑셀 파일 다운로드',
                           data=processed_data,
                           file_name='cytochrome_c_comparison.xlsx',
                           mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

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
    else:
        st.warning("염기 서열을 입력해주세요.")
