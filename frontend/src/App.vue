<template>
  <Toast />
  <router-view />
</template>

<script setup>
import Toast from '@/components/Toast.vue'
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

:root {
  /* Palette — Macaron */
  --bg: #FAFBFE;
  --bg-warm: #F2F4FA;
  --bg-tint: linear-gradient(135deg, #F0F4FF 0%, #FFF0F3 50%, #EDFAF5 100%);
  --surface: #FFFFFF;
  --surface-hover: #F7F8FC;

  --ink: #3D4254;
  --ink-secondary: #5E6478;
  --ink-muted: #9096A6;
  --ink-faint: #BFC4D0;
  --ink-on-dark: #FFFFFF;

  --accent: #7B9BF4;
  --accent-light: #98B2F7;
  --accent-subtle: rgba(123, 155, 244, 0.1);
  --accent-hover: #6485E0;

  --rose: #F0A0B0;
  --rose-subtle: rgba(240, 160, 176, 0.12);
  --sage: #7BCDA8;
  --sage-subtle: rgba(123, 205, 168, 0.1);
  --warm: #F4C78E;

  --border: #E4E7EE;
  --border-light: #EFF1F6;

  --radius-sm: 6px;
  --radius: 12px;
  --radius-lg: 20px;
  --radius-xl: 28px;

  --shadow-sm: 0 1px 3px rgba(16, 43, 46, 0.04);
  --shadow: 0 4px 16px rgba(16, 43, 46, 0.06);
  --shadow-lg: 0 8px 32px rgba(16, 43, 46, 0.07);
  --shadow-xl: 0 16px 48px rgba(16, 43, 46, 0.10);

  --font-display: 'Cormorant Garamond', 'Noto Serif SC', Georgia, serif;
  --font-body: 'Plus Jakarta Sans', -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;

  --ease: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: var(--font-body);
  background-color: var(--bg);
  color: var(--ink);
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.6;
  letter-spacing: -0.01em;
}

#app {
  min-height: 100vh;
}

::selection {
  background: var(--accent-subtle);
  color: var(--ink);
}

input, button, select, textarea {
  font-family: inherit;
}

/* Fade-in animation utility */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.fade-up {
  animation: fadeUp 0.5s var(--ease) both;
}
</style>
