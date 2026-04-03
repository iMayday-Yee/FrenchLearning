<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>管理后台</h1>
      <button @click="logout">退出</button>
    </header>

    <div class="stats">
      <div class="stat-card">
        <div class="value">{{ stats.total_users || 0 }}</div>
        <div class="label">总用户数</div>
      </div>
      <div class="stat-card">
        <div class="value">{{ stats.completed_assessments || 0 }}</div>
        <div class="label">完成测评</div>
      </div>
      <div class="stat-card">
        <div class="value">{{ userStats.total_practice || 0 }}</div>
        <div class="label">总跟读次数</div>
      </div>
      <div class="stat-card">
        <div class="value">{{ userStats.total_conversation_rounds || 0 }}</div>
        <div class="label">总对话轮次</div>
      </div>
      <div class="stat-card">
        <div class="value">{{ userStats.users_with_material_sent || 0 }}</div>
        <div class="label">已发材料人数</div>
      </div>
      <div class="stat-card">
        <div class="value">{{ userStats.total_invalid_audio || 0 }}</div>
        <div class="label">无效音频次数</div>
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
      <h2>用户学习详情</h2>
      <div class="user-stats-filter">
        <select v-model="filterGroup">
          <option value="">全部组别</option>
          <option value="low">低自主性组</option>
          <option value="adjustable">可调自主性组</option>
          <option value="high">高自主性组</option>
        </select>
        <select v-model="filterAvatar">
          <option value="">全部头像</option>
          <option value="human">Human</option>
          <option value="robot">Robot</option>
        </select>
        <select v-model="filterDay">
          <option value="">全部天数</option>
          <option v-for="d in 10" :key="d" :value="d">Day {{ d }}</option>
        </select>
      </div>
      <div class="user-stats-table-wrapper">
        <table class="data-table user-stats-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>昵称</th>
              <th>组别</th>
              <th>头像</th>
              <th v-if="filterDay">Day {{ filterDay }} 跟读</th>
              <th v-if="filterDay">Day {{ filterDay }} 轮次</th>
              <th v-if="filterDay">Day {{ filterDay }} 材料</th>
              <th v-if="filterDay">Day {{ filterDay }} 拒绝</th>
              <th v-if="!filterDay">活跃天数</th>
              <th v-if="!filterDay">总跟读</th>
              <th v-if="!filterDay">总轮次</th>
              <th>测评</th>
              <th v-if="!filterDay">每日详情</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in filteredUserList" :key="u.user_id">
              <td>{{ u.user_id }}</td>
              <td>{{ u.nickname }}</td>
              <td>{{ u.group_type }}</td>
              <td>{{ u.avatar_type }}</td>
              <td v-if="filterDay">{{ getUserDayStatus(u.user_id, filterDay)?.practice_count || 0 }}</td>
              <td v-if="filterDay">{{ getUserDayStatus(u.user_id, filterDay)?.conversation_rounds || 0 }}</td>
              <td v-if="filterDay">
                <span class="badge" :class="getUserDayStatus(u.user_id, filterDay)?.material_sent ? 'success' : 'muted'">
                  {{ getUserDayStatus(u.user_id, filterDay)?.material_sent ? '已发' : '未发' }}
                </span>
              </td>
              <td v-if="filterDay">
                <span class="badge" :class="getUserDayStatus(u.user_id, filterDay)?.rejected ? 'warning' : 'muted'">
                  {{ getUserDayStatus(u.user_id, filterDay)?.rejected ? '已拒' : '否' }}
                </span>
              </td>
              <td v-if="!filterDay">{{ u.active_days }}</td>
              <td v-if="!filterDay">{{ u.total_practice }}</td>
              <td v-if="!filterDay">{{ u.total_rounds }}</td>
              <td>{{ u.assessment_completed ? `${u.assessment_correct}/${u.assessment_total}` : '未完成' }}</td>
              <td v-if="!filterDay">
                <button class="detail-btn" @click="toggleUserDetail(u.user_id)">
                  {{ expandedUsers.includes(u.user_id) ? '收起' : '查看' }}
                </button>
              </td>
            </tr>
            <tr v-if="expandedUsers.length > 0" v-for="uid in expandedUsers" :key="`detail-${uid}`" class="detail-row">
              <td :colspan="filterDay ? 8 : 9">
                <div class="day-grid">
                  <div v-for="d in 10" :key="d" class="day-card" :class="{ 'has-material': getUserDayStatus(uid, d)?.material_sent }">
                    <div class="day-title">Day {{ d }}</div>
                    <div class="day-info">
                      <span v-if="getUserDayStatus(uid, d)">
                        <span class="badge" :class="getUserDayStatus(uid, d).material_sent ? 'success' : 'muted'">
                          {{ getUserDayStatus(uid, d).material_sent ? '已发材料' : '未发' }}
                        </span>
                        <span class="badge" :class="getUserDayStatus(uid, d).rejected ? 'warning' : 'muted'">
                          {{ getUserDayStatus(uid, d).rejected ? '已拒绝' : '' }}
                        </span>
                        <br/>
                        跟读: {{ getUserDayStatus(uid, d).practice_count }}<br/>
                        轮次: {{ getUserDayStatus(uid, d).conversation_rounds }}
                      </span>
                      <span v-else class="no-data">无记录</span>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="section">
      <h2>微信公众号管理</h2>
      <div class="wechat-actions">
        <button class="btn-save" @click="showAddAccount = true">添加公众号</button>
      </div>

      <div v-if="showAddAccount || editingAccount" class="wechat-form">
        <h3>{{ editingAccount ? '编辑公众号' : '添加公众号' }}</h3>
        <div class="form-grid">
          <div class="field"><label>AppID *</label><input v-model="accountForm.app_id" placeholder="wx..."></div>
          <div class="field"><label>AppSecret *</label><input v-model="accountForm.app_secret" placeholder=""></div>
          <div class="field"><label>Token</label><input v-model="accountForm.token" placeholder="回调验证token"></div>
          <div class="field"><label>TemplateID</label><input v-model="accountForm.template_id" placeholder="模板消息ID"></div>
          <div class="field"><label>最大绑定数</label><input v-model.number="accountForm.max_bindable" type="number"></div>
          <div class="field"><label>备注</label><input v-model="accountForm.remark" placeholder="如：张三的号"></div>
        </div>
        <div class="form-actions">
          <button class="btn-save" @click="saveAccount">保存</button>
          <button class="btn-skip" @click="cancelAccountEdit">取消</button>
        </div>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>AppID</th>
            <th>备注</th>
            <th>绑定数/上限</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="acc in wechatAccounts" :key="acc.id">
            <td>{{ acc.id }}</td>
            <td>{{ acc.app_id }}</td>
            <td>{{ acc.remark }}</td>
            <td>{{ acc.bound_count }} / {{ acc.max_bindable }}</td>
            <td>
              <span class="badge" :class="acc.enabled ? 'success' : 'muted'">{{ acc.enabled ? '启用' : '禁用' }}</span>
            </td>
            <td class="action-cell">
              <button class="detail-btn" @click="toggleAccountUsers(acc.id)">用户</button>
              <button class="detail-btn" @click="startEditAccount(acc)">编辑</button>
              <button class="detail-btn" @click="toggleAccountEnabled(acc)">{{ acc.enabled ? '禁用' : '启用' }}</button>
              <button class="detail-btn" @click="deleteAccount(acc)" v-if="acc.bound_count === 0">删除</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="expandedAccountId" class="account-users">
        <h3>公众号 #{{ expandedAccountId }} 绑定用户</h3>
        <table class="data-table" v-if="accountUsers.length > 0">
          <thead><tr><th>ID</th><th>昵称</th><th>邮箱</th></tr></thead>
          <tbody>
            <tr v-for="u in accountUsers" :key="u.id">
              <td>{{ u.id }}</td><td>{{ u.nickname }}</td><td>{{ u.email }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else class="no-data-text">暂无绑定用户</p>
      </div>
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
            <input v-model="word.french" placeholder="法语" class="equal-input" />
            <input v-model="word.phonetic" placeholder="音标" class="equal-input" />
            <input v-model="word.chinese" placeholder="中文" class="equal-input" />
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
import { ref, onMounted, computed } from 'vue'
import { api } from '@/api'
import { useRouter } from 'vue-router'
import { useToastStore } from '@/stores/toast'

const router = useRouter()
const toast = useToastStore()
const stats = ref({ slots: [], group_stats: [], total_users: 0, completed_assessments: 0 })
const userStats = ref({ total_practice: 0, total_conversation_rounds: 0, users_with_material_sent: 0, total_invalid_audio: 0, users_who_rejected: 0 })
const userDetailList = ref([])
const users = ref([])
const adminHeaders = () => ({ headers: { 'Admin-Token': localStorage.getItem('admin_token') } })

const filterGroup = ref('')
const filterAvatar = ref('')
const filterDay = ref('')
const expandedUsers = ref([])

// 微信公众号管理
const wechatAccounts = ref([])
const showAddAccount = ref(false)
const editingAccount = ref(null)
const accountForm = ref({ app_id: '', app_secret: '', token: '', template_id: '', max_bindable: 19, remark: '' })
const expandedAccountId = ref(null)
const accountUsers = ref([])

const loadWechatAccounts = async () => {
  try {
    const res = await api.get('/admin/wechat_accounts', adminHeaders())
    wechatAccounts.value = res.accounts || []
  } catch (e) { console.error('Failed to load wechat accounts', e) }
}

const saveAccount = async () => {
  try {
    if (editingAccount.value) {
      await api.put(`/admin/wechat_accounts/${editingAccount.value.id}`, accountForm.value, adminHeaders())
      toast.success('更新成功')
    } else {
      await api.post('/admin/wechat_accounts', accountForm.value, adminHeaders())
      toast.success('添加成功')
    }
    cancelAccountEdit()
    await loadWechatAccounts()
  } catch (e) { toast.error(e.response?.data?.message || '操作失败') }
}

const startEditAccount = (acc) => {
  editingAccount.value = acc
  showAddAccount.value = false
  accountForm.value = {
    app_id: acc.app_id_full || acc.app_id,
    app_secret: acc.app_secret,
    token: acc.token,
    template_id: acc.template_id,
    max_bindable: acc.max_bindable,
    remark: acc.remark
  }
}

const cancelAccountEdit = () => {
  editingAccount.value = null
  showAddAccount.value = false
  accountForm.value = { app_id: '', app_secret: '', token: '', template_id: '', max_bindable: 19, remark: '' }
}

const toggleAccountEnabled = async (acc) => {
  try {
    await api.put(`/admin/wechat_accounts/${acc.id}`, { enabled: !acc.enabled }, adminHeaders())
    await loadWechatAccounts()
  } catch (e) { toast.error('操作失败') }
}

const deleteAccount = async (acc) => {
  if (!confirm(`确定删除公众号 #${acc.id}？`)) return
  try {
    await api.delete(`/admin/wechat_accounts/${acc.id}`, adminHeaders())
    toast.success('删除成功')
    await loadWechatAccounts()
  } catch (e) { toast.error(e.response?.data?.message || '删除失败') }
}

const toggleAccountUsers = async (accountId) => {
  if (expandedAccountId.value === accountId) {
    expandedAccountId.value = null
    accountUsers.value = []
    return
  }
  try {
    const res = await api.get(`/admin/wechat_accounts/${accountId}/users`, adminHeaders())
    accountUsers.value = res.users || []
    expandedAccountId.value = accountId
  } catch (e) { toast.error('加载用户失败') }
}

const filteredUserList = computed(() => {
  return userDetailList.value.filter(u => {
    if (filterGroup.value && u.group_type !== filterGroup.value) return false
    if (filterAvatar.value && u.avatar_type !== filterAvatar.value) return false
    return true
  })
})

const getUserDayStatus = (userId, day) => {
  const user = userDetailList.value.find(u => u.user_id === userId)
  return user?.daily_status?.[Number(day)] || null
}

const toggleUserDetail = (userId) => {
  const idx = expandedUsers.value.indexOf(userId)
  if (idx >= 0) {
    expandedUsers.value.splice(idx, 1)
  } else {
    expandedUsers.value.push(userId)
  }
}

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

const loadUserStats = async () => {
  try {
    const res = await api.get('/admin/user_stats', adminHeaders())
    userStats.value = res.stats
    userDetailList.value = res.users
  } catch (e) {
    toast.error('用户学习统计数据加载失败')
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
  loadUserStats()
  loadConfig()
  loadWords()
  loadWechatAccounts()
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
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}
@media (max-width: 600px) {
  .stats { grid-template-columns: repeat(2, 1fr); }
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
.word-fields .equal-input { flex: 1; min-width: 0; }
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

/* 用户统计相关 */
.user-stats-filter { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
.user-stats-filter select {
  padding: 0.4rem 0.8rem;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  background: var(--bg);
  color: var(--ink);
  outline: none;
}
.user-stats-table-wrapper { overflow-x: auto; }
.user-stats-table th, .user-stats-table td { white-space: nowrap; }
.detail-btn {
  padding: 0.2rem 0.5rem;
  background: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.75rem;
}
.detail-row td { padding: 0.5rem !important; background: var(--bg); }
.day-grid { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.day-card {
  border: 1px solid var(--border-light);
  border-radius: var(--radius-sm);
  padding: 0.5rem;
  min-width: 80px;
  background: var(--surface);
}
.day-card.has-material { border-color: var(--sage); background: rgba(123, 205, 168, 0.05); }
.day-title { font-weight: 600; font-size: 0.75rem; margin-bottom: 0.3rem; color: var(--ink); }
.day-info { font-size: 0.7rem; color: var(--ink-muted); line-height: 1.4; }
.day-info .badge {
  display: inline-block;
  padding: 0.1rem 0.3rem;
  border-radius: 3px;
  font-size: 0.65rem;
  margin-right: 0.2rem;
}
.day-info .badge.success { background: var(--sage-subtle); color: var(--sage); }
.day-info .badge.warning { background: rgba(255, 200, 87, 0.2); color: #c8a000; }
.day-info .badge.muted { background: var(--bg); color: var(--ink-faint); }
.day-info .no-data { color: var(--ink-faint); font-style: italic; }
.wechat-actions { margin-bottom: 1rem; }
.wechat-form {
  background: #f8f9fc;
  padding: 1.2rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 1px solid #eef1f6;
}
.wechat-form h3 { font-size: 0.95rem; margin-bottom: 0.8rem; }
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.8rem;
}
.form-grid .field label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  color: #666;
  margin-bottom: 0.3rem;
}
.form-grid .field input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
}
.form-actions { margin-top: 0.8rem; display: flex; gap: 0.5rem; }
.action-cell { white-space: nowrap; }
.action-cell .detail-btn { margin-right: 0.3rem; }
.account-users {
  background: #f8f9fc;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 0.8rem;
}
.account-users h3 { font-size: 0.9rem; margin-bottom: 0.5rem; }
.no-data-text { color: #999; font-size: 0.85rem; }
</style>
