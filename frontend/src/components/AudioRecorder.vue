<template>
  <div class="recorder">
    <button :class="['record-btn', { recording: isRecording, disabled: disabled }]" @mousedown="startRecording" @mouseup="stopRecording" @touchstart.prevent="startRecording" @touchend.prevent="stopRecording" :disabled="disabled">
      {{ isRecording ? '⏹' : '🎤' }}
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

const startRecording = async () => {
  if (props.disabled) return
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioChunks = []

    mediaRecorder.ondataavailable = (e) => {
      audioChunks.push(e.data)
    }

    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: 'audio/webm' })
      emit('recorded', blob)
      stream.getTracks().forEach(track => track.stop())
    }

    mediaRecorder.start()
    isRecording.value = true
  } catch (e) {
    alert('无法访问麦克风，请检查权限设置')
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
.recorder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}
.record-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  border: none;
  background: #667eea;
  color: white;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.2s;
}
.record-btn.recording {
  background: #f5222d;
  animation: pulse 1s infinite;
}
.record-btn.disabled {
  background: #ccc;
  cursor: not-allowed;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}
.hint {
  font-size: 0.7rem;
  color: #888;
}
</style>
