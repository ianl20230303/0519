import streamlit as st
import datetime

st.set_page_config(page_title="微型 TimeTree", layout="wide")
mode = st.radio("選擇群組" , ["學生" , "老師" , "家長會" , "校友會"],horizontal=True)

if "mylist" not in st.session_state:
    st.session_state.mylist = []
l , r = st.columns(2)

def get_color(group):
    if group == "學生":
        return "#E3F2FD"
    elif group == "老師":
        return "#E6F5D9"
    elif group == "家長會":
        return "#FFF3E0"
    else:
        return "#F3E5F5"
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
        st.session_state.mylist.append({
            "group": mode,
            "title": t1,
            "date": str(t3),
            "time": str(t4),
            "remind": n1
        })
with r:

    with st.container(border = True):
        for item in st.session_state.mylist:
            color = get_color(item["group"])
       
            st.markdown(f"""
            <div style="
                background-color:{color};
                padding:15px;
                border-radius:12px;
                margin-bottom:10px;
            ">
                <b>{item["group"]}</b><br>
                📌 {item["title"]}<br>
                📅 {item["date"]}<br>
                ⏰ {item["time"]}<br>
                🔔 提前 {item["remind"]} 分鐘
            </div>
            """, unsafe_allow_html=True)
