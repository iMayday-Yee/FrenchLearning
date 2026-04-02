<template>
  <div class="bind-page">
    <div class="container">
      <h2>绑定微信</h2>
      <p class="desc">请使用微信扫描下方二维码关注公众号，以便接收学习提醒</p>

      <div class="qrcode-container" v-if="!bound">
        <img v-if="qrcodeImage" :src="qrcodeImage" alt="微信二维码">
        <div v-else class="loading">加载中...</div>
      </div>

      <div v-if="bound" class="success">
        <p>绑定成功！</p>
      </div>

      <div class="actions">
        <button v-if="!bound" @click="skipBind" class="btn-skip">跳过，稍后绑定</button>
        <button v-if="bound" @click="goNext" class="btn-next">继续</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const qrcodeImage = ref('')
const bound = ref(false)
const userId = localStorage.getItem('pending_user_id')
let pollInterval = null

const loadQRCode = async () => {
  try {
    const res = await api.get(`/get_bind_qrcode?user_id=${userId}`)
    if (res.code === 200) {
      qrcodeImage.value = res.qrcode_image
    }
  } catch (e) {
    console.error('Failed to load QR code', e)
  }
}

const checkBind = async () => {
  try {
    const res = await api.get(`/bindcheck?user_id=${userId}`)
    if (res.bound) {
      bound.value = true
      stopPoll()
      setTimeout(() => router.push('/agreement'), 1000)
    }
  } catch (e) {
    console.error('Bind check failed', e)
  }
}

const skipBind = () => {
  stopPoll()
  router.push('/agreement')
}

const goNext = () => {
  stopPoll()
  router.push('/agreement')
}

const stopPoll = () => {
  if (pollInterval) {
    clearInterval(pollInterval)
    pollInterval = null
  }
}

onMounted(() => {
  if (!userId) {
    router.push('/register')
    return
  }
  loadQRCode()

  // 轮询间隔改为10秒，减少API请求
  pollInterval = setInterval(async () => {
    try {
      const res = await api.get(`/bindcheck?user_id=${userId}`)
      if (res.bound) {
        bound.value = true
        stopPoll()
        setTimeout(() => router.push('/agreement'), 1000)
      }
    } catch (e) {
      // 429错误时停止轮询
      if (e.response?.status === 429) {
        stopPoll()
      }
    }
  }, 10000)

  // 最多轮询18次（3分钟后停止）
  setTimeout(() => stopPoll(), 180000)
})

onUnmounted(() => {
  stopPoll()
})
</script>

<style scoped>
.bind-page {
  min-height: 100vh;
  padding: 2rem;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}
.container {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  max-width: 400px;
}
h2 { margin-bottom: 0.5rem; }
.desc { color: #666; margin-bottom: 1.5rem; font-size: 0.9rem; }
.qrcode-container {
  margin: 1rem auto;
}
.qrcode-container img {
  width: 200px;
  height: 200px;
}
.loading { padding: 50px; color: #999; }
.success { color: #52c41a; padding: 1rem; }
.actions { margin-top: 1.5rem; }
.btn-skip {
  background: none;
  border: 1px solid #ddd;
  padding: 0.6rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  color: #666;
}
.btn-next {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.6rem 2rem;
  border-radius: 6px;
  cursor: pointer;
}
</style>
