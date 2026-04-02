<template>
  <div class="home">
    <div class="container">
      <div class="pill fade-up" style="animation-delay:0.1s">Bonjour !</div>
      <h1 class="title fade-up" style="animation-delay:0.2s">法语学习助手</h1>
      <p class="subtitle fade-up" style="animation-delay:0.3s">每天三个词，轻松开启你的法语之旅</p>
      <div class="actions fade-up" style="animation-delay:0.4s">
        <router-link to="/login" class="btn btn-primary">登录</router-link>
        <router-link to="/register" class="btn btn-soft">注册账号</router-link>
      </div>
      <div class="footer-words fade-up" style="animation-delay:0.6s">
        <span>Merci</span><span class="dot"></span>
        <span>Enchanté</span><span class="dot"></span>
        <span>Au revoir</span>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-tint);
  position: relative;
}
.container {
  text-align: center;
  padding: 3rem 2rem;
  max-width: 420px;
}
.pill {
  display: inline-block;
  padding: 0.3rem 1rem;
  border-radius: var(--radius-xl);
  background: var(--accent-subtle);
  color: var(--accent);
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}
.title {
  font-family: var(--font-display);
  font-size: 2.8rem;
  font-weight: 700;
  color: var(--ink);
  line-height: 1.2;
  margin-bottom: 0.8rem;
}
.subtitle {
  font-size: 1rem;
  color: var(--ink-muted);
  margin-bottom: 2.5rem;
  font-weight: 400;
}
.actions {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  max-width: 260px;
  margin: 0 auto 3.5rem;
}
.btn {
  display: block;
  padding: 0.85rem 2rem;
  border-radius: var(--radius);
  font-size: 0.95rem;
  font-weight: 600;
  text-decoration: none;
  text-align: center;
  transition: all 0.25s var(--ease);
}
.btn-primary {
  background: var(--accent);
  color: white;
}
.btn-primary:hover {
  background: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(123,155,244,0.2);
}
.btn-soft {
  background: var(--surface);
  color: var(--ink);
  border: 1px solid var(--border);
}
.btn-soft:hover {
  border-color: var(--accent-light);
  color: var(--accent);
}
.footer-words {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  font-family: var(--font-display);
  font-size: 0.9rem;
  font-style: italic;
  color: var(--ink-faint);
}
.dot {
  width: 3px;
  height: 3px;
  background: var(--border);
  border-radius: 50%;
}
</style>
