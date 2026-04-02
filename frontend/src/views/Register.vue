<template>
  <div class="register-page">
    <div class="form-container">
      <h2>用户注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>手机号 *</label>
          <input v-model="form.phone" type="tel" required maxlength="20" placeholder="请输入手机号">
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input v-model="form.email" type="email" placeholder="选填，用于接收通知">
        </div>
        <div class="form-group">
          <label>密码 *</label>
          <input v-model="form.password" type="password" required minlength="6" placeholder="至少6位">
        </div>
        <div class="form-group">
          <label>姓名/昵称 *</label>
          <input v-model="form.nickname" type="text" required maxlength="50">
        </div>
        <div class="form-group">
          <label>年龄 *</label>
          <input v-model.number="form.age" type="number" required min="10" max="100">
        </div>
        <div class="form-group">
          <label>性别 *</label>
          <select v-model="form.gender" required>
            <option value="">请选择</option>
            <option value="男">男</option>
            <option value="女">女</option>
            <option value="其他">其他</option>
          </select>
        </div>
        <div class="form-group">
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
        <div class="form-group">
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
        <div class="form-group">
          <label>法语学习基础 *</label>
          <select v-model="form.french_level" required>
            <option value="">请选择</option>
            <option value="零基础">零基础</option>
            <option value="了解少量单词">了解少量单词</option>
            <option value="系统学习过一段时间">系统学习过一段时间</option>
            <option value="较为熟练">较为熟练</option>
          </select>
        </div>
        <div class="form-group">
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
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? '提交中...' : '提交注册' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const form = ref({
  phone: '',
  email: '',
  password: '',
  nickname: '',
  age: null,
  gender: '',
  education: '',
  french_interest: '',
  french_level: '',
  study_time_slot: ''
})

const handleRegister = async () => {
  loading.value = true
  try {
    const res = await api.post('/register', form.value)
    if (res.code === 200) {
      localStorage.setItem('pending_user_id', res.user_id)
      router.push('/bindwechat')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  padding: 2rem 1rem;
  background: #f5f5f5;
}
.form-container {
  max-width: 500px;
  margin: 0 auto;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.1);
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
input, select {
  width: 100%;
  padding: 0.6rem;
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
  margin-top: 1rem;
}
.btn-submit:disabled {
  opacity: 0.6;
}
</style>
