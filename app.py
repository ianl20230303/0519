import streamlit as st
import datetime


st.set_page_config(page_title="微型 TimeTree", layout="wide")

with st.sidebar:
    st.write("###  行事曆群組")
    st.radio("選擇群組", ["工作", "家庭"])

col_left, col_right = st.columns(2, gap="large")

with col_left: 
    st.write("###  新增區") 
    st.button("按鈕放左邊")
    
    with st.container(border=True): 
        st.write(" 標題：開學典禮") 
        st.write(" 時間：09:00")
        
        title = st.text_input("行程主旨",placeholder="請填寫會議名稱...")
        
        my_color = st.color_picker("挑選辨識顏色","#1A73E8")

    view = st.segmented_control("檢視模式",["月視角", "週視角"],default="月視角")
    
    tag = st.pills("行程屬性",["#工作", "#家庭", "#緊急"])

    note = st.text_area("行程備忘錄 / 詳細說明")
    

        
with col_right: 
    st.write("###  設定區") 
    st.button("控制項放右邊")
    
    st.write("###  看板區") 
    st.info("主要行程訊息放這邊")

    with st.expander("查看進階提醒參數設定"):
        st.write("這裡是發信伺服器的底層設定...")
    
    today = st.date_input("選擇日期",datetime.date.today())
    
    meeting_time = st.time_input("選擇時間")

    is_open = st.toggle("開啟 24H 郵件自動發信通知",value=True)

    mins = st.number_input("行程開始前幾分鐘提醒？",min_value=0, max_value=60,value=15)
    
    @st.dialog("系統公告")
    def show_alert():
        st.write("本週作業請確認 requirements.txt 有正確設定！")
        if st.button("查看公告"): show_alert()



st.write("上面是大標題")
st.divider()
st.write("下面是內容區塊")

st.button("按鈕 A")
st.write("")  # 塞入一行空白間距
st.button("按鈕 B")

with st.popover("快速進階篩選"):
    st.checkbox("隱藏已過期行程")
