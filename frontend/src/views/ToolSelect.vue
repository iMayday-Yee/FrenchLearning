<template>
  <div class="tool-select-page">
    <div class="tool-bg"></div>
    <header class="tool-header">
      <h2 class="greeting">你好，{{ nickname }} 👋</h2>
      <button class="btn-logout" @click="logout">退出登录</button>
    </header>
    <main class="tool-main">
      <p class="section-label">选择工具</p>
      <div class="tool-grid">
        <div class="tool-card" @click="goToFrench">
          <span class="tool-icon">🇫🇷</span>
          <div class="tool-info">
            <div class="tool-name">小五智能助手</div>
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
