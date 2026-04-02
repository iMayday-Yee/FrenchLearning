<template>
  <div class="chat-page">
    <header class="chat-header">
      <div class="avatar">
        <img :src="`/avatars/${avatarType}.png`" :alt="avatarType">
      </div>
      <div class="info">
        <h3>法语学习助手</h3>
        <span class="day">Day {{ studyDay }}</span>
      </div>
    </header>

    <MessageList :messages="chatMessages" :studyDay="studyDay" :isDisabled="isThinking" @recorded="handleRecorded" />

    <div v-if="remainingRounds === 0" class="rounds-exceeded">
      今天的对话次数已用完啦，明天再来继续学习吧！
    </div>

    <footer class="chat-footer">
      <div class="remaining-hint">剩余 {{ Math.max(0, remainingRounds) }} 次对话</div>
      <div class="input-area">
        <input v-model="inputText" type="text" placeholder="输入消息..." @keyup.enter="sendMessage" :disabled="isThinking || remainingRounds === 0">
        <button @click="sendMessage" :disabled="isThinking || !inputText.trim() || remainingRounds === 0">
          {{ isThinking ? '思考中...' : '发送' }}
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
import MessageList from '@/components/MessageList.vue'

const userStore = useUserStore()
const studyStore = useStudyStore()

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
    console.error('Failed to load history', e)
  }
}

const sendMessage = async () => {
  if (!inputText.value.trim() || isThinking.value) return

  const text = inputText.value
  inputText.value = ''

  // 添加用户消息
  chatMessages.value.push({
    id: Date.now(),
    role: 'user',
    type: 'text',
    content: text,
    timestamp: new Date().toISOString()
  })

  // 添加思考中消息
  thinkingMsgId.value = Date.now() + 1
  chatMessages.value.push({
    id: thinkingMsgId.value,
    role: 'assistant',
    type: 'thinking',
    content: '正在思考...',
    timestamp: new Date().toISOString()
  })

  isThinking.value = true

  try {
    const res = await api.post('/chat/send', { content: text })

    // 移除思考中消息
    chatMessages.value = chatMessages.value.filter(m => m.id !== thinkingMsgId.value)

    if (res.messages) {
      res.messages.forEach(msg => {
        chatMessages.value.push({
          id: Date.now() + Math.random(),
          role: 'assistant',
          type: msg.type,
          content: msg.content,
          timestamp: new Date().toISOString()
        })
      })
    }

    remainingRounds.value = res.remaining_rounds
  } catch (e) {
    // 移除思考中消息
    chatMessages.value = chatMessages.value.filter(m => m.id !== thinkingMsgId.value)
    console.error('Failed to send message', e)
  } finally {
    isThinking.value = false
    thinkingMsgId.value = null
  }
}

const handleRecorded = async (blob, wordIndex) => {
  if (isThinking.value || remainingRounds.value === 0) return

  const formData = new FormData()
  formData.append('audio', blob, 'recording.webm')
  if (wordIndex !== undefined && wordIndex !== null) {
    formData.append('word_index', wordIndex)
  }

  // 添加用户录音消息
  const userMsgId = Date.now()
  chatMessages.value.push({
    id: userMsgId,
    role: 'user',
    type: 'user_audio',
    content: URL.createObjectURL(blob),
    timestamp: new Date().toISOString()
  })

  // 添加思考中消息
  thinkingMsgId.value = Date.now() + 1
  chatMessages.value.push({
    id: thinkingMsgId.value,
    role: 'assistant',
    type: 'thinking',
    content: '正在思考...',
    timestamp: new Date().toISOString()
  })

  isThinking.value = true

  try {
    const res = await api.post('/chat/upload_audio', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    // 移除思考中消息
    chatMessages.value = chatMessages.value.filter(m => m.id !== thinkingMsgId.value)

    if (res.messages) {
      res.messages.forEach(msg => {
        chatMessages.value.push({
          id: Date.now() + Math.random(),
          role: 'assistant',
          type: msg.type,
          content: msg.content,
          timestamp: new Date().toISOString()
        })
      })
    }

    remainingRounds.value = res.remaining_rounds
  } catch (e) {
    // 移除思考中消息
    chatMessages.value = chatMessages.value.filter(m => m.id !== thinkingMsgId.value)
    console.error('Failed to upload audio', e)
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
          id: Date.now() + Math.random(),
          role: 'assistant',
          type: msg.type,
          content: msg.content,
          timestamp: new Date().toISOString()
        })
      })
    }
  } catch (e) {
    console.error('Failed to call enter API', e)
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
  background: #f5f5f5;
  max-width: 500px;
  margin: 0 auto;
  background: white;
}
.chat-header {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem 1rem;
  background: white;
  border-bottom: 1px solid #eee;
}
.avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}
.info h3 {
  font-size: 1rem;
  margin: 0;
}
.info .day {
  font-size: 0.75rem;
  color: #888;
}
.chat-footer {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.8rem;
  background: white;
  border-top: 1px solid #eee;
}
.remaining-hint {
  font-size: 0.75rem;
  color: #888;
  white-space: nowrap;
}
.input-area {
  flex: 1;
  display: flex;
  gap: 0.5rem;
}
.input-area input {
  flex: 1;
  padding: 0.6rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
}
.input-area button {
  padding: 0.6rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
}
.input-area button:disabled {
  background: #ccc;
}
.rounds-exceeded {
  text-align: center;
  padding: 0.8rem;
  background: #fff7e6;
  color: #fa8c16;
  font-size: 0.9rem;
}
</style>
