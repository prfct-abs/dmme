// stores/notif.store.ts
import { defineStore } from 'pinia'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface Toast {
  id: string
  message: string
  type: ToastType
  duration: number
}

export const useNotifStore = defineStore('notif', {
  state: () => ({
    toasts: [] as Toast[],
  }),

  actions: {
    addToast(message: string, type: ToastType = 'info', duration = 4000) {
      const id = `${Date.now()}-${Math.random()}`
      this.toasts.push({ id, message, type, duration })
      setTimeout(() => this.removeToast(id), duration)
    },

    removeToast(id: string) {
      this.toasts = this.toasts.filter(t => t.id !== id)
    },

    success(message: string) { this.addToast(message, 'success') },
    error(message: string)   { this.addToast(message, 'error') },
    warning(message: string) { this.addToast(message, 'warning') },
    info(message: string)    { this.addToast(message, 'info') },
  },
})
