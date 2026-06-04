# 会话管理类：负责会话的生成、保存、加载、删除等操作

import os
import json
from datetime import datetime
from .constants import SESSIONS_DIR

class SessionManager:
    def __init__(self):
        self.sessions_dir = SESSIONS_DIR
        self._ensure_dir()

    def _ensure_dir(self):
        """确保会话目录存在，若不存在则创建"""
        if not os.path.exists(self.sessions_dir):
            os.mkdir(self.sessions_dir)

    @staticmethod
    def generate_session_name():
        """生成会话标识的函数（原注释保留）"""
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def save_session(self, session_name, data):
        """保存会话信息的函数
        Args:
            session_name: 会话名称
            data: 包含 nick_name, nature, current_session, messages 的字典
        """
        # session目录不存在，则创建新目录（已由_ensure_dir保证）
        file_path = os.path.join(self.sessions_dir, f"{session_name}.json")
        # 保存会话数据
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_sessions(self):
        """加载所有的会话信息（返回会话名称列表）"""
        session_list = []
        # 加载sessions目录下的所有会话信息
        if os.path.exists(self.sessions_dir):
            file_list = os.listdir(self.sessions_dir)
            for filename in file_list:
                if filename.endswith(".json"):
                    session_list.append(filename[0:-5])
        session_list.sort(reverse=True)  # 排序,reverse=True:代表倒序排序
        return session_list

    def load_session(self, session_name):
        """加载指定会话信息，返回数据字典；若失败返回None"""
        try:
            file_path = os.path.join(self.sessions_dir, f"{session_name}.json")
            # 加载sessions目录下的所有会话信息
            if os.path.exists(file_path):
                # 读取会话数据
                with open(file_path, "r", encoding="utf-8") as f:
                    session_data = json.load(f)
                return session_data
        except Exception as e:
            # 异常由调用方处理，此处返回None
            return None

    def delete_session(self, session_name):
        """删除会话信息，返回是否成功"""
        try:
            file_path = os.path.join(self.sessions_dir, f"{session_name}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
        except Exception as e:
            return False
        return False