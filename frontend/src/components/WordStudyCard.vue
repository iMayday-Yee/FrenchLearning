<template>
  <div class="word-study-card">
    <div class="word-header">
      <div class="word-left">
        <div class="word-french">{{ data.french }}</div>
        <div class="word-chinese">{{ data.chinese }}</div>
      </div>
      <div v-if="data.phonetic" class="word-phonetic">{{ data.phonetic }}</div>
    </div>
    <div class="word-actions">
      <AudioPlayer :url="data.audio_url" :word="data.french" />
      <button
        class="rec-btn"
        @mousedown="startRecording"
        @mouseup="stopRecording"
        @touchstart.prevent="startRecording"
        @touchend.prevent="stopRecording"
        :class="{ recording: isRecording }"
        :disabled="disabled"
      >
        <svg v-if="!isRecording" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/></svg>
        <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><rect x="4" y="4" width="16" height="16" rx="2"/></svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AudioPlayer from './AudioPlayer.vue'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()

const props = defineProps({
  data: { type: Object, required: true },
  disabled: { type: Boolean, default: false }
})

const emit = defineEmits(['recorded'])
const isRecording = ref(false)
let mediaRecorder = null
let audioChunks = []

const startRecording = async () => {
  if (props.disabled || isRecording.value) return
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data)
    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: 'audio/webm' })
      emit('recorded', blob, props.data.word_index)
      stream.getTracks().forEach(track => track.stop())
    }
    mediaRecorder.start()
    isRecording.value = true
  } catch (e) {
    toast.error('无法访问麦克风，请检查权限')
  }
}

const stopRecording = () => {
  if (mediaRecorder && isRecording.value) {
    mediaRecorder.stop()
    isRecording.value = false
  }
}
</script>

<style scoped>
.word-study-card {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(6px);
  border-radius: var(--radius);
  box-shadow: 0 2px 12px rgba(0,0,0,0.05), 0 0 0 1px rgba(228,231,238,0.5);
  overflow: hidden;
  min-width: 260px;
  max-width: 360px;
}
.word-header {
  background: linear-gradient(135deg, var(--accent) 0%, #98B2F7 100%);
  padding: 1rem 1.3rem;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.8rem;
}
.word-header::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(255,255,255,0.08) 0%, transparent 100%);
  pointer-events: none;
}
.word-left {
  position: relative;
}
.word-french {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 600;
  color: white;
  text-shadow: 0 1px 3px rgba(0,0,0,0.1);
  line-height: 1.2;
}
.word-phonetic {
  font-size: 1rem;
  color: rgba(255,255,255,0.9);
  position: relative;
  white-space: nowrap;
  text-align: right;
}
.word-chinese {
  font-size: 0.92rem;
  color: rgba(255,255,255,0.88);
  position: relative;
}
.word-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem;
}
.rec-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: var(--surface);
  color: var(--ink-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.25s var(--ease);
  flex-shrink: 0;
}
.rec-btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
  box-shadow: 0 0 0 4px var(--accent-subtle);
}
.rec-btn.recording {
  border-color: var(--rose);
  background: var(--rose-subtle);
  color: var(--rose);
  animation: pulse-rec 1.2s infinite;
}
.rec-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
@keyframes pulse-rec {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.08); box-shadow: 0 0 0 8px rgba(240,160,176,0.12); }
}
</style>
