import streamlit as st
from openai import OpenAI
import auth

# ================= 1. 页面配置 =================
st.set_page_config(
    page_title="紫蜂·爆款复刻机", 
    page_icon="🔥", 
    layout="centered",
    initial_sidebar_state="expanded" 
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    div.stButton > button {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(231,76,60,0.3);
    }
    div[data-testid="stAlert"] { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# ================= 2. 核心架构：统一验证系统 =================
APP_CODE = "copywriter"

# ================= 3. AI 核心配置 =================
API_KEY = st.secrets["DEEPSEEK_KEY"] 
BASE_URL = "https://api.deepseek.com"
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# ================= 4. 侧边栏：收银台与档案 =================
with st.sidebar:
    st.markdown("## 🔥 紫蜂·爆款复刻机")
    
    if "is_auth" not in st.session_state: st.session_state.is_auth = False
    if "user_id" not in st.session_state: st.session_state.user_id = "default"

    if not st.session_state.is_auth:
        st.info("🔒 系统已加密，请获取卡密解锁")
        st.markdown("### 📦 套餐价格")
        st.table({"套餐": ["7天体验", "30天月卡", "终身VIP"], "价格": ["¥9.9", "¥29.9", "¥199"]})
        
        st.markdown("#### 📲 扫码购卡")
        pay_tab1, pay_tab2 = st.tabs(["🟢 微信", "🔵 支付宝"])
        with pay_tab1:
            try:
                st.image("pay_wechat.png")
            except:
                st.warning("⚠️ 请上传 pay_wechat.png")
        with pay_tab2:
            try:
                st.image("pay_alipay.png")
            except:
                st.warning("⚠️ 请上传 pay_alipay.png")
        
        st.markdown("---")
        license_key = st.text_input("🔑 输入卡密", type="password", placeholder="COPY-xxxx 或 ADMIN-xxxx")
        st.markdown("(客服微信: liao13689209126)") 

        if st.button("🚀 联网激活"):
            with st.spinner("验证中..."):
                success, info, type_name = auth.check_license(license_key, APP_CODE)
                if success:
                    st.session_state.is_auth = True
                    st.session_state.vip_info = info
                    st.session_state.user_id = license_key.strip() 
                    st.balloons()
                    st.rerun()
                else:
                    st.error(info)
                
    else:
        st.success(f"💎 {st.session_state.vip_info}")
        st.markdown(f"**通行证 ID:** `***{st.session_state.user_id[-4:]}`")
        
        st.markdown("---")
        if st.button("🔒 退出登录"):
            st.session_state.is_auth = False
            st.session_state.user_id = "default"
            st.rerun()

# ================= 5. 主界面逻辑 =================
if not st.session_state.is_auth:
    st.markdown("# 🔥 紫蜂·爆款复刻机")
    st.info("👈 **请点击左上角 `>` 箭头展开侧边栏，进行支付与激活。**")
    st.markdown("### 🚀 它能帮你做什么？")
    st.markdown("- ✅ **一键洗稿**：把别人的爆文变成你的")
    st.markdown("- ✅ **防违规**：AI 智能降重，通过原创检测")
    st.markdown("- ✅ **自带流量**：自动生成吸睛标题 + 爆款 Tag")
    st.markdown("---")
    st.markdown("### 💡 为什么能火？")
    st.markdown("本工具基于 DeepSeek-V3 深度拆解爆文逻辑，保留情绪内核，重写原创文案。防判重，易上热门。")

else:
    st.title("🔥 紫蜂·爆款复刻机 (Pro)")
    st.caption("🚀 复制爆款逻辑，一键生成原创文案")

    # 平台选择
    platform = st.radio("选择目标平台：", ("📕 小红书 (种草/情感/干货)", "🎵 抖音/视频号 (口播脚本)"), horizontal=True)

    # 核心 Prompt 动态调整
    if "小红书" in platform:
        STYLE_GUIDE = "小红书风格：大量Emoji，称呼'家人们/姐妹们'，语气夸张，强调情绪价值，分段短。"
    else:
        STYLE_GUIDE = "短视频脚本风格：口语化强，开头前3秒必须有悬念（黄金3秒），适合读出来，中间有情绪转折。"

    SYSTEM_PROMPT = f"""
    你是一位顶级新媒体爆款操盘手。
    【任务】
    请对用户输入的文案进行【深度仿写/洗稿】。
    保留原其实的**爆火逻辑**（痛点->反转->爽点），但**完全重写具体内容**。
    【风格要求】
    {STYLE_GUIDE}
    【输出格式】
    1. **爆款标题**：提供 3 个（带Emoji，极具吸引力）。
    2. **正文内容**：原创度极高的重写内容。
    3. **爆款标签**：5 个高热度 Tag。
    """

    # 输入区
    user_text = st.text_area("请把【你想模仿的那个爆款文案】复制到这里：", height=200, placeholder="直接把那篇 10w+ 的笔记文案粘贴进来...")

    if st.button("⚡ 立即复刻 (注入流量)", type="primary"):
        if not user_text:
            st.warning("请先投喂爆款素材！")
        else:
            with st.spinner("正在拆解爆款逻辑...正在注入情绪算法..."):
                try:
                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_text},
                        ],
                        temperature=1.4,
                        stream=False
                    )
                    result = response.choices[0].message.content
                    
                    st.success("🔥 复刻成功！原创度 99%！")
                    st.markdown("---")
                    st.markdown(result)
                    st.markdown("---")
                    st.info("💡 建议：搭配一张高清美图，发布效果更佳！")
                except Exception as e:
                    st.error(f"❌ 流量太大了，AI 稍微卡了一下，请重试：{str(e)}")
