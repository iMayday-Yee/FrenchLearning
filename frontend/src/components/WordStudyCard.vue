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
        @pointerdown.prevent="startRecording"
        @pointerup.prevent="stopRecording"
        @lostpointercapture="stopRecording"
        @contextmenu.prevent
        :class="{ recording: isRecording, 'recording-active': isRecording }"
        :disabled="disabled"
        :title="isRecording ? '松开发送' : '按住说话'"
      >
        <div class="rec-inner">
          <svg v-if="!isRecording" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/></svg>
          <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>
        </div>
        <div v-if="isRecording" class="wave"></div>
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
let pendingStop = false

const startRecording = async (e) => {
  if (props.disabled || isRecording.value) return

  const btn = e.target.closest('button')
  if (btn && e.pointerId !== undefined) {
    btn.setPointerCapture(e.pointerId)
  }

  pendingStop = false
  mediaRecorder = null
  isRecording.value = true

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })

    if (pendingStop) {
      stream.getTracks().forEach(track => track.stop())
      isRecording.value = false
      pendingStop = false
      return
    }

    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data)
    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: 'audio/webm' })
      emit('recorded', blob, props.data.word_index)
      stream.getTracks().forEach(track => track.stop())
    }
    mediaRecorder.start()
  } catch (e) {
    isRecording.value = false
    pendingStop = false
    toast.error('无法访问麦克风，请检查权限')
  }
}

const stopRecording = () => {
  if (!isRecording.value) return

  if (!mediaRecorder || mediaRecorder.state !== 'recording') {
    pendingStop = true
    return
  }

  mediaRecorder.stop()
  mediaRecorder = null
  isRecording.value = false
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
  position: relative;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: var(--surface);
  color: var(--ink-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s, box-shadow 0.2s;
  flex-shrink: 0;
  -webkit-user-select: none;
  user-select: none;
  overflow: visible;
  touch-action: none;
  -webkit-tap-highlight-color: transparent;
}
.rec-btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-subtle);
}
.rec-btn.recording-active {
  border-color: #ef4444;
  background: #fef2f2;
  color: #ef4444;
  box-shadow: 0 0 0 0 rgba(239,68,68,0);
}
.rec-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
.rec-inner {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s;
}
.rec-btn.recording-active .rec-inner {
  transform: scale(1.1);
}
/* 对讲机声波动画 */
.wave {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 2px solid #ef4444;
  top: 0; left: 0;
  opacity: 0;
  z-index: 1;
}
.rec-btn.recording-active .wave {
  animation: wave-out 1.2s ease-out infinite;
}
@keyframes wave-out {
  0%   { transform: scale(1);    opacity: 0.6; }
  100% { transform: scale(2.4);  opacity: 0; }
}
</style>
