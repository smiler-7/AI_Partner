# 🤖 AI 智能伴侣

[![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python)](https://www.python.org/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-API-4A6FA5?logo=deepseek)](https://deepseek.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**AI 智能伴侣** 是一个基于大语言模型的个性化角色聊天系统。你可以为伴侣自定义昵称和性格，系统会根据设置实时生成符合人设的对话。支持多会话管理（新建、保存、加载、删除），提供类似微信的沉浸式聊天体验。

![Demo Screenshot](https://via.placeholder.com/800x400?text=Chat+Interface+Screenshot)  
*(建议替换为你的实际应用截图)*

## ✨ 功能特点

- 🎭 **个性化伴侣** – 自由设置伴侣的昵称和性格描述，AI 完全代入角色
- 💬 **流式对话** – 逐字输出，响应迅速，聊天体验更自然
- 📂 **多会话管理** – 自动保存聊天记录，支持新建、切换、删除会话
- 🎨 **简洁 UI** – 基于 Streamlit，侧边栏管理会话和配置，主区沉浸式聊天
- 🔐 **隐私安全** – 会话数据保存在本地 JSON 文件中，不上传云端
- 🌙 **角色规则约束** – 系统提示词严格限制模型行为（回复简短、无描述文字、使用 Emoji 等）

## 🛠️ 技术栈

| 类别         | 技术                                                         |
| ------------ | ------------------------------------------------------------ |
| 前端/交互    | Streamlit                                                    |
| 后端语言     | Python 3.9+                                                  |
| 大语言模型   | DeepSeek Chat API (OpenAI SDK 兼容)                          |
| 数据持久化   | JSON 文件存储（会话记录）                                    |
| 依赖管理     | pip + requirements.txt                                       |

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/smiler-7/AI_Partner.git
cd AI_Partner