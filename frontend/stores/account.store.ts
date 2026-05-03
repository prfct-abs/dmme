// stores/account.store.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { SocialAccount } from '~/types'

// ── Mock connected accounts ────────────────────────────────────────────────────
const MOCK_ACCOUNTS: SocialAccount[] = [
  {
    id: 'acc-001',
    platform: 'instagram',
    platformUserId: '123456789',
    platformUsername: '@alexdemo',
    isActive: true,
    createdAt: new Date().toISOString(),
  },
  {
    id: 'acc-002',
    platform: 'twitter',
    platformUserId: '987654321',
    platformUsername: '@alexdemo_x',
    isActive: true,
    createdAt: new Date().toISOString(),
  },
]

export const useAccountStore = defineStore('account', () => {
  const accounts  = ref<SocialAccount[]>([])
  const isLoading = ref(false)

  const activeAccounts = computed(() => accounts.value.filter(a => a.isActive))
  const byPlatform     = computed(() => (platform: string) => accounts.value.filter(a => a.platform === platform))
  const hasAnyAccount  = computed(() => accounts.value.length > 0)

  async function fetchAccounts() {
    isLoading.value = true
    // TODO: Replace with real API call when backend is ready
    // const { data } = await useFetch<SocialAccount[]>('/api/accounts', ...)
    await new Promise(r => setTimeout(r, 300))
    accounts.value  = MOCK_ACCOUNTS
    isLoading.value = false
  }

  async function disconnectAccount(id: string) {
    // TODO: await useFetch(`/api/accounts/${id}`, { method: 'DELETE', ... })
    accounts.value = accounts.value.filter(a => a.id !== id)
  }

  // Initiate OAuth flow — redirect to FastAPI OAuth endpoint
  function connectPlatform(platform: string) {
    const config = useRuntimeConfig()
    window.location.href = `${config.public.apiBaseUrl}/api/v1/auth/oauth/${platform}`
  }

  return { accounts, isLoading, activeAccounts, byPlatform, hasAnyAccount, fetchAccounts, disconnectAccount, connectPlatform }
})
