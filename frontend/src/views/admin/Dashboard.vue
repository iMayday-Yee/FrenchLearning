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
            <th>昵称</th>
            <th>组别</th>
            <th>头像</th>
            <th>微信</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
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

const router = useRouter()
const stats = ref({ slots: [], group_stats: [], total_users: 0, completed_assessments: 0 })
const users = ref([])

const loadDashboard = async () => {
  try {
    const res = await api.get('/admin/dashboard', { headers: { 'Admin-Token': localStorage.getItem('admin_token') } })
    stats.value = res
    const usersRes = await api.get('/admin/users', { headers: { 'Admin-Token': localStorage.getItem('admin_token') } })
    users.value = usersRes.users
  } catch (e) {
    console.error('Failed to load dashboard', e)
  }
}

const exportData = async (type) => {
  window.open(`/api/admin/export/${type}`, '_blank')
}

const logout = () => {
  localStorage.removeItem('admin_token')
  router.push('/admin')
}

onMounted(loadDashboard)
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f5f5f5;
  padding: 1rem;
}
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.dashboard-header h1 { font-size: 1.5rem; }
.dashboard-header button {
  padding: 0.5rem 1rem;
  background: #f5222d;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
}
.stat-card .value { font-size: 2rem; font-weight: bold; color: #667eea; }
.stat-card .label { color: #888; margin-top: 0.3rem; }
.section {
  background: white;
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
}
.section h2 { font-size: 1.1rem; margin-bottom: 1rem; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table th, .data-table td {
  padding: 0.5rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}
.data-table th { font-weight: 500; color: #888; }
.export-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.export-buttons button {
  padding: 0.5rem 1rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
