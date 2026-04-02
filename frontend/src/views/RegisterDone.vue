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
