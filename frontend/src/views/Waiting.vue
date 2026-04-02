<template>
  <div class="waiting-page">
    <div class="card fade-up">
      <div class="icon-wrap">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
      </div>
      <span class="tag">Patience</span>
      <h2>学习尚未开始</h2>
      <p>学习将于 <strong>{{ studyStartDate }}</strong> 正式开始</p>
      <p class="tip">届时请再次打开应用</p>
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
const studyStartDate = computed(() => localStorage.getItem('study_start_date') || '待定')

const logout = () => {
  userStore.logout()
  router.push('/')
}
</script>

<style scoped>
.waiting-page {
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
  color: var(--accent);
  margin-bottom: 1.2rem;
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
  margin: 0.3rem 0 1rem;
}
p {
  font-size: 0.9rem;
  color: var(--ink-secondary);
  margin-bottom: 0.3rem;
}
p strong { color: var(--ink); }
.tip {
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
