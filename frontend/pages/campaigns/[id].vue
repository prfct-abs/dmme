<template>
  <div v-if="campaign" class="detail-page">
    <!-- Back + Header -->
    <div class="detail-header">
      <NuxtLink to="/campaigns" class="back-link">
        <Icon name="lucide:arrow-left" size="16" /> Campaigns
      </NuxtLink>
      <div class="header-actions">
        <span class="status-badge" :class="`status--${campaign.status}`">{{ campaign.status }}</span>
        <button
          class="toggle-btn"
          :class="campaign.status === 'active' ? 'btn-pause' : 'btn-activate'"
          @click="handleToggle"
        >
          <Icon :name="campaign.status === 'active' ? 'lucide:pause' : 'lucide:play'" size="15" />
          {{ campaign.status === 'active' ? 'Pause' : 'Activate' }}
        </button>
      </div>
    </div>

    <h1 class="camp-title">{{ campaign.name }}</h1>

    <!-- Two column: trigger + message -->
    <div class="editor-grid">
      <div class="editor-panel">
        <h2 class="section-title">
          <Icon name="lucide:zap" size="16" /> Trigger
        </h2>
        <TriggerBuilder :model-value="triggerConfig" @update:model-value="triggerConfig = $event" />
      </div>
      <div class="editor-panel">
        <h2 class="section-title">
          <Icon name="lucide:message-square" size="16" /> Message
        </h2>
        <MessageEditor :model-value="messageTemplate" @update:model-value="messageTemplate = $event" />
      </div>
    </div>

    <!-- Daily limit -->
    <div class="limit-row">
      <label>Daily DM Limit</label>
      <div class="limit-control">
        <input v-model.number="dailyLimit" type="range" min="1" max="500" step="5" />
        <span class="limit-val">{{ dailyLimit }} / day</span>
      </div>
    </div>

    <!-- Save -->
    <div class="save-row">
      <button id="btn-save-campaign" class="btn-primary" :disabled="saving" @click="handleSave">
        <Icon v-if="!saving" name="lucide:save" size="16" />
        <span class="spinner" v-else />
        {{ saving ? 'Saving…' : 'Save Changes' }}
      </button>
    </div>
  </div>

  <!-- Loading state -->
  <div v-else class="loading-state">
    <div v-for="n in 4" :key="n" class="skeleton-block" />
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const route         = useRoute()
const campaignStore = useCampaignStore()
const notif         = useNotifStore()

const id = route.params.id as string
await campaignStore.fetchCampaigns()

const campaign = computed(() => campaignStore.byId(id))

const triggerConfig   = ref({ ...campaign.value?.triggerConfig  })
const messageTemplate = ref({ ...campaign.value?.messageTemplate })
const dailyLimit      = ref(campaign.value?.dailyLimit ?? 50)
const saving          = ref(false)

async function handleSave() {
  saving.value = true
  try {
    await useFetch(`/api/campaigns/${id}`, {
      method: 'PUT',
      body: { triggerConfig: triggerConfig.value, messageTemplate: messageTemplate.value, dailyLimit: dailyLimit.value },
      headers: { Authorization: `Bearer ${useAuthStore().token}` },
    })
    notif.success('Campaign saved!')
  }
  catch { notif.error('Failed to save campaign.') }
  finally { saving.value = false }
}

async function handleToggle() {
  await campaignStore.toggleCampaign(id)
  notif.success(`Campaign ${campaign.value?.status}.`)
}
</script>

<style scoped>
.detail-page { display: flex; flex-direction: column; gap: 1.5rem; }

.detail-header { display: flex; align-items: center; justify-content: space-between; }
.back-link {
  display: inline-flex; align-items: center; gap: 0.375rem;
  color: var(--color-text-muted); text-decoration: none; font-size: 0.85rem;
  transition: color 0.15s;
}
.back-link:hover { color: var(--color-text); }

.header-actions { display: flex; align-items: center; gap: 0.75rem; }
.status-badge { border-radius: 99px; padding: 0.2rem 0.625rem; font-size: 0.75rem; font-weight: 600; text-transform: capitalize; }
.status--active { background: rgba(34,197,94,0.12); color: var(--color-success); }
.status--paused { background: rgba(245,158,11,0.12); color: var(--color-warning); }
.status--draft  { background: rgba(139,138,168,0.12); color: var(--color-text-muted); }

.toggle-btn {
  display: inline-flex; align-items: center; gap: 0.375rem;
  border: none; border-radius: 8px; padding: 0.45rem 0.875rem;
  font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.15s;
}
.btn-pause    { background: rgba(245,158,11,0.12); color: var(--color-warning); }
.btn-activate { background: rgba(34,197,94,0.12);  color: var(--color-success); }

.camp-title { font-size: 1.5rem; font-weight: 700; letter-spacing: -0.03em; }

.editor-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.editor-panel { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius); padding: 1.5rem; }
.section-title { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; font-weight: 600; margin-bottom: 1.25rem; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.05em; }

.limit-row { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius); padding: 1.25rem; display: flex; align-items: center; justify-content: space-between; }
.limit-row label { font-size: 0.875rem; font-weight: 500; }
.limit-control { display: flex; align-items: center; gap: 1rem; }
.limit-control input[type=range] { width: 160px; accent-color: var(--color-brand); }
.limit-val { font-size: 0.875rem; font-weight: 700; color: var(--color-brand-light); min-width: 70px; }

.save-row { display: flex; justify-content: flex-end; }
.btn-primary {
  display: inline-flex; align-items: center; gap: 0.5rem;
  background: var(--color-brand); color: #fff; border: none; border-radius: 8px;
  padding: 0.6rem 1.25rem; font-size: 0.875rem; font-weight: 600; cursor: pointer;
  transition: background 0.15s;
}
.btn-primary:hover:not(:disabled) { background: var(--color-brand-dark); }
.btn-primary:disabled { opacity: 0.5; cursor: not-allowed; }

.spinner { width: 14px; height: 14px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.loading-state { display: flex; flex-direction: column; gap: 1rem; }
.skeleton-block { height: 80px; border-radius: var(--radius); background: var(--color-surface); animation: pulse 1.4s ease infinite; }
@keyframes pulse { 0%,100%{opacity:.4} 50%{opacity:.8} }
</style>
