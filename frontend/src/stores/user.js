import { defineStore } from 'pinia'
import { api } from '@/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userId: null,
    nickname: '',
    avatarType: '',
  }),
  actions: {
    async setLogin(data) {
      this.token = data.token
      this.userId = data.user_id
      localStorage.setItem('token', data.token)
    },
    async fetchProfile() {
      try {
        const res = await api.get('/user/profile')
        this.userId = res.user_id
        this.nickname = res.nickname
        this.avatarType = res.avatar_type
      } catch (e) {
        this.logout()
      }
    },
    logout() {
      this.token = ''
      this.userId = null
      this.nickname = ''
      this.avatarType = ''
      localStorage.removeItem('token')
    }
  }
})
