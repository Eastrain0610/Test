import streamlit as st
import pandas as pd
import datetime
import io
import xlsxwriter
import pytz
import time

st.title("유연관계 체크")

# 현재 날짜와 시간 가져오기 (한국 시간)
korea_timezone = pytz.timezone('Asia/Seoul')

# 데이터가 없으면 세션 상태에 데이터를 저장할 초기화
if 'relationship_data' not in st.session_state or st.session_state.get('last_update_date') != datetime.datetime.now(korea_timezone).date():
    st.session_state['relationship_data'] = []
    st.session_state['last_update_date'] = datetime.datetime.now(korea_timezone).date()

# 유연관계 정보 입력 필드
animal_common_name = st.text_input("비교할 동물의 이름을 입력하세요:")
animal_name = st.text_input("비교할 동물의 학명을 입력하세요:")
animal_sequence = st.text_area("비교할 동물의 사이토크롬 C 서열을 입력하세요:")

if st.button("제출"):
    # 현재 날짜와 시간 기록
    timestamp = datetime.datetime.now(korea_timezone).strftime("%Y-%m-%d %H:%M:%S")
    # 유연관계 데이터를 세션 상태에 추가
    st.session_state['relationship_data'].append({
        '동물의 이름': animal_common_name,
        '학명': animal_name,
        '염기 서열': animal_sequence,
        '입력 시간': timestamp
    })
    st.success("유연관계 정보가 성공적으로 제출되었습니다!")

# 누적된 유연관계 데이터 표시
if st.session_state['relationship_data']:
    df = pd.DataFrame(st.session_state['relationship_data'])
    st.write("## 입력된 동물 정보:")
    st.dataframe(df)

    # 날짜에 따른 데이터 필터링
    df['입력 날짜'] = pd.to_datetime(df['입력 시간']).dt.date
    unique_dates = df['입력 날짜'].unique()

    # 데이터를 엑셀 파일로 다운로드할 옵션 제공
    @st.cache_data
    def convert_df_to_excel(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        return output.getvalue()

    for date in unique_dates:
        date_data = df[df['입력 날짜'] == date]
        excel_data = convert_df_to_excel(date_data)
        st.download_button(
            label=f"{date}의 데이터를 엑셀 파일로 다운로드",
            data=excel_data,
            file_name=f'유연관계_데이터_{date}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

# 실시간 시간 업데이트
time_placeholder = st.empty()

while True:
    current_time = datetime.datetime.now(korea_timezone).strftime("%Y-%m-%d %H:%M:%S")
    time_placeholder.write(f"오늘 날짜: {datetime.datetime.now(korea_timezone).date()}, 현재 시간: {current_time}")
    time.sleep(1)