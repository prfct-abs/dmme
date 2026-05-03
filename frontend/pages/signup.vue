<template>
  <div>
    <!-- Selected plan badge -->
    <div v-if="selectedPlan" class="plan-badge" :class="`badge--${selectedPlan.key}`">
      <Icon name="lucide:zap" size="13" />
      {{ selectedPlan.name }} plan selected
      <span class="plan-price">{{ selectedPlan.price === 0 ? 'Free' : `$${selectedPlan.price}/mo` }}</span>
    </div>

    <h2 class="page-heading">Create your account</h2>
    <p class="page-sub">
      {{ selectedPlan?.key === 'business' ? 'Tell us about yourself and we\'ll be in touch.' : 'Start automating your DMs in minutes — free forever.' }}
    </p>

    <form class="signup-form" @submit.prevent="handleSignup">
      <div class="field">
        <label for="name">Full Name</label>
        <input id="name" v-model="form.name" type="text" placeholder="Alex Johnson" required autocomplete="name" />
      </div>
      <div class="field">
        <label for="email">Email</label>
        <input id="email" v-model="form.email" type="email" placeholder="you@example.com" required autocomplete="email" />
      </div>
      <div v-if="selectedPlan?.key !== 'business'" class="field">
        <label for="password">Password</label>
        <input id="password" v-model="form.password" type="password" placeholder="••••••••" required minlength="8" autocomplete="new-password" />
        <span class="field-hint">Minimum 8 characters</span>
      </div>

      <p v-if="error" class="error-msg">{{ error }}</p>

      <button id="btn-signup" type="submit" class="btn-submit" :disabled="loading">
        <span v-if="loading" class="spinner" />
        <span v-else>{{ selectedPlan?.key === 'business' ? 'Request a Demo →' : 'Create Account →' }}</span>
      </button>
    </form>

    <p class="switch-link">
      Already have an account? <NuxtLink to="/login">Sign in</NuxtLink>
    </p>
    <p class="terms">
      By signing up you agree to our <a href="#">Terms</a> and <a href="#">Privacy Policy</a>.
    </p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'auth' })

const authStore = useAuthStore()
const route     = useRoute()

if (authStore.isAuthenticated) await navigateTo('/dashboard')

// Read plan from query param
const PLANS = {
  free:     { key: 'free',     name: 'Free',     price: 0  },
  pro:      { key: 'pro',      name: 'Pro',       price: 29 },
  business: { key: 'business', name: 'Business',  price: 79 },
}
const selectedPlan = computed(() => {
  const key = route.query.plan as string
  return key && key in PLANS ? PLANS[key as keyof typeof PLANS] : null
})

const form    = reactive({ name: '', email: '', password: '' })
const loading = ref(false)
const error   = ref('')

async function handleSignup() {
  loading.value = true
  error.value   = ''
  try {
    const { data, error: err } = await useFetch<{ user: any; tokens: any }>('/api/v1/auth/register', {
      method: 'POST',
      body: { name: form.name, email: form.email, password: form.password, plan: selectedPlan.value?.key ?? 'free' },
    })
    if (err.value) throw err.value
    authStore.setSession(data.value!.user, data.value!.tokens)
    await navigateTo('/onboarding')
  }
  catch (e: any) {
    error.value = e?.data?.detail ?? 'Sign up failed. Please try again.'
  }
  finally { loading.value = false }
}
</script>

<style scoped>
/* Plan badge */
.plan-badge {
  display: flex; align-items: center; gap: 0.375rem;
  border-radius: 8px; padding: 0.5rem 0.875rem;
  font-size: 0.78rem; font-weight: 600; margin-bottom: 1.5rem;
  border: 1px solid;
}
.badge--free     { background: rgba(108,99,255,0.1); border-color: rgba(108,99,255,0.25); color: var(--color-brand-light); }
.badge--pro      { background: rgba(245,158,11,0.1); border-color: rgba(245,158,11,0.25); color: #F59E0B; }
.badge--business { background: rgba(34,197,94,0.1);  border-color: rgba(34,197,94,0.25);  color: var(--color-success); }
.plan-price { margin-left: auto; opacity: 0.8; }

.page-heading { font-size: 1.5rem; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 0.25rem; }
.page-sub     { font-size: 0.875rem; color: var(--color-text-muted); margin-bottom: 2rem; }

.signup-form { display: flex; flex-direction: column; gap: 1rem; }
.field       { display: flex; flex-direction: column; gap: 0.375rem; }
.field label { font-size: 0.8rem; font-weight: 500; color: var(--color-text-muted); }
.field input {
  background: var(--color-surface-2); border: 1px solid var(--color-border);
  border-radius: 8px; padding: 0.625rem 0.875rem;
  color: var(--color-text); font-size: 0.9rem; outline: none;
  transition: border-color 0.15s; width: 100%;
}
.field input:focus { border-color: var(--color-brand); }
.field-hint { font-size: 0.72rem; color: var(--color-text-muted); }
.error-msg  { font-size: 0.8rem; color: var(--color-error); background: rgba(239,68,68,0.08); padding: 0.5rem 0.75rem; border-radius: 6px; }

.btn-submit {
  margin-top: 0.5rem; background: var(--color-brand); color: #fff;
  border: none; border-radius: 8px; padding: 0.7rem;
  font-size: 0.9rem; font-weight: 600; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.15s, box-shadow 0.15s;
}
.btn-submit:hover:not(:disabled) { background: var(--color-brand-dark); box-shadow: 0 0 24px rgba(108,99,255,0.3); }
.btn-submit:disabled { opacity: 0.5; cursor: not-allowed; }
.spinner { width: 16px; height: 16px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.3); border-top-color: #fff; animation: spin 0.6s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.switch-link { text-align: center; font-size: 0.85rem; color: var(--color-text-muted); margin-top: 1.25rem; }
.switch-link a { color: var(--color-brand-light); text-decoration: none; font-weight: 600; }
.terms { text-align: center; font-size: 0.72rem; color: var(--color-text-muted); margin-top: 0.75rem; }
.terms a { color: var(--color-text-muted); text-decoration: underline; }
</style>
