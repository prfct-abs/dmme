<template>
  <div class="campaigns-page">
    <!-- Header actions -->
    <div class="page-actions">
      <div class="filters">
        <button
          v-for="f in filters"
          :key="f.value"
          class="filter-btn"
          :class="{ active: activeFilter === f.value }"
          @click="activeFilter = f.value"
        >
          {{ f.label }}
          <span class="filter-count">{{ counts[f.value] }}</span>
        </button>
      </div>
      <button id="btn-new-campaign" class="btn-primary" @click="showModal = true">
        <Icon name="lucide:plus" size="16" /> New Campaign
      </button>
    </div>

    <!-- Loading skeletons -->
    <div v-if="campaignStore.isLoading" class="campaigns-grid">
      <div v-for="n in 6" :key="n" class="skeleton-card" />
    </div>

    <!-- Empty state -->
    <div v-else-if="filtered.length === 0" class="empty-fullpage">
      <div class="empty-icon"><Icon name="lucide:send" size="36" /></div>
      <h3>No campaigns here</h3>
      <p>Create your first Auto DM campaign to get started.</p>
      <button class="btn-primary" @click="showModal = true">
        <Icon name="lucide:plus" size="16" /> Create Campaign
      </button>
    </div>

    <!-- Campaign cards grid -->
    <div v-else class="campaigns-grid">
      <CampaignCard
        v-for="camp in filtered"
        :key="camp.id"
        :campaign="camp"
        @toggle="campaignStore.toggleCampaign(camp.id)"
        @delete="confirmDelete(camp.id)"
        @click="navigateTo(`/campaigns/${camp.id}`)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CampaignStatus } from '~/types'
definePageMeta({ middleware: 'auth' })

const campaignStore = useCampaignStore()
const notif         = useNotifStore()

await campaignStore.fetchCampaigns()

const showModal   = ref(false)
const activeFilter = ref<CampaignStatus | 'all'>('all')

const filters = [
  { label: 'All',    value: 'all'    as const },
  { label: 'Active', value: 'active' as const },
  { label: 'Paused', value: 'paused' as const },
  { label: 'Draft',  value: 'draft'  as const },
]

const counts = computed(() => ({
  all:    campaignStore.campaigns.length,
  active: campaignStore.campaigns.filter(c => c.status === 'active').length,
  paused: campaignStore.campaigns.filter(c => c.status === 'paused').length,
  draft:  campaignStore.campaigns.filter(c => c.status === 'draft').length,
}))

const filtered = computed(() =>
  activeFilter.value === 'all'
    ? campaignStore.campaigns
    : campaignStore.campaigns.filter(c => c.status === activeFilter.value)
)

async function confirmDelete(id: string) {
  if (!confirm('Delete this campaign? This cannot be undone.')) return
  await campaignStore.deleteCampaign(id)
  notif.success('Campaign deleted.')
}
</script>

<style scoped>
.campaigns-page { display: flex; flex-direction: column; gap: 1.5rem; }

.page-actions { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.filters      { display: flex; gap: 0.375rem; }

.filter-btn {
  display: flex; align-items: center; gap: 0.375rem;
  padding: 0.4rem 0.75rem; border-radius: 8px;
  background: none; border: 1px solid var(--color-border);
  color: var(--color-text-muted); font-size: 0.8rem; font-weight: 500;
  cursor: pointer; transition: all 0.15s;
}
.filter-btn:hover { border-color: var(--color-brand); color: var(--color-text); }
.filter-btn.active { background: rgba(108,99,255,0.12); border-color: var(--color-brand); color: var(--color-brand-light); }
.filter-count { background: var(--color-surface-2); border-radius: 99px; padding: 0.05rem 0.4rem; font-size: 0.7rem; }

.btn-primary {
  display: inline-flex; align-items: center; gap: 0.375rem;
  background: var(--color-brand); color: #fff;
  border: none; border-radius: 8px; padding: 0.5rem 1rem;
  font-size: 0.875rem; font-weight: 600; cursor: pointer;
  transition: background 0.15s;
}
.btn-primary:hover { background: var(--color-brand-dark); }

.campaigns-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1rem; }

.skeleton-card {
  height: 160px; border-radius: var(--radius);
  background: var(--color-surface); border: 1px solid var(--color-border);
  animation: pulse 1.4s ease infinite;
}
@keyframes pulse { 0%,100%{opacity:.4} 50%{opacity:.8} }

.empty-fullpage {
  text-align: center; padding: 5rem 2rem;
  display: flex; flex-direction: column; align-items: center; gap: 0.75rem;
}
.empty-icon { width: 72px; height: 72px; border-radius: 50%; background: rgba(108,99,255,0.1); display: grid; place-items: center; color: var(--color-brand-light); margin-bottom: 0.5rem; }
.empty-fullpage h3 { font-size: 1.1rem; font-weight: 600; }
.empty-fullpage p  { font-size: 0.875rem; color: var(--color-text-muted); max-width: 300px; }
</style>
