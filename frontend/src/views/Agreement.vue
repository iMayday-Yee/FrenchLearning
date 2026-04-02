<template>
  <div class="agreement-page">
    <div class="card fade-up">
      <span class="tag">Accord</span>
      <h2>用户协议与隐私说明</h2>
      <div class="content-scroll">
        <p>本研究将收集以下数据用于学术研究：</p>
        <ul>
          <li>您主动发送消息的次数</li>
          <li>您回复同意/拒绝接收学习材料的次数</li>
          <li>您上传语音跟读的次数</li>
          <li>您通过麦克风录音互动的次数</li>
          <li>各组发音准确度评分的平均分差异（如有此功能）</li>
          <li>所有聊天内容的完整记录</li>
          <li>您的注册信息（年龄、性别、教育背景等）</li>
        </ul>
        <p>所有数据仅用于学术研究，匿名处理后分析，不会泄露您的个人身份信息。</p>
      </div>
      <label class="checkbox-row">
        <input type="checkbox" v-model="agreed">
        <span class="checkmark"></span>
        <span>我已阅读并同意上述协议</span>
      </label>
      <button class="btn-submit" :disabled="!agreed" @click="handleAgree">
        同意并继续
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const agreed = ref(false)

const handleAgree = () => {
  if (agreed.value) router.push('/register-done')
}
</script>

<style scoped>
.agreement-page {
  min-height: 100vh;
  padding: 2rem 1rem;
  background: var(--bg);
  display: flex;
  align-items: center;
  justify-content: center;
}
.card {
  background: var(--surface);
  padding: 2.5rem 2rem;
  border-radius: var(--radius-lg);
  max-width: 480px;
  width: 100%;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-light);
}
.tag {
  font-family: var(--font-display);
  font-size: 0.85rem;
  font-style: italic;
  color: var(--accent);
  letter-spacing: 0.1em;
}
h2 {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 600;
  color: var(--ink);
  margin: 0.3rem 0 1.2rem;
}
.content-scroll {
  background: var(--bg);
  padding: 1.2rem;
  border-radius: var(--radius);
  margin-bottom: 1.2rem;
  max-height: 280px;
  overflow-y: auto;
  font-size: 0.85rem;
  line-height: 1.7;
  color: var(--ink-secondary);
  border: 1px solid var(--border-light);
}
.content-scroll p { margin-bottom: 0.6rem; }
.content-scroll ul { margin-left: 1.2rem; }
.content-scroll li { margin-bottom: 0.3rem; }
.checkbox-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin: 1.2rem 0;
  cursor: pointer;
  font-size: 0.9rem;
  color: var(--ink-secondary);
}
.checkbox-row input {
  width: 18px;
  height: 18px;
  accent-color: var(--accent);
}
.btn-submit {
  width: 100%;
  padding: 0.85rem;
  background: var(--accent);
  color: var(--ink-on-dark);
  border: none;
  border-radius: var(--radius);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s var(--ease);
}
.btn-submit:hover:not(:disabled) {
  background: var(--accent);
}
.btn-submit:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}
</style>
