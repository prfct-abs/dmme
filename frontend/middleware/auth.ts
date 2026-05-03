// middleware/auth.ts
// Route middleware — redirects to /login if user is not authenticated.
export default defineNuxtRouteMiddleware(() => {
  const authStore = useAuthStore()
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
})
