<template>
  <div class="register-page">
    <div class="decor-line"></div>
    <div class="form-card fade-up">
      <div class="form-header">
        <span class="form-tag">Inscription</span>
        <h2>创建账号</h2>
      </div>

      <!-- Step 1: 邮箱验证 -->
      <div v-if="!emailVerified" class="verify-section">
        <div class="field">
          <label>邮箱 *</label>
          <div class="input-with-btn">
            <input v-model="form.email" type="email" required placeholder="请输入邮箱" :disabled="codeSent && countdown > 0">
            <button type="button" class="send-code-btn" @click="sendCode" :disabled="sendingCode || (codeSent && countdown > 0)">
              {{ sendingCode ? '发送中...' : (countdown > 0 ? `${countdown}s` : (codeSent ? '重新发送' : '发送验证码')) }}
            </button>
          </div>
        </div>
        <div v-if="codeSent" class="field">
          <label>验证码</label>
          <div class="input-with-btn">
            <input v-model="emailCode" type="text" maxlength="6" inputmode="numeric" placeholder="请输入6位验证码">
            <button type="button" class="verify-btn" @click="verifyEmail" :disabled="emailCode.length !== 6">验证</button>
          </div>
        </div>
      </div>

      <!-- Step 2: 验证成功后填写其余信息 -->
      <form v-if="emailVerified" @submit.prevent="handleRegister">
        <div class="verified-email">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          {{ form.email }}
        </div>
        <div class="field-grid">
          <div class="field span-2">
            <label>手机号 *</label>
            <input v-model="form.phone" type="tel" required maxlength="20" placeholder="请输入手机号">
          </div>
          <div class="field span-2">
            <label>密码 *</label>
            <input v-model="form.password" type="password" required minlength="6" placeholder="至少6位">
          </div>
          <div class="field">
            <label>姓名/昵称 *</label>
            <input v-model="form.nickname" type="text" required maxlength="50">
          </div>
          <div class="field">
            <label>年龄 *</label>
            <input v-model.number="form.age" type="number" required min="10" max="100">
          </div>
          <div class="field">
            <label>性别 *</label>
            <select v-model="form.gender" required>
              <option value="">请选择</option>
              <option value="男">男</option>
              <option value="女">女</option>
            </select>
          </div>
          <div class="field">
            <label>教育背景 *</label>
            <select v-model="form.education" required>
              <option value="">请选择</option>
              <option value="高中及以下">高中及以下</option>
              <option value="大专">大专</option>
              <option value="本科">本科</option>
              <option value="硕士">硕士</option>
              <option value="博士">博士</option>
            </select>
          </div>
          <div class="field span-2">
            <label>对法语的兴趣程度 *</label>
            <select v-model="form.french_interest" required>
              <option value="">请选择</option>
              <option value="非常感兴趣">非常感兴趣</option>
              <option value="比较感兴趣">比较感兴趣</option>
              <option value="一般">一般</option>
              <option value="不太感兴趣">不太感兴趣</option>
              <option value="完全不感兴趣">完全不感兴趣</option>
            </select>
          </div>
          <div class="field span-2">
            <label>法语学习基础 *</label>
            <select v-model="form.french_level" required>
              <option value="">请选择</option>
              <option value="零基础">零基础</option>
              <option value="了解少量单词">了解少量单词</option>
              <option value="系统学习过一段时间">系统学习过一段时间</option>
              <option value="较为熟练">较为熟练</option>
            </select>
          </div>
          <div class="field span-2">
            <label>偏好学习时间段 *</label>
            <select v-model="form.study_time_slot" required>
              <option value="">请选择</option>
              <option value="06:00">6:00-8:00</option>
              <option value="08:00">8:00-10:00</option>
              <option value="10:00">10:00-12:00</option>
              <option value="12:00">12:00-14:00</option>
              <option value="14:00">14:00-16:00</option>
              <option value="16:00">16:00-18:00</option>
              <option value="18:00">18:00-20:00</option>
              <option value="20:00">20:00-22:00</option>
              <option value="22:00">22:00-24:00</option>
            </select>
          </div>
        </div>
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? '提交中...' : '提交注册' }}
        </button>
      </form>
      <div class="form-footer">
        <span @click="$router.push('/login')">已有账号？<strong>登录</strong></span>
      </div>
    </div>
    <router-link to="/" class="back-link fade-up" style="animation-delay:0.3s">← 返回首页</router-link>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const toast = useToastStore()
const loading = ref(false)
const sendingCode = ref(false)
const codeSent = ref(false)
const countdown = ref(0)
const emailCode = ref('')
const emailVerified = ref(false)
let countdownTimer = null

const form = ref({
  email: '', phone: '', password: '', nickname: '',
  age: null, gender: '', education: '',
  french_interest: '', french_level: '', study_time_slot: ''
})

const startCountdown = () => {
  countdown.value = 60
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) clearInterval(countdownTimer)
  }, 1000)
}

const sendCode = async () => {
  if (!form.value.email) {
    toast.error('请输入邮箱地址')
    return
  }
  sendingCode.value = true
  try {
    const res = await api.post('/send-verification-code', { email: form.value.email })
    if (res.code === 200) {
      codeSent.value = true
      toast.success('验证码已发送，请查收邮件')
      startCountdown()
    }
  } catch (e) {
    toast.error(e.response?.data?.message || '发送失败，请稍后重试')
  } finally {
    sendingCode.value = false
  }
}

const verifyEmail = async () => {
  if (emailCode.value.length !== 6) {
    toast.error('请输入6位验证码')
    return
  }
  try {
    const res = await api.post('/verify-email', {
      email: form.value.email,
      code: emailCode.value
    })
    if (res.code === 200) {
      emailVerified.value = true
      toast.success('邮箱验证成功')
    }
  } catch (e) {
    toast.error(e.response?.data?.message || '验证码验证失败')
  }
}

const handleRegister = async () => {
  if (!form.value.phone || !form.value.password || !form.value.nickname) {
    toast.error('请填写所有必填项')
    return
  }
  if (form.value.password.length < 6) {
    toast.error('密码至少需要6位')
    return
  }
  loading.value = true
  try {
    const res = await api.post('/register', {
      ...form.value
    })
    if (res.code === 200) {
      localStorage.setItem('pending_user_id', res.user_id)
      if (res.study_start_date) localStorage.setItem('study_start_date', res.study_start_date)
      router.push('/agreement')
    }
  } catch (e) {
    toast.error(e.response?.data?.message || '注册失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

onUnmounted(() => {
  if (countdownTimer) clearInterval(countdownTimer)
})
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  padding: 2rem 1rem;
  background: var(--bg);
  display: flex;
  flex-direction: column;
  align-items: center;
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
  max-width: 480px;
  background: var(--surface);
  padding: 2.5rem 2rem 2rem;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-light);
  margin-top: 1rem;
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
.verify-section {
  margin-bottom: 1rem;
}
.input-with-btn {
  display: flex;
  gap: 0.5rem;
}
.input-with-btn input {
  flex: 1;
  padding: 0.7rem 0.9rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  color: var(--ink);
  background: var(--bg);
  outline: none;
}
.input-with-btn input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-subtle);
}
.input-with-btn input::placeholder { color: var(--ink-faint); }
.send-code-btn {
  padding: 0.7rem 1rem;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.2s;
}
.send-code-btn:hover:not(:disabled) { background: var(--accent-hover); }
.send-code-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.verify-btn {
  padding: 0.7rem 1.2rem;
  background: var(--sage);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: opacity 0.2s;
}
.verify-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.verified-email {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.6rem 0.9rem;
  background: var(--sage-subtle);
  color: var(--sage);
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-weight: 500;
  margin-bottom: 1.2rem;
  border: 1px solid rgba(123, 205, 168, 0.2);
}
.field-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
.field { margin-bottom: 0; }
.field.span-2 { grid-column: span 2; }
.field label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--ink-secondary);
  margin-bottom: 0.35rem;
  letter-spacing: 0.03em;
  text-transform: uppercase;
}
.field input, .field select {
  width: 100%;
  padding: 0.7rem 0.9rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  color: var(--ink);
  background: var(--bg);
  transition: all 0.2s var(--ease);
  outline: none;
  appearance: none;
  -webkit-appearance: none;
}
.field select {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='%238b95a5' viewBox='0 0 16 16'%3E%3Cpath d='M8 11L3 6h10z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 0.8rem center;
  padding-right: 2rem;
}
.field input:focus, .field select:focus {
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
  margin-top: 1.5rem;
}
.btn-submit:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(123,155,244,0.2);
}
.btn-submit:disabled { opacity: 0.5; }
.form-footer {
  text-align: center;
  margin-top: 1.2rem;
  font-size: 0.85rem;
  color: var(--ink-muted);
}
.form-footer span { cursor: pointer; }
.form-footer strong { color: var(--accent); }
.back-link {
  margin-top: 2rem;
  font-size: 0.85rem;
  color: var(--ink-muted);
  text-decoration: none;
  transition: color 0.2s;
}
.back-link:hover { color: var(--ink); }
@media (max-width: 480px) {
  .field-grid { grid-template-columns: 1fr; }
  .field.span-2 { grid-column: span 1; }
}
</style>
