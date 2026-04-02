<template>
  <div :class="['audio-player', { user: isUser }]">
    <button class="play-btn" @click="togglePlay">
      {{ isPlaying ? '⏸' : '▶' }}
    </button>
    <div class="progress-bar" @click="seek">
      <div class="progress" :style="{ width: progress + '%' }"></div>
    </div>
    <span class="time">{{ formatTime(currentTime) }}</span>
    <audio ref="audioEl" :src="url" @timeupdate="updateTime" @ended="isPlaying = false"></audio>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  url: { type: String, required: true },
  word: { type: String, default: '' },
  isUser: { type: Boolean, default: false }
})

const audioEl = ref(null)
const isPlaying = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const progress = ref(0)

const togglePlay = () => {
  if (!audioEl.value) return
  if (isPlaying.value) {
    audioEl.value.pause()
  } else {
    audioEl.value.play()
  }
  isPlaying.value = !isPlaying.value
}

const updateTime = () => {
  if (!audioEl.value) return
  currentTime.value = audioEl.value.currentTime
  duration.value = audioEl.value.duration || 0
  progress.value = duration.value ? (currentTime.value / duration.value) * 100 : 0
}

const seek = (e) => {
  if (!audioEl.value || !duration.value) return
  const rect = e.target.getBoundingClientRect()
  const percent = (e.clientX - rect.left) / rect.width
  audioEl.value.currentTime = percent * duration.value
}

const formatTime = (s) => {
  if (!s || isNaN(s)) return '0:00'
  const m = Math.floor(s / 60)
  const sec = Math.floor(s % 60)
  return `${m}:${sec.toString().padStart(2, '0')}`
}
</script>

<style scoped>
.audio-player {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  padding: 0.6rem 1rem;
  border-radius: 24px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  min-width: 200px;
}
.audio-player.user {
  background: #667eea;
  color: white;
}
.play-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: #667eea;
  color: white;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.user .play-btn {
  background: white;
  color: #667eea;
}
.progress-bar {
  flex: 1;
  height: 4px;
  background: #e0e0e0;
  border-radius: 2px;
  cursor: pointer;
}
.user .progress-bar {
  background: rgba(255,255,255,0.5);
}
.progress {
  height: 100%;
  background: #667eea;
  border-radius: 2px;
}
.user .progress {
  background: white;
}
.time {
  font-size: 0.75rem;
  color: #888;
  min-width: 35px;
}
.user .time {
  color: rgba(255,255,255,0.8);
}
</style>
