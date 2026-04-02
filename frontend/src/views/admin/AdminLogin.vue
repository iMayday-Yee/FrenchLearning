<template>
  <div class="admin-login-page">
    <div class="form-card fade-up">
      <div class="form-header">
        <span class="tag">Administration</span>
        <h2>管理后台</h2>
      </div>
      <form @submit.prevent="handleLogin">
        <div class="field">
          <label>用户名</label>
          <input v-model="form.username" type="text" required>
        </div>
        <div class="field">
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
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const toast = useToastStore()
const form = ref({ username: '', password: '' })

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) {
    toast.error('请输入用户名和密码')
    return
  }
  try {
    const res = await api.post('/admin/login', form.value)
    if (res.code === 200) {
      localStorage.setItem('admin_token', res.admin_token)
      router.push('/admin/dashboard')
    }
  } catch (e) {
    if (e.response?.status === 401) toast.error('用户名或密码错误')
    else toast.error('登录失败，请稍后重试')
  }
}
</script>

<style scoped>
.admin-login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tint);
  padding: 2rem;
}
.form-card {
  width: 100%;
  max-width: 360px;
  background: var(--surface);
  padding: 2.5rem 2rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
}
.form-header { text-align: center; margin-bottom: 2rem; }
.tag {
  font-family: var(--font-display);
  font-size: 0.8rem;
  font-style: italic;
  color: var(--accent);
  letter-spacing: 0.1em;
}
h2 {
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--ink);
  margin-top: 0.2rem;
}
.field { margin-bottom: 1.2rem; }
.field label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--ink-secondary);
  margin-bottom: 0.35rem;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}
.field input {
  width: 100%;
  padding: 0.7rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  color: var(--ink);
  background: var(--bg);
  outline: none;
  transition: border-color 0.2s;
}
.field input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-subtle); }
.btn-submit {
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
  margin-top: 0.5rem;
}
.btn-submit:hover { background: var(--accent); transform: translateY(-1px); }
</style>
