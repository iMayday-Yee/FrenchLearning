<template>
  <div class="assessment-page">
    <div class="container">
      <div v-if="loading" class="state-msg fade-up">
        <span class="tag">Évaluation</span>
        <p>加载中...</p>
      </div>
      <AssessmentQuestion
        v-else-if="currentQuestion"
        :question="currentQuestion"
        :current="currentIndex"
        :total="questions.length"
        @answered="handleAnswer"
      />
      <div v-else class="state-msg fade-up">
        <span class="tag">Terminé</span>
        <p>测评已完成</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'
import AssessmentQuestion from '@/components/AssessmentQuestion.vue'

const router = useRouter()
const toast = useToastStore()
const loading = ref(true)
const questions = ref([])
const currentIndex = ref(0)
const answers = ref([])
const currentQuestion = ref(null)

const loadQuestions = async () => {
  try {
    const res = await api.get('/assessment/questions')
    questions.value = res.questions
    currentQuestion.value = questions.value[0]
  } catch (e) {
    toast.error('题目加载失败，请刷新页面重试')
  } finally {
    loading.value = false
  }
}

const handleAnswer = async (answer) => {
  answers.value.push(answer)
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    currentQuestion.value = questions.value[currentIndex.value]
  } else {
    await submitAssessment()
  }
}

const submitAssessment = async () => {
  try {
    await api.post('/assessment/submit', { answers: answers.value })
    router.push('/result')
  } catch (e) {
    toast.error('提交失败，请重试')
  }
}

onMounted(loadQuestions)
</script>

<style scoped>
.assessment-page {
  min-height: 100vh;
  background: var(--bg);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding: 3rem 1rem;
}
.container {
  max-width: 420px;
  width: 100%;
}
.state-msg {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow);
}
.state-msg .tag {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-style: italic;
  color: var(--accent);
  letter-spacing: 0.1em;
}
.state-msg p {
  color: var(--ink-muted);
  margin-top: 0.5rem;
}
</style>
