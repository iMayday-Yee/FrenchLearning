# 法语学习AI助手研究平台 - 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个完整的法语学习聊天助手平台，支持3种AI交互风格分组（A/B/C组）和2种头像类型，用于学术研究。

**Architecture:** 前后端分离架构。前端Vue 3响应式应用通过axios与后端Flask API通信。后端使用SQLite存储数据，集成硅基流动LLM API实现智能回复，集成微信测试号实现通知推送。

**Tech Stack:**
- 前端：Vue 3 + Vite + Pinia + Vue Router
- 后端：Flask 3 + SQLAlchemy + APScheduler + JWT
- 数据库：SQLite (WAL模式)
- LLM：硅基流动 API (DeepSeek-V2.5)
- 实时通信：轮询 (Web应用场景适用)

---

## 项目目录结构

```
french-study-platform/
├── frontend/                          # Vue 3 前端项目
│   ├── public/
│   │   ├── avatars/
│   │   │   ├── human.png
│   │   │   └── robot.png
│   │   └── favicon.ico
│   ├── src/
│   │   ├── api/
│   │   │   └── index.js             # axios封装
│   │   ├── components/
│   │   │   ├── ChatBubble.vue
│   │   │   ├── WordCard.vue
│   │   │   ├── AudioPlayer.vue
│   │   │   ├── AudioRecorder.vue
│   │   │   ├── MessageList.vue
│   │   │   └── AssessmentQuestion.vue
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── Register.vue
│   │   │   ├── BindWeChat.vue
│   │   │   ├── Agreement.vue
│   │   │   ├── RegisterDone.vue
│   │   │   ├── Login.vue
│   │   │   ├── Chat.vue
│   │   │   ├── Assessment.vue
│   │   │   ├── Result.vue
│   │   │   ├── Waiting.vue
│   │   │   ├── Completed.vue
│   │   │   └── admin/
│   │   │       ├── AdminLogin.vue
│   │   │       └── Dashboard.vue
│   │   ├── stores/
│   │   │   ├── user.js
│   │   │   └── study.js
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── utils/
│   │   │   ├── audio.js
│   │   │   └── request.js
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── models.py
│   ├── extensions.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── wechat.py
│   │   ├── study.py
│   │   ├── chat.py
│   │   ├── assessment.py
│   │   └── admin.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── llm_service.py
│   │   ├── wechat_service.py
│   │   ├── email_service.py
│   │   ├── audio_service.py
│   │   ├── notification_service.py
│   │   └── group_service.py
│   ├── prompts/
│   │   └── system_prompt.py
│   ├── data/
│   │   └── words.json
│   ├── static/
│   │   └── audio/
│   ├── uploads/
│   ├── requirements.txt
│   └── gunicorn_config.py
│
├── nginx.conf
├── deploy.sh
└── README.md
```

---

## 阶段一：项目基础框架搭建

### Task 1: 创建后端项目结构和依赖

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/config.py`
- Create: `backend/extensions.py`
- Create: `backend/models.py`
- Create: `backend/app.py`
- Create: `backend/routes/__init__.py`
- Create: `backend/services/__init__.py`
- Create: `backend/prompts/system_prompt.py`
- Create: `backend/data/words.json` (示例数据)

- [ ] **Step 1: 创建 backend/requirements.txt**

```txt
flask==3.1.*
flask-cors==5.*
flask-sqlalchemy==3.*
flask-jwt-extended==4.*
flask-limiter==3.*
gunicorn==22.*
gevent==24.*
requests==2.*
APScheduler==3.*
pydub==0.25.*
PyJWT==2.*
python-dotenv==1.*
httpx==0.27.*
Werkzeug==3.*
```

- [ ] **Step 2: 创建 backend/config.py**

```python
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-to-a-random-string')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///french_study.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-this')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    LLM_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
    LLM_API_KEY = os.environ.get('LLM_API_KEY', '')
    LLM_MODEL = "deepseek-ai/DeepSeek-V2.5"
    WECHAT_ACCOUNTS = [
        {"app_id": os.environ.get('WECHAT_APP_ID_1', ''), "app_secret": os.environ.get('WECHAT_APP_SECRET_1', ''), "token": os.environ.get('WECHAT_TOKEN_1', 'fayuxiaozhushou1'), "template_id": os.environ.get('WECHAT_TEMPLATE_ID_1', '')},
        {"app_id": os.environ.get('WECHAT_APP_ID_2', ''), "app_secret": os.environ.get('WECHAT_APP_SECRET_2', ''), "token": os.environ.get('WECHAT_TOKEN_2', 'fayuxiaozhushou2'), "template_id": os.environ.get('WECHAT_TEMPLATE_ID_2', '')},
    ]
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.qq.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))
    SMTP_USER = os.environ.get('SMTP_USER', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    STUDY_START_DATE = '2026-04-07'
    MAX_DAILY_ROUNDS = 20
    REENTER_THRESHOLD_MINUTES = 5
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    AUDIO_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'audio')
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123change')
    GROUP_SLOTS = {'low': {'human': 30, 'robot': 30}, 'adjustable': {'human': 30, 'robot': 30}, 'high': {'human': 30, 'robot': 30}}
```

- [ ] **Step 3: 创建 backend/extensions.py**

```python
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])
```

- [ ] **Step 4: 创建 backend/models.py**

```python
from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100))
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    education = db.Column(db.String(20), nullable=False)
    french_interest = db.Column(db.String(20), nullable=False)
    french_level = db.Column(db.String(20), nullable=False)
    study_time_slot = db.Column(db.String(10), nullable=False)
    group_type = db.Column(db.String(20), nullable=False)  # low / adjustable / high
    avatar_type = db.Column(db.String(10), nullable=False)  # human / robot
    wechat_openid = db.Column(db.String(100))
    wechat_account_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DailyStatus(db.Model):
    __tablename__ = 'daily_status'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    study_day = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    material_sent = db.Column(db.Boolean, default=False)
    rejected = db.Column(db.Boolean, default=False)
    practice_count = db.Column(db.Integer, default=0)
    invalid_audio_count = db.Column(db.Integer, default=0)
    conversation_rounds = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('user_id', 'study_day'),)

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    study_day = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(10), nullable=False)  # user / assistant
    content_type = db.Column(db.String(20), nullable=False)  # text / word_card / audio / user_audio / system
    content = db.Column(db.Text, nullable=False)
    is_template = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.Index('idx_user_study_day', 'user_id', 'study_day'),)

class AudioRecord(db.Model):
    __tablename__ = 'audio_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    study_day = db.Column(db.Integer, nullable=False)
    word_index = db.Column(db.Integer)
    target_word = db.Column(db.String(50))
    audio_path = db.Column(db.String(255), nullable=False)
    is_valid = db.Column(db.Boolean, default=False)
    score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AssessmentAnswer(db.Model):
    __tablename__ = 'assessment_answers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word_french = db.Column(db.String(50), nullable=False)
    correct_chinese = db.Column(db.String(50), nullable=False)
    user_choice = db.Column(db.String(50), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    pronunciation_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AssessmentSummary(db.Model):
    __tablename__ = 'assessment_summary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    vocab_score = db.Column(db.Float, nullable=False)
    pronunciation_avg = db.Column(db.Float)
    total_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.Text, nullable=False)

class GroupSlot(db.Model):
    __tablename__ = 'group_slots'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_type = db.Column(db.String(20), nullable=False)  # low / adjustable / high
    avatar_type = db.Column(db.String(10), nullable=False)  # human / robot
    max_count = db.Column(db.Integer, nullable=False)
    current_count = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('group_type', 'avatar_type'),)
```

- [ ] **Step 5: 创建 backend/app.py**

```python
import os
from flask import Flask
from flask_cors import CORS
from extensions import db, jwt, limiter
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

    from routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()
        init_system_config(app)
        init_group_slots(app)

    return app

def init_system_config(app):
    defaults = {'study_start_date': app.config['STUDY_START_DATE'], 'max_daily_rounds': '20', 'reenter_threshold_minutes': '5'}
    for key, value in defaults.items():
        if not SystemConfig.query.get(key):
            db.session.add(SystemConfig(key=key, value=value))
    db.session.commit()

def init_group_slots(app):
    slots = app.config['GROUP_SLOTS']
    for group_type, avatars in slots.items():
        for avatar_type, count in avatars.items():
            existing = GroupSlot.query.filter_by(group_type=group_type, avatar_type=avatar_type).first()
            if not existing:
                db.session.add(GroupSlot(group_type=group_type, avatar_type=avatar_type, max_count=count, current_count=0))
    db.session.commit()

from models import SystemConfig, GroupSlot

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
```

- [ ] **Step 6: 创建 backend/routes/__init__.py**

```python
from flask import Blueprint

def register_routes(app):
    from routes.auth import auth_bp
    from routes.wechat import wechat_bp
    from routes.study import study_bp
    from routes.chat import chat_bp
    from routes.assessment import assessment_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(wechat_bp, url_prefix='/api')
    app.register_blueprint(study_bp, url_prefix='/api')
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(assessment_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api')
```

- [ ] **Step 7: 创建 backend/prompts/system_prompt.py**

```python
SYSTEM_PROMPT = """你是一个法语学习助手，你的唯一职责是帮助用户学习法语。请严格遵守以下规则：

【核心规则】
1. 你只讨论与法语学习相关的话题。
2. 如果用户发送的内容与法语学习完全无关（如闲聊天气、讲笑话、问其他知识），你必须固定回复："我是一个法语学习助手，目前只能和您聊与法语学习有关的内容哦～有什么法语问题都可以问我！"
3. 如果用户发送的内容与法语有一定关系但不在标准学习流程中（如感叹"今天单词好难"、问"法语难不难学"），你可以简短友好回复（不超过50字），然后引导继续练习。
4. 回复风格：友好、鼓励、简洁。

【关于音频占位符】
- 上下文中 [用户发送了单词"xxx"的跟读录音] 表示用户进行了跟读练习，请给予积极鼓励。
- [该录音无效（空白/无声）] 表示录音没有声音，请温和提醒重新录制。

【输出格式——严格遵守】
你的回复必须且只能是一个JSON对象，不要输出任何其他文字。格式：
{"intent": "分类标签", "reply": "给用户的回复文本"}

intent取值说明：
- "request_material"：用户请求获取今天的法语学习材料（如"给我发音频""我要学习""开始今天的课""发给我"等）
- "accept_learning"：用户同意开始学习（如"好的""行""可以""来吧""搞""OK"等肯定回答）
- "reject_learning"：用户拒绝学习（如"不了""现在不行""等会""不想""算了"等否定回答）
- "follow_up_practice"：用户发送了跟读录音
- "french_related_chat"：与法语有关的非标准流程闲聊
- "unrelated_chat"：与法语完全无关的内容
- "other"：无法归类
"""
```

- [ ] **Step 8: 创建 backend/data/words.json (示例数据)**

```json
[
  {"day": 1, "words": [{"index": 1, "french": "bonjour", "chinese": "你好", "audio": "day1/1-1.mp3"}, {"index": 2, "french": "merci", "chinese": "谢谢", "audio": "day1/1-2.mp3"}, {"index": 3, "french": "au revoir", "chinese": "再见", "audio": "day1/1-3.mp3"}]},
  {"day": 2, "words": [{"index": 1, "french": "salut", "chinese": "你好/再见", "audio": "day2/2-1.mp3"}, {"index": 2, "french": "oui", "chinese": "是", "audio": "day2/2-2.mp3"}, {"index": 3, "french": "non", "chinese": "不", "audio": "day2/2-3.mp3"}]},
  {"day": 3, "words": [{"index": 1, "french": "bonne nuit", "chinese": "晚安", "audio": "day3/3-1.mp3"}, {"index": 2, "french": "s'il vous plaît", "chinese": "请", "audio": "day3/3-2.mp3"}, {"index": 3, "french": "excusez-moi", "chinese": "对不起/打扰一下", "audio": "day3/3-3.mp3"}]},
  {"day": 4, "words": [{"index": 1, "french": "comment allez-vous", "chinese": "你好吗", "audio": "day4/4-1.mp3"}, {"index": 2, "french": "très bien", "chinese": "很好", "audio": "day4/4-2.mp3"}, {"index": 3, "french": "je m'appelle", "chinese": "我叫", "audio": "day4/4-3.mp3"}]},
  {"day": 5, "words": [{"index": 1, "french": "enchanté", "chinese": "很高兴认识你", "audio": "day5/5-1.mp3"}, {"index": 2, "french": "où", "chinese": "哪里", "audio": "day5/5-2.mp3"}, {"index": 3, "french": "ici", "chinese": "这里", "audio": "day5/5-3.mp3"}]},
  {"day": 6, "words": [{"index": 1, "french": "maison", "chinese": "房子", "audio": "day6/6-1.mp3"}, {"index": 2, "french": "travail", "chinese": "工作", "audio": "day6/6-2.mp3"}, {"index": 3, "french": "famille", "chinese": "家庭", "audio": "day6/6-3.mp3"}]},
  {"day": 7, "words": [{"index": 1, "french": "ami", "chinese": "朋友", "audio": "day7/7-1.mp3"}, {"index": 2, "french": "amour", "chinese": "爱", "audio": "day7/7-2.mp3"}, {"index": 3, "french": "temps", "chinese": "时间/天气", "audio": "day7/7-3.mp3"}]},
  {"day": 8, "words": [{"index": 1, "french": "jour", "chinese": "天", "audio": "day8/8-1.mp3"}, {"index": 2, "french": "mois", "chinese": "月", "audio": "day8/8-2.mp3"}, {"index": 3, "french": "année", "chinese": "年", "audio": "day8/8-3.mp3"}]},
  {"day": 9, "words": [{"index": 1, "french": "eau", "chinese": "水", "audio": "day9/9-1.mp3"}, {"index": 2, "french": "pain", "chinese": "面包", "audio": "day9/9-2.mp3"}, {"index": 3, "french": "vin", "chinese": "葡萄酒", "audio": "day9/9-3.mp3"}]},
  {"day": 10, "words": [{"index": 1, "french": "livre", "chinese": "书", "audio": "day10/10-1.mp3"}, {"index": 2, "french": "stylo", "chinese": "笔", "audio": "day10/10-2.mp3"}, {"index": 3, "french": "papier", "chinese": "纸", "audio": "day10/10-3.mp3"}]}
]
```

- [ ] **Step 9: 安装后端依赖并测试**

Run: `cd /home/yu/project/french_learning/backend && pip install -r requirements.txt`
Run: `python app.py` (验证能启动)

---

### Task 2: 创建前端项目结构和依赖

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/src/main.js`
- Create: `frontend/src/App.vue`
- Create: `frontend/src/router/index.js`
- Create: `frontend/src/stores/user.js`
- Create: `frontend/src/stores/study.js`
- Create: `frontend/src/api/index.js`
- Create: `frontend/src/utils/request.js`

- [ ] **Step 1: 创建 frontend/package.json**

```json
{
  "name": "french-learning-frontend",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "vue-router": "^4.2.0",
    "pinia": "^2.1.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0"
  }
}
```

- [ ] **Step 2: 创建 frontend/vite.config.js**

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})
```

- [ ] **Step 3: 创建 frontend/index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>法语学习助手</title>
  <link rel="icon" href="/favicon.ico">
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
```

- [ ] **Step 4: 创建 frontend/src/main.js**

```javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')
```

- [ ] **Step 5: 创建 frontend/src/App.vue**

```vue
<template>
  <router-view />
</template>

<script setup>
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f5f5;
  min-height: 100vh;
}

#app {
  min-height: 100vh;
}
</style>
```

- [ ] **Step 6: 创建 frontend/src/router/index.js**

```javascript
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('@/views/Home.vue') },
  { path: '/register', component: () => import('@/views/Register.vue') },
  { path: '/bindwechat', component: () => import('@/views/BindWeChat.vue') },
  { path: '/agreement', component: () => import('@/views/Agreement.vue') },
  { path: '/register-done', component: () => import('@/views/RegisterDone.vue') },
  { path: '/login', component: () => import('@/views/Login.vue') },
  { path: '/chat', component: () => import('@/views/Chat.vue'), meta: { auth: true } },
  { path: '/assessment', component: () => import('@/views/Assessment.vue'), meta: { auth: true } },
  { path: '/result', component: () => import('@/views/Result.vue'), meta: { auth: true } },
  { path: '/waiting', component: () => import('@/views/Waiting.vue'), meta: { auth: true } },
  { path: '/completed', component: () => import('@/views/Completed.vue'), meta: { auth: true } },
  { path: '/admin', component: () => import('@/views/admin/AdminLogin.vue') },
  { path: '/admin/dashboard', component: () => import('@/views/admin/Dashboard.vue'), meta: { admin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from) => {
  const userStore = await import('@/stores/user')
  const store = userStore.useUserStore()

  if (to.meta.auth && !store.token) {
    return '/login'
  }

  if (to.meta.admin && !localStorage.getItem('admin_token')) {
    return '/admin'
  }

  if (to.path === '/chat') {
    const studyStore = (await import('@/stores/study')).useStudyStore()
    await studyStore.fetchStatus()
    if (studyStore.phase === 'not_started') return '/waiting'
    if (studyStore.phase === 'completed') return '/completed'
    if (studyStore.needAssessment) return '/assessment'
  }
})

export default router
```

- [ ] **Step 7: 创建 frontend/src/stores/user.js**

```javascript
import { defineStore } from 'pinia'
import { api } from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userId: null,
    nickname: '',
    avatarType: '',
  }),
  actions: {
    async setLogin(data) {
      this.token = data.token
      this.userId = data.user_id
      localStorage.setItem('token', data.token)
    },
    async fetchProfile() {
      try {
        const res = await api.get('/user/profile')
        this.userId = res.user_id
        this.nickname = res.nickname
        this.avatarType = res.avatar_type
      } catch (e) {
        this.logout()
      }
    },
    logout() {
      this.token = ''
      this.userId = null
      this.nickname = ''
      this.avatarType = ''
      localStorage.removeItem('token')
    }
  }
})
```

- [ ] **Step 8: 创建 frontend/src/stores/study.js**

```javascript
import { defineStore } from 'pinia'
import { api } from '@/api'

export const useStudyStore = defineStore('study', {
  state: () => ({
    studyDay: 0,
    phase: 'not_started',
    materialSentToday: false,
    remainingRounds: 20,
    chatMessages: [],
    needAssessment: false,
  }),
  actions: {
    async fetchStatus() {
      try {
        const res = await api.get('/study/status')
        this.studyDay = res.study_day
        this.phase = res.phase
        this.materialSentToday = res.material_sent_today
        this.remainingRounds = res.remaining_rounds
        this.needAssessment = res.need_assessment
      } catch (e) {
        console.error('Failed to fetch status', e)
      }
    },
    async loadHistory(day) {
      try {
        const res = await api.get(`/chat/history${day ? '?day=' + day : ''}`)
        this.chatMessages = res.messages || []
      } catch (e) {
        console.error('Failed to load history', e)
      }
    },
    appendMessage(msg) {
      this.chatMessages.push(msg)
    }
  }
})
```

- [ ] **Step 9: 创建 frontend/src/api/index.js**

```javascript
import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    } else {
      ElMessage.error(error.response?.data?.message || '请求失败')
    }
    return Promise.reject(error)
  }
)

export { api }
```

- [ ] **Step 10: 创建 frontend/src/utils/request.js**

```javascript
import axios from 'axios'

const request = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

request.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default request
```

- [ ] **Step 11: 安装前端依赖并测试**

Run: `cd /home/yu/project/french_learning/frontend && npm install`
Run: `npm run dev` (验证能启动)

---

## 阶段二：用户认证模块

### Task 3: 后端认证接口

**Files:**
- Create: `backend/routes/auth.py`
- Modify: `backend/services/group_service.py`

- [ ] **Step 1: 创建 backend/services/group_service.py**

```python
import random
from models import GroupSlot, User

def assign_group(db):
    available_slots = GroupSlot.query.filter(GroupSlot.current_count < GroupSlot.max_count).all()
    if not available_slots:
        raise Exception("所有分组槽位已满")

    chosen = random.choice(available_slots)
    chosen.current_count += 1
    db.session.commit()

    return chosen.group_type, chosen.avatar_type

def check_slot_balance():
    slots = GroupSlot.query.all()
    return [{'group_type': s.group_type, 'avatar_type': s.avatar_type, 'current': s.current_count, 'max': s.max_count} for s in slots]
```

- [ ] **Step 2: 创建 backend/routes/auth.py**

```python
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from extensions import db
from models import User
from services.group_service import assign_group

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required = ['phone', 'password', 'nickname', 'age', 'gender', 'education', 'french_interest', 'french_level', 'study_time_slot']
    for field in required:
        if not data.get(field):
            return jsonify({'code': 400, 'message': f'缺少必填字段: {field}'}), 400

    if User.query.filter_by(phone=data['phone']).first():
        return jsonify({'code': 400, 'message': '手机号已注册'}), 400

    try:
        group_type, avatar_type = assign_group(db)
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

    user = User(
        phone=data['phone'],
        email=data.get('email'),
        password_hash=generate_password_hash(data['password']),
        nickname=data['nickname'],
        age=data['age'],
        gender=data['gender'],
        education=data['education'],
        french_interest=data['french_interest'],
        french_level=data['french_level'],
        study_time_slot=data['study_time_slot'],
        group_type=group_type,
        avatar_type=avatar_type
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'code': 200, 'user_id': user.id, 'message': '注册成功'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    phone = data.get('phone')
    password = data.get('password')

    if not phone or not password:
        return jsonify({'code': 400, 'message': '手机号和密码不能为空'}), 400

    user = User.query.filter_by(phone=phone).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'code': 401, 'message': '手机号或密码错误'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'code': 200, 'token': token, 'user_id': user.id})

@auth_bp.route('/user/profile', methods=['GET'])
def get_profile():
    from flask_jwt_extended import jwt_required, get_jwt_identity
    @jwt_required()
    def inner():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404

        from config import Config
        return jsonify({
            'user_id': user.id,
            'nickname': user.nickname,
            'avatar_type': user.avatar_type,
            'avatar_url': f'/avatars/{user.avatar_type}.png',
            'study_start_date': Config.STUDY_START_DATE,
            'wechat_bound': bool(user.wechat_openid)
        })
    return inner()
```

---

### Task 4: 前端注册和登录页面

**Files:**
- Create: `frontend/src/views/Register.vue`
- Create: `frontend/src/views/Login.vue`
- Create: `frontend/src/views/Home.vue`

- [ ] **Step 1: 创建 frontend/src/views/Home.vue**

```vue
<template>
  <div class="home">
    <div class="container">
      <h1>法语学习助手</h1>
      <p class="subtitle">基于AI的个性化法语学习平台</p>
      <div class="buttons">
        <button @click="$router.push('/login')" class="btn-primary">登录</button>
        <button @click="$router.push('/register')" class="btn-secondary">注册</button>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.container {
  text-align: center;
  color: white;
}
h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}
.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}
.buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}
.btn-primary, .btn-secondary {
  padding: 0.8rem 2rem;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}
.btn-primary {
  background: white;
  color: #667eea;
}
.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}
.btn-primary:hover, .btn-secondary:hover {
  transform: scale(1.05);
}
</style>
```

- [ ] **Step 2: 创建 frontend/src/views/Register.vue**

```vue
<template>
  <div class="register-page">
    <div class="form-container">
      <h2>用户注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>手机号 *</label>
          <input v-model="form.phone" type="tel" required maxlength="20" placeholder="请输入手机号">
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="form.email" type="email" placeholder="选填，用于接收通知">
        </div>
        <div class="form-group">
          <label>密码 *</label>
          <input v-model="form.password" type="password" required minlength="6" placeholder="至少6位">
        </div>
        <div class="form-group">
          <label>姓名/昵称 *</label>
          <input v-model="form.nickname" type="text" required maxlength="50">
        </div>
        <div class="form-group">
          <label>年龄 *</label>
          <input v-model.number="form.age" type="number" required min="10" max="100">
        </div>
        <div class="form-group">
          <label>性别 *</label>
          <select v-model="form.gender" required>
            <option value="">请选择</option>
            <option value="男">男</option>
            <option value="女">女</option>
            <option value="其他">其他</option>
          </select>
        </div>
        <div class="form-group">
          <label>教育背景 *</label>
          <select v-model="form.education" required>
            <option value="">请选择</option>
            <option value="高中及以下">高中及以下</option>
            <option value="大专">大专</option>
            <option value="本科">本科</option>
            <option value="硕士">硕士</option>
            <option value="博士">博士</option>
          </select>
        </div>
        <div class="form-group">
          <label>对法语的兴趣程度 *</label>
          <select v-model="form.french_interest" required>
            <option value="">请选择</option>
            <option value="非常感兴趣">非常感兴趣</option>
            <option value="比较感兴趣">比较感兴趣</option>
            <option value="一般">一般</option>
            <option value="不太感兴趣">不太感兴趣</option>
            <option value="完全不感兴趣">完全不感兴趣</option>
          </select>
        </div>
        <div class="form-group">
          <label>法语学习基础 *</label>
          <select v-model="form.french_level" required>
            <option value="">请选择</option>
            <option value="零基础">零基础</option>
            <option value="了解少量单词">了解少量单词</option>
            <option value="系统学习过一段时间">系统学习过一段时间</option>
            <option value="较为熟练">较为熟练</option>
          </select>
        </div>
        <div class="form-group">
          <label>偏好学习时间段 *</label>
          <select v-model="form.study_time_slot" required>
            <option value="">请选择</option>
            <option value="06:00">6:00-8:00</option>
            <option value="08:00">8:00-10:00</option>
            <option value="10:00">10:00-12:00</option>
            <option value="12:00">12:00-14:00</option>
            <option value="14:00">14:00-16:00</option>
            <option value="16:00">16:00-18:00</option>
            <option value="18:00">18:00-20:00</option>
            <option value="20:00">20:00-22:00</option>
            <option value="22:00">22:00-24:00</option>
          </select>
        </div>
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? '提交中...' : '提交注册' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const form = ref({
  phone: '',
  email: '',
  password: '',
  nickname: '',
  age: null,
  gender: '',
  education: '',
  french_interest: '',
  french_level: '',
  study_time_slot: ''
})

const handleRegister = async () => {
  loading.value = true
  try {
    const res = await api.post('/register', form.value)
    if (res.code === 200) {
      localStorage.setItem('pending_user_id', res.user_id)
      router.push('/bindwechat')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  padding: 2rem 1rem;
  background: #f5f5f5;
}
.form-container {
  max-width: 500px;
  margin: 0 auto;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
}
h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}
.form-group {
  margin-bottom: 1rem;
}
label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
  color: #555;
}
input, select {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}
.btn-submit {
  width: 100%;
  padding: 0.8rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1rem;
}
.btn-submit:disabled {
  opacity: 0.6;
}
</style>
```

- [ ] **Step 3: 创建 frontend/src/views/Login.vue**

```vue
<template>
  <div class="login-page">
    <div class="form-container">
      <h2>用户登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>手机号</label>
          <input v-model="form.phone" type="tel" required placeholder="请输入手机号">
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="form.password" type="password" required placeholder="请输入密码">
        </div>
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      <p class="links">
        <span @click="$router.push('/register')">还没有账号？去注册</span>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const form = ref({ phone: '', password: '' })

const handleLogin = async () => {
  loading.value = true
  try {
    const res = await api.post('/login', form.value)
    if (res.code === 200) {
      await userStore.setLogin(res)
      await userStore.fetchProfile()

      const studyStore = (await import('@/stores/study')).useStudyStore()
      await studyStore.fetchStatus()

      if (studyStore.phase === 'not_started') {
        router.push('/waiting')
      } else if (studyStore.phase === 'completed') {
        router.push('/completed')
      } else if (studyStore.needAssessment) {
        router.push('/assessment')
      } else {
        router.push('/chat')
      }
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.form-container {
  width: 100%;
  max-width: 400px;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}
.form-group {
  margin-bottom: 1rem;
}
label {
  display: block;
  margin-bottom: 0.3rem;
  font-weight: 500;
  color: #555;
}
input {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}
.btn-submit {
  width: 100%;
  padding: 0.8rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 0.5rem;
}
.btn-submit:disabled {
  opacity: 0.6;
}
.links {
  text-align: center;
  margin-top: 1rem;
}
.links span {
  color: #667eea;
  cursor: pointer;
}
</style>
```

---

## 阶段三：微信绑定流程

### Task 5: 微信绑定后端接口

**Files:**
- Create: `backend/routes/wechat.py`
- Create: `backend/services/wechat_service.py`

- [ ] **Step 1: 创建 backend/services/wechat_service.py**

```python
import requests
import time
import random

token_cache = {}

def get_access_token(account_index, app_id, app_secret):
    cache_key = f"wechat_token_{account_index}"
    if cache_key in token_cache:
        cached = token_cache[cache_key]
        if cached['expires_at'] > time.time():
            return cached['token']

    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    resp = requests.get(url).json()
    token = resp.get('access_token')
    if token:
        token_cache[cache_key] = {'token': token, 'expires_at': time.time() + 7000}
    return token

def create_qrcode(account_index, app_id, app_secret, scene_str):
    access_token = get_access_token(account_index, app_id, app_secret)
    if not access_token:
        return None

    url = f"https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={access_token}"
    data = {"action_name": "QR_STR_SCENE", "action_info": {"scene": {"scene_str": scene_str}}}
    resp = requests.post(url, json=data).json()
    return resp.get('ticket')

def send_template_message(openid, template_id, access_token, url, data):
    api_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    payload = {
        "touser": openid,
        "template_id": template_id,
        "url": url,
        "data": data
    }
    return requests.post(api_url, json=payload).json()
```

- [ ] **Step 2: 创建 backend/routes/wechat.py**

```python
from flask import Blueprint, request, jsonify, send_from_directory
import requests
from extensions import db
from models import User
from services.wechat_service import create_qrcode, get_access_token
from config import Config
import qrcode
import io
import base64
import os

wechat_bp = Blueprint('wechat', __name__)

@wechat_bp.route('/get_bind_qrcode', methods=['GET'])
def get_bind_qrcode():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': 'User not found'}), 404

    account_index = 0
    account = Config.WECHAT_ACCOUNTS[account_index]

    scene_str = f"bind_{user_id}"
    ticket = create_qrcode(account_index, account['app_id'], account['app_secret'], scene_str)

    if not ticket:
        return jsonify({'code': 500, 'message': 'Failed to create QR code'}), 500

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(f"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}")
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode()

    return jsonify({
        'code': 200,
        'qrcode_image': f"data:image/png;base64,{img_base64}",
        'user_id': user_id
    })

@wechat_bp.route('/bindcheck', methods=['GET'])
def bindcheck():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'code': 404, 'message': 'User not found'}), 404

    return jsonify({
        'code': 200,
        'bound': bool(user.wechat_openid)
    })

@wechat_bp.route('/wechat/callback', methods=['GET', 'POST'])
def wechat_callback():
    if request.method == 'GET':
        echostr = request.args.get('echostr')
        return echostr

    data = request.get_xml()
    msg_type = data.get('MsgType')

    if msg_type == 'event':
        event = data.get('Event')
        if event == 'subscribe':
            scene_str = data.get('EventKey', '')
            if scene_str.startswith('qrscene_bind_'):
                user_id = scene_str.replace('qrscene_bind_', '')
                openid = data.get('FromUserName')

                user = User.query.get(int(user_id))
                if user:
                    user.wechat_openid = openid
                    user.wechat_account_index = 0
                    db.session.commit()

    return 'success'
```

---

### Task 6: 前端微信绑定页面

**Files:**
- Create: `frontend/src/views/BindWeChat.vue`
- Create: `frontend/src/views/Agreement.vue`
- Create: `frontend/src/views/RegisterDone.vue`

- [ ] **Step 1: 创建 frontend/src/views/BindWeChat.vue**

```vue
<template>
  <div class="bind-page">
    <div class="container">
      <h2>绑定微信</h2>
      <p class="desc">请使用微信扫描下方二维码关注公众号，以便接收学习提醒</p>

      <div class="qrcode-container" v-if="!bound">
        <img v-if="qrcodeImage" :src="qrcodeImage" alt="微信二维码">
        <div v-else class="loading">加载中...</div>
      </div>

      <div v-if="bound" class="success">
        <p>绑定成功！</p>
      </div>

      <div class="actions">
        <button v-if="!bound" @click="checkBind" class="btn-skip">跳过，稍后绑定</button>
        <button v-if="bound" @click="goNext" class="btn-next">继续</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const qrcodeImage = ref('')
const bound = ref(false)
const userId = localStorage.getItem('pending_user_id')

const loadQRCode = async () => {
  try {
    const res = await api.get(`/get_bind_qrcode?user_id=${userId}`)
    if (res.code === 200) {
      qrcodeImage.value = res.qrcode_image
    }
  } catch (e) {
    console.error('Failed to load QR code', e)
  }
}

const checkBind = async () => {
  const res = await api.get(`/bindcheck?user_id=${userId}`)
  if (res.bound) {
    bound.value = true
    setTimeout(() => router.push('/agreement'), 1000)
  }
}

const goNext = () => {
  router.push('/agreement')
}

onMounted(() => {
  if (!userId) {
    router.push('/register')
    return
  }
  loadQRCode()

  const interval = setInterval(async () => {
    const res = await api.get(`/bindcheck?user_id=${userId}`)
    if (res.bound) {
      clearInterval(interval)
      bound.value = true
      setTimeout(() => router.push('/agreement'), 1000)
    }
  }, 3000)

  setTimeout(() => clearInterval(interval), 180000)
})
</script>

<style scoped>
.bind-page {
  min-height: 100vh;
  padding: 2rem;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}
.container {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  max-width: 400px;
}
h2 { margin-bottom: 0.5rem; }
.desc { color: #666; margin-bottom: 1.5rem; font-size: 0.9rem; }
.qrcode-container {
  margin: 1rem auto;
}
.qrcode-container img {
  width: 200px;
  height: 200px;
}
.loading { padding: 50px; color: #999; }
.success { color: #52c41a; padding: 1rem; }
.actions { margin-top: 1.5rem; }
.btn-skip {
  background: none;
  border: 1px solid #ddd;
  padding: 0.6rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  color: #666;
}
.btn-next {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.6rem 2rem;
  border-radius: 6px;
  cursor: pointer;
}
</style>
```

- [ ] **Step 2: 创建 frontend/src/views/Agreement.vue**

```vue
<template>
  <div class="agreement-page">
    <div class="container">
      <h2>用户协议与隐私说明</h2>
      <div class="content">
        <p>本研究将收集以下数据用于学术研究：</p>
        <ul>
          <li>您主动发送消息的次数</li>
          <li>您回复同意/拒绝接收学习材料的次数</li>
          <li>您上传语音跟读的次数</li>
          <li>您通过麦克风录音互动的次数</li>
          <li>各组发音准确度评分的平均分差异（如有此功能）</li>
          <li>所有聊天内容的完整记录</li>
          <li>您的注册信息（年龄、性别、教育背景等）</li>
        </ul>
        <p>所有数据仅用于学术研究，匿名处理后分析，不会泄露您的个人身份信息。</p>
      </div>
      <div class="checkbox">
        <input type="checkbox" v-model="agreed" id="agree">
        <label for="agree">我已阅读并同意上述协议</label>
      </div>
      <button class="btn-submit" :disabled="!agreed" @click="handleAgree">
        同意并继续
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const agreed = ref(false)

const handleAgree = () => {
  if (agreed.value) {
    router.push('/register-done')
  }
}
</script>

<style scoped>
.agreement-page {
  min-height: 100vh;
  padding: 2rem;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}
.container {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
}
h2 { margin-bottom: 1rem; text-align: center; }
.content {
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  max-height: 300px;
  overflow-y: auto;
  font-size: 0.9rem;
  line-height: 1.6;
}
.content p { margin-bottom: 0.5rem; }
.content ul { margin-left: 1.5rem; }
.content li { margin-bottom: 0.3rem; }
.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 1rem 0;
}
.checkbox input { width: 18px; height: 18px; }
.btn-submit {
  width: 100%;
  padding: 0.8rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}
.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
```

- [ ] **Step 3: 创建 frontend/src/views/RegisterDone.vue**

```vue
<template>
  <div class="done-page">
    <div class="container">
      <div class="icon">✓</div>
      <h2>注册完成</h2>
      <p class="message">您的账号已创建成功！</p>
      <p class="date">学习将于 <strong>{{ studyStartDate }}</strong> 开始</p>
      <p class="tip">届时请打开本页面开始学习</p>
      <button class="btn-login" @click="goLogin">前往登录</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const studyStartDate = computed(() => {
  return localStorage.getItem('study_start_date') || '待定'
})

const goLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.done-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.container {
  background: white;
  padding: 3rem 2rem;
  border-radius: 16px;
  text-align: center;
  max-width: 400px;
}
.icon {
  width: 80px;
  height: 80px;
  background: #52c41a;
  color: white;
  font-size: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}
h2 { margin-bottom: 1rem; }
.message { color: #333; margin-bottom: 0.5rem; }
.date {
  background: #f0f5ff;
  padding: 0.8rem;
  border-radius: 8px;
  margin: 1rem 0;
  color: #333;
}
.tip { color: #888; font-size: 0.9rem; margin-bottom: 1.5rem; }
.btn-login {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}
</style>
```

---

## 阶段四：聊天核心功能

### Task 7: 后端聊天接口和LLM服务

**Files:**
- Create: `backend/services/llm_service.py`
- Create: `backend/routes/chat.py`
- Create: `backend/routes/study.py`

- [ ] **Step 1: 创建 backend/services/llm_service.py**

```python
import json
import re
import requests
from config import Config
from prompts.system_prompt import SYSTEM_PROMPT

def build_messages(user, study_day, today_messages, current_message):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in today_messages:
        if msg.is_template or msg.role == 'assistant':
            messages.append({"role": "assistant", "content": msg.content})
        else:
            messages.append({"role": "user", "content": msg.content})

    messages.append({"role": "user", "content": current_message})
    return messages

def call_llm(messages):
    headers = {
        "Authorization": f"Bearer {Config.LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": Config.LLM_MODEL,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(Config.LLM_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"LLM API error: {e}")
        return None

def parse_llm_response(raw_text):
    try:
        return json.loads(raw_text.strip())
    except:
        pass

    match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    return {"intent": "other", "reply": "好的，请继续练习吧！"}

def get_system_prompt_for_group(group_type):
    return SYSTEM_PROMPT
```

- [ ] **Step 2: 创建 backend/routes/study.py**

```python
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from extensions import db
from models import User, DailyStatus, ChatMessage, SystemConfig
from services.llm_service import call_llm, parse_llm_response
import json
import os

study_bp = Blueprint('study', __name__)

def get_study_day(user_id):
    start_date_str = SystemConfig.query.get('study_start_date').value
    start = date.fromisoformat(start_date_str)
    delta = (date.today() - start).days + 1
    if delta < 1:
        return 0
    if delta > 10:
        return -1
    return delta

def get_today_status(user_id, study_day):
    today = date.today()
    status = DailyStatus.query.filter_by(user_id=user_id, study_day=study_day).first()
    if not status:
        status = DailyStatus(user_id=user_id, study_day=study_day, date=today)
        db.session.add(status)
        db.session.commit()
    return status

@study_bp.route('/study/status', methods=['GET'])
@jwt_required()
def get_status():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    study_day = get_study_day(user_id)

    if study_day == 0:
        phase = 'not_started'
    elif study_day == -1:
        phase = 'completed'
    elif study_day == 5:
        has_summary = db.session.query(db.exists().where(db.text(f"user_id={user_id}")).scalar()
        if not has_summary:
            phase = 'learning'
        else:
            phase = 'learning_phase2'
    elif study_day > 5:
        phase = 'learning_phase2'
    else:
        phase = 'learning'

    if phase == 'learning' and study_day == 5:
        from models import AssessmentSummary
        if not AssessmentSummary.query.filter_by(user_id=user_id).first():
            need_assessment = True
        else:
            need_assessment = False
    else:
        need_assessment = False

    today_status = get_today_status(user_id, study_day) if 1 <= study_day <= 10 else None

    return jsonify({
        'study_day': study_day,
        'phase': phase,
        'material_sent_today': today_status.material_sent if today_status else False,
        'remaining_rounds': 20 - (today_status.conversation_rounds if today_status else 0),
        'need_assessment': need_assessment
    })

@study_bp.route('/study/enter', methods=['POST'])
@jwt_required()
def study_enter():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    study_day = get_study_day(user_id)

    if study_day < 1 or study_day > 10:
        return jsonify({'auto_messages': []})

    today_status = get_today_status(user_id, study_day)

    if user.group_type == 'low':
        return jsonify({'auto_messages': []})

    if today_status.material_sent:
        return jsonify({'auto_messages': []})

    if user.group_type == 'adjustable':
        message = {"type": "text", "content": "您好！您现在想要练习法语吗？我可以给您发送今天的练习音频 😊"}
        today_status.material_sent = True
        db.session.commit()
        return jsonify({'auto_messages': [message]})

    if user.group_type == 'high':
        return jsonify({'auto_messages': []})

    return jsonify({'auto_messages': []})

@study_bp.route('/study/words', methods=['GET'])
@jwt_required()
def get_words():
    day = request.args.get('day', type=int)
    if not day or day < 1 or day > 10:
        return jsonify({'code': 400, 'message': 'Invalid day'}), 400

    words_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'words.json')
    with open(words_file, 'r', encoding='utf-8') as f:
        all_words = json.load(f)

    day_data = next((d for d in all_words if d['day'] == day), None)
    if not day_data:
        return jsonify({'code': 404, 'message': 'Words not found'}), 404

    return jsonify({'code': 200, 'words': day_data['words']})
```

- [ ] **Step 3: 创建 backend/routes/chat.py**

```python
from flask import Blueprint, jsonify, request, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from extensions import db
from models import User, DailyStatus, ChatMessage, SystemConfig
from services.llm_service import build_messages, call_llm, parse_llm_response
import json
import os

chat_bp = Blueprint('chat', __name__)

def get_study_day(user_id):
    start_date_str = SystemConfig.query.get('study_start_date').value
    from datetime import date
    start = date.fromisoformat(start_date_str)
    delta = (date.today() - start).days + 1
    if delta < 1: return 0
    if delta > 10: return -1
    return delta

def get_today_status(user_id, study_day):
    today = date.today()
    status = DailyStatus.query.filter_by(user_id=user_id, study_day=study_day).first()
    if not status:
        status = DailyStatus(user_id=user_id, study_day=study_day, date=today)
        db.session.add(status)
        db.session.commit()
    return status

def load_words_json():
    words_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'words.json')
    with open(words_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_material_messages(words, base_url=''):
    messages = []
    messages.append({"type": "text", "content": "好的，这是今天要学习的3个法语单词，请跟着音频练习吧！"})

    for word in words:
        messages.append({"type": "word_card", "content": {"french": word['french'], "chinese": word['chinese']}})
        audio_path = word['audio']
        if not audio_path.startswith('http'):
            audio_path = f"/static/audio/{audio_path}"
        messages.append({"type": "audio", "content": {"url": audio_path, "word": word['french']}})

    messages.append({"type": "text", "content": "以上是今天的3个单词，请跟着音频练习发音吧！你可以点击下方的🎤按钮录制你的跟读。"})
    return messages

@chat_bp.route('/chat/send', methods=['POST'])
@jwt_required()
def send_message():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    study_day = get_study_day(user_id)

    if study_day < 1 or study_day > 10:
        return jsonify({'code': 400, 'messages': [], 'remaining_rounds': 0})

    data = request.get_json()
    content = data.get('content', '')

    today_status = get_today_status(user_id, study_day)

    if today_status.conversation_rounds >= 20:
        return jsonify({
            'messages': [{"type": "text", "content": "今天的对话次数已用完啦，明天再来继续学习吧！😊"}],
            'remaining_rounds': 0
        })

    user_msg = ChatMessage(
        user_id=user_id,
        study_day=study_day,
        role='user',
        content_type='text',
        content=content
    )
    db.session.add(user_msg)
    db.session.commit()

    today_messages = ChatMessage.query.filter_by(
        user_id=user_id,
        study_day=study_day
    ).order_by(ChatMessage.timestamp).all()

    messages = build_messages(user, study_day, today_messages[:-1], content)

    raw_response = call_llm(messages)

    if not raw_response:
        llm_reply = "抱歉，服务出现问题，请稍后重试。"
        parsed = {"intent": "other", "reply": llm_reply}
    else:
        parsed = parse_llm_response(raw_response)

    reply_text = parsed.get('reply', '好的，请继续练习吧！')
    intent = parsed.get('intent', 'other')

    assistant_msgs = []

    if intent == 'request_material':
        if not today_status.material_sent:
            words_data = load_words_json()
            day_words = next((d for d in words_data if d['day'] == study_day), None)
            if day_words:
                today_status.material_sent = True
                material_msgs = build_material_messages(day_words['words'])
                for msg in material_msgs:
                    content_type = msg['type']
                    actual_content = msg['content'] if isinstance(msg['content'], str) else json.dumps(msg['content'])
                    assistant_msg = ChatMessage(
                        user_id=user_id,
                        study_day=study_day,
                        role='assistant',
                        content_type=content_type,
                        content=actual_content
                    )
                    db.session.add(assistant_msg)
                    assistant_msgs.append(msg)
                db.session.commit()

    elif intent == 'accept_learning':
        if not today_status.material_sent:
            words_data = load_words_json()
            day_words = next((d for d in words_data if d['day'] == study_day), None)
            if day_words:
                today_status.material_sent = True
                material_msgs = build_material_messages(day_words['words'])
                for msg in material_msgs:
                    content_type = msg['type']
                    actual_content = msg['content'] if isinstance(msg['content'], str) else json.dumps(msg['content'])
                    assistant_msg = ChatMessage(
                        user_id=user_id,
                        study_day=study_day,
                        role='assistant',
                        content_type=content_type,
                        content=actual_content
                    )
                    db.session.add(assistant_msg)
                    assistant_msgs.append(msg)
                db.session.commit()

    elif intent == 'reject_learning':
        today_status.rejected = True
        db.session.commit()

    elif intent == 'follow_up_practice':
        today_status.practice_count += 1
        today_status.conversation_rounds += 1
        db.session.commit()

    else:
        today_status.conversation_rounds += 1
        db.session.commit()

    final_response = assistant_msgs if assistant_msgs else [{"type": "text", "content": reply_text}]

    if not assistant_msgs:
        assistant_msg_db = ChatMessage(
            user_id=user_id,
            study_day=study_day,
            role='assistant',
            content_type='text',
            content=reply_text
        )
        db.session.add(assistant_msg_db)
        db.session.commit()

    return jsonify({
        'messages': final_response,
        'remaining_rounds': 20 - today_status.conversation_rounds
    })

@chat_bp.route('/chat/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    study_day = get_study_day(user_id)
    day = request.args.get('day', type=int) or study_day

    messages = ChatMessage.query.filter_by(
        user_id=user_id,
        study_day=day
    ).order_by(ChatMessage.timestamp).all()

    result = []
    for msg in messages:
        content = msg.content
        if msg.content_type == 'word_card':
            try:
                content = json.loads(msg.content)
            except:
                pass
        result.append({
            'id': msg.id,
            'role': msg.role,
            'type': msg.content_type,
            'content': content,
            'timestamp': msg.timestamp.isoformat()
        })

    return jsonify({'messages': result})

@chat_bp.route('/chat/upload_audio', methods=['POST'])
@jwt_required()
def upload_audio():
    user_id = get_jwt_identity()
    study_day = get_study_day(user_id)

    if study_day < 1 or study_day > 10:
        return jsonify({'code': 400, 'messages': [], 'remaining_rounds': 0})

    if 'audio' not in request.files:
        return jsonify({'code': 400, 'message': 'No audio file'}), 400

    audio_file = request.files['audio']
    word_index = request.form.get('word_index', type=int)

    from config import Config
    import time
    filename = f"day{study_day}_{word_index or 0}_{int(time.time())}.webm"
    user_dir = os.path.join(Config.UPLOAD_FOLDER, str(user_id))
    os.makedirs(user_dir, exist_ok=True)
    filepath = os.path.join(user_dir, filename)
    audio_file.save(filepath)

    from services.audio_service import validate_audio
    is_valid, reason = validate_audio(filepath)

    from models import AudioRecord
    audio_record = AudioRecord(
        user_id=user_id,
        study_day=study_day,
        word_index=word_index,
        target_word='',
        audio_path=filepath,
        is_valid=is_valid
    )
    db.session.add(audio_record)
    db.session.commit()

    today_status = get_today_status(user_id, study_day)

    if is_valid:
        today_status.practice_count += 1
        placeholder = f"[用户发送了单词的跟读录音]"
    else:
        today_status.invalid_audio_count += 1
        placeholder = "[该录音无效（空白/无声）]"

    today_status.conversation_rounds += 1
    db.session.commit()

    today_messages = ChatMessage.query.filter_by(
        user_id=user_id,
        study_day=study_day
    ).order_by(ChatMessage.timestamp).all()

    messages = build_messages(user, study_day, today_messages, placeholder)

    raw_response = call_llm(messages)

    if raw_response:
        parsed = parse_llm_response(raw_response)
        reply_text = parsed.get('reply', '练习得不错！继续加油！')
    else:
        reply_text = '练习得不错！继续加油！'

    assistant_msg = ChatMessage(
        user_id=user_id,
        study_day=study_day,
        role='assistant',
        content_type='text',
        content=reply_text
    )
    db.session.add(assistant_msg)
    db.session.commit()

    return jsonify({
        'messages': [{"type": "text", "content": reply_text}],
        'remaining_rounds': 20 - today_status.conversation_rounds
    })
```

- [ ] **Step 4: 创建 backend/services/audio_service.py**

```python
import os

def validate_audio(filepath):
    from pydub import AudioSegment
    from pydub.exceptions import CouldntDecodeError

    try:
        audio = AudioSegment.from_file(filepath)
        duration = len(audio) / 1000.0

        if duration < 0.5:
            return False, "音频时长不足0.5秒"

        if audio.dBFS < -50:
            return False, "音频音量过低"

        return True, "有效"
    except CouldntDecodeError:
        return False, "无法解码音频格式"
    except Exception as e:
        return False, f"检测失败: {str(e)}"
```

---

### Task 8: 前端聊天界面组件

**Files:**
- Create: `frontend/src/components/ChatBubble.vue`
- Create: `frontend/src/components/WordCard.vue`
- Create: `frontend/src/components/AudioPlayer.vue`
- Create: `frontend/src/components/AudioRecorder.vue`
- Create: `frontend/src/components/MessageList.vue`
- Create: `frontend/src/views/Chat.vue`

- [ ] **Step 1: 创建 frontend/src/components/ChatBubble.vue**

```vue
<template>
  <div :class="['bubble', isUser ? 'user' : 'assistant']">
    <div v-if="type === 'text'" class="text">{{ content }}</div>
    <WordCard v-else-if="type === 'word_card'" :data="parsedContent" />
    <AudioPlayer v-else-if="type === 'audio'" :url="content.url" :word="content.word" />
    <div v-else-if="type === 'user_audio'" class="user-audio">
      <AudioPlayer :url="content" :isUser="true" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import WordCard from './WordCard.vue'
import AudioPlayer from './AudioPlayer.vue'

const props = defineProps({
  content: [String, Object],
  type: { type: String, default: 'text' },
  isUser: { type: Boolean, default: false }
})

const parsedContent = computed(() => {
  if (typeof props.content === 'string') {
    try {
      return JSON.parse(props.content)
    } catch {
      return props.content
    }
  }
  return props.content
})
</script>

<style scoped>
.bubble {
  display: flex;
  margin-bottom: 1rem;
}
.bubble.user {
  justify-content: flex-end;
}
.bubble.assistant {
  justify-content: flex-start;
}
.text {
  max-width: 75%;
  padding: 0.8rem 1rem;
  border-radius: 16px;
  line-height: 1.5;
}
.user .text {
  background: #667eea;
  color: white;
  border-bottom-right-radius: 4px;
}
.assistant .text {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}
.user-audio {
  max-width: 75%;
}
</style>
```

- [ ] **Step 2: 创建 frontend/src/components/WordCard.vue**

```vue
<template>
  <div class="word-card">
    <div class="word">{{ data.french }}</div>
    <div class="meaning">{{ data.chinese }}</div>
  </div>
</template>

<script setup>
defineProps({
  data: { type: Object, required: true }
})
</script>

<style scoped>
.word-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  min-width: 120px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}
.word {
  font-size: 1.4rem;
  font-weight: bold;
  margin-bottom: 0.3rem;
}
.meaning {
  font-size: 1rem;
  opacity: 0.9;
}
</style>
```

- [ ] **Step 3: 创建 frontend/src/components/AudioPlayer.vue**

```vue
<template>
  <div :class="['audio-player', { user: isUser }]">
    <button class="play-btn" @click="togglePlay">
      {{ isPlaying ? '⏸' : '▶' }}
    </button>
    <div class="progress-bar" @click="seek">
      <div class="progress" :style="{ width: progress + '%' }"></div>
    </div>
    <span class="time">{{ formatTime(currentTime) }}</span>
    <audio ref="audioEl" :src="url" @timeupdate="updateTime" @ended="isPlaying = false"></audio>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  url: { type: String, required: true },
  word: { type: String, default: '' },
  isUser: { type: Boolean, default: false }
})

const audioEl = ref(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const progress = ref(0)

const togglePlay = () => {
  if (!audioEl.value) return
  if (isPlaying.value) {
    audioEl.value.pause()
  } else {
    audioEl.value.play()
  }
  isPlaying.value = !isPlaying.value
}

const updateTime = () => {
  if (!audioEl.value) return
  currentTime.value = audioEl.value.currentTime
  duration.value = audioEl.value.duration || 0
  progress.value = duration.value ? (currentTime.value / duration.value) * 100 : 0
}

const seek = (e) => {
  if (!audioEl.value || !duration.value) return
  const rect = e.target.getBoundingClientRect()
  const percent = (e.clientX - rect.left) / rect.width
  audioEl.value.currentTime = percent * duration.value
}

const formatTime = (s) => {
  if (!s || isNaN(s)) return '0:00'
  const m = Math.floor(s / 60)
  const sec = Math.floor(s % 60)
  return `${m}:${sec.toString().padStart(2, '0')}`
}
</script>

<style scoped>
.audio-player {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  padding: 0.6rem 1rem;
  border-radius: 24px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  min-width: 200px;
}
.audio-player.user {
  background: #667eea;
  color: white;
}
.play-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #667eea;
  color: white;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.user .play-btn {
  background: white;
  color: #667eea;
}
.progress-bar {
  flex: 1;
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  cursor: pointer;
}
.user .progress-bar {
  background: rgba(255,255,255,0.5);
}
.progress {
  height: 100%;
  background: #667eea;
  border-radius: 2px;
}
.user .progress {
  background: white;
}
.time {
  font-size: 0.75rem;
  color: #888;
  min-width: 35px;
}
.user .time {
  color: rgba(255,255,255,0.8);
}
</style>
```

- [ ] **Step 4: 创建 frontend/src/components/AudioRecorder.vue**

```template>
  <div class="recorder">
    <button :class="['record-btn', { recording: isRecording }]" @mousedown="startRecording" @mouseup="stopRecording" @touchstart.prevent="startRecording" @touchend.prevent="stopRecording">
      {{ isRecording ? '⏹' : '🎤' }}
    </button>
    <span class="hint">{{ isRecording ? '松开结束' : '按住录音' }}</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['recorded'])
const isRecording = ref(false)
let mediaRecorder = null
let audioChunks = []

const startRecording = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []

    mediaRecorder.ondataavailable = (e) => {
      audioChunks.push(e.data)
    }

    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: 'audio/webm' })
      emit('recorded', blob)
      stream.getTracks().forEach(track => track.stop())
    }

    mediaRecorder.start()
    isRecording.value = true
  } catch (e) {
    alert('无法访问麦克风，请检查权限设置')
  }
}

const stopRecording = () => {
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.stop()
    isRecording.value = false
  }
}
</script>

<style scoped>
.recorder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}
.record-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background: #667eea;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
}
.record-btn.recording {
  background: #f5222d;
  animation: pulse 1s infinite;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}
.hint {
  font-size: 0.7rem;
  color: #888;
}
</style>
```

- [ ] **Step 5: 创建 frontend/src/components/MessageList.vue**

```vue
<template>
  <div class="message-list" ref="listEl">
    <div v-if="showDateDivider" class="date-divider">
      <span>Day {{ studyDay }} · {{ formattedDate }}</span>
    </div>
    <ChatBubble
      v-for="msg in messages"
      :key="msg.id || msg.timestamp"
      :content="msg.content"
      :type="msg.type"
      :isUser="msg.role === 'user'"
    />
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import ChatBubble from './ChatBubble.vue'

const props = defineProps({
  messages: { type: Array, default: () => [] },
  studyDay: { type: Number, default: 1 }
})

const listEl = ref(null)

const formattedDate = new Date().toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' })
const showDateDivider = ref(true)

const scrollToBottom = () => {
  nextTick(() => {
    if (listEl.value) {
      listEl.value.scrollTop = listEl.value.scrollHeight
    }
  })
}

watch(() => props.messages.length, scrollToBottom)
</script>

<style scoped>
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
}
.date-divider {
  text-align: center;
  color: #999;
  font-size: 0.85rem;
  padding: 0.5rem 0;
  margin: 0.5rem 0;
}
.date-divider span {
  background: #e8e8e8;
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
}
</style>
```

- [ ] **Step 6: 创建 frontend/src/views/Chat.vue**

```vue
<template>
  <div class="chat-page">
    <header class="chat-header">
      <div class="avatar">
        <img :src="`/avatars/${avatarType}.png`" :alt="avatarType">
      </div>
      <div class="info">
        <h3>法语学习助手</h3>
        <span class="day">Day {{ studyDay }}</span>
      </div>
    </header>

    <MessageList :messages="chatMessages" :studyDay="studyDay" />

    <div v-if="remainingRounds === 0" class="rounds-exceeded">
      今天的对话次数已用完啦，明天再来继续学习吧！
    </div>

    <footer class="chat-footer">
      <AudioRecorder @recorded="handleRecorded" />
      <div class="input-area">
        <input v-model="inputText" type="text" placeholder="输入消息..." @keyup.enter="sendMessage" :disabled="remainingRounds === 0">
        <button @click="sendMessage" :disabled="!inputText.trim() || remainingRounds === 0">发送</button>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import { useUserStore } from '@/stores/user'
import { useStudyStore } from '@/stores/study'
import MessageList from '@/components/MessageList.vue'
import AudioRecorder from '@/components/AudioRecorder.vue'

const userStore = useUserStore()
const studyStore = useStudyStore()

const inputText = ref('')
const chatMessages = ref([])
const studyDay = ref(1)
const remainingRounds = ref(20)
const avatarType = ref('human')

const loadHistory = async () => {
  try {
    const res = await api.get('/chat/history')
    chatMessages.value = res.messages || []
  } catch (e) {
    console.error('Failed to load history', e)
  }
}

const sendMessage = async () => {
  if (!inputText.value.trim()) return

  const text = inputText.value
  inputText.value = ''

  chatMessages.value.push({
    id: Date.now(),
    role: 'user',
    type: 'text',
    content: text,
    timestamp: new Date().toISOString()
  })

  try {
    const res = await api.post('/chat/send', { content: text })

    if (res.messages) {
      res.messages.forEach(msg => {
        chatMessages.value.push({
          id: Date.now() + Math.random(),
          role: 'assistant',
          type: msg.type,
          content: msg.content,
          timestamp: new Date().toISOString()
        })
      })
    }

    remainingRounds.value = res.remaining_rounds
  } catch (e) {
    console.error('Failed to send message', e)
  }
}

const handleRecorded = async (blob) => {
  const formData = new FormData()
  formData.append('audio', blob, 'recording.webm')

  try {
    const res = await api.post('/chat/upload_audio', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    chatMessages.value.push({
      id: Date.now(),
      role: 'user',
      type: 'user_audio',
      content: URL.createObjectURL(blob),
      timestamp: new Date().toISOString()
    })

    if (res.messages) {
      res.messages.forEach(msg => {
        chatMessages.value.push({
          id: Date.now() + Math.random(),
          role: 'assistant',
          type: msg.type,
          content: msg.content,
          timestamp: new Date().toISOString()
        })
      })
    }

    remainingRounds.value = res.remaining_rounds
  } catch (e) {
    console.error('Failed to upload audio', e)
  }
}

const callEnterAPI = async () => {
  try {
    const res = await api.post('/study/enter')
    if (res.auto_messages && res.auto_messages.length > 0) {
      res.auto_messages.forEach(msg => {
        chatMessages.value.push({
          id: Date.now() + Math.random(),
          role: 'assistant',
          type: msg.type,
          content: msg.content,
          timestamp: new Date().toISOString()
        })
      })
    }
  } catch (e) {
    console.error('Failed to call enter API', e)
  }
}

onMounted(async () => {
  await userStore.fetchProfile()
  avatarType.value = userStore.avatarType || 'human'
  await studyStore.fetchStatus()
  studyDay.value = studyStore.studyDay || 1
  remainingRounds.value = studyStore.remainingRounds || 20

  await loadHistory()
  await callEnterAPI()

  let hiddenAt = null
  document.addEventListener('visibilitychange', async () => {
    if (document.hidden) {
      hiddenAt = Date.now()
    } else {
      if (hiddenAt && (Date.now() - hiddenAt) > 5 * 60 * 1000) {
        await loadHistory()
        await callEnterAPI()
      }
      hiddenAt = null
    }
  })
})
</script>

<style scoped>
.chat-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f5f5f5;
  max-width: 500px;
  margin: 0 auto;
  background: white;
}
.chat-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem 1rem;
  background: white;
  border-bottom: 1px solid #eee;
}
.avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
.info h3 {
  font-size: 1rem;
  margin: 0;
}
.info .day {
  font-size: 0.75rem;
  color: #888;
}
.chat-footer {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem;
  background: white;
  border-top: 1px solid #eee;
}
.input-area {
  flex: 1;
  display: flex;
  gap: 0.5rem;
}
.input-area input {
  flex: 1;
  padding: 0.6rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}
.input-area button {
  padding: 0.6rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}
.input-area button:disabled {
  background: #ccc;
}
.rounds-exceeded {
  text-align: center;
  padding: 0.8rem;
  background: #fff7e6;
  color: #fa8c16;
  font-size: 0.9rem;
}
</style>
```

---

## 阶段五：测评系统

### Task 9: 后端测评接口

**Files:**
- Create: `backend/routes/assessment.py`

- [ ] **Step 1: 创建 backend/routes/assessment.py**

```python
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, AssessmentAnswer, AssessmentSummary
import json
import os
import random

assessment_bp = Blueprint('assessment', __name__)

def load_words_json():
    words_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'words.json')
    with open(words_file, 'r', encoding='utf-8') as f:
        return json.load(f)

@assessment_bp.route('/assessment/check', methods=['GET'])
@jwt_required()
def check_assessment():
    user_id = get_jwt_identity()

    existing = AssessmentSummary.query.filter_by(user_id=user_id).first()
    if existing:
        return jsonify({'code': 200, 'can_take': False, 'already_completed': True})

    from routes.study import get_study_day
    study_day = get_study_day(user_id)

    if study_day == 5:
        return jsonify({'code': 200, 'can_take': True, 'already_completed': False})

    return jsonify({'code': 200, 'can_take': False, 'already_completed': False})

@assessment_bp.route('/assessment/questions', methods=['GET'])
@jwt_required()
def get_questions():
    words_data = load_words_json()
    day1_5_words = []
    for day_data in words_data[:5]:
        for word in day_data['words']:
            day1_5_words.append({
                'french': word['french'],
                'chinese': word['chinese'],
                'audio': f"/static/audio/{word['audio']}"
            })

    all_chinese = [w['chinese'] for w in day1_5_words]

    questions = []
    for i, word in enumerate(day1_5_words):
        options = random.sample([c for c in all_chinese if c != word['chinese']], 3)
        options.append(word['chinese'])
        random.shuffle(options)

        questions.append({
            'id': i + 1,
            'french': word['french'],
            'options': options,
            'audio_url': word['audio']
        })

    random.shuffle(questions)

    return jsonify({'code': 200, 'questions': questions})

@assessment_bp.route('/assessment/submit', methods=['POST'])
@jwt_required()
def submit_assessment():
    user_id = get_jwt_identity()
    data = request.get_json()
    answers = data.get('answers', [])

    words_data = load_words_json()
    word_map = {}
    for day_data in words_data[:5]:
        for word in day_data['words']:
            word_map[word['french']] = word['chinese']

    correct_count = 0
    total_count = len(answers)

    for answer in answers:
        question_id = answer['question_id']
        user_choice = answer['user_choice']

        questions_res = get_questions()
        question = next((q for q in questions_res.json['questions'] if q['id'] == question_id), None)
        if not question:
            continue

        correct = question['options'][question['options'].index(user_choice)] == user_choice

        if correct:
            correct_count += 1

        record = AssessmentAnswer(
            user_id=user_id,
            word_french=question['french'],
            correct_chinese=word_map.get(question['french'], ''),
            user_choice=user_choice,
            is_correct=correct
        )
        db.session.add(record)

    db.session.commit()

    vocab_score = (correct_count / total_count) * 100 if total_count > 0 else 0

    summary = AssessmentSummary(
        user_id=user_id,
        vocab_score=vocab_score,
        pronunciation_avg=None,
        total_score=vocab_score
    )
    db.session.add(summary)
    db.session.commit()

    return jsonify({
        'code': 200,
        'vocab_score': round(vocab_score, 1),
        'pronunciation_avg': None,
        'total_score': round(vocab_score, 1),
        'correct_count': correct_count,
        'total_count': total_count
    })

@assessment_bp.route('/assessment/result', methods=['GET'])
@jwt_required()
def get_result():
    user_id = get_jwt_identity()
    summary = AssessmentSummary.query.filter_by(user_id=user_id).first()

    if not summary:
        return jsonify({'code': 404, 'message': 'No result found'})

    return jsonify({
        'code': 200,
        'vocab_score': summary.vocab_score,
        'pronunciation_avg': summary.pronunciation_avg,
        'total_score': summary.total_score
    })
```

---

### Task 10: 前端测评页面

**Files:**
- Create: `frontend/src/components/AssessmentQuestion.vue`
- Create: `frontend/src/views/Assessment.vue`
- Create: `frontend/src/views/Result.vue`
- Create: `frontend/src/views/Waiting.vue`
- Create: `frontend/src/views/Completed.vue`

- [ ] **Step 1: 创建 frontend/src/components/AssessmentQuestion.vue**

```vue
<template>
  <div class="question">
    <div class="progress">{{ current + 1 }} / {{ total }}</div>
    <div class="word">{{ question.french }}</div>
    <div class="options">
      <button
        v-for="(option, idx) in question.options"
        :key="idx"
        :class="['option', { selected: selected === option }]"
        @click="selectOption(option)"
      >
        {{ option }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  question: { type: Object, required: true },
  current: { type: Number, required: true },
  total: { type: Number, required: true }
})

const emit = defineEmits(['answered'])
const selected = ref(null)

const selectOption = (option) => {
  selected.value = option
  setTimeout(() => {
    emit('answered', { question_id: props.question.id, user_choice: option })
    selected.value = null
  }, 300)
}

watch(() => props.question, () => {
  selected.value = null
})
</script>

<style scoped>
.question {
  text-align: center;
  padding: 2rem 1rem;
}
.progress {
  color: #888;
  margin-bottom: 1.5rem;
}
.word {
  font-size: 2.5rem;
  color: #667eea;
  margin-bottom: 2rem;
}
.options {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  max-width: 300px;
  margin: 0 auto;
}
.option {
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  background: white;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}
.option:hover {
  border-color: #667eea;
}
.option.selected {
  border-color: #667eea;
  background: #667eea;
  color: white;
}
</style>
```

- [ ] **Step 2: 创建 frontend/src/views/Assessment.vue**

```vue
<template>
  <div class="assessment-page">
    <div class="container">
      <AssessmentQuestion
        v-if="currentQuestion"
        :question="currentQuestion"
        :current="currentIndex"
        :total="questions.length"
        @answered="handleAnswer"
      />
      <div v-else-if="loading" class="loading">加载中...</div>
      <div v-else class="complete">测评已完成</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import AssessmentQuestion from '@/components/AssessmentQuestion.vue'

const router = useRouter()
const loading = ref(true)
const questions = ref([])
const currentIndex = ref(0)
const answers = ref([])
const loading = ref(true)

const currentQuestion = ref(null)

const loadQuestions = async () => {
  try {
    const res = await api.get('/assessment/questions')
    questions.value = res.questions
    currentQuestion.value = questions.value[0]
  } catch (e) {
    console.error('Failed to load questions', e)
  } finally {
    loading.value = false
  }
}

const handleAnswer = async (answer) => {
  answers.value.push(answer)

  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    currentQuestion.value = questions.value[currentIndex.value]
  } else {
    await submitAssessment()
  }
}

const submitAssessment = async () => {
  try {
    const res = await api.post('/assessment/submit', { answers: answers.value })
    router.push('/result')
  } catch (e) {
    console.error('Failed to submit', e)
  }
}

onMounted(loadQuestions)
</script>

<style scoped>
.assessment-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-top: 2rem;
}
.container {
  max-width: 400px;
  margin: 0 auto;
  background: white;
  min-height: calc(100vh - 4rem);
  border-radius: 16px 16px 0 0;
}
.loading, .complete {
  text-align: center;
  padding: 3rem;
  color: #888;
}
</style>
```

- [ ] **Step 3: 创建 frontend/src/views/Result.vue**

```vue
<template>
  <div class="result-page">
    <div class="container">
      <h2>测评结果</h2>
      <div class="score">{{ result.total_score || 0 }}</div>
      <div class="label">综合得分</div>
      <div class="details">
        <div class="detail-item">
          <span class="label">词义正确率</span>
          <span class="value">{{ result.vocab_score || 0 }}%</span>
        </div>
      </div>
      <div class="comment">{{ comment }}</div>
      <button class="btn-continue" @click="goToChat">进入学习</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const result = ref({})

const comment = computed(() => {
  const score = result.value.total_score || 0
  if (score >= 90) return '优秀！🎉'
  if (score >= 70) return '不错！👍'
  if (score >= 50) return '继续加油！💪'
  return '还有很大进步空间，继续努力！'
})

const loadResult = async () => {
  try {
    const res = await api.get('/assessment/result')
    result.value = res
  } catch (e) {
    console.error('Failed to load result', e)
  }
}

const goToChat = () => {
  router.push('/chat')
}

onMounted(loadResult)
</script>

<style scoped>
.result-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}
.container {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  text-align: center;
  max-width: 350px;
  width: 100%;
}
h2 { margin-bottom: 1.5rem; }
.score {
  font-size: 4rem;
  font-weight: bold;
  color: #667eea;
}
.label {
  color: #888;
  margin-bottom: 1.5rem;
}
.details {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}
.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.3rem 0;
}
.comment {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}
.btn-continue {
  width: 100%;
  padding: 0.8rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}
</style>
```

- [ ] **Step 4: 创建 frontend/src/views/Waiting.vue**

```vue
<template>
  <div class="waiting-page">
    <div class="container">
      <div class="icon">📚</div>
      <h2>学习尚未开始</h2>
      <p>学习将于 <strong>{{ studyStartDate }}</strong> 开始</p>
      <p class="tip">请届时再来</p>
      <button class="btn-logout" @click="logout">退出登录</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const studyStartDate = computed(() => {
  return localStorage.getItem('study_start_date') || '待定'
})

const logout = () => {
  userStore.logout()
  router.push('/')
}
</script>

<style scoped>
.waiting-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.container {
  background: white;
  padding: 3rem 2rem;
  border-radius: 16px;
  text-align: center;
  max-width: 350px;
}
.icon { font-size: 4rem; margin-bottom: 1rem; }
h2 { margin-bottom: 1rem; }
p { margin-bottom: 0.5rem; }
.tip { color: #888; margin-bottom: 2rem; }
.btn-logout {
  padding: 0.6rem 1.5rem;
  background: none;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
}
</style>
```

- [ ] **Step 5: 创建 frontend/src/views/Completed.vue**

```vue
<template>
  <div class="completed-page">
    <div class="container">
      <div class="icon">🎉</div>
      <h2>学习已完成</h2>
      <p>感谢您的参与！</p>
      <p class="sub">您已完成全部10天的法语学习</p>
      <button class="btn-logout" @click="logout">退出登录</button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const logout = () => {
  userStore.logout()
  router.push('/')
}
</script>

<style scoped>
.completed-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}
.container {
  background: white;
  padding: 3rem 2rem;
  border-radius: 16px;
  text-align: center;
  max-width: 350px;
}
.icon { font-size: 4rem; margin-bottom: 1rem; }
h2 { margin-bottom: 0.5rem; }
p { margin-bottom: 0.3rem; }
.sub { color: #888; margin-bottom: 2rem; }
.btn-logout {
  padding: 0.6rem 1.5rem;
  background: none;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
}
</style>
```

---

## 阶段六：管理后台

### Task 11: 后端管理接口

**Files:**
- Create: `backend/routes/admin.py`

- [ ] **Step 1: 创建 backend/routes/admin.py**

```python
from flask import Blueprint, request, jsonify, Response
from werkzeug.security import check_password_hash
import csv
import io
from extensions import db
from models import User, DailyStatus, ChatMessage, AudioRecord, AssessmentSummary, GroupSlot, SystemConfig
from config import Config

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        admin_token = request.headers.get('Admin-Token')
        if admin_token != Config.ADMIN_PASSWORD:
            return jsonify({'code': 401, 'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if data.get('username') == Config.ADMIN_USERNAME and data.get('password') == Config.ADMIN_PASSWORD:
        return jsonify({'code': 200, 'admin_token': Config.ADMIN_PASSWORD})
    return jsonify({'code': 401, 'message': 'Invalid credentials'}), 401

@admin_bp.route('/admin/dashboard', methods=['GET'])
@admin_required
def dashboard():
    total_users = User.query.count()

    group_stats = db.session.query(
        User.group_type,
        User.avatar_type,
        db.func.count(User.id)
    ).group_by(User.group_type, User.avatar_type).all()

    slots = GroupSlot.query.all()
    slot_info = [{'group_type': s.group_type, 'avatar_type': s.avatar_type, 'current': s.current_count, 'max': s.max_count} for s in slots]

    completed_assessments = AssessmentSummary.query.count()

    return jsonify({
        'code': 200,
        'total_users': total_users,
        'group_stats': [{'group_type': g[0], 'avatar_type': g[1], 'count': g[2]} for g in group_stats],
        'slots': slot_info,
        'completed_assessments': completed_assessments
    })

@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return jsonify({
        'code': 200,
        'users': [{
            'id': u.id,
            'nickname': u.nickname,
            'phone': u.phone,
            'group_type': u.group_type,
            'avatar_type': u.avatar_type,
            'wechat_bound': bool(u.wechat_openid),
            'created_at': u.created_at.isoformat()
        } for u in users]
    })

@admin_bp.route('/admin/export/chat', methods=['GET'])
@admin_required
def export_chat():
    messages = db.session.query(
        ChatMessage, User.group_type, User.avatar_type
    ).join(User).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['user_id', 'group_type', 'avatar_type', 'study_day', 'role', 'content_type', 'content', 'timestamp'])

    for msg, group_type, avatar_type in messages:
        writer.writerow([msg.user_id, group_type, avatar_type, msg.study_day, msg.role, msg.content_type, msg.content, msg.timestamp.isoformat()])

    return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=chat_export.csv'})

@admin_bp.route('/admin/export/daily', methods=['GET'])
@admin_required
def export_daily():
    statuses = DailyStatus.query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['user_id', 'study_day', 'date', 'material_sent', 'rejected', 'practice_count', 'invalid_audio_count', 'conversation_rounds'])

    for s in statuses:
        writer.writerow([s.user_id, s.study_day, s.date.isoformat(), s.material_sent, s.rejected, s.practice_count, s.invalid_audio_count, s.conversation_rounds])

    return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=daily_export.csv'})

@admin_bp.route('/admin/export/assessment', methods=['GET'])
@admin_required
def export_assessment():
    results = db.session.query(
        AssessmentSummary, User
    ).join(User).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['user_id', 'nickname', 'group_type', 'avatar_type', 'vocab_score', 'pronunciation_avg', 'total_score'])

    for summary, user in results:
        writer.writerow([user.id, user.nickname, user.group_type, user.avatar_type, summary.vocab_score, summary.pronunciation_avg, summary.total_score])

    return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=assessment_export.csv'})

@admin_bp.route('/admin/config', methods=['POST'])
@admin_required
def update_config():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')

    if key and value:
        config = SystemConfig.query.get(key)
        if config:
            config.value = value
        else:
            db.session.add(SystemConfig(key=key, value=value))
        db.session.commit()

    return jsonify({'code': 200, 'message': 'Config updated'})
```

---

### Task 12: 前端管理后台页面

**Files:**
- Create: `frontend/src/views/admin/AdminLogin.vue`
- Create: `frontend/src/views/admin/Dashboard.vue`

- [ ] **Step 1: 创建 frontend/src/views/admin/AdminLogin.vue**

```vue
<template>
  <div class="admin-login-page">
    <div class="form-container">
      <h2>管理员登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="form.username" type="text" required>
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="form.password" type="password" required>
        </div>
        <button type="submit" class="btn-submit">登录</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/api'

const router = useRouter()
const form = ref({ username: '', password: '' })

const handleLogin = async () => {
  try {
    const res = await api.post('/admin/login', form.value)
    if (res.code === 200) {
      localStorage.setItem('admin_token', res.admin_token)
      router.push('/admin/dashboard')
    }
  } catch (e) {
    alert('登录失败')
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1a1a2e;
}
.form-container {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 350px;
}
h2 { text-align: center; margin-bottom: 1.5rem; }
.form-group { margin-bottom: 1rem; }
label { display: block; margin-bottom: 0.3rem; font-weight: 500; }
input { width: 100%; padding: 0.6rem; border: 1px solid #ddd; border-radius: 6px; }
.btn-submit { width: 100%; padding: 0.8rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; margin-top: 0.5rem; }
</style>
```

- [ ] **Step 2: 创建 frontend/src/views/admin/Dashboard.vue**

```vue
<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>管理后台</h1>
      <button @click="logout">退出</button>
    </header>

    <div class="stats">
      <div class="stat-card">
        <div class="value">{{ stats.total_users }}</div>
        <div class="label">总用户数</div>
      </div>
      <div class="stat-card">
        <div class="value">{{ stats.completed_assessments }}</div>
        <div class="label">完成测评</div>
      </div>
    </div>

    <div class="section">
      <h2>分组统计</h2>
      <table class="data-table">
        <thead>
          <tr>
            <th>组别</th>
            <th>头像</th>
            <th>当前/最大</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="slot in stats.slots" :key="`${slot.group_type}-${slot.avatar_type}`">
            <td>{{ slot.group_type }}</td>
            <td>{{ slot.avatar_type }}</td>
            <td>{{ slot.current }} / {{ slot.max }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="section">
      <h2>数据导出</h2>
      <div class="export-buttons">
        <button @click="exportData('chat')">聊天记录</button>
        <button @click="exportData('daily')">每日数据</button>
        <button @click="exportData('assessment')">测评成绩</button>
      </div>
    </div>

    <div class="section">
      <h2>用户列表</h2>
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>昵称</th>
            <th>组别</th>
            <th>头像</th>
            <th>微信</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.nickname }}</td>
            <td>{{ user.group_type }}</td>
            <td>{{ user.avatar_type }}</td>
            <td>{{ user.wechat_bound ? '✓' : '✗' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const stats = ref({ slots: [], group_stats: [], total_users: 0, completed_assessments: 0 })
const users = ref([])

const loadDashboard = async () => {
  try {
    const res = await api.get('/admin/dashboard', { headers: { 'Admin-Token': localStorage.getItem('admin_token') } })
    stats.value = res
    const usersRes = await api.get('/admin/users', { headers: { 'Admin-Token': localStorage.getItem('admin_token') } })
    users.value = usersRes.users
  } catch (e) {
    console.error('Failed to load dashboard', e)
  }
}

const exportData = async (type) => {
  window.open(`/api/admin/export/${type}`, '_blank')
}

const logout = () => {
  localStorage.removeItem('admin_token')
  router.push('/admin')
}

onMounted(loadDashboard)
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 1rem;
}
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.dashboard-header h1 { font-size: 1.5rem; }
.dashboard-header button {
  padding: 0.5rem 1rem;
  background: #f5222d;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
}
.stat-card .value { font-size: 2rem; font-weight: bold; color: #667eea; }
.stat-card .label { color: #888; margin-top: 0.3rem; }
.section {
  background: white;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
}
.section h2 { font-size: 1.1rem; margin-bottom: 1rem; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}
.data-table th { font-weight: 500; color: #888; }
.export-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.export-buttons button {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
```

---

## 阶段七：部署配置

### Task 13: 部署脚本和配置

**Files:**
- Create: `nginx.conf`
- Create: `backend/gunicorn_config.py`
- Create: `deploy.sh`
- Create: `README.md`

- [ ] **Step 1: 创建 nginx.conf**

```nginx
server {
    listen 80;
    server_name _;
    client_max_body_size 10M;

    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /wechat/ {
        proxy_pass http://127.0.0.1:5000;
    }

    location /static/audio/ {
        alias /path/to/backend/static/audio/;
    }

    location /uploads/ {
        alias /path/to/backend/uploads/;
    }
}
```

- [ ] **Step 2: 创建 backend/gunicorn_config.py**

```python
bind = "127.0.0.1:5000"
workers = 4
worker_class = "gevent"
timeout = 120
```

- [ ] **Step 3: 创建 deploy.sh**

```bash
#!/bin/bash

# 前端构建
cd /path/to/frontend
npm install
npm run build

# 后端依赖
cd /path/to/backend
pip install -r requirements.txt

# 复制静态文件
cp -r dist/* /path/to/backend/static/

# 重启服务
sudo systemctl restart french-backend
sudo nginx -s reload
```

- [ ] **Step 4: 创建 README.md**

```markdown
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
```

---

## 阶段八：静态资源和头像

### Task 14: 创建占位头像和音频目录结构

**Files:**
- Create: `frontend/public/avatars/human.png` (1x1透明占位)
- Create: `frontend/public/avatars/robot.png` (1x1透明占位)
- Create: `backend/static/audio/.gitkeep`

- [ ] **Step 1: 创建占位头像**

Run: `echo -n "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==" | base64 -d > frontend/public/avatars/human.png`
Run: `echo -n "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==" | base64 -d > frontend/public/avatars/robot.png`

- [ ] **Step 2: 创建音频目录结构**

Run: `mkdir -p backend/static/audio/day{1..10}`
Run: `touch backend/static/audio/.gitkeep`

---

## 计划执行总结

### 执行顺序

**阶段一 (Task 1-2):** 项目基础框架搭建
**阶段二 (Task 3-4):** 用户认证模块
**阶段三 (Task 5-6):** 微信绑定流程
**阶段四 (Task 7-8):** 聊天核心功能
**阶段五 (Task 9-10):** 测评系统
**阶段六 (Task 11-12):** 管理后台
**阶段七 (Task 13):** 部署配置
**阶段八 (Task 14):** 静态资源

### 关键注意事项

1. **先测试后端API**：确保所有接口正常工作后再开发前端
2. **LLM集成测试**：需要真实的API Key才能完整测试
3. **微信测试号**：需要提前申请并配置测试号
4. **音频文件**：实际部署时需要提供真实的法语单词音频文件
5. **HTTPS问题**：生产环境需要配置SSL证书解决麦克风权限问题

---

**Plan complete.** 计划已保存至 `docs/superpowers/plans/2026-04-02-french-learning-platform.md`

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

Which approach would you prefer?