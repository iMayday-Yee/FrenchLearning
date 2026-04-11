<template>
  <div :class="['bubble', isUser ? 'user' : 'assistant']">
    <img v-if="!isUser" class="avatar" :src="`/avatars/${avatarType}.png`" alt="助手">
    <div class="bubble-content">
      <div v-if="type === 'text'" class="text" v-html="parsedText"></div>
      <div v-else-if="type === 'thinking'" class="thinking">
        <span class="dot"></span><span class="dot"></span><span class="dot"></span>
      </div>
      <WordCard v-else-if="type === 'word_card'" :data="parsedContent" />
      <AudioPlayer v-else-if="type === 'audio'" :url="content.url" :word="content.word" />
      <div v-else-if="type === 'user_audio'" class="user-audio-wrap">
        <AudioPlayer :url="content" :isUser="true" />
      </div>
      <WordStudyCard v-else-if="type === 'word_audio'" :data="parsedContent" :disabled="disabled" @recorded="(blob, idx) => $emit('recorded', blob, idx)" />
    </div>
    <div v-if="isUser" class="avatar user-avatar">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import WordCard from './WordCard.vue'
import AudioPlayer from './AudioPlayer.vue'
import WordStudyCard from './WordStudyCard.vue'

const props = defineProps({
  content: [String, Object],
  type: { type: String, default: 'text' },
  isUser: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  avatarType: { type: String, default: 'human' }
})

defineEmits(['recorded'])

const parsedContent = computed(() => {
  if (typeof props.content === 'string') {
    try { return JSON.parse(props.content) } catch { return props.content }
  }
  return props.content
})

const parsedText = computed(() => {
  if (typeof props.content !== 'string') return props.content
  return props.content.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
})
</script>

<style scoped>
.bubble {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin-bottom: 0.8rem;
  animation: fadeUp 0.3s var(--ease) both;
}
.bubble.user { justify-content: flex-end; }
.bubble.assistant { justify-content: flex-start; }

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  flex-shrink: 0;
  object-fit: cover;
  border: 2px solid rgba(255,255,255,0.8);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin-top: 2px;
}
.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--bg-warm) 0%, var(--surface) 100%);
  color: var(--ink-muted);
  border: 2px solid rgba(255,255,255,0.8);
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.bubble-content {
  min-width: 0;
  max-width: min(75%, 480px);
}

.text {
  padding: 0.7rem 1rem;
  border-radius: var(--radius-lg);
  line-height: 1.6;
  font-size: 0.9rem;
}
.user .text {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%);
  color: white;
  border-bottom-right-radius: var(--radius-sm);
  box-shadow: 0 2px 10px rgba(123,155,244,0.2);
}
.assistant .text {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(6px);
  color: var(--ink);
  border-bottom-left-radius: var(--radius-sm);
  box-shadow: 0 1px 6px rgba(0,0,0,0.04), 0 0 0 1px rgba(228,231,238,0.5);
}

.thinking {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(6px);
  padding: 0.8rem 1.2rem;
  border-radius: var(--radius-lg);
  border-bottom-left-radius: var(--radius-sm);
  box-shadow: 0 1px 6px rgba(0,0,0,0.04), 0 0 0 1px rgba(228,231,238,0.5);
  display: flex;
  gap: 5px;
  align-items: center;
}
.thinking .dot {
  width: 7px;
  height: 7px;
  background: var(--accent-light);
  border-radius: 50%;
  animation: bounce 1.2s infinite;
}
.thinking .dot:nth-child(2) { animation-delay: 0.15s; }
.thinking .dot:nth-child(3) { animation-delay: 0.3s; }
@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.3; }
  40% { transform: translateY(-7px); opacity: 1; }
}

.user-audio-wrap { width: 100%; }
</style>
