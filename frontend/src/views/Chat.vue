<template>
  <div class="chat-page">
    <div class="chat-bg"></div>
    <header class="chat-header">
      <div class="header-side"></div>
      <h3 class="header-title">法语助手</h3>
      <div class="header-side header-right">
        <div class="rounds-tag">{{ Math.max(0, remainingRounds) }}/20</div>
      </div>
    </header>

    <MessageList :messages="chatMessages" :studyDay="studyDay" :isDisabled="isThinking" :avatarType="avatarType" @recorded="handleRecorded" />

    <div v-if="remainingRounds === 0" class="rounds-banner">
      <span>Terminé</span> — 今天的对话次数已用完，明天再来
    </div>

    <footer class="chat-footer">
      <div class="input-row">
        <input
          v-model="inputText"
          type="text"
          placeholder="输入消息..."
          @keyup.enter="sendMessage"
          :disabled="isThinking || remainingRounds === 0"
        >
        <button class="send-btn" @click="sendMessage" :disabled="isThinking || !inputText.trim() || remainingRounds === 0">
          <svg v-if="!isThinking" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          <span v-else class="spinner"></span>
        </button>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import { useUserStore } from '@/stores/user'
import { useStudyStore } from '@/stores/study'
import { useToastStore } from '@/stores/toast'
import MessageList from '@/components/MessageList.vue'

const userStore = useUserStore()
const studyStore = useStudyStore()
const toast = useToastStore()

const inputText = ref('')
const chatMessages = ref([])
const studyDay = ref(1)
const remainingRounds = ref(20)
const avatarType = ref('human')
const isThinking = ref(false)
const thinkingMsgId = ref(null)

const loadHistory = async () => {
  try {
    const res = await api.get('/chat/history')
    chatMessages.value = res.messages || []
  } catch (e) {
    toast.error('聊天记录加载失败')
  }
}

const sendMessage = async () => {
  if (!inputText.value.trim() || isThinking.value) return
  const text = inputText.value
  inputText.value = ''

  chatMessages.value.push({
    id: Date.now(), role: 'user', type: 'text',
    content: text, timestamp: new Date().toISOString()
  })

  thinkingMsgId.value = Date.now() + 1
  chatMessages.value.push({
    id: thinkingMsgId.value, role: 'assistant', type: 'thinking',
    content: '', timestamp: new Date().toISOString()
  })
  isThinking.value = true

  try {
    const res = await api.post('/chat/send', { content: text })
    chatMessages.value = chatMessages.value.filter(m => m.id !== thinkingMsgId.value)
    if (res.messages) {
      res.messages.forEach(msg => {
        chatMessages.value.push({
          id: Date.now() + Math.random(), role: 'assistant',
          type: msg.type, content: msg.content, timestamp: new Date().toISOString()
        })
      })
    }
    remainingRounds.value = res.remaining_rounds
  } catch (e) {
    chatMessages.value = chatMessages.value.filter(m => m.id !== thinkingMsgId.value)
    toast.error('消息发送失败，请重试')
  } finally {
    isThinking.value = false
    thinkingMsgId.value = null
  }
}

const handleRecorded = async (blob, wordIndex) => {
  if (isThinking.value || remainingRounds.value === 0) return
  const formData = new FormData()
  formData.append('audio', blob, 'recording.webm')
  if (wordIndex !== undefined && wordIndex !== null) formData.append('word_index', wordIndex)

  chatMessages.value.push({
    id: Date.now(), role: 'user', type: 'user_audio',
    content: URL.createObjectURL(blob), timestamp: new Date().toISOString()
  })

  thinkingMsgId.value = Date.now() + 1
  chatMessages.value.push({
    id: thinkingMsgId.value, role: 'assistant', type: 'thinking',
    content: '', timestamp: new Date().toISOString()
  })
  isThinking.value = true

  try {
    const res = await api.post('/chat/upload_audio', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    chatMessages.value = chatMessages.value.filter(m => m.id !== thinkingMsgId.value)
    if (res.messages) {
      res.messages.forEach(msg => {
        chatMessages.value.push({
          id: Date.now() + Math.random(), role: 'assistant',
          type: msg.type, content: msg.content, timestamp: new Date().toISOString()
        })
      })
    }
    remainingRounds.value = res.remaining_rounds
  } catch (e) {
    chatMessages.value = chatMessages.value.filter(m => m.id !== thinkingMsgId.value)
    toast.error('录音上传失败，请重试')
  } finally {
    isThinking.value = false
    thinkingMsgId.value = null
  }
}

const callEnterAPI = async () => {
  try {
    const res = await api.post('/study/enter')
    if (res.auto_messages && res.auto_messages.length > 0) {
      res.auto_messages.forEach(msg => {
        chatMessages.value.push({
          id: Date.now() + Math.random(), role: 'assistant',
          type: msg.type, content: msg.content, timestamp: new Date().toISOString()
        })
      })
    }
  } catch (e) {
    // 静默处理
  }
}

onMounted(async () => {
  await userStore.fetchProfile()
  avatarType.value = userStore.avatarType || 'human'
  await studyStore.fetchStatus()
  studyDay.value = studyStore.studyDay || 1
  remainingRounds.value = studyStore.remainingRounds || 20

  await loadHistory()
  await callEnterAPI()

  let hiddenAt = null
  document.addEventListener('visibilitychange', async () => {
    if (document.hidden) {
      hiddenAt = Date.now()
    } else {
      if (hiddenAt && (Date.now() - hiddenAt) > 5 * 60 * 1000) {
        await loadHistory()
        await callEnterAPI()
      }
      hiddenAt = null
    }
  })
})
</script>

<style scoped>
.chat-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  background: #F0F2F8;
}
/* 柔和的背景纹理层 */
.chat-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(ellipse 50% 40% at 10% 0%, rgba(123,155,244,0.06) 0%, transparent 70%),
    radial-gradient(ellipse 40% 50% at 90% 100%, rgba(123,205,168,0.05) 0%, transparent 70%),
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 40px,
      rgba(123,155,244,0.015) 40px,
      rgba(123,155,244,0.015) 41px
    ),
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 40px,
      rgba(123,155,244,0.015) 40px,
      rgba(123,155,244,0.015) 41px
    );
}

/* 毛玻璃头部 */
.chat-header {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1.2rem;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(228, 231, 238, 0.6);
}
.header-side {
  width: 50px;
  flex-shrink: 0;
}
.header-right {
  display: flex;
  justify-content: flex-end;
}
.header-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--ink);
  text-align: center;
  letter-spacing: 0.02em;
}
.rounds-tag {
  padding: 0.2rem 0.6rem;
  border-radius: var(--radius);
  background: rgba(123,155,244,0.08);
  color: var(--accent);
  font-size: 0.72rem;
  font-weight: 600;
  font-variant-numeric: tabular-nums;
}

.rounds-banner {
  position: relative;
  z-index: 10;
  padding: 0.7rem 1rem;
  background: rgba(255,255,255,0.7);
  backdrop-filter: blur(8px);
  border-top: 1px solid rgba(228,231,238,0.5);
  font-size: 0.82rem;
  color: var(--ink-secondary);
  text-align: center;
}
.rounds-banner span {
  font-family: var(--font-display);
  font-style: italic;
  color: var(--accent);
  font-weight: 600;
}

/* 毛玻璃底栏 */
.chat-footer {
  position: relative;
  z-index: 10;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-top: 1px solid rgba(228, 231, 238, 0.6);
}
.input-row {
  display: flex;
  gap: 0.6rem;
  align-items: center;
}
.input-row input {
  flex: 1;
  padding: 0.75rem 1.1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  font-size: 0.9rem;
  color: var(--ink);
  background: var(--surface);
  outline: none;
  transition: all 0.25s var(--ease);
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
}
.input-row input:focus {
  border-color: var(--accent-light);
  box-shadow: 0 0 0 3px var(--accent-subtle), 0 2px 8px rgba(123,155,244,0.08);
}
.input-row input::placeholder { color: var(--ink-faint); }
.input-row input:disabled { opacity: 0.4; }
.send-btn {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.25s var(--ease);
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(123,155,244,0.25);
}
.send-btn:hover:not(:disabled) {
  transform: scale(1.08);
  box-shadow: 0 4px 14px rgba(123,155,244,0.35);
}
.send-btn:disabled { opacity: 0.25; cursor: not-allowed; box-shadow: none; }
.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
