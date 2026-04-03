<template>
  <div class="ended-page">
    <div class="card fade-up">
      <div class="icon-wrap">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      </div>
      <span class="tag">Fin</span>
      <h2>体验已结束</h2>
      <p>本次小五智能助手体验已于 <strong>{{ endDate }}</strong> 结束</p>
      <p class="tip">感谢您的参与</p>
      <button class="btn-logout" @click="logout">退出登录</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const studyStartDate = ref('')

onMounted(async () => {
  // 尝试从 userStore 获取
  if (userStore.studyStartDate) {
    studyStartDate.value = userStore.studyStartDate
  } else {
    // 未登录用户，从 can_register 接口获取
    try {
      const res = await fetch('/api/study/can_register')
      const data = await res.json()
      if (data.study_start_date) {
        studyStartDate.value = data.study_start_date
      }
    } catch (e) {
      // ignore
    }
  }
})

const endDate = computed(() => {
  if (studyStartDate.value) {
    const start = new Date(studyStartDate.value)
    start.setDate(start.getDate() + 9)
    return start.toISOString().split('T')[0]
  }
  return '10天学习周期'
})

const logout = () => {
  userStore.logout()
  router.push('/')
}
</script>

<style scoped>
.ended-page {
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
  color: var(--rose);
  margin-bottom: 1.2rem;
}
.tag {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-style: italic;
  color: var(--rose);
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
