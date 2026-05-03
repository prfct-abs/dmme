// ── Shared TypeScript interfaces across the Nuxt 3 app ──

export type Platform = 'instagram' | 'twitter' | 'linkedin'
export type CampaignStatus = 'active' | 'paused' | 'draft'
export type TriggerType = 'comment_keyword' | 'story_reply' | 'new_follower' | 'dm_keyword'
export type DmEventStatus = 'pending' | 'sent' | 'failed' | 'replied'
export type UserPlan = 'free' | 'pro' | 'business'

// ── Auth ────────────────────────────────────────────────
export interface User {
  id: string
  email: string
  name: string
  avatarUrl?: string
  plan: UserPlan
  createdAt: string
}

export interface AuthTokens {
  accessToken: string
  refreshToken: string
  expiresIn: number
}

// ── Social Accounts ─────────────────────────────────────
export interface SocialAccount {
  id: string
  platform: Platform
  platformUserId: string
  platformUsername: string
  avatarUrl?: string
  isActive: boolean
  tokenExpiresAt: string
}

// ── Campaigns ───────────────────────────────────────────
export interface TriggerConfig {
  type: TriggerType
  keywords?: string[]          // for comment_keyword / dm_keyword
  replyTo?: string             // for story_reply (story ID or 'any')
}

export interface MessageTemplate {
  body: string                 // Supports {{first_name}} placeholders
  mediaUrl?: string
  ctaUrl?: string
}

export interface Campaign {
  id: string
  name: string
  status: CampaignStatus
  platform: Platform
  socialAccountId: string
  triggerConfig: TriggerConfig
  messageTemplate: MessageTemplate
  dailyLimit: number
  sentToday: number
  totalSent: number
  createdAt: string
  updatedAt: string
}

export interface CreateCampaignPayload {
  name: string
  platform: Platform
  socialAccountId: string
  triggerConfig: TriggerConfig
  messageTemplate: MessageTemplate
  dailyLimit?: number
}

// ── Analytics ───────────────────────────────────────────
export interface DmEvent {
  id: string
  campaignId: string
  campaignName: string
  recipientPlatformId: string
  recipientUsername?: string
  status: DmEventStatus
  sentAt: string
  repliedAt?: string
}

export interface CampaignMetrics {
  campaignId: string
  totalSent: number
  totalReplied: number
  replyRate: number
  failureRate: number
  sentByDay: { date: string; count: number }[]
}

// ── API responses ────────────────────────────────────────
export interface ApiError {
  detail: string
  statusCode: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}
