# 小五智能助手品牌重构 + 工具选择页 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将应用品牌从"法语学习助手"重构为"小五智能助手"平台，新增工具选择页，法语学习变为平台下的一个工具入口。

**Architecture:** 前端新增 ToolSelect.vue 作为登录后的工具选择页（`/home`），原 Home.vue 重命名为 Landing.vue 作为落地页（`/`）。路由守卫根据登录状态在两个页面间跳转。后端只改邮件文案。

**Tech Stack:** Vue 3 + Vite（前端），Flask（后端邮件服务）

**Note:** 本项目没有自动化测试，所有验证通过手动测试完成。WeChat 模板消息函数 `send_template_message` 目前未被调用，无需修改；未来启用时署名行用 `📚 法语学习助手 · 来自小五智能助手`。

---

### Task 1: 重命名 Home.vue 为 Landing.vue 并更新品牌文案

**Files:**
- Rename: `frontend/src/views/Home.vue` → `frontend/src/views/Landing.vue`
- Modify: `frontend/src/views/Landing.vue`（重命名后修改内容）

- [ ] **Step 1: 重命名文件**

```bash
cd /root/FrenchLearning
git mv frontend/src/views/Home.vue frontend/src/views/Landing.vue
```

- [ ] **Step 2: 更新品牌文案**

在 `frontend/src/views/Landing.vue` 中修改：

```html
<!-- 第4行：pill 标签改为平台标语 -->
<div class="pill fade-up" style="animation-delay:0.1s">Hi there !</div>

<!-- 第5行：标题 -->
<h1 class="title fade-up" style="animation-delay:0.2s">小五智能助手</h1>

<!-- 第6行：副标题 -->
<p class="subtitle fade-up" style="animation-delay:0.3s">你的智能学习与效率伙伴</p>
```

底部 footer-words 改为通用标语：

```html
<div class="footer-words fade-up" style="animation-delay:0.6s">
  <span>智能</span><span class="dot"></span>
  <span>高效</span><span class="dot"></span>
  <span>有趣</span>
</div>
```

- [ ] **Step 3: Commit**

```bash
git add -A
git commit -m "重命名 Home.vue 为 Landing.vue，更新品牌文案为小五智能助手"
```

---

### Task 2: 创建工具选择页 ToolSelect.vue

**Files:**
- Create: `frontend/src/views/ToolSelect.vue`

- [ ] **Step 1: 创建文件**

创建 `frontend/src/views/ToolSelect.vue`，内容如下：

```vue
<template>
  <div class="tool-select-page">
    <div class="tool-bg"></div>
    <header class="tool-header">
      <h2 class="greeting">你好，{{ nickname }} 👋</h2>
      <button class="btn-logout" @click="logout">退出</button>
    </header>
    <main class="tool-main">
      <p class="section-label">选择工具</p>
      <div class="tool-grid">
        <div class="tool-card" @click="goToFrench">
          <span class="tool-icon">🇫🇷</span>
          <div class="tool-info">
            <div class="tool-name">法语学习助手</div>
            <div class="tool-desc">每天三个词，轻松开启你的法语之旅</div>
          </div>
          <svg class="tool-arrow" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const nickname = computed(() => userStore.nickname || '同学')

onMounted(async () => {
  if (!userStore.nickname) {
    await userStore.fetchProfile()
  }
})

const goToFrench = () => router.push('/chat')

const logout = () => {
  userStore.logout()
  router.push('/')
}
</script>

<style scoped>
.tool-select-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  background: #F0F2F8;
}
.tool-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(ellipse 50% 40% at 10% 0%, rgba(123,155,244,0.06) 0%, transparent 70%),
    radial-gradient(ellipse 40% 50% at 90% 100%, rgba(123,205,168,0.05) 0%, transparent 70%);
}
.tool-header {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 1.5rem 0;
}
.greeting {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--ink);
}
.btn-logout {
  padding: 0.4rem 1rem;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--ink-secondary);
  font-size: 0.82rem;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-logout:hover {
  border-color: var(--ink-muted);
  color: var(--ink);
}
.tool-main {
  position: relative;
  z-index: 10;
  padding: 2rem 1.5rem;
  flex: 1;
}
.section-label {
  font-size: 0.85rem;
  color: var(--ink-muted);
  margin-bottom: 1rem;
  font-weight: 500;
}
.tool-grid {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}
.tool-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.2rem 1.2rem;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(228, 231, 238, 0.6);
  border-radius: var(--radius-lg, 12px);
  cursor: pointer;
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.tool-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(123,155,244,0.12);
  border-color: rgba(123,155,244,0.3);
}
.tool-icon {
  font-size: 2rem;
  flex-shrink: 0;
}
.tool-info {
  flex: 1;
  min-width: 0;
}
.tool-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 0.2rem;
}
.tool-desc {
  font-size: 0.82rem;
  color: var(--ink-secondary);
}
.tool-arrow {
  flex-shrink: 0;
  color: var(--ink-faint);
}
</style>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/ToolSelect.vue
git commit -m "新增工具选择页 ToolSelect.vue"
```

---

### Task 3: 更新路由配置

**Files:**
- Modify: `frontend/src/router/index.js`

- [ ] **Step 1: 更新路由表和守卫**

完整替换 `frontend/src/router/index.js` 内容：

```javascript
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('@/views/Landing.vue') },
  { path: '/home', component: () => import('@/views/ToolSelect.vue'), meta: { auth: true } },
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
  { path: '/ended', component: () => import('@/views/Ended.vue') },
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

  // 已登录用户访问落地页，跳转到工具选择页
  if (to.path === '/' && store.token) {
    return '/home'
  }

  // 注册页面检查：如果是第11天起，不允许注册
  if (to.path === '/register') {
    try {
      const res = await fetch('/api/study/can_register')
      const data = await res.json()
      if (!data.can_register) {
        return '/ended'
      }
    } catch (e) {
      // ignore, allow registration attempt
    }
  }

  if (to.path === '/chat') {
    const studyStore = (await import('@/stores/study')).useStudyStore()
    await studyStore.fetchStatus()
    if (studyStore.phase === 'not_started') return '/waiting'
    if (studyStore.phase === 'completed') return '/ended'
  }
})

export default router
```

关键变更：
- `Home.vue` → `Landing.vue`
- 新增 `/home` 路由指向 `ToolSelect.vue`（需登录）
- 新增守卫：已登录用户访问 `/` 时跳转到 `/home`

- [ ] **Step 2: Commit**

```bash
git add frontend/src/router/index.js
git commit -m "更新路由：Landing.vue + ToolSelect.vue + 已登录跳转逻辑"
```

---

### Task 4: 更新 index.html 标题

**Files:**
- Modify: `frontend/index.html`

- [ ] **Step 1: 修改 title**

```html
<!-- 第6行 -->
<title>小五智能助手</title>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/index.html
git commit -m "更新页面标题为小五智能助手"
```

---

### Task 5: 更新 Ended.vue 和 Completed.vue 文案

**Files:**
- Modify: `frontend/src/views/Ended.vue`
- Modify: `frontend/src/views/Completed.vue`

- [ ] **Step 1: 更新 Ended.vue**

```html
<!-- 第8行：标题 -->
<h2>体验已结束</h2>
<!-- 第9行：描述 -->
<p>本次小五智能助手体验已于 <strong>{{ endDate }}</strong> 结束</p>
```

- [ ] **Step 2: 更新 Completed.vue**

```html
<!-- 第8行：标题 -->
<h2>体验已完成</h2>
<!-- 第9行：描述 -->
<p>您已完成本次小五智能助手体验，期待下次再见</p>
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/Ended.vue frontend/src/views/Completed.vue
git commit -m "更新 Ended/Completed 页面文案为小五智能助手体验"
```

---

### Task 6: 更新邮件服务品牌文案

**Files:**
- Modify: `backend/services/email_service.py`

- [ ] **Step 1: 更新页脚（`_build_html_email` 函数，第39行）**

```python
<div style="font-size:12px;color:#9096A6;">小五智能助手 · <a href="https://xiaowu.quest" style="color:#7B9BF4;text-decoration:none;">xiaowu.quest</a></div>
```

- [ ] **Step 2: 更新验证码邮件（`send_verification_email` 函数）**

第72行正文：
```python
<p style="margin:0 0 24px;">你正在注册小五智能助手，请使用以下验证码完成验证：</p>
```

第83行主题：
```python
msg['Subject'] = '小五智能助手 - 邮箱验证码'
```

- [ ] **Step 3: 更新学习提醒邮件（`send_study_reminder` 函数）**

第104-111行正文，在开头加署名行：
```python
body_html = f"""
<p style="margin:0 0 6px;font-size:13px;color:#7B9BF4;font-weight:600;">📚 法语学习助手 · 来自小五智能助手</p>
<p style="margin:0 0 20px;">Bonjour !</p>
<p style="margin:0 0 8px;">今天是法语学习的<strong>第 {study_day} 天</strong>，今天的学习内容已经准备好了。</p>
<p style="margin:0 0 28px;color:#5E6478;">点击下方按钮开始今天的学习吧！</p>
<div style="text-align:center;margin:0 0 24px;">
  <a href="https://xiaowu.quest" style="display:inline-block;padding:12px 36px;background:linear-gradient(135deg,#7B9BF4 0%,#98B2F7 100%);border-radius:10px;font-size:15px;font-weight:600;color:#ffffff;text-decoration:none;">开始学习</a>
</div>
<p style="margin:0;color:#9096A6;font-size:13px;">每天坚持一点点，进步看得见。</p>
"""
```

第117行主题：
```python
msg['Subject'] = f'法语学习提醒 - 第{study_day}天 | 小五智能助手'
```

第118行纯文本备用：
```python
msg.attach(MIMEText(f'[法语学习助手 · 来自小五智能助手] 今天是法语学习第{study_day}天，打开 https://xiaowu.quest 开始学习吧！', 'plain', 'utf-8'))
```

- [ ] **Step 4: Commit**

```bash
git add backend/services/email_service.py
git commit -m "更新邮件服务品牌文案：小五智能助手 + 法语学习助手署名"
```

---

### Task 7: 更新登录后跳转目标

**Files:**
- Modify: `frontend/src/views/Login.vue`（第55-60行）

- [ ] **Step 1: 简化登录后跳转逻辑**

Login.vue 第55-60行当前有复杂的阶段判断跳转。现在登录后统一跳转到 `/home`（工具选择页），学习阶段判断由 `/chat` 路由守卫处理。

将第55-60行：
```javascript
      const studyStore = (await import('@/stores/study')).useStudyStore()
      await studyStore.fetchStatus()
      if (studyStore.phase === 'not_started') router.push('/waiting')
      else if (studyStore.phase === 'completed') router.push('/completed')
      else if (studyStore.needAssessment) router.push('/assessment')
      else router.push('/chat')
```

替换为：
```javascript
      router.push('/home')
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/Login.vue
git commit -m "登录成功后统一跳转到工具选择页"
```

---

### Task 8: 手动验证

- [ ] **Step 1: 启动前后端**

```bash
cd /root/FrenchLearning && ./start.sh
```

- [ ] **Step 2: 验证清单**

1. 未登录访问 `/` → 看到"小五智能助手"落地页
2. 点击登录 → 登录成功 → 跳转到 `/home` 工具选择页
3. 工具选择页显示用户名、法语学习助手卡片
4. 点击卡片 → 进入 `/chat`（或 `/waiting`/`/ended` 取决于学习阶段）
5. 已登录状态直接访问 `/` → 自动跳转到 `/home`
6. 浏览器标签显示"小五智能助手"
7. `/ended` 页面显示"本次小五智能助手体验已于...结束"
8. `/completed` 页面显示"您已完成本次小五智能助手体验，期待下次再见"
