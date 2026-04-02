<template>
  <div class="done-page">
    <div class="card fade-up">
      <div class="icon-wrap">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      </div>
      <span class="tag">Bienvenue</span>
      <h2>注册完成</h2>
      <p>您的账号已创建成功</p>
      <div class="date-card">
        学习将于 <strong>{{ studyStartDate }}</strong> 开始
      </div>
      <p class="tip">届时请打开应用开始学习</p>
      <button class="btn-login" @click="goLogin">前往登录</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const studyStartDate = computed(() => localStorage.getItem('study_start_date') || '待定')
const goLogin = () => router.push('/login')
</script>

<style scoped>
.done-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg);
  padding: 2rem;
}
.card {
  background: var(--surface);
  padding: 3rem 2.5rem;
  border-radius: var(--radius-lg);
  text-align: center;
  max-width: 380px;
  width: 100%;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-light);
}
.icon-wrap {
  color: var(--sage);
  margin-bottom: 1rem;
}
.tag {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-style: italic;
  color: var(--accent);
  letter-spacing: 0.1em;
}
h2 {
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--ink);
  margin: 0.3rem 0 0.5rem;
}
p {
  font-size: 0.9rem;
  color: var(--ink-secondary);
}
.date-card {
  background: var(--accent-subtle);
  padding: 0.9rem 1.2rem;
  border-radius: var(--radius);
  margin: 1.2rem 0;
  font-size: 0.9rem;
  color: var(--ink-secondary);
  border: 1px solid rgba(123,155,244,0.12);
}
.date-card strong { color: var(--ink); }
.tip {
  color: var(--ink-muted);
  font-size: 0.85rem;
  margin-bottom: 1.5rem;
}
.btn-login {
  width: 100%;
  padding: 0.85rem;
  background: var(--accent);
  color: var(--ink-on-dark);
  border: none;
  border-radius: var(--radius);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s var(--ease);
}
.btn-login:hover {
  background: var(--accent);
  transform: translateY(-1px);
}
</style>
