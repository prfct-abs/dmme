// stores/analytics.store.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { DmEvent, CampaignMetrics } from '~/types'

// ── Mock data ─────────────────────────────────────────────────────────────────
const MOCK_EVENTS: DmEvent[] = [
  { id: 'ev-1', campaignId: 'camp-001', recipientPlatformId: '11111', recipientUsername: 'sarah_designs', status: 'replied',  sentAt: new Date(Date.now() - 5 * 60000).toISOString(),  repliedAt: new Date(Date.now() - 2 * 60000).toISOString() },
  { id: 'ev-2', campaignId: 'camp-001', recipientPlatformId: '22222', recipientUsername: 'mike_photos',   status: 'sent',    sentAt: new Date(Date.now() - 12 * 60000).toISOString() },
  { id: 'ev-3', campaignId: 'camp-002', recipientPlatformId: '33333', recipientUsername: 'jenny_codes',   status: 'sent',    sentAt: new Date(Date.now() - 20 * 60000).toISOString() },
  { id: 'ev-4', campaignId: 'camp-001', recipientPlatformId: '44444', recipientUsername: 'alex_travels',  status: 'failed',  sentAt: new Date(Date.now() - 35 * 60000).toISOString() },
  { id: 'ev-5', campaignId: 'camp-002', recipientPlatformId: '55555', recipientUsername: 'tom_dev',       status: 'replied', sentAt: new Date(Date.now() - 60 * 60000).toISOString(),  repliedAt: new Date(Date.now() - 45 * 60000).toISOString() },
  { id: 'ev-6', campaignId: 'camp-001', recipientPlatformId: '66666', recipientUsername: 'nina_artist',   status: 'sent',    sentAt: new Date(Date.now() - 90 * 60000).toISOString() },
]

const MOCK_METRICS: CampaignMetrics = {
  totalSent:    1247,
  totalReplied: 312,
  replyRate:    25.0,
  failureRate:  2.1,
  sentByDay: [
    { date: '2026-03-20', count: 142 },
    { date: '2026-03-21', count: 198 },
    { date: '2026-03-22', count: 176 },
    { date: '2026-03-23', count: 231 },
    { date: '2026-03-24', count: 189 },
    { date: '2026-03-25', count: 167 },
    { date: '2026-03-26', count: 144 },
  ],
}

function defaultDateRange() {
  const to   = new Date().toISOString().slice(0, 10)
  const from = new Date(Date.now() - 7 * 864e5).toISOString().slice(0, 10)
  return { from, to }
}

export const useAnalyticsStore = defineStore('analytics', () => {
  const metrics   = ref<CampaignMetrics | null>(null)
  const events    = ref<DmEvent[]>([])
  const dateRange = ref(defaultDateRange())
  const isLoading = ref(false)

  async function fetchMetrics(_campaignId?: string) {
    isLoading.value = true
    await new Promise(r => setTimeout(r, 300))
    metrics.value   = MOCK_METRICS
    isLoading.value = false
  }

  async function fetchEvents(_campaignId?: string) {
    await new Promise(r => setTimeout(r, 200))
    events.value = MOCK_EVENTS
  }

  function setDateRange(from: string, to: string) {
    dateRange.value = { from, to }
  }

  return { metrics, events, dateRange, isLoading, fetchMetrics, fetchEvents, setDateRange }
})
