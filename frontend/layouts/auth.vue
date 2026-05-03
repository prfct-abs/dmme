<template>
  <div class="auth-shell">
    <div class="auth-card">
      <div class="auth-brand">
        <Icon name="lucide:zap" size="28" class="brand-icon" />
        <span class="brand-name">AutoDM</span>
      </div>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.auth-shell {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background:
    radial-gradient(ellipse 60% 50% at 50% -10%, rgba(108,99,255,0.18) 0%, transparent 70%),
    var(--color-bg);
  padding: 1rem;
}
.auth-card {
  width: 100%;
  max-width: 420px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 2.5rem;
  box-shadow: 0 32px 64px rgba(0,0,0,0.4);
}
.auth-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
}
.brand-icon { color: var(--color-brand); }
.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text);
  letter-spacing: -0.02em;
}
</style>
