<template>
  <div :class="['audio-player', { user: isUser }]">
    <button class="play-btn" @click="togglePlay">
      <svg v-if="!isPlaying" width="12" height="14" viewBox="0 0 12 14" fill="currentColor"><path d="M0 0L12 7L0 14z"/></svg>
      <svg v-else width="10" height="12" viewBox="0 0 10 12" fill="currentColor"><rect width="3" height="12"/><rect x="7" width="3" height="12"/></svg>
    </button>
    <div class="progress-bar" @click="seek">
      <div class="progress-track">
        <div class="progress-fill" :style="{ width: progress + '%' }"></div>
      </div>
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
  if (isPlaying.value) audioEl.value.pause()
  else audioEl.value.play()
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
  return `${Math.floor(s / 60)}:${Math.floor(s % 60).toString().padStart(2, '0')}`
}
</script>

<style scoped>
.audio-player {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(6px);
  padding: 0.55rem 0.9rem;
  border-radius: var(--radius-xl);
  box-shadow: 0 1px 4px rgba(0,0,0,0.04), 0 0 0 1px rgba(228,231,238,0.4);
  min-width: 180px;
}
.audio-player.user {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%);
  backdrop-filter: none;
  box-shadow: 0 2px 10px rgba(123,155,244,0.2);
}
.play-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.25s var(--ease);
  box-shadow: 0 2px 6px rgba(123,155,244,0.2);
}
.play-btn:hover { transform: scale(1.1); }
.user .play-btn {
  background: rgba(255,255,255,0.25);
  box-shadow: none;
}
.progress-bar {
  flex: 1;
  padding: 4px 0;
  cursor: pointer;
}
.progress-track {
  height: 3px;
  background: var(--border);
  border-radius: 2px;
  overflow: hidden;
}
.user .progress-track { background: rgba(255,255,255,0.25); }
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent-light));
  border-radius: 2px;
  transition: width 0.1s linear;
}
.user .progress-fill { background: rgba(255,255,255,0.8); }
.time {
  font-size: 0.7rem;
  color: var(--ink-muted);
  min-width: 30px;
  text-align: right;
  font-variant-numeric: tabular-nums;
}
.user .time { color: rgba(255,255,255,0.6); }
</style>
