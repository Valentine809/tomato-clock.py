import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ---------- 初始化 session state ----------
if "running" not in st.session_state:
    st.session_state.running = False      # 是否正在运行
if "total" not in st.session_state:
    st.session_state.total = 25 * 60      # 总秒数，默认25分钟
if "remaining" not in st.session_state:
    st.session_state.remaining = 25 * 60  # 剩余秒数

# ---------- 页面配置 ----------
st.set_page_config(page_title="🍅 极简番茄钟", layout="centered")

# ---------- 背景颜色根据剩余时间渐变 ----------
# ratio=1 时红色，ratio=0 时绿色
def set_background_color(ratio):
    hue = int(ratio * 120)  # 0 = 红, 120 = 绿
    css = f"""
    <style>
    .stApp {{
        background-color: hsl({hue}, 70%, 50%);
        transition: background-color 1s linear;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---------- 标题 ----------
st.title("🍅 极简番茄钟")

# ---------- 时间调节滑块（1~60分钟） ----------
minutes = st.slider(
    "设置分钟数", 1, 60, 25,
    disabled=st.session_state.running   # 运行中禁止调整
)

# 如果滑块被修改了，就同步更新总时间和剩余时间
if minutes * 60 != st.session_state.total:
    st.session_state.total = minutes * 60
    st.session_state.remaining = minutes * 60

# ---------- 显示剩余时间 ----------
mm = st.session_state.remaining // 60
ss = st.session_state.remaining % 60
st.markdown(f"## {mm:02d}:{ss:02d}", unsafe_allow_html=True)

# ---------- 进度条 ----------
ratio = st.session_state.remaining / st.session_state.total if st.session_state.total else 0
st.progress(ratio)

# ---------- 更新背景色 ----------
set_background_color(ratio)

# ---------- 控制按钮 ----------
col1, col2 = st.columns(2)

with col1:
    if not st.session_state.running:
        # 显示“开始”
        if st.button("▶ 开始", use_container_width=True):
            st.session_state.running = True
            # 如果已经倒到0，重新开始
            if st.session_state.remaining <= 0:
                st.session_state.remaining = st.session_state.total
            st.rerun()
    else:
        # 显示“暂停”
        if st.button("⏸ 暂停", use_container_width=True):
            st.session_state.running = False
            st.rerun()

with col2:
    # 重置按钮
    if st.button("↺ 重置", use_container_width=True):
        st.session_state.running = False
        st.session_state.remaining = st.session_state.total
        st.rerun()

# ---------- 核心倒计时逻辑 ----------
if st.session_state.running:
    # 每秒自动刷新页面
    st_autorefresh(interval=1000, key="timer_refresh")

    # 如果还有剩余时间，就减一秒
    if st.session_state.remaining > 0:
        st.session_state.remaining -= 1
    else:
        # 倒计时结束，自动停下
        st.session_state.running = False