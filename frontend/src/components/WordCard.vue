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
  background: linear-gradient(135deg, var(--accent) 0%, #98B2F7 100%);
  padding: 1rem 1.4rem;
  border-radius: var(--radius);
  min-width: 120px;
  box-shadow: 0 2px 10px rgba(123,155,244,0.2);
  position: relative;
}
.word-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius);
  background: linear-gradient(180deg, rgba(255,255,255,0.1) 0%, transparent 100%);
  pointer-events: none;
}
.word {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 600;
  color: white;
  margin-bottom: 0.2rem;
  text-shadow: 0 1px 3px rgba(0,0,0,0.1);
  position: relative;
}
.meaning {
  font-size: 0.85rem;
  color: rgba(255,255,255,0.85);
  position: relative;
}
</style>
