import os
import streamlit as st
import matplotlib.pyplot as plt
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
    fontprop = None  # 폰트를 찾지 못했을 경우 기본 폰트를 사용

# 사용자의 혈액형에 따른 부모의 가능한 혈액형 조합 예측 함수
def predict_parents_blood_type(child):
    if child == 'A':
        return ['AA, AO', 'AO, AO', 'AO, AB', 'AA, AA', 'AA, AB']
    elif child == 'B':
        return ['BB, BO', 'BO, BO', 'BO, AB', 'BB, BB', 'BB, AB']
    elif child == 'O':
        return ['OO, OO', 'AO, BO', 'BO, AO']
    elif child == 'AB':
        return ['AB, AB', 'AA, BB', 'AO, BB', 'AA, BO', 'AB, AA', 'AB, BB']
    else:
        return []

# 자녀의 혈액형이 A형일 때 부모의 가능한 조합과 각 조합의 확률 계산 함수
def calculate_probability(child):
    if child == 'A':
        return {
            'AA, AO': 0.5,
            'AO, AO': 0.25,
            'AO, AB': 0.25,
            'AA, AA': 1.0,
            'AA, AB': 0.5
        }
    elif child == 'B':
        return {
            'BB, BO': 0.5,
            'BO, BO': 0.25,
            'BO, AB': 0.25,
            'BB, BB': 1.0,
            'BB, AB': 0.5
        }
    elif child == 'O':
        return {
            'OO, OO': 1.0,
            'AO, BO': 0.25,
            'BO, AO': 0.25
        }
    elif child == 'AB':
        return {
            'AB, AB': 1.0,
            'AA, BB': 0.5,
            'AO, BB': 0.25,
            'AA, BO': 0.25,
            'AB, AA': 0.5,
            'AB, BB': 0.5
        }
    else:
        return {}

# Streamlit 앱 인터페이스 정의
st.title('부모님의 혈액형 예측기')
st.write('자녀의 혈액형을 입력하면 가능한 부모님의 혈액형 조합을 알려드립니다.')

# 자녀 혈액형 선택
child = st.selectbox('자녀의 혈액형을 선택하세요:', ['A', 'B', 'AB', 'O'])

# 예측 버튼 클릭 시 결과 보여주기
if st.button('예측하기'):
    parent_combinations = predict_parents_blood_type(child)
    probabilities = calculate_probability(child)
    if not parent_combinations:
        st.error('올바른 혈액형을 입력해주세요.')
    else:
        st.success(f'가능한 부모님의 혈액형 조합은: {parent_combinations} 입니다.')
        st.write('각 조합의 확률은 다음과 같습니다:')
        for combination in parent_combinations:
            prob = probabilities.get(combination, '알 수 없음')
            st.write(f'{combination}: {prob * 100}%')
        
        # 부모-자녀 혈액형 관계를 가계도로 시각화
        fig, ax = plt.subplots(figsize=(12, 8))
        plt.title('부모-자녀 혈액형 관계 가계도', fontsize=16, fontproperties=fontprop if fontprop else None)

        # 부모와 자녀 노드를 그리기
        y_positions = [0.8, 0.8, 0.5]  # 부모와 자녀의 y축 위치
        x_positions = [0.3, 0.7, 0.5]  # 부모와 자녀의 x축 위치

        # 부모 노드 그리기
        for i, combination in enumerate(parent_combinations):
            parent1, parent2 = combination.split(', ')[0], combination.split(', ')[1]  # 가능한 부모 혈액형 표현
            prob = probabilities.get(combination, '알 수 없음')
            ax.text(x_positions[0], y_positions[0] - i * 0.2, f'부모 1: {parent1}', fontsize=12, color='blue', ha='center', bbox=dict(facecolor='white', edgecolor='black'), fontproperties=fontprop if fontprop else None)
            ax.text(x_positions[1], y_positions[1] - i * 0.2, f'부모 2: {parent2}', fontsize=12, color='green', ha='center', bbox=dict(facecolor='white', edgecolor='black'), fontproperties=fontprop if fontprop else None)
            # 자녀 노드 그리기
            ax.text(x_positions[2], y_positions[2] - i * 0.2, f'자녀: {child}', fontsize=12, color='red', ha='center', bbox=dict(facecolor='white', edgecolor='black'), fontproperties=fontprop if fontprop else None)
            # 부모와 자녀 연결선 그리기
            ax.plot([x_positions[0], x_positions[2]], [y_positions[0] - i * 0.2, y_positions[2] - i * 0.2], 'k-', lw=2)
            ax.plot([x_positions[1], x_positions[2]], [y_positions[1] - i * 0.2, y_positions[2] - i * 0.2], 'k-', lw=2)
            # 확률 표시
            ax.text(x_positions[2], y_positions[2] - i * 0.2 - 0.05, f'확률: {prob * 100}%', fontsize=10, color='purple', ha='center', fontproperties=fontprop if fontprop else None)

        plt.axis('off')
        st.pyplot(fig)
