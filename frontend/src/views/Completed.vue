<template>
  <div class="completed-page">
    <div class="card fade-up">
      <div class="icon-wrap">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
      </div>
      <span class="tag">Félicitations</span>
      <h2>体验已完成</h2>
      <p>您已完成本次小五智能助手体验，期待下次再见</p>
      <p class="sub">感谢您的参与和坚持</p>
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
  max-width: 360px;
  width: 100%;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-light);
}
.icon-wrap {
  color: var(--sage);
  margin-bottom: 1.2rem;
}
.tag {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-style: italic;
  color: var(--sage);
  letter-spacing: 0.1em;
}
h2 {
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--ink);
  margin: 0.3rem 0 1rem;
}
p {
  font-size: 0.9rem;
  color: var(--ink-secondary);
  margin-bottom: 0.3rem;
}
.sub {
  color: var(--ink-muted);
  margin-bottom: 2rem;
}
.btn-logout {
  padding: 0.6rem 1.5rem;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--ink-secondary);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-logout:hover {
  border-color: var(--ink-muted);
  color: var(--ink);
}
</style>
