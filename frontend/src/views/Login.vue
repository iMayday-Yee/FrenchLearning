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
