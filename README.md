# 紫蜂·爆款复刻机 Pro

基于 DeepSeek-V3 的爆款文案智能复刻工具，一键生成原创爆款内容。

## 功能特性

- ⚡ 一键洗稿：把别人的爆文变成你的
- 🛡️ 防违规：AI 智能降重，通过原创检测
- 🎯 自带流量：自动生成吸睛标题 + 爆款 Tag
- 📱 多平台支持：小红书、抖音/视频号

## 本地运行

### 1. 创建虚拟环境

```bash
python -m venv venv
```

### 2. 激活虚拟环境

Windows:
```bash
.\venv\Scripts\Activate.ps1
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置API密钥

在 `.streamlit/secrets.toml` 中填入你的API密钥：

```toml
DEEPSEEK_KEY = "your_deepseek_api_key_here"
GITHUB_TOKEN = "your_github_token_here"
GIST_ID = "your_gist_id_here"
```

### 5. 启动应用

```bash
streamlit run app.py
```

## 部署到 Streamlit Cloud

### 使用 Streamlit Community Cloud (share.streamlit.io)

Streamlit Cloud 会自动读取你的 secrets.toml 文件中的配置，无需在代码中硬编码密码。

1. 将代码推送到 GitHub
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 点击 "New app"
4. 连接你的 GitHub 仓库
5. 在 "Secrets" 部分添加以下配置：

```
DEEPSEEK_KEY=your_deepseek_api_key_here
GITHUB_TOKEN=your_github_token_here
GIST_ID=your_gist_id_here
```

6. 点击 "Deploy"

## 使用方法

1. 启动应用后，在侧边栏输入卡密解锁
2. 选择目标平台（小红书或抖音）
3. 将爆款文案粘贴到输入框
4. 点击"立即复刻"按钮
5. 系统将自动生成原创标题、正文和标签

## 安全说明

- ⚠️ **不要**将 `.streamlit/secrets.toml` 提交到 Git
- ⚠️ **不要**在代码中硬编码任何密钥或密码
- ✅ 使用 `.gitignore` 文件排除敏感文件
- ✅ 在 Streamlit Cloud 中通过 Secrets 管理配置

## 技术栈

- Streamlit - Web应用框架
- DeepSeek API - AI文案生成
- OpenAI SDK - API客户端

## 许可证

MIT License
