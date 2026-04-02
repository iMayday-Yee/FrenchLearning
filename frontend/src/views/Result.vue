<template>
  <div class="result-page">
    <div class="container">
      <h2>测评结果</h2>
      <div class="score">{{ result.total_score || 0 }}</div>
      <div class="label">综合得分</div>
      <div class="details">
        <div class="detail-item">
          <span class="label">词义正确率</span>
          <span class="value">{{ result.vocab_score || 0 }}%</span>
        </div>
      </div>
      <div class="comment">{{ comment }}</div>
      <button class="btn-continue" @click="goToChat">进入学习</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const result = ref({})

const comment = computed(() => {
  const score = result.value.total_score || 0
  if (score >= 90) return '优秀！🎉'
  if (score >= 70) return '不错！👍'
  if (score >= 50) return '继续加油！💪'
  return '还有很大进步空间，继续努力！'
})

const loadResult = async () => {
  try {
    const res = await api.get('/assessment/result')
    result.value = res
  } catch (e) {
    console.error('Failed to load result', e)
  }
}

const goToChat = () => {
  router.push('/chat')
}

onMounted(loadResult)
</script>

<style scoped>
.result-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}
.container {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  text-align: center;
  max-width: 350px;
  width: 100%;
}
h2 { margin-bottom: 1.5rem; }
.score {
  font-size: 4rem;
  font-weight: bold;
  color: #667eea;
}
.label {
  color: #888;
  margin-bottom: 1.5rem;
}
.details {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}
.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 0.3rem 0;
}
.comment {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}
.btn-continue {
  width: 100%;
  padding: 0.8rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}
</style>
