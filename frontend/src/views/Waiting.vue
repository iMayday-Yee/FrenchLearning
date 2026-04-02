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
