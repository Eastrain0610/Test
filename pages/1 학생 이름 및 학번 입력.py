import streamlit as st
import pandas as pd
import datetime
import io
import xlsxwriter
import pytz

st.title("출석 체크")

# 현재 날짜와 시간 가져오기 (한국 시간)
korea_timezone = pytz.timezone('Asia/Seoul')

# 데이터가 없으면 세션 상태에 데이터를 저장할 초기화
if 'student_data' not in st.session_state or st.session_state.get('last_update_date') != datetime.datetime.now(korea_timezone).date():
    st.session_state['student_data'] = []
    st.session_state['last_update_date'] = datetime.datetime.now(korea_timezone).date()

# 학생 정보 입력 필드
student_number = st.text_input("학생 번호를 입력하세요:")
student_name = st.text_input("학생 이름을 입력하세요:")

if st.button("제출"):
    # 현재 날짜와 시간 기록
    timestamp = datetime.datetime.now(korea_timezone).strftime("%Y-%m-%d %H:%M:%S")
    # 학생 데이터를 세션 상태에 추가
    st.session_state['student_data'].append({
        '학생 번호': student_number,
        '학생 이름': student_name,
        '입력 시간': timestamp
    })
    st.success("학생 정보가 성공적으로 제출되었습니다!")

# 누적된 학생 데이터 표시
if st.session_state['student_data']:
    df = pd.DataFrame(st.session_state['student_data'])
    st.write("## 출석한 학생:")
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
            file_name=f'학생_데이터_{date}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

# 실시간 시간 업데이트
def update_time():
    current_time = datetime.datetime.now(korea_timezone).strftime("%Y-%m-%d %H:%M:%S")
    st.write(f"오늘 날짜: {datetime.datetime.now(korea_timezone).date()}, 현재 시간: {current_time}")

# 매초마다 시간을 업데이트하도록 Streamlit의 `st.empty()` 사용
time_placeholder = st.empty()
import time
while True:
    current_time = datetime.datetime.now(korea_timezone).strftime("%Y-%m-%d %H:%M:%S")
    time_placeholder.write(f"오늘 날짜: {datetime.datetime.now(korea_timezone).date()}, 현재 시간: {current_time}")
    time.sleep(1)