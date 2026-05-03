<template>
  <aside class="sidebar">
    <div class="sidebar-brand">
      <Icon name="lucide:zap" size="22" />
      <span>AutoDM</span>
    </div>

    <nav class="sidebar-nav">
      <NuxtLink
        v-for="item in navItems"
        :key="item.to"
        :to="item.to"
        class="nav-item"
        active-class="nav-item--active"
      >
        <Icon :name="item.icon" size="18" />
        <span>{{ item.label }}</span>
      </NuxtLink>
    </nav>

    <div class="sidebar-footer">
      <div class="user-chip">
        <div class="user-avatar">{{ initials }}</div>
        <div class="user-info">
          <p class="user-name">{{ authStore.fullName }}</p>
          <p class="user-plan">{{ authStore.user?.plan }}</p>
        </div>
      </div>
      <button class="logout-btn" @click="authStore.logout()">
        <Icon name="lucide:log-out" size="16" />
      </button>
    </div>
  </aside>
</template>

<script setup lang="ts">
const authStore = useAuthStore()
const initials = computed(() =>
  authStore.fullName.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
)

const navItems = [
  { to: '/dashboard',  icon: 'lucide:layout-dashboard', label: 'Dashboard' },
  { to: '/campaigns',  icon: 'lucide:send',             label: 'Campaigns' },
  { to: '/analytics',  icon: 'lucide:bar-chart-3',      label: 'Analytics' },
  { to: '/accounts',   icon: 'lucide:link',             label: 'Accounts' },
  { to: '/templates',  icon: 'lucide:file-text',        label: 'Templates' },
]
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-w);
  min-width: var(--sidebar-w);
  height: 100vh;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  padding: 1.25rem 0.75rem;
  gap: 0.5rem;
}
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-brand);
  padding: 0.5rem 0.75rem 1.25rem;
  letter-spacing: -0.02em;
}
.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 0.75rem;
  border-radius: 8px;
  color: var(--color-text-muted);
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.15s ease;
}
.nav-item:hover  { background: var(--color-surface-2); color: var(--color-text); }
.nav-item--active { background: rgba(108,99,255,0.12); color: var(--color-brand-light); }
.sidebar-footer {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--color-border);
}
.user-chip { display: flex; align-items: center; gap: 0.5rem; flex: 1; overflow: hidden; }
.user-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: var(--color-brand-dark);
  color: #fff;
  display: grid; place-items: center;
  font-size: 0.75rem; font-weight: 700; flex-shrink: 0;
}
.user-info { overflow: hidden; }
.user-name  { font-size: 0.8rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.user-plan  { font-size: 0.7rem; color: var(--color-text-muted); text-transform: capitalize; }
.logout-btn {
  background: none; border: none; cursor: pointer;
  color: var(--color-text-muted); padding: 0.375rem;
  border-radius: 6px; transition: all 0.15s;
}
.logout-btn:hover { background: rgba(239,68,68,0.1); color: var(--color-error); }
</style>
