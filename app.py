import datetime
import uuid  # 引入 uuid 用來產生不重複的行程 ID
import streamlit as st

st.set_page_config(
    page_title="微型 TimeTree Calendar", page_icon="📅", layout="wide"
)

# 全域 CSS
st.markdown(
    """
    <style>
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
    }
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1E293B; margin-bottom: 5px; }
    .sub-title { font-size: 1rem; color: #64748B; margin-bottom: 25px; }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown('<p class="main-title">📅 微型 TimeTree</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">隨時掌握校園各群組最新動態，點擊上方切換群組檢視</p>',
    unsafe_allow_html=True,
)

if "mylist" not in st.session_state:
    st.session_state.mylist = []


def get_color_style(group):
    styles = {
        "學生": {"bg": "#E0F2FE", "text": "#0369A1", "border": "#BAE6FD"},
        "老師": {"bg": "#DCFCE7", "text": "#15803D", "border": "#BBF7D0"},
        "家長會": {"bg": "#FEF3C7", "text": "#B45309", "border": "#FDE68A"},
        "校友會": {"bg": "#F3E8FF", "text": "#6B21A8", "border": "#E9D5FF"},
    }
    return styles.get(group, {"bg": "#F1F5F9", "text": "#334155", "border": "#E2E8F0"})


mode = st.radio(
    "👥 請選擇目前發布群組",
    ["學生", "老師", "家長會", "校友會"],
    horizontal=True,
)
st.write("---")

l, r = st.columns([2, 3], gap="large")

# --- 左側：新增行程 ---
with l:
    st.subheader("✍️ 新增行程內容")

    with st.container(border=True):
        t1 = st.text_input("行程主旨", placeholder="例如：期末成果發表會")

        d_col, t_col = st.columns(2)
        with d_col:
            t3 = st.date_input("日期選擇", datetime.date.today())
        with t_col:
            t4 = st.time_input("時間選擇")

        n1 = st.number_input(
            "🔔 行程開始前幾分鐘提醒？", min_value=0, max_value=60, value=15
        )

        st.write("")
        if st.button("➕ 將行程加入日曆"):
            if t1.strip() == "":
                st.error("請輸入行程主旨！")
            else:
                # 💡 重點 1：新增行程時，多塞一個不重複的 "id"
                st.session_state.mylist.append(
                    {
                        "id": str(uuid.uuid4()),  # 產生唯一識別碼
                        "group": mode,
                        "title": t1,
                        "date": str(t3),
                        "time": str(t4)[:5],
                        "remind": n1,
                    }
                )
                st.toast("🎉 行程新增成功！", icon="✅")
                st.rerun()

# --- 右側：行程看板與刪除功能 ---
with r:
    st.subheader("📋 行程看板")

    if not st.session_state.mylist:
        st.info("目前還沒有任何行程，快在左側建立一個吧！")
    else:
        # 💡 重點 2：遍歷行程，並建立對應的刪除按鈕
        for item in st.session_state.mylist:
            style = get_color_style(item["group"])

            # 使用一個外層 container 包裹「卡片HTML」與「刪除按鈕」
            # border=False 讓它隱形，只用來做區塊綁定
            with st.container():
                # 顯示行程卡片
                st.markdown(
                    f"""
                <div style="
                    background-color: {style['bg']};
                    color: #1E293B;
                    padding: 18px 18px 10px 18px; /* 縮減底部 padding 讓按鈕貼合 */
                    border-radius: 12px 12px 0px 0px; /* 下方直角，準備接按鈕 */
                    border-left: 6px solid {style['text']};
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="background-color: white; color: {style['text']}; padding: 2px 10px; border-radius: 20px; font-size: 0.85rem; font-weight: bold; border: 1px solid {style['border']};">
                            {item["group"]}
                        </span>
                        <span style="font-size: 0.85rem; color: #64748B;">
                            🔔 提前 {item["remind"]} 分鐘提醒
                        </span>
                    </div>
                    <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 8px; color: #0F172A;">
                        {item["title"]}
                    </div>
                    <div style="font-size: 0.9rem; color: #475569; display: flex; gap: 15px; margin-bottom: 5px;">
                        <span>📅 {item["date"]}</span>
                        <span>⏰ {item["time"]}</span>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

                # 💡 重點 3：在卡片正下方緊接著放置「刪除行程」按鈕
                # 為了避免按鈕在迴圈中發生 Key 衝突，必須指定唯一識別的 key=item["id"]
                if st.button(
                    f"🗑️ 刪除此行程", key=item["id"], type="secondary"
                ):
                    # 利用列表推導式，過濾掉點擊的那筆 ID
                    st.session_state.mylist = [
                        x for x in st.session_state.mylist if x["id"] != item["id"]
                    ]
                    st.toast("🗑️ 行程已刪除")
                    st.rerun()  # 刪除後立即重整畫面

                # 在卡片群組之間留一點空隙
                st.write("")
