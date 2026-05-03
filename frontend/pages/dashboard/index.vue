<template>
  <div class="dashboard">
    <!-- Stat cards -->
    <section class="stats-grid">
      <div v-for="stat in stats" :key="stat.label" class="stat-card">
        <div class="stat-icon" :style="{ background: stat.color + '18', color: stat.color }">
          <Icon :name="stat.icon" size="20" />
        </div>
        <div class="stat-body">
          <p class="stat-value">{{ stat.value }}</p>
          <p class="stat-label">{{ stat.label }}</p>
        </div>
        <div class="stat-trend" :class="stat.trend >= 0 ? 'up' : 'down'">
          <Icon :name="stat.trend >= 0 ? 'lucide:trending-up' : 'lucide:trending-down'" size="14" />
          {{ Math.abs(stat.trend) }}%
        </div>
      </div>
    </section>

    <!-- Active campaigns + Recent events -->
    <section class="two-col">
      <!-- Active Campaigns -->
      <div class="panel">
        <div class="panel-header">
          <h2 class="panel-title">Active Campaigns</h2>
          <NuxtLink to="/campaigns" class="panel-link">View all →</NuxtLink>
        </div>
        <div v-if="campaignStore.isLoading" class="skeleton-list">
          <div v-for="n in 3" :key="n" class="skeleton-row" />
        </div>
        <div v-else-if="campaignStore.activeCampaigns.length === 0" class="empty-state">
          <Icon name="lucide:send" size="28" />
          <p>No active campaigns yet</p>
          <NuxtLink to="/campaigns" class="btn-sm">Create one →</NuxtLink>
        </div>
        <ul v-else class="campaign-list">
          <li v-for="camp in campaignStore.activeCampaigns.slice(0, 5)" :key="camp.id" class="campaign-row">
            <div class="camp-platform">
              <Icon :name="platformIcon(camp.platform)" size="16" />
            </div>
            <div class="camp-info">
              <p class="camp-name">{{ camp.name }}</p>
              <p class="camp-meta">{{ camp.sentToday }}/{{ camp.dailyLimit }} DMs today</p>
            </div>
            <div class="camp-bar-wrap">
              <div class="camp-bar" :style="{ width: pct(camp.sentToday, camp.dailyLimit) + '%' }" />
            </div>
          </li>
        </ul>
      </div>

      <!-- Recent DM Events -->
      <div class="panel">
        <div class="panel-header">
          <h2 class="panel-title">Recent DMs</h2>
          <NuxtLink to="/analytics" class="panel-link">View all →</NuxtLink>
        </div>
        <ul class="event-list">
          <li v-for="ev in analyticsStore.events.slice(0, 6)" :key="ev.id" class="event-row">
            <span class="event-badge" :class="`badge--${ev.status}`">{{ ev.status }}</span>
            <span class="event-user">@{{ ev.recipientUsername ?? ev.recipientPlatformId }}</span>
            <span class="event-time">{{ relativeTime(ev.sentAt) }}</span>
          </li>
          <li v-if="analyticsStore.events.length === 0" class="empty-events">
            No DMs sent yet
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const campaignStore  = useCampaignStore()
const analyticsStore = useAnalyticsStore()

await Promise.all([
  campaignStore.fetchCampaigns(),
  analyticsStore.fetchEvents(),
  analyticsStore.fetchMetrics(),
])

const m = analyticsStore.metrics

const stats = computed(() => [
  { label: 'Total DMs Sent',   value: m?.totalSent?.toLocaleString()    ?? '–', icon: 'lucide:send',         color: '#6C63FF', trend: 12 },
  { label: 'Reply Rate',       value: m ? `${m.replyRate}%`             : '–',  icon: 'lucide:message-circle',color: '#22C55E', trend: 4  },
  { label: 'Active Campaigns', value: campaignStore.activeCampaigns.length,      icon: 'lucide:zap',           color: '#F59E0B', trend: 0  },
  { label: 'Failed DMs',       value: m?.totalSent && m?.failureRate ? Math.round(m.totalSent * m.failureRate / 100) : '–', icon: 'lucide:x-circle', color: '#EF4444', trend: -2 },
])

function platformIcon(p: string) {
  return p === 'instagram' ? 'mdi:instagram' : p === 'twitter' ? 'mdi:twitter' : 'mdi:linkedin'
}
function pct(sent: number, limit: number) {
  return Math.min(100, Math.round((sent / limit) * 100))
}
function relativeTime(iso: string) {
  const diff = Date.now() - new Date(iso).getTime()
  const m = Math.floor(diff / 60000)
  if (m < 60)  return `${m}m ago`
  if (m < 1440) return `${Math.floor(m / 60)}h ago`
  return `${Math.floor(m / 1440)}d ago`
}
</script>

<style scoped>
.dashboard { display: flex; flex-direction: column; gap: 1.75rem; }

/* ── Stat cards ── */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.stat-card {
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius); padding: 1.25rem;
  display: flex; align-items: center; gap: 0.875rem;
  transition: transform 0.2s, box-shadow 0.2s;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }
.stat-icon { width: 40px; height: 40px; border-radius: 10px; display: grid; place-items: center; flex-shrink: 0; }
.stat-body { flex: 1; }
.stat-value { font-size: 1.5rem; font-weight: 700; letter-spacing: -0.03em; }
.stat-label { font-size: 0.75rem; color: var(--color-text-muted); margin-top: 2px; }
.stat-trend { font-size: 0.75rem; font-weight: 600; display: flex; align-items: center; gap: 2px; }
.stat-trend.up   { color: var(--color-success); }
.stat-trend.down { color: var(--color-error); }

/* ── Two-col panels ── */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.panel { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius); padding: 1.25rem; }
.panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.panel-title  { font-size: 0.9rem; font-weight: 600; }
.panel-link   { font-size: 0.8rem; color: var(--color-brand-light); text-decoration: none; }
.panel-link:hover { text-decoration: underline; }

/* ── Skeleton ── */
.skeleton-list { display: flex; flex-direction: column; gap: 0.625rem; }
.skeleton-row  { height: 40px; border-radius: 8px; background: var(--color-surface-2); animation: pulse 1.4s ease infinite; }
@keyframes pulse { 0%,100%{opacity:.5} 50%{opacity:1} }

/* ── Empty state ── */
.empty-state { text-align: center; padding: 2rem 0; color: var(--color-text-muted); display: flex; flex-direction: column; align-items: center; gap: 0.5rem; font-size: 0.875rem; }
.btn-sm { font-size: 0.8rem; color: var(--color-brand-light); text-decoration: none; }

/* ── Campaign list ── */
.campaign-list { list-style: none; display: flex; flex-direction: column; gap: 0.75rem; }
.campaign-row  { display: flex; align-items: center; gap: 0.75rem; }
.camp-platform { width: 32px; height: 32px; border-radius: 8px; background: var(--color-surface-2); display: grid; place-items: center; color: var(--color-text-muted); flex-shrink: 0; }
.camp-info     { flex: 1; min-width: 0; }
.camp-name     { font-size: 0.85rem; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.camp-meta     { font-size: 0.72rem; color: var(--color-text-muted); }
.camp-bar-wrap { width: 60px; height: 4px; background: var(--color-surface-2); border-radius: 99px; overflow: hidden; }
.camp-bar      { height: 100%; background: var(--color-brand); border-radius: 99px; transition: width 0.4s ease; }

/* ── Event list ── */
.event-list  { list-style: none; display: flex; flex-direction: column; gap: 0.625rem; }
.event-row   { display: flex; align-items: center; gap: 0.625rem; font-size: 0.82rem; }
.empty-events { font-size: 0.85rem; color: var(--color-text-muted); text-align: center; padding: 2rem 0; }
.event-badge { border-radius: 99px; padding: 0.15rem 0.5rem; font-size: 0.7rem; font-weight: 600; text-transform: capitalize; }
.badge--sent    { background: rgba(34,197,94,0.12);  color: var(--color-success); }
.badge--failed  { background: rgba(239,68,68,0.12);  color: var(--color-error); }
.badge--replied { background: rgba(108,99,255,0.12); color: var(--color-brand-light); }
.badge--pending { background: rgba(245,158,11,0.12); color: var(--color-warning); }
.event-user  { flex: 1; font-weight: 500; }
.event-time  { color: var(--color-text-muted); font-size: 0.75rem; flex-shrink: 0; }
</style>
