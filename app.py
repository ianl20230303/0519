import streamlit as st
import datetime

st.set_page_config(page_title="微型 TimeTree", layout="wide", page_icon="📅")

# 頂部標題與風格
st.title("📅 微型 TimeTree 行程管理")
mode = st.radio("選擇群組" , ["學生" , "老師" , "家長會" , "校友會"], horizontal=True)

# 使用字典結構，讓每個群組有獨立的行程清單
if "group_events" not in st.session_state:
    st.session_state.group_events = {
        "學生": [], "老師": [], "家長會": [], "校友會": []
    }

l, r = st.columns([1, 1.2]) # 微調左右比例，給右邊多一點空間

with l:
    st.subheader("➕ 新增行程")
    # 用 container 包起來讓左側輸入框更有整體感
    with st.container(border=True):
        t1 = st.text_input("行程主旨", placeholder="例如：期末考、班會...")
        t3 = st.date_input("日期選擇", datetime.date.today())
        t4 = st.time_input("時間選擇")
        n1 = st.number_input(
            "行程開始前幾分鐘提醒？",
            min_value=0, max_value=60,
            value=15
        )
        
        # 新增按鈕加上顏色與寬度優化
        if st.button("新增行程", type="primary", use_container_width=True):
            if t1.strip() == "":
                st.error("請輸入行程主旨！")
            else:
                # 儲存為字典結構，方便後續美化排版
                event_data = {
                    "title": t1,
                    "date": t3.strftime("%Y-%m-%d"),
                    "time": t4.strftime("%H:%M"),
                    "remind": n1
                }
                st.session_state.group_events[mode].append(event_data)
                st.toast(f"✅ 已成功加入【{mode}】群組！")
                st.rerun()

with r:
    st.subheader(f"📋 【{mode}】行程列表")
    
    current_events = st.session_state.group_events[mode]
    
    if not current_events:
        st.info("目前尚無行程，快在左側新增一個吧！")
    else:
        # 依據日期與時間排序行程（讓越早的排在越前面）
        sorted_events = sorted(current_events, key=lambda x: (x['date'], x['time']))
        
        for idx, event in enumerate(sorted_events):
            # 使用 border=True 創造類似卡片（Card）的效果
            with st.container(border=True):
                # 標題與時間排版
                col_title, col_time = st.columns([3, 1])
                with col_title:
                    st.markdown(f"### 📌 {event['title']}")
                with col_time:
                    # 顯示倒數提醒的小標籤
                    st.caption(f"🔔 {event['remind']} 分鐘前提醒")
                
                # 具體時間細節
                st.markdown(f"📅 **日期：** {event['date']} | ⏰ **時間：** {event['time']}")
                
                # 加一個小小的刪除按鈕（選配，點擊可刪除該行程）
                if st.button("🗑️ 刪除", key=f"del_{idx}", size="small"):
                    st.session_state.group_events[mode].remove(event)
                    st.rerun()
