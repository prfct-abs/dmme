<template>
  <div class="onboarding-page">

    <!-- Progress header -->
    <div class="ob-header">
      <div class="ob-brand">
        <Icon name="lucide:zap" size="20" />
        <span>AutoDM</span>
      </div>
      <div class="ob-steps">
        <div class="ob-step done"><Icon name="lucide:check" size="13" /> Account</div>
        <div class="ob-step-line" />
        <div class="ob-step active"><span class="ob-dot" /> Connect</div>
        <div class="ob-step-line" />
        <div class="ob-step">Dashboard</div>
      </div>
    </div>

    <!-- Main content -->
    <div class="ob-body">
      <div class="ob-card">
        <h1 class="ob-title">Connect your social accounts</h1>
        <p class="ob-sub">
          Connect at least one platform to start automating DMs.
          You can always add more from the dashboard.
        </p>

        <!-- Platform connect list -->
        <div class="platform-list">
          <div
            v-for="p in platforms"
            :key="p.id"
            class="platform-row"
            :class="{ connected: connectedIds.includes(p.id) }"
          >
            <div class="plat-left">
              <div class="plat-icon" :style="{ background: p.color + '18', color: p.color }">
                <Icon :name="p.icon" size="22" />
              </div>
              <div>
                <p class="plat-name">{{ p.name }}</p>
                <p class="plat-desc">{{ p.desc }}</p>
              </div>
            </div>
            <button
              class="connect-btn"
              :class="connectedIds.includes(p.id) ? 'connected-btn' : 'connect-btn-outline'"
              :style="!connectedIds.includes(p.id) ? { '--btn-color': p.color } : {}"
              @click="handleConnect(p.id)"
            >
              <Icon :name="connectedIds.includes(p.id) ? 'lucide:check' : 'lucide:plus'" size="15" />
              {{ connectedIds.includes(p.id) ? 'Connected' : 'Connect' }}
            </button>
          </div>
        </div>

        <!-- More platforms coming soon -->
        <p class="coming-soon">
          <Icon name="lucide:clock" size="14" />
          TikTok, Facebook, and YouTube coming soon
        </p>

        <!-- CTA -->
        <div class="ob-actions">
          <button
            id="btn-go-dashboard"
            class="btn-continue"
            :disabled="connectedIds.length === 0"
            @click="goToDashboard"
          >
            {{ connectedIds.length > 0 ? 'Continue to Dashboard →' : 'Connect at least one account' }}
          </button>
          <button class="btn-skip" @click="goToDashboard">Skip for now</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false, middleware: 'auth' })

const config       = useRuntimeConfig()
const connectedIds = ref<string[]>([])

const platforms = [
  { id: 'instagram', name: 'Instagram',   icon: 'mdi:instagram', color: '#E1306C', desc: 'Comment → DM, story replies, new followers' },
  { id: 'twitter',   name: 'X (Twitter)', icon: 'mdi:twitter',   color: '#1DA1F2', desc: 'DM keyword triggers, automated replies'      },
  { id: 'linkedin',  name: 'LinkedIn',    icon: 'mdi:linkedin',  color: '#0A66C2', desc: 'Connection request DMs, message automation'  },
]

function handleConnect(platformId: string) {
  if (connectedIds.value.includes(platformId)) return
  // In dev/mock mode — just mark as connected locally
  // In production — redirect to OAuth flow:
  // window.location.href = `${config.public.apiBaseUrl}/api/v1/auth/oauth/${platformId}`
  connectedIds.value.push(platformId)
}

async function goToDashboard() {
  await navigateTo('/dashboard')
}
</script>

<style scoped>
.onboarding-page { min-height: 100vh; background: var(--color-bg); display: flex; flex-direction: column; }

/* Header */
.ob-header { display: flex; align-items: center; justify-content: space-between; padding: 1.25rem 2rem; border-bottom: 1px solid var(--color-border); }
.ob-brand  { display: flex; align-items: center; gap: 0.5rem; font-weight: 700; color: var(--color-brand); font-size: 1rem; }
.ob-steps  { display: flex; align-items: center; gap: 0.5rem; font-size: 0.78rem; }
.ob-step   { display: flex; align-items: center; gap: 0.3rem; color: var(--color-text-muted); font-weight: 500; }
.ob-step.done   { color: var(--color-success); }
.ob-step.active { color: var(--color-text); }
.ob-step-line   { width: 32px; height: 1px; background: var(--color-border); }
.ob-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--color-brand); box-shadow: 0 0 8px var(--color-brand); }

/* Body */
.ob-body { flex: 1; display: grid; place-items: center; padding: 3rem 1rem; }
.ob-card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 20px; padding: 2.5rem; width: 100%; max-width: 560px; }
.ob-title { font-size: 1.5rem; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 0.5rem; }
.ob-sub   { font-size: 0.875rem; color: var(--color-text-muted); line-height: 1.6; margin-bottom: 2rem; }

/* Platform list */
.platform-list { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1rem; }
.platform-row  {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1rem 1.25rem; border-radius: 12px;
  border: 1px solid var(--color-border); background: var(--color-surface-2);
  transition: border-color 0.2s;
}
.platform-row.connected { border-color: rgba(34,197,94,0.3); background: rgba(34,197,94,0.04); }
.plat-left { display: flex; align-items: center; gap: 0.875rem; }
.plat-icon { width: 42px; height: 42px; border-radius: 10px; display: grid; place-items: center; flex-shrink: 0; }
.plat-name { font-size: 0.9rem; font-weight: 600; }
.plat-desc { font-size: 0.75rem; color: var(--color-text-muted); margin-top: 2px; }

.connect-btn        { display: flex; align-items: center; gap: 0.375rem; border-radius: 8px; padding: 0.45rem 1rem; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.15s; border: 1px solid var(--btn-color, var(--color-border)); color: var(--btn-color, var(--color-text)); background: transparent; }
.connect-btn:hover  { background: rgba(255,255,255,0.04); }
.connected-btn      { border-color: var(--color-success); color: var(--color-success); background: rgba(34,197,94,0.08); cursor: default; }

.coming-soon { display: flex; align-items: center; gap: 0.375rem; font-size: 0.75rem; color: var(--color-text-muted); margin: 0.75rem 0 1.75rem; }

/* Actions */
.ob-actions   { display: flex; flex-direction: column; gap: 0.75rem; }
.btn-continue {
  background: var(--color-brand); color: #fff; border: none; border-radius: 10px;
  padding: 0.875rem; font-size: 0.9rem; font-weight: 600; cursor: pointer;
  transition: all 0.15s; width: 100%;
}
.btn-continue:hover:not(:disabled) { background: var(--color-brand-dark); box-shadow: 0 0 24px rgba(108,99,255,0.3); }
.btn-continue:disabled { opacity: 0.4; cursor: not-allowed; }
.btn-skip { background: none; border: none; color: var(--color-text-muted); font-size: 0.85rem; cursor: pointer; text-align: center; padding: 0.25rem; transition: color 0.15s; }
.btn-skip:hover { color: var(--color-text); }
</style>
