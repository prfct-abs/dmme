// server/routes/api/v1/[...path].ts
// Production proxy: forwards ALL /api/v1/** requests to FastAPI.
// In dev mode this is handled by nitro.devProxy; in production (Docker)
// this Nitro route takes over and does the same thing.
import { proxyRequest } from 'h3'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const target = `${config.fastapiBaseUrl}${event.path}`
  return proxyRequest(event, target, {
    fetchOptions: { redirect: 'manual' }, // keep OAuth 302 redirects intact
  })
})
