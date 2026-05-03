// composables/useErrorHandler.ts
// Centralised error → user-friendly toast mapper.

export function useErrorHandler() {
  const notif = useNotifStore()

  function handle(error: unknown, fallback = 'Something went wrong.') {
    if (!error) return
    if (error instanceof Error) {
      notif.addToast(error.message || fallback, 'error')
    }
    else if (typeof error === 'object' && error !== null && 'detail' in error) {
      notif.addToast((error as { detail: string }).detail, 'error')
    }
    else {
      notif.addToast(fallback, 'error')
    }
  }

  return { handle }
}
