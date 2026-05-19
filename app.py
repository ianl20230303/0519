import datetime
import streamlit as st

# 1. 網頁初始化與設定（更換為更精緻的 icon）
st.set_page_config(
    page_title="微型 TimeTree Calendar", page_icon="📅", layout="wide"
)

# 套用全域自訂 CSS，讓按鈕與文字輸入框更有質感
st.markdown(
    """
    <style>
    /* 調整主要按鈕的寬度與懸停效果 */
    .stButton > button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #4338CA;
        color: white;
        transform: translateY(-1px);
    }
    /* 讓側邊欄或標題字體更精緻 */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 25px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 頂部精緻標題區
st.markdown('<p class="main-title">📅 微型 TimeTree</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">隨時掌握校園各群組最新動態，點擊上方切換群組檢視</p>',
    unsafe_allow_html=True,
)

# 2. 初始化行程清單
if "mylist" not in st.session_state:
    st.session_state.mylist = []


# 3. 調整群組顏色配置（使用更高質感的粉彩與莫蘭迪色系，並加上文字顏色提升對比）
def get_color_style(group):
    styles = {
        "學生": {"bg": "#E0F2FE", "text": "#0369A1", "border": "#BAE6FD"},
        "老師": {"bg": "#DCFCE7", "text": "#15803D", "border": "#BBF7D0"},
        "家長會": {"bg": "#FEF3C7", "text": "#B45309", "border": "#FDE68A"},
        "校友會": {"bg": "#F3E8FF", "text": "#6B21A8", "border": "#E9D5FF"},
    }
    return styles.get(group, {"bg": "#F1F5F9", "text": "#334155", "border": "#E2E8F0"})


# 群組選擇區加點小巧思
mode = st.radio(
    "👥 請選擇目前發布群組",
    ["學生", "老師", "家長會", "校友會"],
    horizontal=True,
)
st.write("---")

# 4. 左右版面配置（調整比例為 4:6，讓右側行程展示區更寬敞舒適）
l, r = st.columns([2, 3], gap="large")

with l:
    st.subheader("✍️ 新增行程內容")

    # 使用容器包裹輸入框，視覺上更有區塊感
    with st.container(border=True):
        t1 = st.text_input("行程主旨", placeholder="例如：期末成果發表會")

        # 將日期與時間並排，節省垂直空間，看起來更緊湊
        d_col, t_col = st.columns(2)
        with d_col:
            t3 = st.date_input("日期選擇", datetime.date.today())
        with t_col:
            t4 = st.time_input("時間選擇")

        n1 = st.number_input(
            "🔔 行程開始前幾分鐘提醒？", min_value=0, max_value=60, value=15
        )

        st.write("")  # 增加一點留白
        if st.button("➕ 將行程加入日曆"):
            if t1.strip() == "":
                st.error("請輸入行程主旨！")
            else:
                st.session_state.mylist.append(
                    {
                        "group": mode,
                        "title": t1,
                        "date": str(t3),
                        "time": str(t4)[:5],  # 只取到 12:30，去掉秒數更乾淨
                        "remind": n1,
                    }
                )
                st.toast("🎉 行程新增成功！", icon="✅")
                st.rerun()  # 立即重新整理，讓右側畫面同步

with r:
    st.subheader("📋 行程看板")

    if not st.session_state.mylist:
        # 當沒有行程時，顯示好看的空白狀態提示
        st.info("目前還沒有任何行程，快在左側建立一個吧！")
    else:
        # 行程卡片清單
        for item in st.session_state.mylist:
            style = get_color_style(item["group"])

            st.markdown(
                f"""
            <div style="
                background-color: {style['bg']};
                color: #1E293B;
                padding: 18px;
                border-radius: 12px;
                border-left: 6px solid {style['text']};
                margin-bottom: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.04);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="
                        background-color: white; 
                        color: {style['text']}; 
                        padding: 2px 10px; 
                        border-radius: 20px; 
                        font-size: 0.85rem; 
                        font-weight: bold;
                        border: 1px solid {style['border']};
                    ">
                        {item["group"]}
                    </span>
                    <span style="font-size: 0.85rem; color: #64748B;">
                        🔔 提前 {item["remind"]} 分鐘提醒
                    </span>
                </div>
                <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 8px; color: #0F172A;">
                    {item["title"]}
                </div>
                <div style="font-size: 0.9rem; color: #475569; display: flex; gap: 15px;">
                    <span>📅 {item["date"]}</span>
                    <span>⏰ {item["time"]}</span>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
