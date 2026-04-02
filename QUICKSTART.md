# 法语学习助手 - 快速启动指南

## 最快开始（5分钟）

### 前置条件
- Python 3.9+
- Node.js 16+
- FFmpeg（可选，用于音频处理）
- 有效的 SiliconFlow LLM API 密钥

### 一键启动

```bash
# 1. 进入项目目录
cd french_learning

# 2. 配置 API 密钥
# 编辑 backend/config.py，填入你的 API 密钥

# 3. 运行启动脚本
chmod +x start.sh
./start.sh
```

访问：
- 🌐 前端：http://localhost:3000
- 🔌 后端 API：http://localhost:5000

## 分离启动（开发推荐）

### 启动后端（终端 1）
```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python3 app.py
```

### 启动前端（终端 2）
```bash
cd frontend

# 安装依赖（首次）
npm install

# 启动开发服务器
npm run dev
```

## 常用命令

### 查看日志
```bash
tail -f /tmp/flask.log   # 后端日志
tail -f /tmp/vite.log    # 前端日志
```

### 停止服务
```bash
pkill -f "python3 app.py"  # 停止后端
pkill -f "npm run dev"     # 停止前端
```

### 重置数据库
```bash
cd backend
rm instance/french_study.db
# 重启后端，数据库会自动创建
```

### 查看数据库
```bash
sqlite3 backend/instance/french_study.db ".tables"
sqlite3 backend/instance/french_study.db ".schema users"
```

## 配置说明

### 必需配置（backend/config.py）
```python
LLM_API_KEY = "your-api-key-here"
LLM_MODEL = "Pro/deepseek-ai/DeepSeek-V3.2"
```

### 可选配置
- `WECHAT_APPID` / `WECHAT_APPSECRET`：微信集成
- `SMTP_EMAIL` / `SMTP_PASSWORD`：邮件通知

## 文件结构速查

```
french_learning/
├── SETUP_GUIDE.md          ← 详细配置指南
├── start.sh                ← 一键启动脚本
├── backend/
│   ├── app.py             ← 后端入口
│   ├── config.py          ← ⭐ 配置文件（需要填入 API 密钥）
│   ├── routes/            ← API 路由
│   ├── data/words.json    ← 学习单词库
│   └── instance/          ← 数据库（自动生成）
└── frontend/
    ├── package.json
    └── src/
```

## 故障排查

| 问题 | 解决方案 |
|------|--------|
| 无法连接后端 | 检查 http://localhost:5000 是否可访问 |
| 模块找不到 | 运行 `pip install -r requirements.txt` |
| 数据库锁定 | 删除 `backend/instance/french_study.db` 后重启 |
| FFmpeg 缺失 | `sudo apt install ffmpeg` (Linux) 或 `brew install ffmpeg` (macOS) |
| 端口被占用 | 检查：`lsof -i :5000` 或 `lsof -i :3000` |

## 详细文档

- 📚 **完整配置指南**：参考 `SETUP_GUIDE.md`
- 🗄️ **数据库表结构**：参考 `database_schema.md`
- 📖 **项目说明**：参考 `README.md`

## 常见 API

```bash
# 登录
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "13800000000", "password": "password"}'

# 获取学习状态
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:5000/api/study/status

# 发送聊天消息
curl -X POST http://localhost:5000/api/chat/send \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "我想学习法语"}'
```

## 下一步

1. ✅ 配置 API 密钥
2. ✅ 运行 `./start.sh` 启动
3. ✅ 访问 http://localhost:3000
4. ✅ 进行注册��测试

有问题？查看 `SETUP_GUIDE.md` 获取更详细的帮助。
