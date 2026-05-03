// server/api/campaigns.get.ts
// Nitro BFF route — proxies GET /api/campaigns to FastAPI with server-side auth.

import { defineEventHandler, getQuery, getHeader, createError } from 'h3'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const query  = getQuery(event)
  const token  = getHeader(event, 'authorization')

  if (!token) throw createError({ statusCode: 401, message: 'Unauthorized' })

  const params = new URLSearchParams(query as Record<string, string>)
  const url    = `${config.fastapiBaseUrl}/api/v1/campaigns?${params}`

  const response = await $fetch(url, {
    headers: { Authorization: token },
  })

  return response
})
