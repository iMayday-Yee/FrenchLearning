<template>
  <div class="recorder">
    <button :class="['record-btn', { recording: isRecording, 'recording-active': isRecording, disabled: disabled }]" @mousedown.prevent="startRecording" @mouseup.prevent="stopRecording" @mouseleave="stopRecording" @touchstart.prevent="startRecording" @touchend.prevent="stopRecording" :disabled="disabled" :title="isRecording ? '松开发送' : '按住说话'">
      <div class="rec-inner">
        <svg v-if="!isRecording" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/></svg>
        <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>
      </div>
      <div v-if="isRecording" class="wave"></div>
    </button>
    <span class="hint">{{ isRecording ? '松开结束' : (disabled ? '等待中...' : '按住录音') }}</span>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  disabled: { type: Boolean, default: false }
})

const emit = defineEmits(['recorded'])
const isRecording = ref(false)
let mediaRecorder = null
let audioChunks = []
let holdTimer = null  // 短按超时，区分短按 vs 按住

const startRecording = async () => {
  if (props.disabled || isRecording.value) return
  holdTimer = setTimeout(() => { holdTimer = null }, 300)
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []
    mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data)
    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: 'audio/webm' })
      emit('recorded', blob)
      stream.getTracks().forEach(track => track.stop())
    }
    mediaRecorder.start()
    isRecording.value = true
  } catch (e) {
    clearTimeout(holdTimer)
    alert('无法访问麦克风，请检查权限设置')
  }
}

const stopRecording = () => {
  if (!mediaRecorder || !isRecording.value) return
  // 按住时间不足 300ms 视为误触，不停止
  if (holdTimer) {
    clearTimeout(holdTimer)
    holdTimer = null
    return
  }
  mediaRecorder.stop()
  isRecording.value = false
}
</script>

<style scoped>
.recorder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}
.record-btn {
  position: relative;
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background: var(--surface);
  color: var(--ink-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.2s, color 0.2s, box-shadow 0.2s;
  overflow: visible;
  -webkit-user-select: none;
  user-select: none;
  touch-action: manipulation;
  -webkit-tap-highlight-color: transparent;
}
.record-btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
  box-shadow: 0 0 0 4px var(--accent-subtle);
}
.record-btn.recording-active {
  border-color: #ef4444;
  background: #fef2f2;
  color: #ef4444;
}
.record-btn.disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
.rec-inner {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
}
.rec-inner svg { transition: transform 0.15s; }
.record-btn.recording-active .rec-inner svg { transform: scale(1.1); }
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
.record-btn.recording-active .wave { animation: wave-out 1.2s ease-out infinite; }
@keyframes wave-out {
  0%   { transform: scale(1);    opacity: 0.6; }
  100% { transform: scale(2.4);  opacity: 0; }
}
.hint {
  font-size: 0.7rem;
  color: var(--ink-muted);
}
</style>
