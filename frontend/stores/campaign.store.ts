// stores/campaign.store.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Campaign, CreateCampaignPayload, PaginatedResponse } from '~/types'

// ── Mock data ─────────────────────────────────────────────────────────────────
const MOCK_CAMPAIGNS: Campaign[] = [
  {
    id: 'camp-001',
    name: 'Instagram Comment Funnel',
    platform: 'instagram',
    status: 'active',
    triggerConfig: { type: 'comment_keyword', keywords: ['FREE', 'GUIDE', 'LINK'] },
    messageTemplate: { body: 'Hey {{first_name}}! Here\'s the free guide you asked for 👇 {{link}}' },
    dailyLimit: 100,
    sentToday: 47,
    socialAccountId: 'acc-001',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'camp-002',
    name: 'New Follower Welcome',
    platform: 'instagram',
    status: 'active',
    triggerConfig: { type: 'new_follower', keywords: [] },
    messageTemplate: { body: 'Welcome {{first_name}}! 🎉 So glad you\'re here. DM me "START" to get my free guide.' },
    dailyLimit: 50,
    sentToday: 23,
    socialAccountId: 'acc-001',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'camp-003',
    name: 'X Keyword DM Campaign',
    platform: 'twitter',
    status: 'paused',
    triggerConfig: { type: 'dm_keyword', keywords: ['PROMO', 'DEAL'] },
    messageTemplate: { body: 'Hey! I saw you\'re interested in deals — here\'s an exclusive offer for you 🔥' },
    dailyLimit: 30,
    sentToday: 0,
    socialAccountId: 'acc-002',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'camp-004',
    name: 'Story Reply Capture',
    platform: 'instagram',
    status: 'draft',
    triggerConfig: { type: 'story_reply', keywords: [] },
    messageTemplate: { body: 'Thanks for replying to my story! Drop your email below to get the full resource 📩' },
    dailyLimit: 200,
    sentToday: 0,
    socialAccountId: 'acc-001',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  },
]

export const useCampaignStore = defineStore('campaign', () => {
  const campaigns      = ref<Campaign[]>([])
  const activeCampaign = ref<Campaign | null>(null)
  const isLoading      = ref(false)
  const total          = ref(0)
  const page           = ref(1)

  const activeCampaigns = computed(() => campaigns.value.filter(c => c.status === 'active'))
  const draftCampaigns  = computed(() => campaigns.value.filter(c => c.status === 'draft'))
  const byId            = computed(() => (id: string) => campaigns.value.find(c => c.id === id))

  async function fetchCampaigns(_page = 1) {
    isLoading.value = true
    // TODO: replace with real API call when backend is ready
    // const { data } = await useFetch(`/api/campaigns?page=${_page}`, { ... })
    await new Promise(r => setTimeout(r, 400)) // simulate network
    campaigns.value = MOCK_CAMPAIGNS
    total.value     = MOCK_CAMPAIGNS.length
    page.value      = _page
    isLoading.value = false
  }

  async function createCampaign(payload: CreateCampaignPayload): Promise<Campaign> {
    const camp: Campaign = {
      id: `camp-${Date.now()}`,
      ...payload,
      status: 'draft',
      sentToday: 0,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    } as any
    campaigns.value.unshift(camp)
    return camp
  }

  async function toggleCampaign(id: string) {
    const camp = campaigns.value.find(c => c.id === id)
    if (!camp) return
    camp.status = camp.status === 'active' ? 'paused' : 'active'
  }

  async function deleteCampaign(id: string) {
    campaigns.value = campaigns.value.filter(c => c.id !== id)
  }

  function setActive(campaign: Campaign | null) {
    activeCampaign.value = campaign
  }

  return {
    campaigns, activeCampaign, isLoading, total, page,
    activeCampaigns, draftCampaigns, byId,
    fetchCampaigns, createCampaign, toggleCampaign, deleteCampaign, setActive,
  }
})
