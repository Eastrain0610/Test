import os
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import requests

# 페이지 설정
st.set_page_config(page_title="사이토크롬 C 서열 비교: 사람 vs 다른 동물", layout="wide")

# Google API 및 Gemini API 키 입력
api_key = st.text_input("Google 또는 Gemini API 키를 입력하세요:", type="password")
if not api_key:
    st.error("이 애플리케이션을 사용하려면 유효한 API 키가 필요합니다.")
    st.stop()

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

# 학명 검색 및 입력
search_term = st.text_input("검색할 동물의 이름 또는 키워드를 입력하세요:", "chimpanzee")

# Google Generative Language API를 사용해 검색어에 따른 설명 생성하기
if search_term and api_key:
    try:
        # Google Generative Language API 호출
        headers = {
            'Content-Type': 'application/json',
        }
        data = {
            "prompt": {
                "text": search_term
            },
            "temperature": 0.7,
            "candidate_count": 1
        }
        response = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={api_key}',
            headers=headers,
            json=data
        )

        # API 응답 디버깅
        st.write(f"API 요청 URL: {response.url}")
        st.write(f"API 요청 데이터: {data}")

        if response.status_code == 200:
            response_data = response.json()
            st.write(f"API 응답 데이터: {response_data}")  # 디버깅을 위해 전체 응답 출력
            generated_text = response_data.get('candidates', [{}])[0].get('output', "결과 없음")
            st.write(f"검색 결과: {generated_text}")
        else:
            if 'API key expired' in response.text or 'API_KEY_INVALID' in response.text:
                st.error("API 키가 만료되었거나 유효하지 않습니다. 새 API 키를 발급받아 입력해 주세요.")
            else:
                st.error(f"API 호출 실패: 상태 코드 {response.status_code} - {response.text}")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

    st.warning("검색 결과가 없으므로 직접 학명을 입력하세요.")
    animal_name = st.text_input("비교할 동물의 학명을 입력하세요:", "Pan troglodytes")

# 사람의 사이토크롬 C 서열
human_sequence = "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE"

# 서열 일치율 계산 함수
def calculate_similarity(seq1, seq2):
    matches = sum(a == b for a, b in zip(seq1, seq2))
    return matches / len(seq1) * 100

# 사람의 서열 출력
st.subheader("사람의 사이토크롬 C 서열")
st.text(human_sequence[:80] + '\n' + human_sequence[80:])

# 다른 동물의 서열 입력
dog_sequence = st.text_area("비교할 동물의 사이토크롬 C 서열을 입력하세요:", "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTAP")

# 일치율 계산 및 출력
similarity = calculate_similarity(human_sequence, dog_sequence)
st.write(f"사람과 입력된 동물의 서열 일치율: {similarity:.2f}%")

# 서열 비교 시각화
fig, ax = plt.subplots(figsize=(10, 6))
labels = ['사람', '입력된 동물']
similarity_values = [100, similarity]
ax.bar(labels, similarity_values, color=['blue', 'green'])
ax.set_ylabel('서열 일치율 (%)', fontproperties=fontprop if fontprop else None)
ax.set_title('사이토크롬 C 서열 일치율 비교', fontproperties=fontprop if fontprop else None)
ax.tick_params(axis='x', labelsize=10)
for label in ax.get_xticklabels():
    label.set_fontproperties(fontprop if fontprop else None)

# Streamlit에 그래프 출력
st.pyplot(fig)