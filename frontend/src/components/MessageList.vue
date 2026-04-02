<template>
  <div class="message-list" ref="listEl">
    <div v-if="showDateDivider" class="date-divider">
      <span>Day {{ studyDay }} · {{ formattedDate }}</span>
    </div>
    <ChatBubble
      v-for="msg in messages"
      :key="msg.id || msg.timestamp"
      :content="msg.content"
      :type="msg.type"
      :isUser="msg.role === 'user'"
      :disabled="isDisabled"
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
  isDisabled: { type: Boolean, default: false }
})

defineEmits(['recorded'])

const listEl = ref(null)

const formattedDate = new Date().toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' })
const showDateDivider = ref(true)

const scrollToBottom = () => {
  nextTick(() => {
    if (listEl.value) {
      listEl.value.scrollTop = listEl.value.scrollHeight
    }
  })
}

watch(() => props.messages.length, scrollToBottom)
</script>

<style scoped>
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
}
.date-divider {
  text-align: center;
  color: #999;
  font-size: 0.85rem;
  padding: 0.5rem 0;
  margin: 0.5rem 0;
}
.date-divider span {
  background: #e8e8e8;
  padding: 0.3rem 0.8rem;
  border-radius: 12px;
}
</style>
