<template>
  <div class="question-card fade-up">
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: ((current + 1) / total) * 100 + '%' }"></div>
    </div>
    <div class="progress-text">{{ current + 1 }} / {{ total }}</div>
    <div class="word-display">{{ question.french }}</div>
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
    emit('answered', { question_id: props.question.id, french: props.question.french, user_choice: option })
    selected.value = null
  }, 300)
}

watch(() => props.question, () => { selected.value = null })
</script>

<style scoped>
.question-card {
  background: var(--surface);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow);
  overflow: hidden;
  padding: 0 0 2rem;
}
.progress-bar {
  height: 3px;
  background: var(--border-light);
}
.progress-fill {
  height: 100%;
  background: var(--accent);
  transition: width 0.4s var(--ease);
}
.progress-text {
  text-align: center;
  font-size: 0.75rem;
  color: var(--ink-faint);
  margin-top: 1.2rem;
  letter-spacing: 0.08em;
  font-variant-numeric: tabular-nums;
}
.word-display {
  text-align: center;
  font-family: var(--font-display);
  font-size: 2.8rem;
  font-weight: 600;
  color: var(--ink);
  padding: 1.5rem 1rem 2rem;
  letter-spacing: 0.02em;
}
.options {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  padding: 0 1.5rem;
}
.option {
  padding: 0.85rem 1rem;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  font-size: 0.95rem;
  color: var(--ink);
  cursor: pointer;
  transition: all 0.2s var(--ease);
  text-align: left;
}
.option:hover {
  border-color: var(--accent);
  background: var(--accent-subtle);
}
.option.selected {
  border-color: var(--accent);
  background: var(--accent);
  color: white;
}
</style>
