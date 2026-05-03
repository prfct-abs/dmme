<template>
  <div class="campaign-card" @click="$emit('click')">
    <!-- Platform badge -->
    <div class="card-top">
      <div class="platform-chip" :style="{ background: color + '18', color }">
        <Icon :name="platformIcon" size="14" />
        {{ campaign.platform }}
      </div>
      <span class="status-dot-badge" :class="`dot--${campaign.status}`" />
    </div>

    <h3 class="card-name">{{ campaign.name }}</h3>

    <p class="card-trigger">
      <Icon name="lucide:zap" size="12" />
      {{ triggerLabel }}
    </p>

    <!-- Daily progress -->
    <div class="progress-section">
      <div class="progress-bar-bg">
        <div class="progress-bar-fill" :style="{ width: pct + '%' }" />
      </div>
      <span class="progress-label">{{ campaign.sentToday }}/{{ campaign.dailyLimit }} DMs</span>
    </div>

    <!-- Actions -->
    <div class="card-actions" @click.stop>
      <button
        class="action-btn"
        :class="campaign.status === 'active' ? 'btn-pause' : 'btn-play'"
        :title="campaign.status === 'active' ? 'Pause' : 'Activate'"
        @click="$emit('toggle')"
      >
        <Icon :name="campaign.status === 'active' ? 'lucide:pause' : 'lucide:play'" size="14" />
      </button>
      <NuxtLink :to="`/campaigns/${campaign.id}`" class="action-btn btn-edit" title="Edit">
        <Icon name="lucide:pencil" size="14" />
      </NuxtLink>
      <button class="action-btn btn-delete" title="Delete" @click="$emit('delete')">
        <Icon name="lucide:trash-2" size="14" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Campaign } from '~/types'

const props = defineProps<{ campaign: Campaign }>()
defineEmits<{ click: []; toggle: []; delete: [] }>()

const platformColors: Record<string, string> = {
  instagram: '#E1306C', twitter: '#1DA1F2', linkedin: '#0A66C2',
}
const color       = computed(() => platformColors[props.campaign.platform] ?? '#6C63FF')
const platformIcon = computed(() =>
  props.campaign.platform === 'instagram' ? 'mdi:instagram'
  : props.campaign.platform === 'twitter' ? 'mdi:twitter'
  : 'mdi:linkedin'
)

const triggerLabel = computed(() => {
  const t = props.campaign.triggerConfig
  if (t.type === 'comment_keyword') return `Comment: ${(t.keywords ?? []).join(', ')}`
  if (t.type === 'story_reply')     return 'Story Reply'
  if (t.type === 'new_follower')    return 'New Follower'
  return t.type
})

const pct = computed(() =>
  Math.min(100, Math.round((props.campaign.sentToday / props.campaign.dailyLimit) * 100))
)
</script>

<style scoped>
.campaign-card {
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius); padding: 1.25rem;
  cursor: pointer; transition: all 0.18s;
  display: flex; flex-direction: column; gap: 0.75rem;
}
.campaign-card:hover { border-color: rgba(108,99,255,0.35); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }

.card-top { display: flex; justify-content: space-between; align-items: center; }
.platform-chip { display: inline-flex; align-items: center; gap: 0.3rem; border-radius: 99px; padding: 0.2rem 0.625rem; font-size: 0.72rem; font-weight: 600; text-transform: capitalize; }
.status-dot-badge { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.dot--active { background: var(--color-success); box-shadow: 0 0 6px var(--color-success); }
.dot--paused { background: var(--color-warning); }
.dot--draft  { background: var(--color-text-muted); }

.card-name    { font-size: 0.95rem; font-weight: 600; line-height: 1.3; }
.card-trigger { display: flex; align-items: center; gap: 0.3rem; font-size: 0.77rem; color: var(--color-text-muted); }

.progress-section { display: flex; flex-direction: column; gap: 0.25rem; }
.progress-bar-bg   { height: 4px; background: var(--color-surface-2); border-radius: 99px; overflow: hidden; }
.progress-bar-fill { height: 100%; background: var(--color-brand); border-radius: 99px; transition: width 0.4s; }
.progress-label    { font-size: 0.72rem; color: var(--color-text-muted); }

.card-actions { display: flex; gap: 0.5rem; }
.action-btn {
  display: inline-flex; align-items: center; justify-content: center;
  width: 30px; height: 30px; border-radius: 7px;
  border: 1px solid var(--color-border); background: none;
  cursor: pointer; text-decoration: none; transition: all 0.15s;
  color: var(--color-text-muted);
}
.action-btn:hover { background: var(--color-surface-2); }
.btn-pause:hover  { border-color: var(--color-warning); color: var(--color-warning); }
.btn-play:hover   { border-color: var(--color-success); color: var(--color-success); }
.btn-edit:hover   { border-color: var(--color-brand);   color: var(--color-brand-light); }
.btn-delete:hover { border-color: var(--color-error);   color: var(--color-error); background: rgba(239,68,68,0.08); }
</style>
