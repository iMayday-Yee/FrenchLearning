<template>
  <div class="login-page">
    <div class="decor-line"></div>
    <div class="form-card fade-up">
      <div class="form-header">
        <span class="form-tag">Bienvenue</span>
        <h2>欢迎回来</h2>
      </div>
      <form @submit.prevent="handleLogin">
        <div class="field">
          <label>邮箱</label>
          <input v-model="form.email" type="email" required placeholder="请输入邮箱">
        </div>
        <div class="field">
          <label>密码</label>
          <input v-model="form.password" type="password" required placeholder="请输入密码">
        </div>
        <button type="submit" class="btn-submit" :disabled="loading">
          <span v-if="!loading">登录</span>
          <span v-else class="loading-dots">登录中<span>.</span><span>.</span><span>.</span></span>
        </button>
      </form>
      <div class="form-footer">
        <span @click="$router.push('/reset-password')" class="forgot-link">忘记密码？</span>
        <span @click="$router.push('/register')">还没有账号？<strong>注册</strong></span>
      </div>
    </div>
    <router-link to="/" class="back-link fade-up" style="animation-delay:0.3s">← 返回首页</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const userStore = useUserStore()
const toast = useToastStore()
const loading = ref(false)
const form = ref({ email: '', password: '' })

const handleLogin = async () => {
  if (!form.value.email || !form.value.password) {
    toast.error('请输入邮箱和密码')
    return
  }
  loading.value = true
  try {
    const res = await api.post('/login', form.value)
    if (res.code === 200) {
      await userStore.setLogin(res)
      await userStore.fetchProfile()
      router.push('/chat')
    }
  } catch (e) {
    const msg = e.response?.data?.message
    if (e.response?.status === 401) toast.error(msg || '邮箱或密码错误')
    else toast.error(msg || '登录失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--bg);
  padding: 2rem;
  position: relative;
}
.decor-line {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--accent), var(--sage), var(--rose));
}
.form-card {
  width: 100%;
  max-width: 380px;
  background: var(--surface);
  padding: 2.5rem 2rem 2rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-light);
}
.form-header {
  text-align: center;
  margin-bottom: 2rem;
}
.form-tag {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-style: italic;
  color: var(--accent);
  letter-spacing: 0.1em;
}
.form-header h2 {
  font-family: var(--font-display);
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--ink);
  margin-top: 0.3rem;
}
.field {
  margin-bottom: 1.2rem;
}
.field label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--ink-secondary);
  margin-bottom: 0.4rem;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}
.field input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  font-size: 0.95rem;
  color: var(--ink);
  background: var(--bg);
  transition: all 0.2s var(--ease);
  outline: none;
}
.field input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-subtle);
}
.field input::placeholder { color: var(--ink-faint); }
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
  letter-spacing: 0.02em;
}
.btn-submit:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(123,155,244,0.2);
}
.btn-submit:disabled { opacity: 0.5; cursor: not-allowed; }
.loading-dots span {
  animation: blink 1.2s infinite;
}
.loading-dots span:nth-child(2) { animation-delay: 0.2s; }
.loading-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  font-size: 0.85rem;
  color: var(--ink-muted);
}
.form-footer span { cursor: pointer; transition: color 0.2s; }
.form-footer span:hover { color: var(--accent); }
.form-footer strong { font-weight: 600; color: var(--accent); }
.forgot-link { font-size: 0.8rem; }
.back-link {
  margin-top: 2rem;
  font-size: 0.85rem;
  color: var(--ink-muted);
  text-decoration: none;
  transition: color 0.2s;
}
.back-link:hover { color: var(--ink); }
</style>
