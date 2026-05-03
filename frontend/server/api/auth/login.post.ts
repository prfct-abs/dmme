// server/api/auth/login.post.ts
import { defineEventHandler, readBody, createError } from 'h3'

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body   = await readBody(event)

  try {
    return await $fetch(`${config.fastapiBaseUrl}/api/v1/auth/login`, {
      method: 'POST',
      body,
      headers: { 'Content-Type': 'application/json' },
    })
  }
  catch (err: any) {
    throw createError({
      statusCode: err?.response?.status ?? 401,
      message: err?.data?.detail ?? 'Login failed',
    })
  }
})
