import { defineStore } from 'pinia'

export const useToastStore = defineStore('toast', {
  state: () => ({
    messages: []
  }),
  actions: {
    show(text, type = 'error', duration = 3000) {
      const id = Date.now() + Math.random()
      this.messages.push({ id, text, type })
      setTimeout(() => {
        this.messages = this.messages.filter(m => m.id !== id)
      }, duration)
    },
    error(text) { this.show(text, 'error') },
    success(text) { this.show(text, 'success', 2000) },
    info(text) { this.show(text, 'info', 2500) }
  }
})
