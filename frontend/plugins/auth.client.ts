// plugins/auth.client.ts
// Runs ONLY on the client (.client.ts suffix).
export default defineNuxtPlugin(() => {
  const authStore = useAuthStore()
  authStore.hydrate()

  // ── TEMP: Auto-login with test user for UI dev/testing ───────────────────
  // Skips login on dashboard/app routes. Landing page (/) is always public.
  // Remove this block once the real login + backend are wired up.
  const route = useRoute()
  const publicRoutes = ['/', '/login', '/signup', '/onboarding']
  const isPublicRoute = publicRoutes.some(r => route.path === r || route.path.startsWith('/onboarding'))

  if (!authStore.isAuthenticated && !isPublicRoute) {
    authStore.setSession(
      {
        id:        'test-user-001',
        name:      'Alex Demo',
        email:     'alex@autodm.dev',
        plan:      'pro' as any,
        createdAt: new Date().toISOString(),
      },
      {
        accessToken:  'mock-access-token',
        refreshToken: 'mock-refresh-token',
      }
    )
  }
})
