<template>
  <Teleport to="body">
    <div class="toast-container" aria-live="polite">
      <TransitionGroup name="toast">
        <div
          v-for="toast in notifStore.toasts"
          :key="toast.id"
          class="toast"
          :class="`toast--${toast.type}`"
          @click="notifStore.removeToast(toast.id)"
        >
          <Icon :name="iconMap[toast.type]" size="17" class="toast-icon" />
          <span class="toast-msg">{{ toast.message }}</span>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
const notifStore = useNotifStore()
const iconMap = {
  success: 'lucide:check-circle-2',
  error:   'lucide:x-circle',
  warning: 'lucide:alert-triangle',
  info:    'lucide:info',
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 360px;
}
.toast {
  display: flex; align-items: center; gap: 0.625rem;
  padding: 0.75rem 1rem;
  border-radius: 10px;
  cursor: pointer;
  backdrop-filter: blur(12px);
  border: 1px solid var(--color-border);
  background: var(--color-surface-2);
  font-size: 0.875rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}
.toast--success { border-color: rgba(34,197,94,0.3); }
.toast--error   { border-color: rgba(239,68,68,0.3); }
.toast--warning { border-color: rgba(245,158,11,0.3); }
.toast--success .toast-icon { color: var(--color-success); }
.toast--error   .toast-icon { color: var(--color-error); }
.toast--warning .toast-icon { color: var(--color-warning); }
.toast--info    .toast-icon { color: var(--color-brand-light); }

/* TransitionGroup animations */
.toast-enter-active { animation: slideInRight 0.25s ease; }
.toast-leave-active { animation: slideOutRight 0.2s ease forwards; }
@keyframes slideInRight  { from { opacity:0; transform:translateX(16px); } to { opacity:1; transform:translateX(0); } }
@keyframes slideOutRight { from { opacity:1; transform:translateX(0); } to { opacity:0; transform:translateX(16px); } }
</style>
