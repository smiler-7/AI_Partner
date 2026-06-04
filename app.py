# 主程序入口，包含Streamlit UI和状态管理

import streamlit as st
from utils.constants import *
from utils.session_manager import SessionManager
from utils.ai_client import AIClient

# ----------------------------- 页面配置 -----------------------------
# 设置页面配置项
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE,
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': ABOUT_TEXT
    }
)

# logo
st.logo("resources/Columbina.png")

# ----------------------------- 初始化session_state -----------------------------
def init_session_state():
    """初始化Streamlit会话状态中的各项变量"""
    # 初始化聊天信息
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # 昵称
    if "nick_name" not in st.session_state:
        st.session_state.nick_name = DEFAULT_NICKNAME
    # 性格
    if "nature" not in st.session_state:
        st.session_state.nature = DEFAULT_NATURE
    # 会话标识
    if "current_session" not in st.session_state:
        st.session_state.current_session = SessionManager.generate_session_name()
    # 会话管理器实例
    if "session_manager" not in st.session_state:
        st.session_state.session_manager = SessionManager()
    # AI客户端实例
    if "ai_client" not in st.session_state:
        st.session_state.ai_client = AIClient()

init_session_state()
sm = st.session_state.session_manager
ai_client = st.session_state.ai_client

# ----------------------------- 辅助函数 -----------------------------
def save_current_session():
    """保存当前会话到文件"""
    # 构建新的会话对象
    session_data = {
        "nick_name": st.session_state.nick_name,
        "nature": st.session_state.nature,
        "current_session": st.session_state.current_session,
        "messages": st.session_state.messages
    }
    sm.save_session(st.session_state.current_session, session_data)

def load_session(session_name):
    """加载指定会话到当前状态"""
    data = sm.load_session(session_name)
    if data:
        st.session_state.messages = data["messages"]
        st.session_state.nick_name = data["nick_name"]
        st.session_state.nature = data["nature"]
        st.session_state.current_session = session_name
    else:
        st.error("加载会话失败!")

def delete_session(session_name):
    """删除会话文件，如果删除的是当前会话则重置"""
    if sm.delete_session(session_name):
        # 如果删除当前会话，则更新消息列表
        if session_name == st.session_state.current_session:
            st.session_state.messages = []
            st.session_state.current_session = SessionManager.generate_session_name()
    else:
        st.error("删除会话失败!")

def build_system_prompt():
    """根据当前伴侣昵称和性格构建系统提示词"""
    return SYSTEM_PROMPT_TEMPLATE % (st.session_state.nick_name, st.session_state.nature)

# ----------------------------- 侧边栏UI -----------------------------
with st.sidebar:
    # 会话管理
    st.subheader("会话管理")

    # 新建会话按钮
    if st.button("新建会话", width="stretch", icon="✏️"):
        # 1.保存当前会话信息
        save_current_session()
        # 2.创建新会话
        if st.session_state.messages:  # 如果聊天消息非空，则保存
            st.session_state.messages = []
            st.session_state.current_session = SessionManager.generate_session_name()
            save_current_session()
            st.rerun()  # 重新运行页面

    # 会话历史列表
    st.text("历史会话")
    with st.container(height=150):
        session_list = sm.load_sessions()
        for session in session_list:
            col1, col2 = st.columns([4, 1])
            with col1:
                # 加载指定的会话信息
                btn_type = "primary" if session == st.session_state.current_session else "secondary"
                if st.button(session, width="stretch", icon="❤️", key=f"load_{session}", type=btn_type):
                    load_session(session)
                    st.rerun()
            with col2:
                # 删除指定会话信息
                if st.button("", width="stretch", icon="✖️", key=f"delete_{session}"):
                    delete_session(session)
                    st.rerun()

    # 分割线
    st.divider()

    # 伴侣信息编辑
    st.subheader("伴侣信息")
    nick_name = st.text_input("昵称", placeholder="请输入昵称", value=st.session_state.nick_name)
    nature = st.text_input("性格", placeholder="请输入性格", value=st.session_state.nature)

    # 保存昵称和性格
    if nick_name:
        st.session_state.nick_name = nick_name
    if nature:
        st.session_state.nature = nature

# ----------------------------- 主聊天区 -----------------------------
# 大标题
st.title(PAGE_TITLE)

# 显示当前会话名称
st.text(f"会话名称:{st.session_state.current_session}")

# 显示历史聊天记录
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 消息输入框
prompt = st.chat_input("请输入你的问题")
if prompt:
    # 显示用户消息
    st.chat_message("user").write(prompt)
    print("----->调用AI大模型，提示词:", prompt)

    # 保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 构建系统提示词并调用AI（流式）
    system_prompt = build_system_prompt()
    response_stream = ai_client.stream_chat(system_prompt, st.session_state.messages)

    # 输出大模型返回的结果(流式输出的解析方式)
    response_message = st.empty()   # 创建一个空的消息框，用于显示大模型返回的结果
    full_response = ""
    for chunk in response_stream:
        full_response += chunk
        response_message.chat_message("assistant").write(full_response)

    # 保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    # 保存会话信息
    save_current_session()