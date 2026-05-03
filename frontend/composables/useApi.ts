// composables/useApi.ts
// SSR-safe API wrapper around useFetch that automatically injects the JWT
// Bearer token from the auth store and maps FastAPI error shapes.

import type { UseFetchOptions } from 'nuxt/app'
import type { ApiError } from '~/types'

export function useApi() {
  const authStore = useAuthStore()
  const notifStore = useNotifStore()
  const config = useRuntimeConfig()

  // Build options with auth header injected
  function buildOptions<T>(opts: UseFetchOptions<T> = {}): UseFetchOptions<T> {
    return {
      baseURL: '/api',          // Nitro BFF prefix
      ...opts,
      headers: {
        ...(authStore.token ? { Authorization: `Bearer ${authStore.token}` } : {}),
        'Content-Type': 'application/json',
        ...(opts.headers as Record<string, string> ?? {}),
      },
      onResponseError({ response }) {
        const err = response._data as ApiError
        notifStore.addToast(err?.detail ?? 'An unexpected error occurred.', 'error')
        // Trigger token refresh on 401
        if (response.status === 401) authStore.logout()
      },
    }
  }

  function get<T>(url: string, opts?: UseFetchOptions<T>) {
    return useFetch<T>(url, { method: 'GET', ...buildOptions(opts) })
  }

  function post<T>(url: string, body: unknown, opts?: UseFetchOptions<T>) {
    return useFetch<T>(url, { method: 'POST', body, ...buildOptions(opts) })
  }

  function put<T>(url: string, body: unknown, opts?: UseFetchOptions<T>) {
    return useFetch<T>(url, { method: 'PUT', body, ...buildOptions(opts) })
  }

  function patch<T>(url: string, body: unknown, opts?: UseFetchOptions<T>) {
    return useFetch<T>(url, { method: 'PATCH', body, ...buildOptions(opts) })
  }

  function del<T>(url: string, opts?: UseFetchOptions<T>) {
    return useFetch<T>(url, { method: 'DELETE', ...buildOptions(opts) })
  }

  return { get, post, put, patch, del }
}
