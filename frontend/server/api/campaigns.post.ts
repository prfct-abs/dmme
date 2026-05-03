// server/api/campaigns.post.ts
import { defineEventHandler, readBody, getHeader, createError } from 'h3'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const token  = getHeader(event, 'authorization')
  const body   = await readBody(event)

  if (!token) throw createError({ statusCode: 401, message: 'Unauthorized' })

  return $fetch(`${config.fastapiBaseUrl}/api/v1/campaigns`, {
    method: 'POST',
    body,
    headers: { Authorization: token, 'Content-Type': 'application/json' },
  })
})
