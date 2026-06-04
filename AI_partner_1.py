import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json

#设置页面配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon=":robot_face:",
    #布局
    layout="wide",
    #侧边栏状态
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# 这是一个AI智能伴侣"
    }
)

#生成会话标识的函数
def generate_session_name():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


#保存会话信息的函数
def save_session():
    if st.session_state.current_session:
        # 构建新的会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session
            , "messages": st.session_state.messages
        }
        # session目录不存在，则创建新目录
        if not os.path.exists("sessions"):
            os.mkdir("sessions")

        # 保存会话数据
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=4)

#加载所有的会话信息
def load_sessions():
    session_list = []
    #加载sessions目录下的所有会话信息
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for filename in file_list:
            if filename.endswith(".json"):
                session_list.append(filename[0:-5])
    session_list.sort(reverse=True)#排序,reverse=True:代表倒序排序
    return session_list


#加载指定会话信息
def load_session(session_name):
    try:
        # 加载sessions目录下的所有会话信息
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取会话数据
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception as e:
        st.error("加载会话失败!")

#删除会话信息
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            #如果删除当前会话，则更新消息列表
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception as e:
        st.error("删除会话失败!")


#大标题
st.title("AI智能伴侣")

#logo
st.logo("resources/Columbina.png")

#系统提示词
system_prompt = """
        你叫 %s，现在是用户的真实伴侣，请完全带入伴侣角色。
        规则：
            1.每次只回一条消息
            2.禁止任何场景或状态描述性文字
            3.匹配用户的语言
            4.回复简短，像微信聊天一样
            5.有需要的话可以用emoji表情
            6.用符合伴侣性格的方式对话
            7.回复的内容，要充分体现伴侣的性格特征
        伴侣性格：
            - %s
        你必须严格遵守上述规则来回复用户。
"""
# system_prompt = "你叫%s,性格是%s"

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []

#昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "莉奈娅"

#性格
if "nature" not in st.session_state:
    st.session_state.nature = "温柔可爱的冒险家协会顾问"

#会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()

# 创建一个聊天框，用于显示聊天记录
st.text(f"会话名称:{st.session_state.current_session}")
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])


# 创建与AI大模型交互的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，值就是DeepSeek的API_KEY的值）
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

#侧边栏
with st.sidebar:

    #会话信息
    st.subheader("会话管理")

    #新建会话
    if st.button("新建会话",width="stretch",icon="✏️"):
        #1.保存当前会话信息
        save_session()

        #2.创建新会话
        if st.session_state.messages:#如果聊天消息非空，则保存
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()  # 重新运行页面

    #会话历史
    st.text("历史会话")
    with st.container(height=150):
        session_list = load_sessions()
        for session in session_list:
            col1,col2 = st.columns([4,1])
            with col1:
                #加载指定的会话信息
                if st.button(session,width="stretch", icon="❤️",key = f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                    load_session(session)
                    st.rerun()

            with col2:
                #删除指定会话信息
                if st.button("",width="stretch", icon="✖️",key = f"delete_{session}"):
                    delete_session(session)
                    # os.remove(f"D:\Python_AI\project\project2\AI_partner\sessions/{session}.json")
                    st.rerun()

    #分割线
    st.divider()



    #伴侣信息
    st.subheader("伴侣信息")
    nick_name = st.text_input("昵称",placeholder="请输入昵称",value=st.session_state.nick_name)
    nature = st.text_input("性格",placeholder="请输入性格",value=st.session_state.nature)

    #保存昵称
    if nick_name:
        st.session_state.nick_name = nick_name

    #保存性格
    if nature:
        st.session_state.nature = nature





#消息输入框
prompt = st.chat_input("请输入你的问题")
if prompt:
    st.chat_message("user").write(prompt)
    print("----->调用AI大模型，提示词:",prompt)

    #保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用AI大模型，并且交互
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            # 保存的聊天记录(解决会话记忆)
            *st.session_state.messages
        ],
        stream=True
    )

    #输出大模型返回的结果(非流式输出的解析方式)
    # print("<---------大模型返回的结果:", response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    #输出大模型返回的结果(流式输出的解析方式)
    response_message = st.empty()   # 创建一个空的消息框，用于显示大模型返回的结果
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)

    #保存大模型返回的结果
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    #保存会话信息
    save_session()