<template>
  <div class="word-study-card">
    <div class="word-section">
      <div class="word">{{ data.french }}</div>
      <div class="meaning">{{ data.chinese }}</div>
    </div>
    <div class="action-section">
      <AudioPlayer :url="data.audio_url" :word="data.french" />
      <button
        class="record-btn"
        @mousedown="startRecording"
        @mouseup="stopRecording"
        @touchstart.prevent="startRecording"
        @touchend.prevent="stopRecording"
        :class="{ recording: isRecording }"
        :disabled="disabled"
      >
        {{ isRecording ? '⏹' : '🎤' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AudioPlayer from './AudioPlayer.vue'

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

    mediaRecorder.ondataavailable = (e) => {
      audioChunks.push(e.data)
    }

    mediaRecorder.onstop = () => {
      const blob = new Blob(audioChunks, { type: 'audio/webm' })
      emit('recorded', blob, props.data.word_index)
      stream.getTracks().forEach(track => track.stop())
    }

    mediaRecorder.start()
    isRecording.value = true
  } catch (e) {
    console.error('Failed to start recording', e)
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
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  padding: 0.8rem;
  min-width: 280px;
  max-width: 320px;
}
.word-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.8rem 1rem;
  border-radius: 8px;
  margin-bottom: 0.6rem;
}
.word {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 0.2rem;
}
.meaning {
  font-size: 0.9rem;
  opacity: 0.9;
}
.action-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.record-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: #667eea;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.record-btn:hover:not(:disabled) {
  background: #5a6fd6;
}
.record-btn.recording {
  background: #f5222d;
  animation: pulse 1s infinite;
}
.record-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}
</style>
