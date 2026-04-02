<template>
  <div class="admin-login-page">
    <div class="form-container">
      <h2>管理员登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="form.username" type="text" required>
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="form.password" type="password" required>
        </div>
        <button type="submit" class="btn-submit">登录</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/api'

const router = useRouter()
const form = ref({ username: '', password: '' })

const handleLogin = async () => {
  try {
    const res = await api.post('/admin/login', form.value)
    if (res.code === 200) {
      localStorage.setItem('admin_token', res.admin_token)
      router.push('/admin/dashboard')
    }
  } catch (e) {
    alert('登录失败')
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1a1a2e;
}
.form-container {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 350px;
}
h2 { text-align: center; margin-bottom: 1.5rem; }
.form-group { margin-bottom: 1rem; }
label { display: block; margin-bottom: 0.3rem; font-weight: 500; }
input { width: 100%; padding: 0.6rem; border: 1px solid #ddd; border-radius: 6px; }
.btn-submit { width: 100%; padding: 0.8rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer; margin-top: 0.5rem; }
</style>
