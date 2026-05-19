import streamlit as st
import datetime

st.set_page_config(page_title="微型 TimeTree", layout="wide")
mode = st.radio("選擇群組" , ["學生" , "老師" , "家長會" , "校友會"],horizontal=True)

if "mylist" not in st.session_state:
    st.session_state.mylist = []
l , r = st.columns(2)

with l:
    t1=st.text_input("行程主旨")
    t3=st.date_input("日期選擇" , datetime.date.today())
    t4=st.time_input("時間選擇")
    n1= st.number_input(
     "行程開始前幾分鐘提醒？",
     min_value=0, max_value=60,
     value=15
    )
    if st.button("新增行程"):
        st.session_state.mylist.append(f"行程主旨:{t1},日期選擇:{t3},時間選擇:{t4},幾分鐘前提醒:{n1}")
with r:
    for i in st.session_state.mylist:
        st.write(i)
