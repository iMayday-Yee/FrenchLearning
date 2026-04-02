import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 65000,
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response.data,
  error => {
    const url = error.config?.url || ''
    if (error.response?.status === 401 && !url.includes('/admin') && !url.includes('/login') && !url.includes('/register')) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export { api }
