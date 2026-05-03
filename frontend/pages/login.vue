<template>
  <div>
    <h2 class="page-heading">Welcome back</h2>
    <p class="page-sub">Sign in to your AutoDM account</p>

    <form class="login-form" @submit.prevent="handleLogin">
      <div class="field">
        <label for="email">Email</label>
        <input id="email" v-model="form.email" type="email" placeholder="you@example.com" required autocomplete="email" />
      </div>
      <div class="field">
        <label for="password">Password</label>
        <input id="password" v-model="form.password" type="password" placeholder="••••••••" required autocomplete="current-password" />
      </div>

      <p v-if="error" class="error-msg">{{ error }}</p>

      <button id="btn-login" type="submit" class="btn-submit" :disabled="loading">
        <span v-if="loading" class="spinner" />
        <span v-else>Sign In</span>
      </button>
    </form>

    <div class="divider"><span>or continue with</span></div>

    <div class="oauth-row">
      <button id="btn-oauth-instagram" class="oauth-btn" @click="connectOAuth('instagram')">
        <Icon name="mdi:instagram" size="18" /> Instagram
      </button>
      <button id="btn-oauth-twitter" class="oauth-btn" @click="connectOAuth('twitter')">
        <Icon name="mdi:twitter" size="18" /> X (Twitter)
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const authStore = useAuthStore()
const config    = useRuntimeConfig()

// Redirect if already logged in
if (authStore.isAuthenticated) await navigateTo('/dashboard')

const form    = reactive({ email: '', password: '' })
const loading = ref(false)
const error   = ref('')

async function handleLogin() {
  loading.value = true
  error.value   = ''
  try {
    await authStore.login(form.email, form.password)
  }
  catch (e: any) {
    error.value = e?.data?.detail ?? 'Login failed. Please try again.'
  }
  finally { loading.value = false }
}

// Redirect directly to FastAPI — OAuth flow must go to the real backend, 
// not through the Nuxt BFF (devProxy only works in `nuxt dev` mode).
function connectOAuth(platform: string) {
  window.location.href = `${config.public.apiBaseUrl}/api/v1/auth/oauth/${platform}`
}
</script>

<style scoped>
.page-heading { font-size: 1.5rem; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 0.25rem; }
.page-sub     { font-size: 0.875rem; color: var(--color-text-muted); margin-bottom: 2rem; }

.login-form   { display: flex; flex-direction: column; gap: 1rem; }

.field        { display: flex; flex-direction: column; gap: 0.375rem; }
.field label  { font-size: 0.8rem; font-weight: 500; color: var(--color-text-muted); }
.field input  {
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 0.625rem 0.875rem;
  color: var(--color-text);
  font-size: 0.9rem;
  transition: border-color 0.15s;
  outline: none;
  width: 100%;
}
.field input:focus { border-color: var(--color-brand); }

.error-msg { font-size: 0.8rem; color: var(--color-error); background: rgba(239,68,68,0.08); padding: 0.5rem 0.75rem; border-radius: 6px; }

.btn-submit {
  margin-top: 0.5rem;
  background: var(--color-brand); color: #fff;
  border: none; border-radius: 8px;
  padding: 0.7rem;
  font-size: 0.9rem; font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, box-shadow 0.15s;
  display: flex; align-items: center; justify-content: center;
}
.btn-submit:hover:not(:disabled) { background: var(--color-brand-dark); box-shadow: 0 0 20px rgba(108,99,255,0.3); }
.btn-submit:disabled { opacity: 0.5; cursor: not-allowed; }

.spinner {
  width: 16px; height: 16px; border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  animation: spin 0.6s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.divider {
  text-align: center; position: relative;
  margin: 1.5rem 0;
  color: var(--color-text-muted); font-size: 0.75rem;
}
.divider::before {
  content: ''; position: absolute;
  top: 50%; left: 0; right: 0; height: 1px;
  background: var(--color-border);
}
.divider span { background: var(--color-surface); padding: 0 0.75rem; position: relative; }

.oauth-row { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
.oauth-btn {
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
  padding: 0.6rem; border-radius: 8px;
  background: var(--color-surface-2);
  border: 1px solid var(--color-border);
  color: var(--color-text); font-size: 0.85rem; font-weight: 500;
  cursor: pointer; transition: all 0.15s;
}
.oauth-btn:hover { border-color: var(--color-brand); color: var(--color-brand-light); }
</style>
