<template>
  <div class="accounts-page">
    <div class="page-top">
      <p class="page-desc">Connect your social accounts to start automating DMs.</p>
      <div class="connect-row">
        <button
          v-for="p in platforms"
          :key="p.id"
          class="connect-btn"
          :style="{ '--btn-color': p.color }"
          @click="accountStore.connectPlatform(p.id)"
        >
          <Icon :name="p.icon" size="18" /> Connect {{ p.label }}
        </button>
      </div>
    </div>

    <!-- Connected accounts -->
    <div v-if="accountStore.isLoading" class="accounts-list">
      <div v-for="n in 3" :key="n" class="skeleton-account" />
    </div>

    <div v-else-if="accountStore.accounts.length === 0" class="empty-state">
      <Icon name="lucide:link-2-off" size="32" />
      <p>No accounts connected yet</p>
    </div>

    <div v-else class="accounts-list">
      <div v-for="acc in accountStore.accounts" :key="acc.id" class="account-card">
        <div class="acc-platform-icon" :style="{ background: platformColor(acc.platform) + '18', color: platformColor(acc.platform) }">
          <Icon :name="platformIcon(acc.platform)" size="22" />
        </div>
        <div class="acc-info">
          <p class="acc-username">@{{ acc.platformUsername }}</p>
          <p class="acc-platform">{{ acc.platform }}</p>
        </div>
        <div class="acc-status" :class="acc.isActive ? 'status-ok' : 'status-expired'">
          <span class="status-dot" />
          {{ acc.isActive ? 'Active' : 'Token Expired' }}
        </div>
        <button class="disconnect-btn" @click="confirmDisconnect(acc.id)">
          <Icon name="lucide:unlink" size="15" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const accountStore = useAccountStore()
const notif        = useNotifStore()

await accountStore.fetchAccounts()

const platforms = [
  { id: 'instagram', label: 'Instagram', icon: 'mdi:instagram', color: '#E1306C' },
  { id: 'twitter',   label: 'X (Twitter)', icon: 'mdi:twitter',  color: '#1DA1F2' },
  { id: 'linkedin',  label: 'LinkedIn',  icon: 'mdi:linkedin',  color: '#0A66C2' },
]

function platformIcon(p: string)  { return platforms.find(x => x.id === p)?.icon  ?? 'lucide:link' }
function platformColor(p: string) { return platforms.find(x => x.id === p)?.color ?? '#6C63FF' }

async function confirmDisconnect(id: string) {
  if (!confirm('Disconnect this account? Running campaigns using it will be paused.')) return
  await accountStore.disconnectAccount(id)
  notif.success('Account disconnected.')
}
</script>

<style scoped>
.accounts-page { display: flex; flex-direction: column; gap: 1.5rem; }

.page-desc { font-size: 0.875rem; color: var(--color-text-muted); margin-bottom: 0.75rem; }
.connect-row { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.connect-btn {
  display: inline-flex; align-items: center; gap: 0.5rem;
  border: 1px solid var(--btn-color, var(--color-border));
  border-radius: 8px; padding: 0.5rem 1rem;
  background: transparent; color: var(--btn-color, var(--color-text));
  font-size: 0.85rem; font-weight: 600; cursor: pointer;
  transition: all 0.15s;
}
.connect-btn:hover { background: rgba(255,255,255,0.04); }

.accounts-list { display: flex; flex-direction: column; gap: 0.75rem; }
.skeleton-account { height: 72px; border-radius: var(--radius); background: var(--color-surface); animation: pulse 1.4s ease infinite; }
@keyframes pulse { 0%,100%{opacity:.4} 50%{opacity:.8} }

.empty-state { text-align: center; padding: 4rem; color: var(--color-text-muted); display: flex; flex-direction: column; align-items: center; gap: 0.625rem; font-size: 0.875rem; }

.account-card {
  display: flex; align-items: center; gap: 1rem;
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius); padding: 1rem 1.25rem;
  transition: border-color 0.15s;
}
.account-card:hover { border-color: rgba(108,99,255,0.3); }

.acc-platform-icon { width: 44px; height: 44px; border-radius: 12px; display: grid; place-items: center; flex-shrink: 0; }
.acc-info { flex: 1; }
.acc-username { font-size: 0.9rem; font-weight: 600; }
.acc-platform { font-size: 0.75rem; color: var(--color-text-muted); text-transform: capitalize; margin-top: 2px; }

.acc-status { display: flex; align-items: center; gap: 0.375rem; font-size: 0.78rem; font-weight: 500; }
.status-ok      { color: var(--color-success); }
.status-expired { color: var(--color-warning); }
.status-dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; }

.disconnect-btn {
  background: none; border: 1px solid var(--color-border);
  border-radius: 8px; padding: 0.375rem; cursor: pointer;
  color: var(--color-text-muted); transition: all 0.15s;
}
.disconnect-btn:hover { border-color: var(--color-error); color: var(--color-error); background: rgba(239,68,68,0.08); }
</style>
