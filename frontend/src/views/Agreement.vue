<template>
  <div class="agreement-page">
    <div class="card fade-up">
      <span class="tag">Accord</span>
      <h2>用户协议</h2>
      <div class="content-scroll">
        <p class="intro">欢迎您使用"AI小五智能助手"（以下简称"APP"），本协议是您与APP运营方（以下简称"我们"）之间就APP使用所达成的法律协议。请您在使用APP前仔细阅读并充分理解本协议所有条款，您点击"同意"或使用APP服务，即视为您已接受本协议全部内容，自愿受本协议约束。若您不同意本协议，请勿使用本APP。</p>

        <p class="section-title">一、用户账号与信息</p>
        <ol>
          <li>您可通过邮箱、手机号注册登录APP，注册时需提供真实、准确、完整的信息，若信息虚假或失效，我们有权暂停或终止您的账号使用，由此产生的损失由您自行承担。</li>
          <li>您应妥善保管账号及密码，对账号下的所有操作行为负责。若发现账号被盗用、泄露，应及时通知我们，我们将协助您采取安全措施，因您保管不当导致的损失，我们不承担责任。</li>
          <li>我们将严格按照《个人信息保护法》等相关法律法规，保护您的个人信息安全，不会擅自泄露、出售您的个人信息，具体详见APP内《隐私政策》。</li>
        </ol>

        <p class="section-title">二、用户权利与义务</p>
        <ol>
          <li>您有权在遵守本协议的前提下，使用APP提供的法语学习相关服务（如课程学习、单词背诵、听力练习等），并可对APP功能提出建议。</li>
          <li>您不得利用APP从事违法违规活动，包括但不限于传播违法信息、恶意攻击APP系统、盗用他人账号、上传侵权内容等，不得利用APP损害我们或第三方的合法权益。</li>
          <li>您在APP内上传、发布的学习内容（如笔记、发音、练习成果等），所有权归您所有，您同意授予我们一项非独占、免费的使用权，用于APP的运营、优化及相关学习服务的展示（您可随时通过设置关闭该授权）。</li>
        </ol>

        <p class="section-title">三、APP运营方权利与义务</p>
        <ol>
          <li>我们有权根据技术升级、运营需求，对APP功能、服务内容进行更新、调整，并通过APP弹窗、公告等方式通知您，若您不同意调整，可选择停止使用APP。</li>
          <li>我们将尽力保障APP正常运行，提供稳定的学习服务，但不保证服务无中断、无错误，因不可抗力、系统故障、网络问题等导致的服务中断，我们不承担赔偿责任。</li>
          <li>我们有权对违反本协议的用户，采取警告、限制功能、暂停账号、封禁账号等措施，必要时将追究其法律责任。</li>
        </ol>

        <p class="section-title">四、知识产权</p>
        <ol>
          <li>APP内所有法语课程、单词库、听力素材、图文内容、软件程序等知识产权，均归我们或相关授权方所有，未经授权，您不得复制、传播、修改、转载或用于商业用途。</li>
          <li>您不得上传、发布侵犯他人知识产权的内容（如盗版课程、侵权音频等），若因此引发纠纷，由您自行承担全部责任，给我们造成损失的，您需予以赔偿。</li>
        </ol>

        <p class="section-title">五、免责条款</p>
        <ol>
          <li>因您自身操作不当、设备故障、网络问题等导致的使用异常或损失，我们不承担责任。</li>
          <li>因第三方侵权、违法操作等导致您遭受损失的，我们不承担直接责任，但会尽力协助您维权。</li>
          <li>您因使用APP学习产生的任何学习效果，均由您自身努力决定，我们不承诺具体的学习成果。</li>
        </ol>

        <p class="section-title">六、协议变更与终止</p>
        <ol>
          <li>我们可根据法律法规变化、运营需求，修改本协议条款，修改后将在APP内公告，公告后即生效，若您继续使用APP，视为接受修改后的协议。</li>
          <li>您可随时注销账号，账号注销后，您的个人信息将按照《隐私政策》进行处理，相关学习数据将无法恢复。</li>
          <li>若您严重违反本协议，或出现法律法规规定的其他情形，我们有权单方终止本协议，停止为您提供服务。</li>
        </ol>

        <p class="section-title">七、其他</p>
        <ol>
          <li>本协议的争议解决，优先通过友好协商解决，协商不成的，提交APP运营方所在地有管辖权的人民法院诉讼解决。</li>
          <li>本协议自您同意之日起生效，未尽事宜，按照相关法律法规执行。</li>
          <li>若您有任何疑问，可与我们沟通。</li>
        </ol>
        <p class="footer-org">华中科技大学管理学院</p>
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
  padding: 1.5rem 1rem;
  background: var(--bg);
  display: flex;
  align-items: flex-start;
  justify-content: center;
  overflow-y: auto;
}
.card {
  background: var(--surface);
  padding: 2rem 1.5rem;
  border-radius: var(--radius-lg);
  max-width: 520px;
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
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--ink);
  margin: 0.3rem 0 1rem;
}
.content-scroll {
  background: var(--bg);
  padding: 1rem 1.2rem;
  border-radius: var(--radius);
  margin-bottom: 1.2rem;
  max-height: 420px;
  overflow-y: auto;
  font-size: 0.78rem;
  line-height: 1.8;
  color: var(--ink-secondary);
  border: 1px solid var(--border-light);
}
.content-scroll p { margin-bottom: 0.5rem; }
.content-scroll p.intro { margin-bottom: 1rem; color: var(--ink); font-weight: 500; }
.content-scroll .section-title {
  font-weight: 600;
  color: var(--ink);
  margin-top: 1rem;
  margin-bottom: 0.4rem;
}
.content-scroll ol {
  margin: 0 0 0 1.1rem;
  padding: 0;
}
.content-scroll ol li { margin-bottom: 0.4rem; }
.content-scroll .footer-org {
  text-align: right;
  font-size: 0.72rem;
  color: var(--ink-muted);
  margin-top: 1.2rem;
}
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
.footer-org {
  text-align: right;
  font-size: 0.72rem;
  color: var(--ink-muted);
  margin: 0.8rem 0 0;
}
</style>
