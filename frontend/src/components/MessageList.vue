<template>
  <div class="message-list" ref="listEl">
    <div class="day-divider">
      <span class="divider-line"></span>
      <span class="divider-pill">Jour {{ studyDay }}</span>
      <span class="divider-line"></span>
    </div>
    <ChatBubble
      v-for="msg in messages"
      :key="msg.id || msg.timestamp"
      :content="msg.content"
      :type="msg.type"
      :isUser="msg.role === 'user'"
      :disabled="isDisabled"
      :avatarType="avatarType"
      @recorded="(blob, idx) => $emit('recorded', blob, idx)"
    />
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import ChatBubble from './ChatBubble.vue'

const props = defineProps({
  messages: { type: Array, default: () => [] },
  studyDay: { type: Number, default: 1 },
  isDisabled: { type: Boolean, default: false },
  avatarType: { type: String, default: 'human' }
})

defineEmits(['recorded'])
const listEl = ref(null)

watch(() => props.messages.length, () => {
  nextTick(() => {
    if (listEl.value) listEl.value.scrollTop = listEl.value.scrollHeight
  })
})
</script>

<style scoped>
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem 1.2rem 0.5rem;
  display: flex;
  flex-direction: column;
  scroll-behavior: smooth;
  position: relative;
  z-index: 1;
}
.day-divider {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin: 0.3rem 0 1.2rem;
}
.divider-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(123,155,244,0.15), transparent);
}
.divider-pill {
  font-family: var(--font-display);
  font-size: 0.78rem;
  font-style: italic;
  color: var(--accent);
  letter-spacing: 0.08em;
  padding: 0.2rem 0.8rem;
  background: rgba(123,155,244,0.06);
  border-radius: var(--radius-xl);
}
</style>
