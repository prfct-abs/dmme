<template>
  <div class="analytics-page">
    <!-- Date range picker -->
    <div class="toolbar">
      <div class="date-range">
        <input id="date-from" v-model="from" type="date" class="date-input" @change="reload" />
        <span class="date-sep">→</span>
        <input id="date-to" v-model="to" type="date" class="date-input" @change="reload" />
      </div>
      <div class="quick-ranges">
        <button v-for="r in quickRanges" :key="r.label" class="range-btn" @click="applyRange(r.days)">
          {{ r.label }}
        </button>
      </div>
    </div>

    <!-- Summary cards -->
    <div class="summary-grid">
      <div v-for="s in summary" :key="s.label" class="summary-card">
        <p class="sum-val">{{ s.value }}</p>
        <p class="sum-label">{{ s.label }}</p>
      </div>
    </div>

    <!-- Chart -->
    <div class="chart-panel">
      <h2 class="panel-title">DMs Sent Per Day</h2>
      <AnalyticsMetricsChart v-if="chartData" :data="chartData" />
      <div v-else class="chart-skeleton" />
    </div>

    <!-- Event log table -->
    <div class="table-panel">
      <h2 class="panel-title">DM Event Log</h2>
      <div class="table-wrap">
        <table id="events-table">
          <thead>
            <tr>
              <th>Status</th><th>Recipient</th><th>Campaign</th><th>Sent At</th><th>Replied At</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ev in analyticsStore.events" :key="ev.id">
              <td><span class="badge" :class="`badge--${ev.status}`">{{ ev.status }}</span></td>
              <td>@{{ ev.recipientUsername ?? ev.recipientPlatformId }}</td>
              <td>{{ ev.campaignName }}</td>
              <td>{{ fmtDate(ev.sentAt) }}</td>
              <td>{{ ev.repliedAt ? fmtDate(ev.repliedAt) : '–' }}</td>
            </tr>
            <tr v-if="analyticsStore.events.length === 0">
              <td colspan="5" class="empty-row">No events yet</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const analyticsStore = useAnalyticsStore()

const from = ref(analyticsStore.dateRange.from)
const to   = ref(analyticsStore.dateRange.to)

async function reload() {
  analyticsStore.setDateRange(from.value, to.value)
  await Promise.all([analyticsStore.fetchMetrics(), analyticsStore.fetchEvents()])
}

await reload()

const quickRanges = [
  { label: '7d', days: 7 }, { label: '14d', days: 14 },
  { label: '30d', days: 30 }, { label: '90d', days: 90 },
]
function applyRange(days: number) {
  to.value   = new Date().toISOString().slice(0, 10)
  from.value = new Date(Date.now() - days * 864e5).toISOString().slice(0, 10)
  reload()
}

const m = computed(() => analyticsStore.metrics)
const summary = computed(() => [
  { label: 'Total Sent',   value: m.value?.totalSent?.toLocaleString() ?? '–' },
  { label: 'Total Replied', value: m.value?.totalReplied?.toLocaleString() ?? '–' },
  { label: 'Reply Rate',   value: m.value ? `${m.value.replyRate}%` : '–' },
  { label: 'Failure Rate', value: m.value ? `${m.value.failureRate}%` : '–' },
])

const chartData = computed(() => {
  const days = m.value?.sentByDay
  if (!days?.length) return null
  return {
    labels:   days.map(d => d.date),
    datasets: [{
      label: 'DMs Sent',
      data:  days.map(d => d.count),
      borderColor: '#6C63FF',
      backgroundColor: 'rgba(108,99,255,0.1)',
      fill: true, tension: 0.4,
    }],
  }
})

function fmtDate(iso: string) {
  return new Date(iso).toLocaleString(undefined, { dateStyle: 'short', timeStyle: 'short' })
}
</script>

<style scoped>
.analytics-page { display: flex; flex-direction: column; gap: 1.5rem; }

.toolbar { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.date-range { display: flex; align-items: center; gap: 0.5rem; }
.date-input {
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: 8px; padding: 0.4rem 0.625rem;
  color: var(--color-text); font-size: 0.8rem; outline: none;
}
.date-input:focus { border-color: var(--color-brand); }
.date-sep { color: var(--color-text-muted); font-size: 0.8rem; }

.quick-ranges { display: flex; gap: 0.375rem; }
.range-btn {
  padding: 0.35rem 0.625rem; border-radius: 6px;
  background: var(--color-surface); border: 1px solid var(--color-border);
  color: var(--color-text-muted); font-size: 0.78rem; cursor: pointer;
  transition: all 0.15s;
}
.range-btn:hover { border-color: var(--color-brand); color: var(--color-brand-light); }

.summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.summary-card {
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius); padding: 1.25rem; text-align: center;
}
.sum-val   { font-size: 1.75rem; font-weight: 700; letter-spacing: -0.04em; }
.sum-label { font-size: 0.75rem; color: var(--color-text-muted); margin-top: 4px; }

.chart-panel, .table-panel {
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius); padding: 1.5rem;
}
.panel-title { font-size: 0.9rem; font-weight: 600; margin-bottom: 1.25rem; }
.chart-skeleton { height: 220px; border-radius: 8px; background: var(--color-surface-2); animation: pulse 1.4s ease infinite; }
@keyframes pulse { 0%,100%{opacity:.4} 50%{opacity:.8} }

.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
th { text-align: left; padding: 0.625rem 0.75rem; color: var(--color-text-muted); font-size: 0.75rem; font-weight: 500; border-bottom: 1px solid var(--color-border); }
td { padding: 0.625rem 0.75rem; border-bottom: 1px solid var(--color-border); }
tr:last-child td { border-bottom: none; }
tr:hover td { background: var(--color-surface-2); }
.empty-row { text-align: center; color: var(--color-text-muted); padding: 2rem; }

.badge { border-radius: 99px; padding: 0.15rem 0.5rem; font-size: 0.7rem; font-weight: 600; text-transform: capitalize; }
.badge--sent    { background: rgba(34,197,94,0.12);  color: var(--color-success); }
.badge--failed  { background: rgba(239,68,68,0.12);  color: var(--color-error); }
.badge--replied { background: rgba(108,99,255,0.12); color: var(--color-brand-light); }
.badge--pending { background: rgba(245,158,11,0.12); color: var(--color-warning); }
</style>
