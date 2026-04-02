import { defineStore } from 'pinia'
import { api } from '@/api'

export const useStudyStore = defineStore('study', {
  state: () => ({
    studyDay: 0,
    phase: 'not_started',
    materialSentToday: false,
    remainingRounds: 20,
    chatMessages: [],
    needAssessment: false,
  }),
  actions: {
    async fetchStatus() {
      try {
        const res = await api.get('/study/status')
        this.studyDay = res.study_day
        this.phase = res.phase
        this.materialSentToday = res.material_sent_today
        this.remainingRounds = res.remaining_rounds
        this.needAssessment = res.need_assessment
      } catch (e) {
        console.error('Failed to fetch status', e)
      }
    },
    async loadHistory(day) {
      try {
        const res = await api.get(`/chat/history${day ? '?day=' + day : ''}`)
        this.chatMessages = res.messages || []
      } catch (e) {
        console.error('Failed to load history', e)
      }
    },
    appendMessage(msg) {
      this.chatMessages.push(msg)
    }
  }
})
