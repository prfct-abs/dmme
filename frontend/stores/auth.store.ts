// stores/auth.store.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, AuthTokens } from '~/types'

// ── localStorage helpers (SSR-safe) ──────────────────────────────────────────
const ls = {
  get: (k: string) => (typeof window !== 'undefined' ? window.localStorage.getItem(k) : null),
  set: (k: string, v: string) => typeof window !== 'undefined' && window.localStorage.setItem(k, v),
  del: (k: string) => typeof window !== 'undefined' && window.localStorage.removeItem(k),
}

export const useAuthStore = defineStore('auth', () => {
  // ── State ─────────────────────────────────────────────────────────────────
  // Always null on SSR. Hydrated client-side via hydrate() called from plugin.
  const token        = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const user         = ref<User | null>(null)

  // ── Getters ───────────────────────────────────────────────────────────────
  const isAuthenticated = computed<boolean>(() => !!token.value && !!user.value)
  const fullName        = computed<string>(() => user.value?.name ?? '')

  // ── Hydrate from localStorage — call ONLY on client ───────────────────────
  function hydrate() {
    token.value        = ls.get('autodm_token')
    refreshToken.value = ls.get('autodm_refresh')
    const raw          = ls.get('autodm_user')
    user.value         = raw ? (JSON.parse(raw) as User) : null
  }

  // ── Actions ───────────────────────────────────────────────────────────────
  function setSession(u: User, tokens: AuthTokens) {
    user.value         = u
    token.value        = tokens.accessToken
    refreshToken.value = tokens.refreshToken
    ls.set('autodm_token',   tokens.accessToken)
    ls.set('autodm_refresh', tokens.refreshToken)
    ls.set('autodm_user',    JSON.stringify(u))
  }

  async function login(email: string, password: string) {
    const { data, error } = await useFetch<{ user: User; tokens: AuthTokens }>('/api/auth/login', {
      method: 'POST',
      body: { email, password },
    })
    if (error.value) throw error.value
    setSession(data.value!.user, data.value!.tokens)
    await navigateTo('/dashboard')
  }

  async function fetchMe() {
    const { data } = await useFetch<User>('/api/auth/me', {
      headers: token.value ? { Authorization: `Bearer ${token.value}` } : {},
    })
    if (data.value) {
      user.value = data.value
      ls.set('autodm_user', JSON.stringify(data.value))
    }
  }

  function logout() {
    user.value = null
    token.value = null
    refreshToken.value = null
    ls.del('autodm_token')
    ls.del('autodm_refresh')
    ls.del('autodm_user')
    navigateTo('/login')
  }

  return {
    user, token, refreshToken,
    isAuthenticated, fullName,
    hydrate, setSession, login, fetchMe, logout,
  }
})
