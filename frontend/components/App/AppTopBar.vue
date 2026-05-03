<template>
  <header class="topbar">
    <div class="topbar-left">
      <h1 class="page-title">{{ pageTitle }}</h1>
    </div>
    <div class="topbar-right">
      <div class="ws-indicator" :class="{ connected: ws.isConnected.value }">
        <span class="ws-dot" />
        <span class="ws-label">{{ ws.isConnected.value ? 'Live' : 'Offline' }}</span>
      </div>
      <NuxtLink to="/campaigns/new" class="btn-primary">
        <Icon name="lucide:plus" size="16" />
        New Campaign
      </NuxtLink>
    </div>
  </header>
</template>

<script setup lang="ts">
const route = useRoute()
const ws    = useWebSocket()

const titleMap: Record<string, string> = {
  '/dashboard':  'Dashboard',
  '/campaigns':  'Campaigns',
  '/analytics':  'Analytics',
  '/accounts':   'Connected Accounts',
  '/templates':  'Templates',
}
const pageTitle = computed(() => titleMap[route.path] ?? 'AutoDM')

onMounted(() => { if (useAuthStore().isAuthenticated) ws.connect() })
</script>

<style scoped>
.topbar {
  height: var(--topbar-h);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
  flex-shrink: 0;
}
.page-title { font-size: 1rem; font-weight: 600; }

.topbar-right { display: flex; align-items: center; gap: 1rem; }

.ws-indicator {
  display: flex; align-items: center; gap: 0.375rem;
  font-size: 0.75rem; color: var(--color-text-muted);
}
.ws-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--color-text-muted);
  transition: background 0.3s;
}
.ws-indicator.connected .ws-dot  { background: var(--color-success); box-shadow: 0 0 6px var(--color-success); }
.ws-indicator.connected .ws-label { color: var(--color-success); }

.btn-primary {
  display: inline-flex; align-items: center; gap: 0.375rem;
  background: var(--color-brand); color: #fff;
  border: none; border-radius: 8px;
  padding: 0.45rem 0.9rem;
  font-size: 0.875rem; font-weight: 600;
  cursor: pointer; text-decoration: none;
  transition: background 0.15s, box-shadow 0.15s;
}
.btn-primary:hover { background: var(--color-brand-dark); box-shadow: var(--shadow-glow); }
</style>
