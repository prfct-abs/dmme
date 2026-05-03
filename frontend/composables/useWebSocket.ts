// composables/useWebSocket.ts
// Manages a persistent WebSocket connection to the FastAPI /ws endpoint
// for real-time campaign status and DM delivery updates.

export type WsEventType = 'dm_sent' | 'dm_failed' | 'dm_replied' | 'campaign_status'

export interface WsMessage {
  type: WsEventType
  payload: Record<string, unknown>
}

type WsHandler = (msg: WsMessage) => void

export function useWebSocket() {
  const config = useRuntimeConfig()
  const authStore = useAuthStore()

  let socket: WebSocket | null = null
  const handlers = new Map<WsEventType, WsHandler[]>()
  const isConnected = ref(false)

  function connect() {
    if (socket?.readyState === WebSocket.OPEN) return
    const url = `${config.public.wsUrl}?token=${authStore.token}`
    socket = new WebSocket(url)

    socket.onopen = () => { isConnected.value = true }
    socket.onclose = () => {
      isConnected.value = false
      // Auto-reconnect after 3s if still authenticated
      if (authStore.isAuthenticated) setTimeout(connect, 3000)
    }
    socket.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data) as WsMessage
        handlers.get(msg.type)?.forEach(h => h(msg))
      }
      catch { /* ignore malformed messages */ }
    }
  }

  function disconnect() {
    socket?.close()
    socket = null
  }

  function on(type: WsEventType, handler: WsHandler) {
    if (!handlers.has(type)) handlers.set(type, [])
    handlers.get(type)!.push(handler)
  }

  function off(type: WsEventType, handler: WsHandler) {
    const list = handlers.get(type) ?? []
    handlers.set(type, list.filter(h => h !== handler))
  }

  // Auto-disconnect on component unmount
  onUnmounted(disconnect)

  return { connect, disconnect, on, off, isConnected: readonly(isConnected) }
}
