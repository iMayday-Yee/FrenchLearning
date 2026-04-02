<template>
  <div class="assessment-page">
    <div class="container">
      <AssessmentQuestion
        v-if="currentQuestion"
        :question="currentQuestion"
        :current="currentIndex"
        :total="questions.length"
        @answered="handleAnswer"
      />
      <div v-else-if="loading" class="loading">加载中...</div>
      <div v-else class="complete">测评已完成</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import AssessmentQuestion from '@/components/AssessmentQuestion.vue'

const router = useRouter()
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
    console.error('Failed to load questions', e)
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
    console.error('Failed to submit', e)
  }
}

onMounted(loadQuestions)
</script>

<style scoped>
.assessment-page {
  min-height: 100vh;
  background: #f5f5f5;
  padding-top: 2rem;
}
.container {
  max-width: 400px;
  margin: 0 auto;
  background: white;
  min-height: calc(100vh - 4rem);
  border-radius: 16px 16px 0 0;
}
.loading, .complete {
  text-align: center;
  padding: 3rem;
  color: #888;
}
</style>
