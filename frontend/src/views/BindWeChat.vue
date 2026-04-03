<template>
  <div class="bind-page">
    <div class="card fade-up">
      <span class="tag">WeChat</span>
      <h2>绑定微信公众号</h2>
      <p class="desc">扫描二维码关注公众号，接收每日学习提醒</p>

      <div class="qrcode-area">
        <!-- 加载中状态 -->
        <div v-if="loading" class="loading-state">
          <div class="spinner-ring"></div>
          <p class="loading-tip">正在生成二维码...</p>
        </div>
        <!-- 二维码 -->
        <img v-else-if="qrUrl" :src="qrUrl" alt="微信二维码" class="qr-img">
        <!-- 错误状态 -->
        <div v-else-if="errorMsg" class="error-state">
          <p>{{ errorMsg }}</p>
        </div>
        <!-- 加载超时 -->
        <div v-else-if="loadTimeout" class="timeout-state">
          <p class="timeout-tip">二维码生成超时</p>
          <p class="timeout-sub">请稍后重试，或跳过绑定</p>
        </div>
      </div>

      <div v-if="bound" class="success-msg">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
        绑定成功
      </div>

      <div class="actions">
        <button v-if="canSkip" @click="skipBind" class="btn-skip">跳过，稍后绑定</button>
        <button v-if="bound" @click="goNext" class="btn-next">继续</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const toast = useToastStore()
const qrUrl = ref('')
const bound = ref(false)
const errorMsg = ref('')
const loading = ref(false)
const loadTimeout = ref(false)
const canSkip = ref(false)
const userId = localStorage.getItem('pending_user_id')
let pollInterval = null
let loadTimer = null
let qrShownAt = null  // 二维码显示时间

const loadQRCode = async () => {
  loading.value = true
  loadTimeout.value = false

  // 10秒超时
  loadTimer = setTimeout(() => {
    loading.value = false
    loadTimeout.value = true
  }, 10000)

  try {
    const res = await api.get(`/get_bind_qrcode?user_id=${userId}`)
    clearTimeout(loadTimer)
    loading.value = false
    if (res.code === 200) {
      if (res.already_bound) {
        bound.value = true
        return
      }
      qrUrl.value = res.qr_url
      qrShownAt = Date.now()
    }
  } catch (e) {
    clearTimeout(loadTimer)
    loading.value = false
    if (e.response?.status === 503) {
      errorMsg.value = e.response.data.message || '公众号暂不可用'
    } else {
      errorMsg.value = '二维码加载失败，可跳过此步'
    }
  }
}

const skipBind = () => { stopAll(); router.push('/agreement') }
const goNext = () => { stopAll(); router.push('/agreement') }
const stopAll = () => {
  if (pollInterval) { clearInterval(pollInterval); pollInterval = null }
  if (loadTimer) { clearTimeout(loadTimer); loadTimer = null }
}

onMounted(() => {
  if (!userId) { router.push('/register'); return }
  loadQRCode()
  // 轮询绑定状态，同时检测是否可跳过（二维码显示超过20秒后才可跳过）
  pollInterval = setInterval(async () => {
    try {
      const res = await api.get(`/bind_status?user_id=${userId}`)
      if (res.status === 'bound') {
        bound.value = true
        stopAll()
        setTimeout(() => router.push('/agreement'), 1500)
      } else if (res.can_skip && qrShownAt && Date.now() - qrShownAt > 20000) {
        canSkip.value = true
      }
    } catch (e) {
      if (e.response?.status === 429) stopAll()
    }
  }, 3000)
  setTimeout(() => stopAll(), 180000)
})
onUnmounted(() => stopAll())
</script>

<style scoped>
.bind-page {
  min-height: 100vh;
  padding: 2rem;
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
}
.card {
  background: var(--surface);
  padding: 2.5rem 2rem;
  border-radius: var(--radius-lg);
  text-align: center;
  max-width: 400px;
  width: 100%;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-light);
}
.tag {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-style: italic;
  color: var(--accent);
  letter-spacing: 0.1em;
}
h2 {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--ink);
  margin: 0.3rem 0 0.5rem;
}
.desc { color: var(--ink-muted); font-size: 0.85rem; margin-bottom: 1.5rem; }
.qrcode-area {
  margin: 0 auto 1.5rem;
  width: 200px;
  height: 200px;
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fafafa;
}
.qr-img { width: 100%; height: 100%; object-fit: contain; }
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}
.spinner-ring {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-tip { color: var(--ink-muted); font-size: 0.8rem; margin: 0; }
.error-state, .timeout-state {
  padding: 1rem;
  text-align: center;
}
.error-state p, .timeout-tip { color: var(--rose, #ef6461); font-size: 0.85rem; margin: 0 0 0.25rem; }
.timeout-sub { color: var(--ink-muted); font-size: 0.75rem; margin: 0; }
.success-msg {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--sage);
  font-weight: 600;
  padding: 1rem;
}
.actions { margin-top: 1rem; }
.btn-skip {
  background: transparent;
  border: 1px solid var(--border);
  padding: 0.6rem 1.5rem;
  border-radius: var(--radius);
  cursor: pointer;
  color: var(--ink-muted);
  font-size: 0.85rem;
  transition: all 0.2s;
}
.btn-skip:hover { border-color: var(--ink-muted); color: var(--ink); }
.btn-next {
  background: var(--accent);
  color: var(--ink-on-dark);
  border: none;
  padding: 0.7rem 2rem;
  border-radius: var(--radius);
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}
.btn-next:hover { background: var(--accent); }
.error-msg {
  padding: 1rem;
  background: rgba(239, 100, 97, 0.08);
  border: 1px solid rgba(239, 100, 97, 0.2);
  border-radius: var(--radius);
  color: var(--rose, #ef6461);
  font-size: 0.85rem;
  margin-bottom: 1rem;
  text-align: center;
}
</style>
