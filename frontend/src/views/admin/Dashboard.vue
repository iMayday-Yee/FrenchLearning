<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>管理后台</h1>
      <button @click="logout">退出</button>
    </header>

    <div class="stats">
      <div class="stat-card">
        <div class="value">{{ stats.total_users }}</div>
        <div class="label">总用户数</div>
      </div>
      <div class="stat-card">
        <div class="value">{{ stats.completed_assessments }}</div>
        <div class="label">完成测评</div>
      </div>
    </div>

    <div class="section">
      <h2>分组统计</h2>
      <table class="data-table">
        <thead>
          <tr>
            <th>组别</th>
            <th>头像</th>
            <th>当前/最大</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="slot in stats.slots" :key="`${slot.group_type}-${slot.avatar_type}`">
            <td>{{ slot.group_type }}</td>
            <td>{{ slot.avatar_type }}</td>
            <td>{{ slot.current }} / {{ slot.max }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="section">
      <h2>系统设置</h2>
      <div class="setting-row">
        <label>学习开始日期</label>
        <input type="date" v-model="startDate" />
        <button class="btn-save" @click="saveStartDate">保存</button>
        <span v-if="startDateMsg" class="save-msg">{{ startDateMsg }}</span>
      </div>
    </div>

    <div class="section">
      <h2>学习资源管理</h2>
      <div class="day-tabs">
        <button
          v-for="d in 10" :key="d"
          :class="['tab', { active: selectedDay === d }]"
          @click="selectDay(d)"
        >Day {{ d }}</button>
      </div>

      <div v-if="editingWords" class="words-editor">
        <div v-for="(word, idx) in editingWords" :key="idx" class="word-row">
          <div class="word-fields">
            <label>单词 {{ idx + 1 }}</label>
            <input v-model="word.french" placeholder="法语" />
            <input v-model="word.chinese" placeholder="中文" />
          </div>
          <div class="word-audio">
            <span class="audio-path">{{ word.audio || '未设置' }}</span>
            <button v-if="word.audio" class="preview-btn" @click="previewAudio(word.audio)">试听</button>
            <label class="upload-btn">
              上传音频
              <input type="file" accept="audio/*" hidden @change="e => uploadAudio(idx, e)" />
            </label>
          </div>
        </div>
        <div class="editor-actions">
          <button class="btn-save" @click="saveWords">保存</button>
          <span v-if="saveMsg" class="save-msg">{{ saveMsg }}</span>
        </div>
      </div>
    </div>

    <div class="section">
      <h2>数据导出</h2>
      <div class="export-buttons">
        <button @click="exportData('chat')">聊天记录</button>
        <button @click="exportData('daily')">每日数据</button>
        <button @click="exportData('assessment')">测评成绩</button>
      </div>
    </div>

    <div class="section">
      <h2>用户列表</h2>
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>邮箱</th>
            <th>昵称</th>
            <th>组别</th>
            <th>头像</th>
            <th>微信</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.nickname }}</td>
            <td>{{ user.group_type }}</td>
            <td>{{ user.avatar_type }}</td>
            <td>{{ user.wechat_bound ? '✓' : '✗' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const toast = useToastStore()
const stats = ref({ slots: [], group_stats: [], total_users: 0, completed_assessments: 0 })
const users = ref([])
const adminHeaders = () => ({ headers: { 'Admin-Token': localStorage.getItem('admin_token') } })

const startDate = ref('')
const startDateMsg = ref('')

const allWords = ref([])
const selectedDay = ref(1)
const editingWords = ref(null)
const saveMsg = ref('')

const loadDashboard = async () => {
  try {
    const res = await api.get('/admin/dashboard', adminHeaders())
    stats.value = res
    const usersRes = await api.get('/admin/users', adminHeaders())
    users.value = usersRes.users
  } catch (e) {
    toast.error('仪表盘数据加载失败')
  }
}

const loadConfig = async () => {
  try {
    const res = await api.get('/admin/config', adminHeaders())
    startDate.value = res.study_start_date || ''
  } catch (e) {
    toast.error('配置加载失败')
  }
}

const saveStartDate = async () => {
  if (!startDate.value) return
  try {
    await api.post('/admin/config', { key: 'study_start_date', value: startDate.value }, adminHeaders())
    startDateMsg.value = '保存成功'
    setTimeout(() => { startDateMsg.value = '' }, 2000)
  } catch (e) {
    startDateMsg.value = '保存失败'
  }
}

const loadWords = async () => {
  try {
    const res = await api.get('/admin/words', adminHeaders())
    allWords.value = res.words
    selectDay(selectedDay.value)
  } catch (e) {
    toast.error('单词数据加载失败')
  }
}

const selectDay = (day) => {
  selectedDay.value = day
  saveMsg.value = ''
  const dayData = allWords.value.find(d => d.day === day)
  if (dayData) {
    editingWords.value = dayData.words.map(w => ({ ...w }))
  } else {
    editingWords.value = [
      { index: 1, french: '', chinese: '', audio: `day${day}/${day}-1.mp3` },
      { index: 2, french: '', chinese: '', audio: `day${day}/${day}-2.mp3` },
      { index: 3, french: '', chinese: '', audio: `day${day}/${day}-3.mp3` }
    ]
  }
}

const saveWords = async () => {
  try {
    await api.put(`/admin/words/${selectedDay.value}`, { words: editingWords.value }, adminHeaders())
    saveMsg.value = '保存成功'
    await loadWords()
    setTimeout(() => { saveMsg.value = '' }, 2000)
  } catch (e) {
    saveMsg.value = '保存失败'
  }
}

const uploadAudio = async (idx, event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('audio', file)
  formData.append('word_index', idx + 1)

  try {
    const res = await fetch(`/api/admin/words/${selectedDay.value}/audio`, {
      method: 'POST',
      headers: { 'Admin-Token': localStorage.getItem('admin_token') },
      body: formData
    })
    const data = await res.json()
    if (data.code === 200) {
      editingWords.value[idx].audio = data.audio_path
      saveMsg.value = '音频上传成功'
      setTimeout(() => { saveMsg.value = '' }, 2000)
    }
  } catch (e) {
    saveMsg.value = '音频上传失败'
  }
  event.target.value = ''
}

const previewAudio = (audioPath) => {
  const url = audioPath.startsWith('http') ? audioPath : `/static/audio/${audioPath}`
  const audio = new Audio(url)
  audio.play()
}

const exportData = async (type) => {
  try {
    const response = await fetch(`/api/admin/export/${type}`, {
      headers: { 'Admin-Token': localStorage.getItem('admin_token') }
    })
    if (!response.ok) throw new Error('Export failed')
    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${type}_export.csv`
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    toast.error('导出失败，请重试')
  }
}

const logout = () => {
  localStorage.removeItem('admin_token')
  router.push('/admin')
}

onMounted(() => {
  loadDashboard()
  loadConfig()
  loadWords()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: var(--bg);
  padding: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.dashboard-header h1 {
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--ink);
}
.dashboard-header button {
  padding: 0.45rem 1rem;
  background: transparent;
  color: var(--rose);
  border: 1px solid var(--rose);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s;
}
.dashboard-header button:hover { background: var(--rose-subtle); }
.stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.stat-card {
  background: var(--surface);
  padding: 1.5rem;
  border-radius: var(--radius);
  text-align: center;
  border: 1px solid var(--border-light);
}
.stat-card .value {
  font-family: var(--font-display);
  font-size: 2.2rem;
  font-weight: 700;
  color: var(--accent);
}
.stat-card .label { color: var(--ink-muted); margin-top: 0.2rem; font-size: 0.85rem; }
.section {
  background: var(--surface);
  padding: 1.2rem;
  border-radius: var(--radius);
  margin-bottom: 1rem;
  border: 1px solid var(--border-light);
}
.section h2 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 1rem;
}
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td {
  padding: 0.5rem 0.6rem;
  text-align: left;
  border-bottom: 1px solid var(--border-light);
  font-size: 0.85rem;
}
.data-table th { font-weight: 500; color: var(--ink-muted); text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.05em; }
.export-buttons, .setting-row { display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap; }
.setting-row label { font-weight: 500; white-space: nowrap; font-size: 0.85rem; color: var(--ink-secondary); }
.setting-row input[type="date"] {
  padding: 0.45rem 0.7rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  color: var(--ink);
  background: var(--bg);
  outline: none;
}
.setting-row input[type="date"]:focus { border-color: var(--accent); }
.day-tabs { display: flex; gap: 0.4rem; flex-wrap: wrap; }
.export-buttons button {
  padding: 0.45rem 1rem;
  background: var(--accent);
  color: var(--ink-on-dark);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.2s;
}
.export-buttons button:hover { background: var(--accent); }
.tab {
  padding: 0.35rem 0.7rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--surface);
  cursor: pointer;
  font-size: 0.8rem;
  color: var(--ink-secondary);
  transition: all 0.2s;
}
.tab.active {
  background: var(--accent);
  color: var(--ink-on-dark);
  border-color: var(--ink);
}
.words-editor { margin-top: 1rem; }
.word-row {
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  padding: 0.8rem;
  margin-bottom: 0.7rem;
  background: var(--bg);
}
.word-fields { display: flex; gap: 0.5rem; align-items: center; margin-bottom: 0.5rem; }
.word-fields label { font-weight: 600; font-size: 0.75rem; white-space: nowrap; color: var(--ink-muted); text-transform: uppercase; letter-spacing: 0.03em; }
.word-fields input {
  flex: 1;
  padding: 0.4rem 0.6rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  color: var(--ink);
  background: var(--surface);
  outline: none;
}
.word-fields input:focus { border-color: var(--accent); }
.word-audio { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; }
.audio-path { color: var(--ink-muted); flex: 1; font-size: 0.75rem; }
.preview-btn {
  padding: 0.25rem 0.5rem;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.75rem;
  white-space: nowrap;
  transition: background 0.2s;
}
.preview-btn:hover { background: var(--accent-hover); }
.upload-btn {
  padding: 0.25rem 0.5rem;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.75rem;
  white-space: nowrap;
  color: var(--ink-secondary);
  transition: all 0.2s;
}
.upload-btn:hover { border-color: var(--ink-muted); }
.editor-actions { display: flex; align-items: center; gap: 0.8rem; margin-top: 0.5rem; }
.btn-save {
  padding: 0.45rem 1.2rem;
  background: var(--sage);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.85rem;
  transition: all 0.2s;
}
.btn-save:hover { opacity: 0.9; }
.save-msg { color: var(--sage); font-size: 0.8rem; }
</style>
