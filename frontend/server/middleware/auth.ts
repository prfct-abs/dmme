// server/middleware/auth.ts
// Protects only /api/* BFF routes EXCEPT /api/auth/**
// Must NOT run on page routes — Nitro renders pages server-side too.
//
// ⚠️  VS Code may show "cannot find h3" until you run:
//     cd frontend && npm install && npx nuxt prepare
// These errors are false-positives — h3 ships with Nitro.
import { defineEventHandler, getHeader, createError } from 'h3'
import type { H3Event } from 'h3'

export default defineEventHandler((event: H3Event) => {
  const url = event.path ?? ''

  // ── Only guard BFF API routes ────────────────────────────────────────────
  if (!url.startsWith('/api/')) return   // page routes — let them pass

  // ── Public API routes (no token required) ────────────────────────────────
  if (url.startsWith('/api/auth')) return

  // ── Protected API routes — require Bearer token ──────────────────────────
  const token = getHeader(event, 'authorization')
  if (!token?.startsWith('Bearer ')) {
    throw createError({ statusCode: 401, message: 'Missing or invalid token' })
  }
})
