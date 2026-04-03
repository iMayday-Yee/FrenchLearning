<template>
  <div class="reset-page">
    <div class="decor-line"></div>
    <div class="form-card fade-up">
      <div class="form-header">
        <span class="form-tag">Mot de passe oublié</span>
        <h2>重置密码</h2>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="field">
          <label>邮箱</label>
          <input v-model="form.email" type="email" required placeholder="请输入注册邮箱" :disabled="step === 'done'">
        </div>

        <div class="field" v-if="step !== 'done'">
          <label>验证码</label>
          <div class="code-row">
            <input v-model="form.code" type="text" required maxlength="6" placeholder="请输入6位验证码" class="code-input">
            <button type="button" class="btn-code" :disabled="cooldown > 0 || sendingCode" @click="sendCode">
              {{ cooldown > 0 ? `${cooldown}秒` : '发送验证码' }}
            </button>
          </div>
        </div>

        <div class="field" v-if="step !== 'done'">
          <label>新密码</label>
          <input v-model="form.new_password" type="password" required placeholder="至少6位" minlength="6">
        </div>

        <div v-if="errorMsg" class="error-tip">{{ errorMsg }}</div>

        <button v-if="step !== 'done'" type="submit" class="btn-submit" :disabled="loading">
          <span v-if="!loading">重置密码</span>
          <span v-else class="loading-dots">处理中<span>.</span><span>.</span><span>.</span></span>
        </button>
      </form>

      <div v-if="step === 'done'" class="success-box">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        <p>密码重置成功！</p>
        <button @click="$router.push('/login')" class="btn-submit" style="margin-top:1rem;">返回登录</button>
      </div>

      <div class="form-footer">
        <span @click="$router.push('/login')">想起密码了？<strong>返回登录</strong></span>
      </div>
    </div>
    <router-link to="/" class="back-link fade-up" style="animation-delay:0.3s">← 返回首页</router-link>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const toast = useToastStore()
const step = ref('verify') // 'verify' | 'done'
const loading = ref(false)
const sendingCode = ref(false)
const cooldown = ref(0)
const errorMsg = ref('')
const form = ref({ email: '', code: '', new_password: '' })
let cooldownTimer = null

const sendCode = async () => {
  if (!form.value.email) {
    toast.error('请先输入邮箱')
    return
  }
  sendingCode.value = true
  try {
    const res = await api.post('/send-reset-code', { email: form.value.email })
    if (res.code === 200) {
      toast.success(res.message || '验证码已发送')
      cooldown.value = 60
      cooldownTimer = setInterval(() => {
        cooldown.value--
        if (cooldown.value <= 0) clearInterval(cooldownTimer)
      }, 1000)
    }
  } catch (e) {
    toast.error(e.response?.data?.message || '发送失败，请稍后重试')
  } finally {
    sendingCode.value = false
  }
}

const handleSubmit = async () => {
  errorMsg.value = ''
  loading.value = true
  try {
    const res = await api.post('/reset-password', {
      email: form.value.email,
      code: form.value.code,
      new_password: form.value.new_password
    })
    if (res.code === 200) {
      step.value = 'done'
    }
  } catch (e) {
    errorMsg.value = e.response?.data?.message || '重置失败，请检查验证码'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.reset-page {
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
.field input:disabled { opacity: 0.6; cursor: not-allowed; }
.code-row {
  display: flex;
  gap: 0.5rem;
}
.code-input { flex: 1; }
.btn-code {
  padding: 0 0.8rem;
  white-space: nowrap;
  background: var(--accent-subtle);
  color: var(--accent);
  border: 1px solid var(--accent);
  border-radius: var(--radius);
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-code:hover:not(:disabled) { background: var(--accent); color: #fff; }
.btn-code:disabled { opacity: 0.5; cursor: not-allowed; }
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
.success-box {
  text-align: center;
  padding: 1.5rem;
  color: var(--sage);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}
.success-box p { margin: 0; font-weight: 600; }
.error-tip {
  color: var(--rose, #ef6461);
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  text-align: center;
}
.form-footer {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.85rem;
  color: var(--ink-muted);
}
.form-footer span { cursor: pointer; transition: color 0.2s; }
.form-footer span:hover { color: var(--accent); }
.form-footer strong { font-weight: 600; color: var(--accent); }
.back-link {
  margin-top: 2rem;
  font-size: 0.85rem;
  color: var(--ink-muted);
  text-decoration: none;
  transition: color 0.2s;
}
.back-link:hover { color: var(--ink); }
</style>
