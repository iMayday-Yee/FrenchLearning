<template>
  <div class="assessment-page">
    <div class="container">
      <!-- Phase 1: 问卷打分 -->
      <div v-if="phase === 'survey'" class="survey-card fade-up">
        <span class="tag">Questionnaire</span>
        <h2>学习体验评价</h2>
        <p class="survey-desc">请根据你这几天的使用感受，对以下各项进行评分</p>

        <div class="survey-items">
          <div v-for="(item, idx) in surveyItems" :key="idx" class="survey-item">
            <div class="item-label">{{ item.label }}</div>
            <div class="rating-row">
              <span class="rating-hint">不满意</span>
              <div class="dots">
                <button
                  v-for="n in 5" :key="n"
                  :class="['dot', { active: surveyData[item.key] >= n }]"
                  @click="surveyData[item.key] = n"
                >{{ n }}</button>
              </div>
              <span class="rating-hint">非常满意</span>
            </div>
          </div>
        </div>

        <button class="btn-primary" :disabled="!surveyComplete" @click="submitSurvey">
          {{ submittingSurvey ? '提交中...' : '下一步' }}
        </button>
      </div>

      <!-- Phase 2: 测试须知 -->
      <div v-else-if="phase === 'instructions'" class="instructions-card fade-up">
        <span class="tag">Évaluation</span>
        <h2>测试须知</h2>
        <div class="instructions-body">
          <p>接下来你将进行一个简短的词汇测试，检验这5天的学习成果。</p>
          <ul>
            <li>测试共 <strong>15</strong> 道选择题，每题有4个选项</li>
            <li>请根据所学内容选出正确的中文释义</li>
            <li>没有时间限制，请仔细作答</li>
          </ul>
          <p>准备好了就点击下方按钮开始吧！</p>
        </div>
        <button class="btn-primary" @click="phase = 'questions'; loadQuestions()">我已知晓，开始测试</button>
      </div>

      <!-- Phase 3: 正式测试 -->
      <template v-else-if="phase === 'questions'">
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
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'
import AssessmentQuestion from '@/components/AssessmentQuestion.vue'

const router = useRouter()
const toast = useToastStore()

const phase = ref('survey')
const submittingSurvey = ref(false)

// 问卷数据
const surveyItems = [
  { key: 'satisfaction', label: '学习体验满意度' },
  { key: 'helpfulness', label: 'AI助手的帮助程度' },
  { key: 'content_quality', label: '学习内容的实用性' },
  { key: 'ease_of_use', label: '操作界面的易用性' },
  { key: 'willingness', label: '继续使用的意愿' }
]
const surveyData = ref({
  satisfaction: 0,
  helpfulness: 0,
  content_quality: 0,
  ease_of_use: 0,
  willingness: 0
})
const surveyComplete = computed(() =>
  Object.values(surveyData.value).every(v => v >= 1)
)

const submitSurvey = async () => {
  if (!surveyComplete.value || submittingSurvey.value) return
  submittingSurvey.value = true
  try {
    await api.post('/assessment/survey', surveyData.value)
    phase.value = 'instructions'
  } catch (e) {
    toast.error(e.response?.data?.message || '提交失败，请重试')
  } finally {
    submittingSurvey.value = false
  }
}

// 测试数据
const loading = ref(false)
const questions = ref([])
const currentIndex = ref(0)
const answers = ref([])
const currentQuestion = ref(null)

const loadQuestions = async () => {
  loading.value = true
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

/* 通用 */
.tag {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-style: italic;
  color: var(--accent);
  letter-spacing: 0.1em;
}
.state-msg {
  text-align: center;
  padding: 4rem 2rem;
  background: var(--surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow);
}
.state-msg p {
  color: var(--ink-muted);
  margin-top: 0.5rem;
}

/* 问卷 */
.survey-card {
  background: var(--surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow);
  padding: 2rem 1.5rem;
  text-align: center;
}
.survey-card h2 {
  font-family: var(--font-display);
  font-size: 1.4rem;
  color: var(--ink);
  margin: 0.5rem 0 0.3rem;
}
.survey-desc {
  font-size: 0.85rem;
  color: var(--ink-muted);
  margin-bottom: 1.5rem;
}
.survey-items {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  margin-bottom: 1.8rem;
}
.survey-item {
  text-align: left;
}
.item-label {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--ink);
  margin-bottom: 0.4rem;
}
.rating-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.rating-hint {
  font-size: 0.65rem;
  color: var(--ink-faint);
  white-space: nowrap;
  min-width: 3em;
}
.rating-hint:last-child {
  text-align: right;
}
.dots {
  display: flex;
  gap: 0.4rem;
  flex: 1;
  justify-content: center;
}
.dot {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: var(--surface);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--ink-muted);
  cursor: pointer;
  transition: all 0.2s var(--ease);
  display: flex;
  align-items: center;
  justify-content: center;
}
.dot:hover {
  border-color: var(--accent);
  color: var(--accent);
}
.dot.active {
  border-color: var(--accent);
  background: var(--accent);
  color: white;
}

/* 须知 */
.instructions-card {
  background: var(--surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow);
  padding: 2rem 1.5rem;
  text-align: center;
}
.instructions-card h2 {
  font-family: var(--font-display);
  font-size: 1.4rem;
  color: var(--ink);
  margin: 0.5rem 0 1.2rem;
}
.instructions-body {
  text-align: left;
  font-size: 0.9rem;
  color: var(--ink-secondary);
  line-height: 1.7;
  margin-bottom: 1.8rem;
}
.instructions-body ul {
  padding-left: 1.2rem;
  margin: 0.8rem 0;
}
.instructions-body li {
  margin-bottom: 0.3rem;
}
.instructions-body strong {
  color: var(--ink);
}

/* 按钮 */
.btn-primary {
  width: 100%;
  padding: 0.85rem;
  border: none;
  border-radius: var(--radius);
  background: var(--accent);
  color: white;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.1s;
}
.btn-primary:hover:not(:disabled) {
  opacity: 0.9;
}
.btn-primary:active:not(:disabled) {
  transform: scale(0.98);
}
.btn-primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>
