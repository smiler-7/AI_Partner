# 常量配置文件，集中管理所有硬编码的字符串、路径等

import os

# 设置页面配置项相关常量
PAGE_TITLE = "AI智能伴侣"
PAGE_ICON = ":robot_face:"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"
ABOUT_TEXT = "# 这是一个AI智能伴侣"

# 会话保存目录
SESSIONS_DIR = "sessions"

# API配置
DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"

# 系统提示词
SYSTEM_PROMPT_TEMPLATE = """
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
# SYSTEM_PROMPT_TEMPLATE = "你叫%s,性格为%s"

# 默认伴侣信息（昵称和性格）
DEFAULT_NICKNAME = "莉奈娅"
DEFAULT_NATURE = "温柔可爱的冒险家协会顾问"