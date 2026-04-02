# 法语学习AI助手研究平台

## 项目简介

这是一个基于Web的法语学习聊天助手平台，用于研究不同AI交互风格对学习效果的影响。

## 技术栈

- 前端：Vue 3 + Vite + Pinia
- 后端：Flask 3 + SQLAlchemy
- 数据库：SQLite
- LLM：硅基流动 API

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 部署

1. 构建前端：`npm run build`
2. 配置Nginx和Gunicorn
3. 设置环境变量
4. 启动服务

## 环境变量

- `LLM_API_KEY`: 硅基流动API密钥
- `WECHAT_APP_ID_1`, `WECHAT_APP_SECRET_1`: 微信测试号配置
- `SMTP_USER`, `SMTP_PASSWORD`: 邮件发送配置
