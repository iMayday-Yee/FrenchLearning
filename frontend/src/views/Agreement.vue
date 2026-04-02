<template>
  <div class="agreement-page">
    <div class="container">
      <h2>用户协议与隐私说明</h2>
      <div class="content">
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
      <div class="checkbox">
        <input type="checkbox" v-model="agreed" id="agree">
        <label for="agree">我已阅读并同意上述协议</label>
      </div>
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
  if (agreed.value) {
    router.push('/register-done')
  }
}
</script>

<style scoped>
.agreement-page {
  min-height: 100vh;
  padding: 2rem;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}
.container {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
}
h2 { margin-bottom: 1rem; text-align: center; }
.content {
  background: #f9f9f9;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  max-height: 300px;
  overflow-y: auto;
  font-size: 0.9rem;
  line-height: 1.6;
}
.content p { margin-bottom: 0.5rem; }
.content ul { margin-left: 1.5rem; }
.content li { margin-bottom: 0.3rem; }
.checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 1rem 0;
}
.checkbox input { width: 18px; height: 18px; }
.btn-submit {
  width: 100%;
  padding: 0.8rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
}
.btn-submit:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
