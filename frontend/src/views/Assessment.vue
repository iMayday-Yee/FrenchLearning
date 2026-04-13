<template>
  <div class="assessment-page">
    <div class="container">
      <!-- Phase 1: App Store 评分 -->
      <div v-if="phase === 'survey1'" class="survey-card fade-up">
        <span class="tag">Questionnaire</span>
        <h2>感谢您的使用，<br>请对小五智能助手打分</h2>
        <div class="stars-row">
          <button
            v-for="n in 7" :key="n"
            :class="['star-btn', { active: appRating >= n }]"
            @click="appRating = n"
          >
            <svg width="40" height="40" viewBox="0 0 24 24" :fill="appRating >= n ? 'var(--accent)' : 'none'" stroke="var(--accent)" stroke-width="1.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          </button>
          <span class="stars-label">{{ appRating }}/7</span>
        </div>

        <button class="btn-primary" :disabled="appRating < 1" @click="goToSurvey2">
          下一页
        </button>
      </div>

      <!-- Phase 1b: 量表题（第二页） -->
      <div v-else-if="phase === 'survey2'" class="survey-card survey-card-long fade-up">
        <span class="tag">Questionnaire</span>
        <h2>请对小五智能助手打分</h2>

        <div class="survey-section" v-for="section in surveySections" :key="section.title">
          <p class="section-lead">{{ section.lead }}</p>
          <div class="survey-items">
            <div v-for="item in section.items" :key="item.key" class="survey-item">
              <div class="item-label">{{ item.label }}</div>
              <div class="likert-row">
                <span class="likert-hint">{{ section.left }}</span>
                <div class="likert-dots">
                  <button
                    v-for="n in 7" :key="n"
                    :class="['likert-dot', { active: surveyData[item.key] === n }]"
                    @click="surveyData[item.key] = n"
                  >{{ n }}</button>
                </div>
                <span class="likert-hint">{{ section.right }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="btn-row">
          <button class="btn-ghost" @click="phase = 'survey1'">上一页</button>
          <button class="btn-primary" :disabled="!survey2Complete || submittingSurvey" @click="submitSurvey">
            {{ submittingSurvey ? '提交中...' : '下一步' }}
          </button>
        </div>
      </div>

      <!-- Phase 2: 测试须知 -->
      <div v-else-if="phase === 'instructions'" class="instructions-card fade-up">
        <span class="tag">Évaluation</span>
        <h2>测试须知</h2>
        <div class="instructions-body">
          <p>接下来你将进行两项测试，检验这5天的学习成果。</p>
          <p class="red-note">答题正确率不影响报酬发放，请你集中注意力，凭记忆认真完成即可！</p>
          <div class="instructions-section">
            <h3>第一项：词汇含义测试</h3>
            <ul>
              <li>共 <strong>15</strong> 道选择题，每题有4个选项</li>
              <li>请根据所学内容选出正确的中文释义</li>
              <li>限时 <strong>3分钟</strong> 内完成，超时将自动提交</li>
            </ul>
          </div>
          <div class="instructions-section">
            <h3>第二项：发音跟读测试</h3>
            <ul>
              <li>根据所学内容，按住麦克风按钮录制单词发音</li>
              <li>不限时间，完成所有单词即可</li>
            </ul>
          </div>
          <p>准备好了就点击下方按钮开始吧！</p>
        </div>
        <button class="btn-primary" @click="startQuestions">我已知晓，开始测试</button>
      </div>

      <!-- Phase 3: 词汇测试（限时） -->
      <template v-else-if="phase === 'questions'">
        <div v-if="loading" class="state-msg fade-up">
          <span class="tag">Évaluation</span>
          <p>加载中...</p>
        </div>
        <template v-else-if="currentQuestion">
          <div class="timer-bar" :class="{ urgent: timeLeft <= 30 }">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            {{ timerDisplay }}
          </div>
          <AssessmentQuestion
            :question="currentQuestion"
            :current="currentIndex"
            :total="questions.length"
            @answered="handleAnswer"
          />
        </template>
      </template>

      <!-- Phase 4: 发音跟读测试 -->
      <div v-else-if="phase === 'pronunciation'" class="pron-card fade-up">
        <div class="pron-header">
          <span class="tag">Prononciation</span>
          <div class="pron-progress">{{ pronIndex + 1 }} / {{ pronWords.length }}</div>
        </div>
        <div class="pron-word">{{ pronWords[pronIndex].french }}</div>
        <div class="pron-phonetic">{{ pronWords[pronIndex].phonetic }}</div>
        <div class="pron-chinese">{{ pronWords[pronIndex].chinese }}</div>

        <div class="pron-actions">
          <!-- 录音按钮 -->
          <div class="pron-action-group">
            <button
              class="rec-btn"
              :class="{ 'recording-active': isRecording }"
              @pointerdown.prevent="startRecording"
              @pointerup.prevent="stopRecording"
              @lostpointercapture="stopRecording"
              @contextmenu.prevent
              :disabled="isUploading"
            >
              <svg v-if="!isRecording" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/></svg>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>
              <div v-if="isRecording" class="wave"></div>
            </button>
            <span class="action-label">{{ isUploading ? '上传中...' : (isRecording ? '松开结束' : (pronRecorded[pronIndex] ? '已录制 ✓ 可重录（仅保留最新）' : '按住录音')) }}</span>
          </div>
        </div>

        <button
          class="btn-primary"
          :disabled="!pronRecorded[pronIndex] || isUploading"
          @click="nextPronWord"
        >
          {{ pronIndex < pronWords.length - 1 ? '下一个' : '完成测试' }}
        </button>
      </div>

      <!-- Phase 5: 完成 -->
      <div v-else-if="phase === 'done'" class="state-msg fade-up">
        <span class="tag">Terminé</span>
        <p>测评已完成</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onBeforeUnmount } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'
import AssessmentQuestion from '@/components/AssessmentQuestion.vue'

const router = useRouter()
const toast = useToastStore()

const phase = ref('survey1')
const submittingSurvey = ref(false)
const appRating = ref(0)

// ========== 问卷（两页） ==========
const surveyData = ref({
  // App评分（1-5）
  app_rating: 0,
  // 第一组
  q1_service: 0,
  q1_happy: 0,
  q1_willingness: 0,
  // 第二组
  q2_share: 0,
  q2_comfort: 0,
  q2_care: 0,
  q2_decision: 0,
  q2_support: 0,
  // 第三组
  q3_self_thought: 0,
  q3_self_decide: 0,
  q3_responsible: 0,
  q3_adjust_behavior: 0,
  q3_adjust_decision: 0,
  q3_adjust_willingness: 0,
  // 第四组
  satisfaction: 0,
  helpfulness: 0,
  willingness_to_continue: 0,
  willingness_to_recommend: 0
})

const surveySections = [
  {
    title: 'group1',
    lead: '请对下面陈述表达你的看法，1表示非常不同意，7表示非常同意：',
    left: '1 非常不同意', right: '7 非常同意',
    items: [
      { key: 'q1_service', label: '你喜欢小五提供的服务。' },
      { key: 'q1_happy', label: '你与小五互动得开心。' },
      { key: 'q1_willingness', label: '你愿意使用小五。' }
    ]
  },
  {
    title: 'group2',
    lead: '请对下面陈述表达你的看法，1表示非常不同意，7表示非常同意：',
    left: '1 非常不同意', right: '7 非常同意',
    items: [
      { key: 'q2_share', label: '我可以与小五分享我的心情。' },
      { key: 'q2_comfort', label: '小五让我感到慰藉。' },
      { key: 'q2_care', label: '小五关心我的感受。' },
      { key: 'q2_decision', label: '小五愿意帮我做出决策。' },
      { key: 'q2_support', label: '我从小五那里获得了情感上的帮助与支持。' }
    ]
  },
  {
    title: 'group3',
    lead: '请对下面陈述表达你的看法，1表示非常不同意，7表示非常同意：',
    left: '1 非常不同意', right: '7 非常同意',
    items: [
      { key: 'q3_self_thought', label: '我认为小五的行为完全是出于它自己的想法。' },
      { key: 'q3_self_decide', label: '我认为小五的行为是自己决定的。' },
      { key: 'q3_responsible', label: '我认为小五可以为自己的行为负责。' },
      { key: 'q3_adjust_behavior', label: '我觉得小五可以调整自己的行为方式。' },
      { key: 'q3_adjust_decision', label: '我觉得小五可以调整自己的决策或计划。' },
      { key: 'q3_adjust_willingness', label: '我觉得小五可以调整自己的意愿或意图。' }
    ]
  },
  {
    title: 'group4',
    lead: '请对下面陈述表达你的看法，1表示非常不同意，7表示非常同意：',
    left: '1 非常不同意', right: '7 非常同意',
    items: [
      { key: 'satisfaction', label: '你对使用小五智能助手完成这次学习体验感到满意。' },
      { key: 'helpfulness', label: '你觉得小五智能助手对你有帮助。' },
      { key: 'willingness_to_continue', label: '你以后愿意继续使用小五智能助手。' },
      { key: 'willingness_to_recommend', label: '你愿意将小五智能助手推荐给其他人。' }
    ]
  }
]

const survey1Complete = computed(() => appRating.value >= 1)

const survey2Complete = computed(() => {
  return surveyData.value.q1_service >= 1 &&
    surveyData.value.q1_happy >= 1 &&
    surveyData.value.q1_willingness >= 1 &&
    surveyData.value.q2_share >= 1 &&
    surveyData.value.q2_comfort >= 1 &&
    surveyData.value.q2_care >= 1 &&
    surveyData.value.q2_decision >= 1 &&
    surveyData.value.q2_support >= 1 &&
    surveyData.value.q3_self_thought >= 1 &&
    surveyData.value.q3_self_decide >= 1 &&
    surveyData.value.q3_responsible >= 1 &&
    surveyData.value.q3_adjust_behavior >= 1 &&
    surveyData.value.q3_adjust_decision >= 1 &&
    surveyData.value.q3_adjust_willingness >= 1 &&
    surveyData.value.satisfaction >= 1 &&
    surveyData.value.helpfulness >= 1 &&
    surveyData.value.willingness_to_continue >= 1 &&
    surveyData.value.willingness_to_recommend >= 1
})

const goToSurvey2 = () => {
  if (survey1Complete.value) phase.value = 'survey2'
}

const submitSurvey = async () => {
  if (!survey2Complete.value || submittingSurvey.value) return
  submittingSurvey.value = true
  try {
    const payload = {
      app_rating: appRating.value,
      details: {
        q1_service: surveyData.value.q1_service,
        q1_happy: surveyData.value.q1_happy,
        q1_willingness: surveyData.value.q1_willingness,
        q2_share: surveyData.value.q2_share,
        q2_comfort: surveyData.value.q2_comfort,
        q2_care: surveyData.value.q2_care,
        q2_decision: surveyData.value.q2_decision,
        q2_support: surveyData.value.q2_support,
        q3_self_thought: surveyData.value.q3_self_thought,
        q3_self_decide: surveyData.value.q3_self_decide,
        q3_responsible: surveyData.value.q3_responsible,
        q3_adjust_behavior: surveyData.value.q3_adjust_behavior,
        q3_adjust_decision: surveyData.value.q3_adjust_decision,
        q3_adjust_willingness: surveyData.value.q3_adjust_willingness,
        satisfaction: surveyData.value.satisfaction,
        helpfulness: surveyData.value.helpfulness,
        willingness_to_continue: surveyData.value.willingness_to_continue,
        willingness_to_recommend: surveyData.value.willingness_to_recommend
      }
    }
    await api.post('/assessment/survey', payload)
    phase.value = 'instructions'
  } catch (e) {
    toast.error(e.response?.data?.message || '提交失败，请重试')
  } finally {
    submittingSurvey.value = false
  }
}

// ========== 词汇测试 ==========
const loading = ref(false)
const questions = ref([])
const currentIndex = ref(0)
const answers = ref([])
const currentQuestion = ref(null)

// 倒计时
const timeLeft = ref(180)
let timerInterval = null
const timerDisplay = computed(() => {
  const m = Math.floor(timeLeft.value / 60)
  const s = timeLeft.value % 60
  return `${m}:${s.toString().padStart(2, '0')}`
})

const startQuestions = async () => {
  phase.value = 'questions'
  loading.value = true
  try {
    const res = await api.get('/assessment/questions')
    questions.value = res.questions
    currentQuestion.value = questions.value[0]
    // 开始倒计时
    timeLeft.value = 180
    timerInterval = setInterval(() => {
      timeLeft.value--
      if (timeLeft.value <= 0) {
        clearInterval(timerInterval)
        submitAssessment()
      }
    }, 1000)
  } catch (e) {
    toast.error('题目加载失败，请刷新页面重试')
  } finally {
    loading.value = false
  }
}

const handleAnswer = (answer) => {
  answers.value.push(answer)
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    currentQuestion.value = questions.value[currentIndex.value]
  } else {
    clearInterval(timerInterval)
    submitAssessment()
  }
}

const submitAssessment = async () => {
  clearInterval(timerInterval)
  currentQuestion.value = null
  try {
    await api.post('/assessment/submit', { answers: answers.value })
    // 进入发音测试
    await loadPronWords()
    phase.value = 'pronunciation'
  } catch (e) {
    toast.error('提交失败，请重试')
  }
}

// ========== 发音测试 ==========
const pronWords = ref([])
const pronIndex = ref(0)
const pronRecorded = ref({})  // { index: true } 是否有录音
const pronBlobs = {}          // { index: Blob } 本地暂存录音
const isRecording = ref(false)
const isUploading = ref(false)
let mediaRecorder = null
let audioChunks = []
let pendingStop = false

const loadPronWords = async () => {
  const res = await api.get('/assessment/pronunciation_words')
  pronWords.value = res.words
}

const startRecording = async (e) => {
  if (isUploading.value || isRecording.value) return
  const btn = e.target.closest('button')
  if (btn && e.pointerId !== undefined) btn.setPointerCapture(e.pointerId)

  pendingStop = false
  mediaRecorder = null
  isRecording.value = true

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    if (pendingStop) {
      stream.getTracks().forEach(t => t.stop())
      isRecording.value = false
      pendingStop = false
      return
    }
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data)
    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: 'audio/mp4' })
      stream.getTracks().forEach(t => t.stop())
      // 只存本地，覆盖上一次
      pronBlobs[pronIndex.value] = blob
      pronRecorded.value[pronIndex.value] = true
    }
    mediaRecorder.start()
  } catch (e) {
    isRecording.value = false
    pendingStop = false
    toast.error('无法访问麦克风，请检查权限')
  }
}

const stopRecording = () => {
  if (!isRecording.value) return
  if (!mediaRecorder || mediaRecorder.state !== 'recording') {
    pendingStop = true
    return
  }
  mediaRecorder.stop()
  mediaRecorder = null
  isRecording.value = false
}

const uploadCurrentPron = async () => {
  const idx = pronIndex.value
  const blob = pronBlobs[idx]
  if (!blob) return
  isUploading.value = true
  const formData = new FormData()
  formData.append('audio', blob, 'pron.m4a')
  formData.append('word_index', idx)
  formData.append('target_word', pronWords.value[idx].french)
  try {
    await api.post('/assessment/upload_pronunciation', formData)
  } catch (e) {
    toast.error('录音上传失败，请重试')
    throw e
  } finally {
    isUploading.value = false
  }
}

const nextPronWord = async () => {
  try {
    await uploadCurrentPron()
  } catch { return }
  if (pronIndex.value < pronWords.value.length - 1) {
    pronIndex.value++
  } else {
    router.push('/result')
  }
}

onBeforeUnmount(() => {
  clearInterval(timerInterval)
})
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
  max-width: 600px;
  margin: 0 auto;
}
.survey-card-long {
  max-height: 85vh;
  overflow-y: auto;
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
.stars-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.3rem;
  margin-bottom: 2rem;
}
.star-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.2rem;
  transition: transform 0.15s;
}
.star-btn:hover { transform: scale(1.15); }
.stars-label {
  font-size: 0.85rem;
  color: var(--ink-muted);
  margin-left: 0.5rem;
  font-weight: 600;
}
.survey-section {
  margin-bottom: 1.5rem;
  text-align: left;
}
.section-lead {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 0.8rem;
  line-height: 1.6;
  padding: 0.6rem 0.8rem;
  background: rgba(123, 155, 244, 0.06);
  border-left: 3px solid var(--accent);
  border-radius: 0 4px 4px 0;
}
.survey-items {
  display: flex;
  flex-direction: column;
  gap: 0.9rem;
  margin-bottom: 0.8rem;
}
.survey-item { text-align: left; }
.item-label {
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--ink);
  margin-bottom: 0.3rem;
  line-height: 1.4;
}
.likert-row {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}
.likert-hint {
  font-size: 0.58rem;
  color: var(--ink-faint);
  white-space: nowrap;
  min-width: 2.6em;
}
.likert-hint:last-child { text-align: right; }
.likert-dots {
  display: flex;
  gap: 0.25rem;
  flex: 1;
  justify-content: center;
}
.likert-dot {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: var(--surface);
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--ink-muted);
  cursor: pointer;
  transition: all 0.2s var(--ease);
  display: flex;
  align-items: center;
  justify-content: center;
}
.likert-dot:hover { border-color: var(--accent); color: var(--accent); }
.likert-dot.active { border-color: var(--accent); background: var(--accent); color: white; }
.btn-row {
  display: flex;
  gap: 0.8rem;
  justify-content: center;
  flex-wrap: nowrap;
}
.btn-ghost {
  flex: 1;
  padding: 0.7rem 1rem;
  white-space: nowrap;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--ink-secondary);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-ghost:hover { border-color: var(--ink-muted); color: var(--ink); }

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
  margin: 0.5rem 0;
}
.instructions-body li { margin-bottom: 0.3rem; }
.instructions-body strong { color: var(--ink); }
.red-note { color: #e53e3e; font-weight: 600; margin-top: 0.5rem; }
.instructions-section {
  margin: 1rem 0;
  padding: 0.8rem 1rem;
  background: var(--bg);
  border-radius: var(--radius);
}
.instructions-section h3 {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 0.3rem;
}

/* 倒计时 */
.timer-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.6rem;
  margin-bottom: 0.8rem;
  font-size: 1.1rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
  color: var(--ink-secondary);
  background: var(--surface);
  border-radius: var(--radius);
  border: 1px solid var(--border-light);
}
.timer-bar.urgent { color: #ef4444; border-color: #fecaca; background: #fef2f2; }

/* 发音测试 */
.pron-card {
  background: var(--surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow);
  padding: 2rem 1.5rem;
  text-align: center;
}
.pron-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.pron-progress {
  font-size: 0.75rem;
  color: var(--ink-faint);
  letter-spacing: 0.08em;
  font-variant-numeric: tabular-nums;
}
.pron-word {
  font-family: var(--font-display);
  font-size: 2.8rem;
  font-weight: 600;
  color: var(--ink);
  letter-spacing: 0.02em;
}
.pron-phonetic {
  font-size: 1rem;
  color: var(--ink-muted);
  margin: 0.3rem 0;
}
.pron-chinese {
  font-size: 0.95rem;
  color: var(--ink-secondary);
  margin-bottom: 1.5rem;
}
.pron-actions {
  display: flex;
  justify-content: center;
  gap: 2.5rem;
  margin-bottom: 1.8rem;
}
.pron-action-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
}
.action-label {
  font-size: 0.7rem;
  color: var(--ink-muted);
}
.play-btn {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: 2px solid var(--accent);
  background: var(--accent-subtle);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
}
.play-btn:hover:not(:disabled) { background: var(--accent); color: white; }
.play-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.rec-btn {
  position: relative;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: var(--surface);
  color: var(--ink-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  overflow: visible;
  -webkit-user-select: none;
  user-select: none;
  touch-action: none;
  -webkit-tap-highlight-color: transparent;
}
.rec-btn:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }
.rec-btn.recording-active { border-color: #ef4444; background: #fef2f2; color: #ef4444; }
.rec-btn:disabled { opacity: 0.35; cursor: not-allowed; }
.wave {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid #ef4444;
  top: 0; left: 0;
  opacity: 0;
  z-index: 1;
}
.rec-btn.recording-active .wave { animation: wave-out 1.2s ease-out infinite; }
@keyframes wave-out {
  0%   { transform: scale(1);    opacity: 0.6; }
  100% { transform: scale(2.4);  opacity: 0; }
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
.btn-primary:hover:not(:disabled) { opacity: 0.9; }
.btn-primary:active:not(:disabled) { transform: scale(0.98); }
.btn-primary:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
