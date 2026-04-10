<template>
  <div class="result-page">
    <div class="card fade-up">
      <div class="pill">Résultat</div>
      <h2>测评结果</h2>
      <div class="score-ring">
        <span class="correct">{{ result.correct_count || 0 }}</span>
        <span class="sep">/</span>
        <span class="total">{{ result.total_count || 0 }}</span>
      </div>
      <div class="score-label">答对题数</div>
      <div class="comment">{{ comment }}</div>
      <p class="after-note">恭喜你完成了五天的学习！接下来平台仍将开放一周，你可以随时回来继续学习。</p>
      <button class="btn-continue" @click="goToChat">继续学习</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const toast = useToastStore()
const result = ref({})

const comment = computed(() => {
  const correct = result.value.correct_count || 0
  const total = result.value.total_count || 1
  const ratio = correct / total
  if (ratio >= 0.9) return 'Excellent !'
  if (ratio >= 0.7) return 'Très bien !'
  if (ratio >= 0.5) return 'Pas mal, continuez !'
  return 'Courage, continuez !'
})

const loadResult = async () => {
  try {
    result.value = await api.get('/assessment/result')
  } catch (e) {
    toast.error('成绩加载失败')
  }
}
const goToChat = () => router.push('/chat')
onMounted(loadResult)
</script>

<style scoped>
.result-page {
  min-height: 100vh;
  background: var(--bg-tint);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}
.card {
  background: var(--surface);
  padding: 3rem 2.5rem;
  border-radius: var(--radius-lg);
  text-align: center;
  max-width: 360px;
  width: 100%;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-light);
}
.pill {
  display: inline-block;
  padding: 0.25rem 0.8rem;
  border-radius: var(--radius-xl);
  background: var(--accent-subtle);
  color: var(--accent);
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
h2 {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 1.5rem;
}
.score-ring {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.2rem;
  margin-bottom: 0.3rem;
}
.correct {
  font-family: var(--font-display);
  font-size: 3.5rem;
  font-weight: 700;
  color: var(--accent);
  line-height: 1;
}
.sep {
  font-size: 1.8rem;
  color: var(--ink-faint);
  margin: 0 0.15rem;
}
.total {
  font-family: var(--font-display);
  font-size: 1.8rem;
  color: var(--ink-muted);
}
.score-label {
  font-size: 0.8rem;
  color: var(--ink-muted);
  margin-bottom: 1.2rem;
}
.comment {
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-style: italic;
  color: var(--ink-secondary);
  margin-bottom: 1.2rem;
}
.after-note {
  font-size: 0.82rem;
  color: var(--ink-muted);
  line-height: 1.6;
  margin-bottom: 1.8rem;
  padding: 0.8rem 1rem;
  background: var(--bg);
  border-radius: var(--radius);
}
.btn-continue {
  width: 100%;
  padding: 0.85rem;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s var(--ease);
}
.btn-continue:hover {
  background: var(--accent-hover);
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(123,155,244,0.2);
}
</style>
