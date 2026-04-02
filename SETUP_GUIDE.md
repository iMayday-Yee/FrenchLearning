# 法语学习助手 - 环境配置和启动手册

## 项目概述

这是一个基于 Vue 3 + Flask 的法语学习 AI 助手研究平台，支持多用户、多组交互风格、AI 对话、跟读录音等功能。

## 系统要求

- **操作系统**：Linux / macOS / Windows（WSL2）
- **Python**：3.9+
- **Node.js**：16+
- **FFmpeg**：用于音频处理

## 环境准备

### 1. 系统依赖安装

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nodejs npm ffmpeg
```

#### macOS
```bash
brew install python3 node ffmpeg
```

#### Windows (WSL2)
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nodejs npm ffmpeg
```

### 2. API 密钥配置

在 `backend/config.py` 中配置以下密钥：

| 密钥 | 来源 | 说明 |
|------|------|------|
| `LLM_API_KEY` | SiliconFlow | LLM API 密钥 |
| `LLM_MODEL` | SiliconFlow | 使用的模型 ID |
| `WECHAT_APPID` | 微信公众号 | 微信集成（可选） |
| `WECHAT_APPSECRET` | 微信公众号 | 微信集成（可选） |
| `SMTP_EMAIL` | 邮箱服务商 | 邮件通知（可选） |
| `SMTP_PASSWORD` | 邮箱服务商 | 邮件通知（可选） |

## 项目结构

```
french_learning/
├── backend/                      # Flask 后端
│   ├── app.py                   # 应用入口
│   ├── config.py                # 配置文件（需要填入 API 密钥）
│   ├── models.py                # 数据库模型
│   ├── extensions.py            # Flask 扩展初始化
│   ├── routes/                  # API 路由
│   │   ├── auth.py             # 认证相关
│   │   ├── chat.py             # 聊天接口
│   │   ├── study.py            # 学习状态管理
│   │   ├── wechat.py           # 微信集成
│   │   ├── assessment.py       # 评估接口
│   │   └── admin.py            # 管理后台
│   ├── services/                # 业务逻辑
│   │   ├── llm_service.py      # LLM 调用
│   │   └── audio_service.py    # 音频处理
│   ├── prompts/                 # LLM 提示词
│   │   └── system_prompt.py    # 系统提示词
│   ├── data/                    # 学习资料
│   │   ├── words.json          # 单词库
│   │   └── audio/              # 音频文件
│   ├── instance/                # SQLite 数据库（自动生成）
│   │   └── french_study.db
│   └── uploads/                 # 用户上传的录音（自动生成）
│
├── frontend/                     # Vue 3 前端
│   ├── src/
│   │   ├── main.js             # 应用入口
│   │   ├── api/                # API 调用
│   │   ├── views/              # 页面组件
│   │   ├── components/         # 可复用组件
│   │   ├── stores/             # Pinia 状态管理
│   │   └── router/             # Vue Router 路由
│   ├── index.html
│   ├── vite.config.js          # Vite 配置
│   └── package.json
│
├── database_schema.md            # 数据库表结构文档
├── SETUP_GUIDE.md               # 本文件
└── README.md                    # 项目说明
```

## 快速启动

### 方式一：分离启动（开发推荐）

#### 终端 1：启动后端
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

后端将运行在 `http://localhost:5000`

#### 终端 2：启动前端
```bash
cd frontend
npm install
npm run dev
```

前端将运行在 `http://localhost:3000`

### 方式二：一键启动脚本

创建 `start.sh`（Linux/macOS）：
```bash
#!/bin/bash

# 启动后端
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nohup python3 app.py > /tmp/flask.log 2>&1 &
BACKEND_PID=$!

# 启动前端
cd ../frontend
npm install
nohup npm run dev > /tmp/vite.log 2>&1 &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
```

运行：
```bash
chmod +x start.sh
./start.sh
```

## 依赖安装

### 后端依赖

创建 `backend/requirements.txt`：
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-JWT-Extended==4.4.4
Flask-CORS==4.0.0
Flask-Limiter==3.5.0
python-dotenv==1.0.0
requests==2.31.0
pydub==0.25.1
pyaudio==0.2.13
```

安装：
```bash
cd backend
pip install -r requirements.txt
```

### 前端依赖

```bash
cd frontend
npm install
```

主要依赖：
- Vue 3
- Vite
- Pinia
- Vue Router
- Axios

## 数据库初始化

首次运行时，Flask 会自动创建数据库和表。如需手动初始化：

```bash
cd backend
python3
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
>>>     db.create_all()
```

## 用户创建

### 方式一：通过注册页面
访问 `http://localhost:3000/register` 进行注册

### 方式二：直接操作数据库
```bash
sqlite3 backend/instance/french_study.db
```

## 配置说明

### 后端配置（backend/config.py）

| 配置项 | 说明 | 默认值 |
|-------|------|--------|
| `LLM_API_KEY` | SiliconFlow API 密钥 | 需要配置 |
| `LLM_MODEL` | 使用的 LLM 模型 | Pro/deepseek-ai/DeepSeek-V3.2 |
| `LLM_TIMEOUT` | LLM 请求超时（秒） | 120 |
| `STUDY_START_DATE` | 学习开始日期 | 2026-04-02 |
| `DATABASE_URL` | 数据库连接 | sqlite:///instance/french_study.db |
| `UPLOAD_FOLDER` | 录音上传目录 | uploads/ |
| `JWT_SECRET_KEY` | JWT 密钥 | 随机生成 |
| `MAX_CONTENT_LENGTH` | 最大上传文件大小 | 50MB |

### 前端配置（frontend/src/api/index.js）

| 配置项 | 说明 |
|-------|------|
| `baseURL` | 后端 API 地址 |
| `timeout` | 请求超时时间 |

## 常见问题

### 1. 连接超时
**症状**：前端无法连接后端
**解决**：
- 检查后端是否正常运行：`curl http://localhost:5000/api/study/status`
- 检查防火墙设置
- 确保后端和前端在同一网络

### 2. FFmpeg 错误
**症状**：音频验证失败
**解决**：
```bash
# 检查 FFmpeg 安装
which ffmpeg

# 重新安装
sudo apt install ffmpeg  # Linux
brew install ffmpeg     # macOS
```

### 3. 数据库锁定
**症状**：数据库被占用
**解决**：
```bash
# 关闭所有 Python 进程
pkill -f "python3 app.py"

# 清空数据库
rm backend/instance/french_study.db
```

### 4. 模块找不到
**症状**：`ModuleNotFoundError: No module named 'xxx'`
**解决**：
```bash
cd backend
pip install -r requirements.txt --upgrade
```

## 开发工作流

### 后端开发
1. 修改代码后，Flask 会自动重载（debug 模式）
2. 查看日志：`tail -f /tmp/flask.log`
3. 测试 API：使用 Postman 或 curl

### 前端开发
1. 修改代码后，Vite 会热更新
2. 打开浏览器开发者工具（F12）查看错误
3. 构建生产版本：`npm run build`

## 性能优化

### 数据库优化
- 当前使用 SQLite WAL 模式，适合小规模应用
- 大规模应用建议迁移至 PostgreSQL

### LLM 优化
- 当前 timeout 设置为 120 秒
- 可根据网络情况调整
- 使用更快的模型可减少响应时间

## 部署

### Docker 部署
创建 `Dockerfile`：
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY backend /app/backend
COPY frontend /app/frontend

# 安装后端依赖
RUN cd /app/backend && pip install -r requirements.txt

# 构建前端
RUN cd /app/frontend && npm install && npm run build

EXPOSE 5000 3000
CMD ["python3", "/app/backend/app.py"]
```

### 生产环境建议
- 使用 Gunicorn 替代 Flask 开发服务器
- 使用 Nginx 作为反向代理
- 配置 HTTPS/SSL
- 设置数据库备份

## 故障排查

### 日志位置
- 后端：`/tmp/flask.log`
- 前端：`/tmp/vite.log` 或浏览器控制台

### 常用调试命令
```bash
# 查看后端进程
ps aux | grep python3

# 查看前端进程
ps aux | grep npm

# 检查端口占用
lsof -i :5000
lsof -i :3000

# 查看数据库状态
sqlite3 backend/instance/french_study.db ".tables"
```

## 联系和支持

- 问题追踪：查看项目的 GitHub Issues
- 数据库文档：参考 `database_schema.md`
- API 文档：查看各路由文件的注释

## 版本信息

- Python：3.9+
- Node.js：16+
- Vue：3.x
- Flask：2.3+

更新时间：2026-04-02
