<template>
  <div class="toast-container">
    <transition-group name="toast">
      <div v-for="msg in messages" :key="msg.id" :class="['toast', msg.type]">
        {{ msg.text }}
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useToastStore } from '@/stores/toast'
const toastStore = useToastStore()
const messages = computed(() => toastStore.messages)
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  pointer-events: none;
  width: 90%;
  max-width: 360px;
}
.toast {
  padding: 0.7rem 1.2rem;
  border-radius: 10px;
  font-size: 0.85rem;
  line-height: 1.4;
  text-align: center;
  pointer-events: auto;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}
.toast.error {
  background: #FEF2F2;
  color: #B91C1C;
  border: 1px solid #FECACA;
}
.toast.success {
  background: #F0FDF4;
  color: #166534;
  border: 1px solid #BBF7D0;
}
.toast.info {
  background: #EFF6FF;
  color: #1E40AF;
  border: 1px solid #BFDBFE;
}
.toast-enter-active {
  transition: all 0.3s ease;
}
.toast-leave-active {
  transition: all 0.25s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(-12px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
