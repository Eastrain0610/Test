import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
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
else:
    st.warning("NanumGothic.ttf 폰트 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.")
    fontprop = None

# 파일 자동 업로드 및 데이터 처리
def 점수_데이터_업로드():
    폴더_경로 = "./data"
    파일_이름 = "점수.csv"
    파일_경로 = os.path.join(폴더_경로, 파일_이름)

    if os.path.exists(파일_경로):
        데이터 = pd.read_csv(파일_경로, encoding='cp949')
        return 데이터
    else:
        st.warning(f"{폴더_경로}에서 파일 {파일_이름}을(를) 찾을 수 없습니다. 폴더와 파일 이름을 확인해주세요.")
    return None

# 점수 데이터 분석
def 점수_데이터_분석(데이터):
    총_학생_수 = 데이터.shape[0]
    평균_점수 = 데이터['점수'].mean()
    정렬된_점수 = 데이터['점수'].sort_values(ascending=False).reset_index(drop=True)

    # 등급별 인원 수 계산
    등급_기준 = {
        1: round(총_학생_수 * 0.04),
        2: round(총_학생_수 * 0.07),
        3: round(총_학생_수 * 0.12),
        4: round(총_학생_수 * 0.17),
        5: round(총_학생_수 * 0.20),
        6: round(총_학생_수 * 0.17),
        7: round(총_학생_수 * 0.12),
        8: round(총_학생_수 * 0.07),
        9: round(총_학생_수 * 0.04)
    }

    기준_점수 = {}
    시작_인덱스 = 0
    for 등급, 인원 in 등급_기준.items():
        종료_인덱스 = 시작_인덱스 + 인원 - 1
        기준_점수[등급] = 정렬된_점수.iloc[종료_인덱스]
        시작_인덱스 = 종료_인덱스 + 1

    return 기준_점수, 평균_점수

# 등급 결정
def 등급_결정(기준_점수, 점수):
    for 등급 in sorted(기준_점수.keys()):
        if 점수 >= 기준_점수[등급]:
            return 등급
    return 9

# 난이도 판별
def 난이도_판별(평균_점수, 표준_편차):
    if 평균_점수 > 70 and 표준_편차 < 15:
        return "쉬움"
    elif 평균_점수 < 50 and 표준_편차 > 15:
        return "어려움"
    else:
        return "보통"

# 등급 분포 시각화
def 등급_분포_시각화(기준_점수, 학생_점수, 평균_점수, 표준_편차, 난이도):
    등급들 = list(기준_점수.keys())
    점수들 = [기준_점수[등급] for 등급 in 등급들]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(등급들, 점수들, marker='o', linestyle='-', label='등급 경계')
    # 학생의 등급에 해당하는 지점에 별 표시
    # 학생의 등급 위치 계산 후 별 표시
    학생_등급 = 등급_결정(기준_점수, 학생_점수)
    ax.plot(학생_등급, 학생_점수, marker='*', color='purple', markersize=15, label='학생 등급 위치')
    ax.text(학생_등급, 학생_점수 + 3, f'{학생_등급}등급', color='purple', fontsize=12, ha='center', fontproperties=fontprop if fontprop else None)
    ax.set_xlabel('등급', fontproperties=fontprop if fontprop else None)
    ax.set_ylabel('점수', fontproperties=fontprop if fontprop else None)
    ax.set_title(f'점수에 따른 등급 경계 - 난이도: {난이도}', fontproperties=fontprop if fontprop else None)

    ax.axhline(y=평균_점수, color='blue', linestyle='--', label='평균 점수', linewidth=1.5)
    ax.text(x=1.1, y=평균_점수 - 3, s=f'평균: {평균_점수:.2f}', color='blue', va='top', fontproperties=fontprop if fontprop else None)

    학생_등급 = 등급_결정(기준_점수, 학생_점수)
    ax.axhline(y=학생_점수, color='red', linestyle='--', label=f'학생 점수: {학생_점수}', linewidth=1.5)
    ax.text(x=1.1, y=학생_점수 - 3, s=f'학생 점수: {학생_점수}', color='red', va='top', fontproperties=fontprop if fontprop else None)

    ax.set_xticks(등급들)
    ax.invert_xaxis()
    ax.legend(prop=fontprop if fontprop else None)
    ax.grid(True)

    st.pyplot(fig)

# Streamlit 앱 구현
st.title("생명 과학 점수 등급표")

# 파일 업로드
데이터 = 점수_데이터_업로드()

if 데이터 is not None:
    st.write(f"총 학생 인원: {데이터.shape[0]}명")
    # 데이터 분석
    기준_점수, 평균_점수 = 점수_데이터_분석(데이터)
    표준_편차 = 데이터['점수'].std()
    난이도 = 난이도_판별(평균_점수, 표준_편차)

    # 사용자 점수 입력
    학생_점수 = st.number_input("학생 점수를 입력해주세요:", min_value=0.0, max_value=100.0, value=85.0)
    학생_등급 = 등급_결정(기준_점수, 학생_점수)

    # 결과 출력
    st.write(f"학생의 점수는 {학생_점수}, {학생_등급}등급입니다.")
    st.write(f"학생의 총 평균 점수는: {평균_점수:.2f}")
    st.write(f"표준 편차는: {표준_편차:.2f}")
    st.write(f"시험 난이도는: {난이도}")

    # 등급 분포 시각화
    등급_분포_시각화(기준_점수, 학생_점수, 평균_점수, 표준_편차, 난이도)