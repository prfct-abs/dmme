<template>
  <div class="templates-page">
    <div class="page-top">
      <button id="btn-new-template" class="btn-primary" @click="startNew">
        <Icon name="lucide:plus" size="16" /> New Template
      </button>
    </div>

    <!-- Editor panel (create/edit) -->
    <div v-if="editing" class="editor-card">
      <h2 class="editor-title">{{ editing.id ? 'Edit Template' : 'New Template' }}</h2>
      <div class="field">
        <label>Template Name</label>
        <input v-model="editing.name" placeholder="e.g. Instagram Comment Reply" />
      </div>
      <div class="field">
        <label>Message Body</label>
        <textarea v-model="editing.body" rows="5" placeholder="Hey {{first_name}}, thanks for commenting! Here's the link you asked for: {{link}}" />
        <p class="field-hint">Use <code>&#123;&#123;first_name&#125;&#125;</code>, <code>&#123;&#123;link&#125;&#125;</code>, <code>&#123;&#123;username&#125;&#125;</code> as variables.</p>
      </div>
      <div class="editor-actions">
        <button class="btn-ghost" @click="editing = null">Cancel</button>
        <button class="btn-primary" @click="saveTemplate">Save Template</button>
      </div>
    </div>

    <!-- Template list -->
    <div v-if="templates.length === 0 && !editing" class="empty-state">
      <Icon name="lucide:file-text" size="32" />
      <p>No templates yet. Create one to reuse across campaigns.</p>
    </div>

    <div class="templates-grid">
      <div
        v-for="tpl in templates"
        :key="tpl.id"
        class="template-card"
        @click="editTemplate(tpl)"
      >
        <div class="tpl-header">
          <p class="tpl-name">{{ tpl.name }}</p>
          <button class="tpl-delete" @click.stop="deleteTemplate(tpl.id)">
            <Icon name="lucide:trash-2" size="14" />
          </button>
        </div>
        <p class="tpl-body">{{ tpl.body }}</p>
        <div class="tpl-vars">
          <span v-for="v in extractVars(tpl.body)" :key="v" class="tpl-var-chip">&#123;&#123; {{ v }} &#125;&#125;</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

interface Template { id: string; name: string; body: string }

// Local state (would be backed by API in production)
const templates = ref<Template[]>([
  { id: '1', name: 'Comment Reply', body: 'Hey {{first_name}}! Thanks for your interest — here\'s the link: {{link}} 🎉' },
  { id: '2', name: 'New Follower Welcome', body: 'Welcome to my community, {{first_name}}! 🙌 So glad you\'re here. DM me "START" to get my free guide.' },
])

const editing = ref<Partial<Template> | null>(null)

function startNew() { editing.value = { name: '', body: '' } }
function editTemplate(tpl: Template) { editing.value = { ...tpl } }
function saveTemplate() {
  if (!editing.value?.name || !editing.value?.body) return
  if (editing.value.id) {
    const i = templates.value.findIndex(t => t.id === editing.value!.id)
    if (i > -1) templates.value[i] = editing.value as Template
  } else {
    templates.value.unshift({ id: Date.now().toString(), name: editing.value.name!, body: editing.value.body! })
  }
  editing.value = null
}
function deleteTemplate(id: string) {
  if (!confirm('Delete this template?')) return
  templates.value = templates.value.filter(t => t.id !== id)
}
function extractVars(body: string): string[] {
  return [...new Set([...body.matchAll(/\{\{(\w+)\}\}/g)].map(m => m[1]))]
}
</script>

<style scoped>
.templates-page { display: flex; flex-direction: column; gap: 1.5rem; }
.page-top { display: flex; justify-content: flex-end; }

.btn-primary {
  display: inline-flex; align-items: center; gap: 0.375rem;
  background: var(--color-brand); color: #fff; border: none; border-radius: 8px;
  padding: 0.5rem 1rem; font-size: 0.875rem; font-weight: 600; cursor: pointer;
  transition: background 0.15s;
}
.btn-primary:hover { background: var(--color-brand-dark); }

.editor-card {
  background: var(--color-surface); border: 1px solid var(--color-brand);
  border-radius: var(--radius); padding: 1.5rem;
  display: flex; flex-direction: column; gap: 1rem;
}
.editor-title { font-size: 1rem; font-weight: 600; }
.field { display: flex; flex-direction: column; gap: 0.375rem; }
.field label { font-size: 0.8rem; font-weight: 500; color: var(--color-text-muted); }
.field input, .field textarea {
  background: var(--color-surface-2); border: 1px solid var(--color-border);
  border-radius: 8px; padding: 0.625rem 0.875rem;
  color: var(--color-text); font-size: 0.875rem; outline: none; resize: vertical;
  font-family: inherit; transition: border-color 0.15s;
}
.field input:focus, .field textarea:focus { border-color: var(--color-brand); }
.field-hint { font-size: 0.75rem; color: var(--color-text-muted); }
.field-hint code { background: var(--color-surface); border-radius: 4px; padding: 0.1rem 0.3rem; font-size: 0.72rem; color: var(--color-brand-light); }
.editor-actions { display: flex; justify-content: flex-end; gap: 0.75rem; }
.btn-ghost {
  background: none; border: 1px solid var(--color-border); border-radius: 8px;
  padding: 0.5rem 1rem; color: var(--color-text-muted); font-size: 0.875rem;
  cursor: pointer; transition: all 0.15s;
}
.btn-ghost:hover { border-color: var(--color-text-muted); color: var(--color-text); }

.empty-state { text-align: center; padding: 4rem; color: var(--color-text-muted); display: flex; flex-direction: column; align-items: center; gap: 0.625rem; font-size: 0.875rem; }

.templates-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
.template-card {
  background: var(--color-surface); border: 1px solid var(--color-border);
  border-radius: var(--radius); padding: 1.25rem;
  cursor: pointer; transition: all 0.15s; display: flex; flex-direction: column; gap: 0.625rem;
}
.template-card:hover { border-color: rgba(108,99,255,0.4); transform: translateY(-1px); }
.tpl-header { display: flex; justify-content: space-between; align-items: center; }
.tpl-name   { font-size: 0.9rem; font-weight: 600; }
.tpl-delete { background: none; border: none; cursor: pointer; color: var(--color-text-muted); padding: 0.25rem; border-radius: 6px; transition: all 0.15s; }
.tpl-delete:hover { color: var(--color-error); background: rgba(239,68,68,0.1); }
.tpl-body  { font-size: 0.8rem; color: var(--color-text-muted); display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.5; }
.tpl-vars  { display: flex; flex-wrap: wrap; gap: 0.375rem; }
.tpl-var-chip { background: rgba(108,99,255,0.1); color: var(--color-brand-light); border-radius: 99px; padding: 0.1rem 0.5rem; font-size: 0.7rem; font-weight: 500; }
</style>
