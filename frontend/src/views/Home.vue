<template>
  <div class="home">
    <div class="container">
      <h1>法语学习助手</h1>
      <p class="subtitle">基于AI的个性化法语学习平台</p>
      <div class="buttons">
        <button @click="$router.push('/login')" class="btn-primary">登录</button>
        <button @click="$router.push('/register')" class="btn-secondary">注册</button>
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
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.container {
  text-align: center;
  color: white;
}
h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}
.subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 2rem;
}
.buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
}
.btn-primary, .btn-secondary {
  padding: 0.8rem 2rem;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}
.btn-primary {
  background: white;
  color: #667eea;
}
.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}
.btn-primary:hover, .btn-secondary:hover {
  transform: scale(1.05);
}
</style>
