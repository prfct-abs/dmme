<template>
  <div class="message-editor">
    <div class="field">
      <div class="label-row">
        <label>Message Body</label>
        <span class="char-count" :class="{ warn: charCount > 900 }">{{ charCount }}/1000</span>
      </div>
      <textarea
        v-model="local.body"
        rows="6"
        placeholder="Hey {{first_name}}, thanks for commenting! Here's the link you asked for 👇"
        maxlength="1000"
      />
    </div>

    <!-- Variable inserter -->
    <div class="var-row">
      <span class="var-label">Insert variable:</span>
      <button
        v-for="v in variables"
        :key="v"
        class="var-btn"
        @click="insertVar(v)"
      >
        {{ '{{'+ v +'}}' }}
      </button>
    </div>

    <!-- CTA URL -->
    <div class="field">
      <label>CTA Link <span class="optional">(optional)</span></label>
      <input v-model="local.ctaUrl" type="url" placeholder="https://example.com/offer" />
    </div>

    <!-- Preview -->
    <div class="preview-box">
      <p class="preview-label">Preview</p>
      <p class="preview-text">{{ preview }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { MessageTemplate } from '~/types'

const props = defineProps<{ modelValue: Partial<MessageTemplate> }>()
const emit  = defineEmits<{ 'update:modelValue': [v: MessageTemplate] }>()

const local = reactive<MessageTemplate>({
  body:     props.modelValue.body    ?? '',
  ctaUrl:   props.modelValue.ctaUrl  ?? '',
  mediaUrl: props.modelValue.mediaUrl ?? '',
})

watch(local, (v) => emit('update:modelValue', { ...v }), { deep: true })

const charCount = computed(() => local.body.length)

const variables = ['first_name', 'username', 'link', 'offer']

function insertVar(v: string) {
  local.body += `{{${v}}}`
}

const demoValues: Record<string, string> = {
  first_name: 'Alex', username: 'alex_dev', link: 'https://bit.ly/3xyz', offer: '50% OFF',
}

const preview = computed(() =>
  local.body.replace(/\{\{(\w+)\}\}/g, (_, k) => demoValues[k] ?? `{{${k}}}`)
)
</script>

<style scoped>
.message-editor { display: flex; flex-direction: column; gap: 1rem; }

.field { display: flex; flex-direction: column; gap: 0.4rem; }
.label-row { display: flex; justify-content: space-between; align-items: center; }
.field label { font-size: 0.8rem; font-weight: 500; color: var(--color-text-muted); }
.optional { font-weight: 400; opacity: 0.7; }
.char-count { font-size: 0.72rem; color: var(--color-text-muted); }
.char-count.warn { color: var(--color-warning); }

.field textarea, .field input {
  background: var(--color-surface-2); border: 1px solid var(--color-border);
  border-radius: 8px; padding: 0.625rem 0.875rem;
  color: var(--color-text); font-size: 0.875rem; font-family: inherit;
  outline: none; resize: vertical; transition: border-color 0.15s;
}
.field textarea:focus, .field input:focus { border-color: var(--color-brand); }

.var-row { display: flex; align-items: center; flex-wrap: wrap; gap: 0.375rem; }
.var-label { font-size: 0.75rem; color: var(--color-text-muted); margin-right: 0.25rem; }
.var-btn {
  background: rgba(108,99,255,0.1); color: var(--color-brand-light);
  border: 1px solid rgba(108,99,255,0.2); border-radius: 99px;
  padding: 0.15rem 0.625rem; font-size: 0.72rem; font-weight: 600;
  cursor: pointer; transition: all 0.15s;
}
.var-btn:hover { background: rgba(108,99,255,0.2); }

.preview-box {
  background: var(--color-surface-2); border: 1px dashed var(--color-border);
  border-radius: 8px; padding: 0.875rem;
}
.preview-label { font-size: 0.7rem; font-weight: 600; color: var(--color-text-muted); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
.preview-text  { font-size: 0.875rem; line-height: 1.6; color: var(--color-text); white-space: pre-wrap; }
</style>
