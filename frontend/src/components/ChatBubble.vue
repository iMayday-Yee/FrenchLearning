<template>
  <div :class="['bubble', isUser ? 'user' : 'assistant']">
    <div v-if="type === 'text'" class="text">{{ content }}</div>
    <div v-else-if="type === 'thinking'" class="thinking">
      <span class="dot">·</span><span class="dot">·</span><span class="dot">·</span>
    </div>
    <WordCard v-else-if="type === 'word_card'" :data="parsedContent" />
    <AudioPlayer v-else-if="type === 'audio'" :url="content.url" :word="content.word" />
    <div v-else-if="type === 'user_audio'" class="user-audio">
      <AudioPlayer :url="content" :isUser="true" />
    </div>
    <WordStudyCard v-else-if="type === 'word_audio'" :data="parsedContent" :disabled="disabled" @recorded="(blob, idx) => $emit('recorded', blob, idx)" />
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
  disabled: { type: Boolean, default: false }
})

defineEmits(['recorded'])

const parsedContent = computed(() => {
  if (typeof props.content === 'string') {
    try {
      return JSON.parse(props.content)
    } catch {
      return props.content
    }
  }
  return props.content
})
</script>

<style scoped>
.bubble {
  display: flex;
  margin-bottom: 1rem;
}
.bubble.user {
  justify-content: flex-end;
}
.bubble.assistant {
  justify-content: flex-start;
}
.text {
  max-width: 75%;
  padding: 0.8rem 1rem;
  border-radius: 16px;
  line-height: 1.5;
}
.user .text {
  background: #667eea;
  color: white;
  border-bottom-right-radius: 4px;
}
.assistant .text {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}
.thinking {
  background: white;
  color: #999;
  padding: 0.8rem 1.2rem;
  border-radius: 16px;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  font-size: 1.2rem;
  letter-spacing: 4px;
}
.thinking .dot {
  animation: blink 1.4s infinite both;
}
.thinking .dot:nth-child(2) {
  animation-delay: 0.2s;
}
.thinking .dot:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes blink {
  0%, 80%, 100% { opacity: 0; }
  40% { opacity: 1; }
}
.user-audio {
  max-width: 75%;
}
</style>
