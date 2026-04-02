<template>
  <div class="word-card">
    <div class="word">{{ data.french }}</div>
    <div class="meaning">{{ data.chinese }}</div>
  </div>
</template>

<script setup>
defineProps({
  data: { type: Object, required: true }
})
</script>

<style scoped>
.word-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  min-width: 120px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}
.word {
  font-size: 1.4rem;
  font-weight: bold;
  margin-bottom: 0.3rem;
}
.meaning {
  font-size: 1rem;
  opacity: 0.9;
}
</style>
