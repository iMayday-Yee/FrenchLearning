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
