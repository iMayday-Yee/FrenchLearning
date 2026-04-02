<template>
  <div class="question">
    <div class="progress">{{ current + 1 }} / {{ total }}</div>
    <div class="word">{{ question.french }}</div>
    <div class="options">
      <button
        v-for="(option, idx) in question.options"
        :key="idx"
        :class="['option', { selected: selected === option }]"
        @click="selectOption(option)"
      >
        {{ option }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  question: { type: Object, required: true },
  current: { type: Number, required: true },
  total: { type: Number, required: true }
})

const emit = defineEmits(['answered'])
const selected = ref(null)

const selectOption = (option) => {
  selected.value = option
  setTimeout(() => {
    emit('answered', { question_id: props.question.id, user_choice: option })
    selected.value = null
  }, 300)
}

watch(() => props.question, () => {
  selected.value = null
})
</script>

<style scoped>
.question {
  text-align: center;
  padding: 2rem 1rem;
}
.progress {
  color: #888;
  margin-bottom: 1.5rem;
}
.word {
  font-size: 2.5rem;
  color: #667eea;
  margin-bottom: 2rem;
}
.options {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  max-width: 300px;
  margin: 0 auto;
}
.option {
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  background: white;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s;
}
.option:hover {
  border-color: #667eea;
}
.option.selected {
  border-color: #667eea;
  background: #667eea;
  color: white;
}
</style>
