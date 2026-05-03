<template>
  <div class="trigger-builder">
    <!-- Trigger type selector -->
    <div class="type-grid">
      <button
        v-for="t in triggerTypes"
        :key="t.value"
        class="type-btn"
        :class="{ active: local.type === t.value }"
        @click="local.type = t.value"
      >
        <Icon :name="t.icon" size="18" />
        <span>{{ t.label }}</span>
      </button>
    </div>

    <!-- Keyword config -->
    <div v-if="local.type === 'comment_keyword' || local.type === 'dm_keyword'" class="config-block">
      <label>Trigger Keywords <span class="hint">(comma-separated)</span></label>
      <input
        v-model="keywordsRaw"
        placeholder="FREE, GUIDE, LINK"
        @blur="local.keywords = keywordsRaw.split(',').map(k => k.trim()).filter(Boolean)"
      />
      <div class="keyword-chips">
        <span v-for="kw in local.keywords" :key="kw" class="kw-chip">{{ kw }}</span>
      </div>
    </div>

    <!-- Story reply config -->
    <div v-if="local.type === 'story_reply'" class="config-block">
      <label>Story ID <span class="hint">(or leave blank for any story)</span></label>
      <input v-model="local.replyTo" placeholder="18012345678 or any" />
    </div>

    <div class="info-box">
      <Icon name="lucide:info" size="14" />
      {{ triggerDescription }}
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TriggerType, TriggerConfig } from '~/types'

const props = defineProps<{ modelValue: Partial<TriggerConfig> }>()
const emit  = defineEmits<{ 'update:modelValue': [v: TriggerConfig] }>()

const local = reactive<TriggerConfig>({
  type: (props.modelValue.type as TriggerType) ?? 'comment_keyword',
  keywords: props.modelValue.keywords ?? [],
  replyTo:  props.modelValue.replyTo,
})

const keywordsRaw = ref(local.keywords?.join(', ') ?? '')

watch(local, (v) => emit('update:modelValue', { ...v }), { deep: true })

const triggerTypes = [
  { value: 'comment_keyword', label: 'Comment',     icon: 'lucide:message-circle' },
  { value: 'story_reply',     label: 'Story Reply', icon: 'lucide:image'          },
  { value: 'new_follower',    label: 'New Follower', icon: 'lucide:user-plus'     },
  { value: 'dm_keyword',     label: 'DM Keyword',  icon: 'lucide:mail'           },
] as const

const triggerDescription = computed(() => {
  if (local.type === 'comment_keyword')
    return `DM is sent when someone comments one of your keywords on a post.`
  if (local.type === 'story_reply')
    return `DM is sent when someone replies to your story.`
  if (local.type === 'new_follower')
    return `DM is sent automatically when someone follows you.`
  if (local.type === 'dm_keyword')
    return `DM is sent when someone messages you with a matching keyword.`
  return ''
})
</script>

<style scoped>
.trigger-builder { display: flex; flex-direction: column; gap: 1rem; }

.type-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; }
.type-btn {
  display: flex; flex-direction: column; align-items: center; gap: 0.375rem;
  padding: 0.875rem; border-radius: 10px;
  background: var(--color-surface-2); border: 1px solid var(--color-border);
  color: var(--color-text-muted); font-size: 0.8rem; font-weight: 500;
  cursor: pointer; transition: all 0.15s;
}
.type-btn:hover { border-color: var(--color-brand); color: var(--color-text); }
.type-btn.active { background: rgba(108,99,255,0.12); border-color: var(--color-brand); color: var(--color-brand-light); }

.config-block { display: flex; flex-direction: column; gap: 0.5rem; }
.config-block label { font-size: 0.8rem; font-weight: 500; color: var(--color-text-muted); }
.hint { font-weight: 400; opacity: 0.7; }
.config-block input {
  background: var(--color-surface-2); border: 1px solid var(--color-border);
  border-radius: 8px; padding: 0.5rem 0.75rem;
  color: var(--color-text); font-size: 0.85rem; outline: none;
  transition: border-color 0.15s;
}
.config-block input:focus { border-color: var(--color-brand); }
.keyword-chips { display: flex; flex-wrap: wrap; gap: 0.375rem; }
.kw-chip { background: rgba(108,99,255,0.12); color: var(--color-brand-light); border-radius: 99px; padding: 0.15rem 0.625rem; font-size: 0.75rem; font-weight: 600; }

.info-box {
  display: flex; align-items: flex-start; gap: 0.5rem;
  background: rgba(108,99,255,0.06); border: 1px solid rgba(108,99,255,0.15);
  border-radius: 8px; padding: 0.625rem 0.875rem;
  font-size: 0.78rem; color: var(--color-text-muted); line-height: 1.5;
}
</style>
