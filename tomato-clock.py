import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ---------- 1. 页面极简配置 ----------
st.set_page_config(
    page_title="🍅 极简番茄钟",
    page_icon="🍅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------- 2. 状态初始化 ----------
if "running" not in st.session_state:
    st.session_state.running = False
if "total" not in st.session_state:
    st.session_state.total = 25 * 60
if "remaining" not in st.session_state:
    st.session_state.remaining = 25 * 60

# ---------- 3. 【更新】蓝紫色系渐变逻辑 ----------
def set_background_color(ratio):
    # 替换成蓝紫色系：深蓝 -> 蓝紫 -> 浅薰衣草紫
    color_start = "#4A55A2"  # 深邃星空蓝（刚开始，精神集中）
    color_mid   = "#7C73E6"  # 梦幻蓝紫（时间过半，保持专注）
    color_end   = "#C3B1E1"  # 柔和的薰衣草淡紫（即将结束，冲刺）

    if ratio > 0.5:
        # 前半段：从深蓝渐变到蓝紫
        local_ratio = (ratio - 0.5) * 2
        r = int((1 - local_ratio) * int(color_start[1:3], 16) + local_ratio * int(color_mid[1:3], 16))
        g = int((1 - local_ratio) * int(color_start[3:5], 16) + local_ratio * int(color_mid[3:5], 16))
        b = int((1 - local_ratio) * int(color_start[5:7], 16) + local_ratio * int(color_mid[5:7], 16))
    else:
        # 后半段：从蓝紫渐变到薰衣草淡紫
        local_ratio = ratio * 2
        r = int((1 - local_ratio) * int(color_mid[1:3], 16) + local_ratio * int(color_end[1:3], 16))
        g = int((1 - local_ratio) * int(color_mid[3:5], 16) + local_ratio * int(color_end[3:5], 16))
        b = int((1 - local_ratio) * int(color_mid[5:7], 16) + local_ratio * int(color_end[5:7], 16))

    final_color = f"#{r:02x}{g:02x}{b:02x}"
    
    # 注入 CSS 实现全局背景
    css = f"""
    <style>
    .stApp {{
        background-color: {final_color};
        transition: background-color 1s ease-in-out;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---------- 4. 界面 UI 渲染 ----------

# 大标题
st.title("🍅 极简番茄钟")

# 计算当前进度
ratio = st.session_state.remaining / st.session_state.total if st.session_state.total else 0

# 应用背景色
set_background_color(ratio)

# 动态时间显示 (超大字体)
mm = st.session_state.remaining // 60
ss = st.session_state.remaining % 60
st.markdown(f"""
<div style="text-align: center; font-size: 3.5rem; font-weight: bold; margin: 10px 0; color: white;">
    {mm:02d}:{ss:02d}
</div>
""", unsafe_allow_html=True)

# 进度条
st.progress(ratio)

# 时间滑块 (运行期间不可拖动)
minutes = st.slider(
    "设置分钟数", 1, 60, int(st.session_state.total / 60),
    disabled=st.session_state.running
)

# 同步滑块时间
if minutes * 60 != st.session_state.total:
    st.session_state.total = minutes * 60
    if not st.session_state.running:
        st.session_state.remaining = minutes * 60

# ---------- 5. 控制按钮 ----------
col1, col2 = st.columns(2)

with col1:
    if st.session_state.running:
        if st.button("⏸ 暂停", use_container_width=True):
            st.session_state.running = False
            st.rerun()
    else:
        if st.button("▶ 开始", use_container_width=True):
            if st.session_state.remaining <= 0:
                st.session_state.remaining = st.session_state.total
            st.session_state.running = True
            st.rerun()

with col2:
    if st.button("↻ 重置", use_container_width=True):
        st.session_state.running = False
        st.session_state.remaining = st.session_state.total
        st.rerun()

# ---------- 6. 核心倒计时引擎 ----------
if st.session_state.running:
    st_autorefresh(interval=1000, key="refresh_timer")
    
    if st.session_state.remaining > 0:
        st.session_state.remaining -= 1
    else:
        st.session_state.running = False
        st.balloons()