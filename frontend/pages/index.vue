<template>
  <div class="landing">

    <!-- ── Navbar ─────────────────────────────────────────────────────────── -->
    <nav class="navbar">
      <div class="nav-brand">
        <Icon name="lucide:zap" size="22" />
        <span>AutoDM</span>
      </div>
      <div class="nav-links">
        <a href="#features">Features</a>
        <a href="#how">How it works</a>
        <a href="#pricing">Pricing</a>
      </div>
      <div class="nav-cta">
        <NuxtLink to="/login"  class="btn-ghost-sm">Log in</NuxtLink>
        <NuxtLink to="/signup?plan=free" class="btn-primary-sm">Get Started Free →</NuxtLink>
      </div>
    </nav>

    <!-- ── Hero ──────────────────────────────────────────────────────────── -->
    <section class="hero">
      <div class="hero-pill">🚀 Trusted by 12,000+ creators & brands</div>
      <h1 class="hero-title">
        Turn every comment<br />
        into a <span class="gradient-text">paying customer</span>
      </h1>
      <p class="hero-sub">
        AutoDM automatically sends personalized DMs the moment someone comments,
        follows, or replies to your story — on Instagram, X, and LinkedIn.
      </p>
      <div class="hero-actions">
        <NuxtLink to="/signup?plan=free" class="btn-hero-primary" id="btn-hero-cta">
          Start for free — no credit card
        </NuxtLink>
        <a href="#how" class="btn-hero-ghost">See how it works ↓</a>
      </div>

      <!-- Floating platform badges -->
      <div class="platform-badges">
        <div class="badge"><Icon name="mdi:instagram" size="20" /> Instagram</div>
        <div class="badge"><Icon name="mdi:twitter"   size="20" /> X (Twitter)</div>
        <div class="badge"><Icon name="mdi:linkedin"  size="20" /> LinkedIn</div>
      </div>

      <!-- Dashboard preview -->
      <div class="hero-preview">
        <div class="preview-bar">
          <span class="dot red"/><span class="dot yellow"/><span class="dot green"/>
          <span class="preview-url">app.autodm.io/dashboard</span>
        </div>
        <div class="preview-body">
          <div class="preview-stat" v-for="s in previewStats" :key="s.label">
            <p class="ps-val">{{ s.val }}</p>
            <p class="ps-label">{{ s.label }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Features ──────────────────────────────────────────────────────── -->
    <section id="features" class="section">
      <div class="section-badge">Features</div>
      <h2 class="section-title">Everything you need to scale your DMs</h2>
      <div class="features-grid">
        <div class="feature-card" v-for="f in features" :key="f.title">
          <div class="feature-icon" :style="{ background: f.color + '18', color: f.color }">
            <Icon :name="f.icon" size="24" />
          </div>
          <h3>{{ f.title }}</h3>
          <p>{{ f.desc }}</p>
        </div>
      </div>
    </section>

    <!-- ── How it works ───────────────────────────────────────────────────── -->
    <section id="how" class="section section-alt">
      <div class="section-badge">How it works</div>
      <h2 class="section-title">Set up in 3 minutes</h2>
      <div class="steps">
        <div class="step" v-for="(s, i) in steps" :key="s.title">
          <div class="step-num">{{ i + 1 }}</div>
          <div class="step-content">
            <h3>{{ s.title }}</h3>
            <p>{{ s.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Social proof ───────────────────────────────────────────────────── -->
    <section class="section">
      <div class="section-badge">Testimonials</div>
      <h2 class="section-title">Loved by creators worldwide</h2>
      <div class="testimonials">
        <div class="testimonial" v-for="t in testimonials" :key="t.name">
          <p class="t-quote">"{{ t.quote }}"</p>
          <div class="t-author">
            <div class="t-avatar">{{ t.name[0] }}</div>
            <div>
              <p class="t-name">{{ t.name }}</p>
              <p class="t-role">{{ t.role }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Pricing ────────────────────────────────────────────────────────── -->
    <section id="pricing" class="section section-alt">
      <div class="section-badge">Pricing</div>
      <h2 class="section-title">Simple, transparent pricing</h2>
      <div class="pricing-grid">
        <div class="price-card" v-for="p in plans" :key="p.name" :class="{ featured: p.featured }">
          <div v-if="p.featured" class="popular-badge">Most Popular</div>
          <h3 class="plan-name">{{ p.name }}</h3>
          <p class="plan-price"><span class="price-num">${{ p.price }}</span>/mo</p>
          <ul class="plan-features">
            <li v-for="f in p.features" :key="f"><Icon name="lucide:check" size="14" /> {{ f }}</li>
          </ul>
          <NuxtLink :to="`/signup?plan=${p.planKey}`" class="plan-cta" :class="{ 'cta-primary': p.featured }">
            {{ p.cta }}
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- ── Footer ─────────────────────────────────────────────────────────── -->
    <footer class="footer">
      <div class="footer-brand">
        <Icon name="lucide:zap" size="18" />
        <span>AutoDM</span>
      </div>
      <p class="footer-copy">© 2026 AutoDM. All rights reserved.</p>
      <div class="footer-links">
        <a href="#">Privacy</a>
        <a href="#">Terms</a>
        <a href="#">Contact</a>
      </div>
    </footer>

  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false }) // full-width landing, no dashboard shell

useHead({ title: 'AutoDM — Automate Your Social DMs' })

const previewStats = [
  { val: '1,247', label: 'DMs Sent' },
  { val: '25%',   label: 'Reply Rate' },
  { val: '3',     label: 'Active Campaigns' },
  { val: '$0',    label: 'Ad Spend' },
]

const features = [
  { icon: 'lucide:message-circle', color: '#6C63FF', title: 'Comment → DM Automation', desc: 'Trigger a personalized DM the moment someone comments a keyword on your posts. Capture leads on autopilot, 24/7.' },
  { icon: 'lucide:zap',            color: '#22C55E', title: 'Smart Campaigns', desc: 'Build campaigns with daily limits, keyword filters, and multi-platform support. Stay safe from platform rate limits.' },
  { icon: 'lucide:sparkles',       color: '#F59E0B', title: 'AI Personalization', desc: 'Uses AI to tailor each DM with the recipient\'s name, context, and intent — so it never feels like spam.' },
  { icon: 'lucide:bar-chart-3',    color: '#E1306C', title: 'Real-Time Analytics', desc: 'Track sent, replied, and conversion rates across all campaigns in one live dashboard.' },
  { icon: 'lucide:link',           color: '#1DA1F2', title: 'Multi-Platform', desc: 'Connect Instagram, X (Twitter), and LinkedIn from a single account. More platforms coming soon.' },
  { icon: 'lucide:shield-check',   color: '#8B5CF6', title: 'Safe & Compliant', desc: 'Built-in daily send limits, randomized delays, and opt-out handling to protect your accounts.' },
]

const steps = [
  { title: 'Connect your accounts', desc: 'Link Instagram, X, or LinkedIn in one click with secure OAuth — takes under 30 seconds.' },
  { title: 'Set your trigger & message', desc: 'Choose what fires the DM (comment keyword, new follower, story reply) and write your message template.' },
  { title: 'Watch the DMs send', desc: 'AutoDM handles the rest. Monitor replies, track conversions, and scale your reach — automatically.' },
]

const testimonials = [
  { quote: 'I went from 50 leads/month to 400 using AutoDM. My comment funnel runs itself while I sleep.', name: 'Sarah Chen', role: 'Instagram Coach · 280K followers' },
  { quote: 'Best tool I\'ve found for converting followers into clients. The AI personalization is unreal.', name: 'Marcus Webb', role: 'Fitness Creator · LinkedIn' },
  { quote: 'Grew my email list by 3,000 subscribers in 6 weeks with zero ad spend. Worth every penny.', name: 'Priya Nair', role: 'Digital Marketer · X/Twitter' },
]

const plans = [
  {
    name: 'Free', price: 0, featured: false, cta: 'Get started free', planKey: 'free',
    features: ['1 connected account', '50 DMs/day', '1 active campaign', 'Basic analytics'],
  },
  {
    name: 'Pro', price: 29, featured: true, cta: 'Start free trial', planKey: 'pro',
    features: ['5 connected accounts', '500 DMs/day', 'Unlimited campaigns', 'AI personalization', 'Real-time analytics', 'Priority support'],
  },
  {
    name: 'Business', price: 79, featured: false, cta: 'Contact sales', planKey: 'business',
    features: ['Unlimited accounts', 'Unlimited DMs', 'Team members', 'API access', 'Custom integrations', 'Dedicated manager'],
  },
]
</script>

<style scoped>
.landing { background: var(--color-bg); color: var(--color-text); font-family: var(--font-sans); }

/* ── Navbar ── */
.navbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 1.25rem 4rem; border-bottom: 1px solid var(--color-border);
  position: sticky; top: 0; z-index: 100;
  background: rgba(14,14,22,0.8); backdrop-filter: blur(16px);
}
.nav-brand { display: flex; align-items: center; gap: 0.5rem; font-size: 1.1rem; font-weight: 700; color: var(--color-brand); }
.nav-links { display: flex; gap: 2rem; }
.nav-links a { color: var(--color-text-muted); text-decoration: none; font-size: 0.875rem; transition: color 0.15s; }
.nav-links a:hover { color: var(--color-text); }
.nav-cta { display: flex; gap: 0.75rem; align-items: center; }
.btn-ghost-sm { color: var(--color-text-muted); text-decoration: none; font-size: 0.875rem; transition: color 0.15s; }
.btn-ghost-sm:hover { color: var(--color-text); }
.btn-primary-sm { background: var(--color-brand); color: #fff; border-radius: 8px; padding: 0.45rem 1rem; font-size: 0.875rem; font-weight: 600; text-decoration: none; transition: background 0.15s; }
.btn-primary-sm:hover { background: var(--color-brand-dark); }

/* ── Hero ── */
.hero { text-align: center; padding: 6rem 2rem 4rem; display: flex; flex-direction: column; align-items: center; gap: 1.5rem; }
.hero-pill { background: rgba(108,99,255,0.12); border: 1px solid rgba(108,99,255,0.3); color: var(--color-brand-light); border-radius: 99px; padding: 0.35rem 1rem; font-size: 0.8rem; font-weight: 600; }
.hero-title { font-size: clamp(2.5rem, 6vw, 4rem); font-weight: 800; letter-spacing: -0.04em; line-height: 1.1; max-width: 820px; }
.gradient-text { background: linear-gradient(135deg, #6C63FF, #E1306C, #F59E0B); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.hero-sub { font-size: 1.1rem; color: var(--color-text-muted); max-width: 560px; line-height: 1.7; }
.hero-actions { display: flex; gap: 1rem; align-items: center; flex-wrap: wrap; justify-content: center; }
.btn-hero-primary { background: var(--color-brand); color: #fff; border-radius: 10px; padding: 0.875rem 2rem; font-size: 1rem; font-weight: 700; text-decoration: none; transition: all 0.2s; box-shadow: 0 0 40px rgba(108,99,255,0.3); }
.btn-hero-primary:hover { background: var(--color-brand-dark); box-shadow: 0 0 60px rgba(108,99,255,0.5); transform: translateY(-1px); }
.btn-hero-ghost { color: var(--color-text-muted); text-decoration: none; font-size: 0.9rem; transition: color 0.15s; }
.btn-hero-ghost:hover { color: var(--color-text); }

.platform-badges { display: flex; gap: 0.75rem; flex-wrap: wrap; justify-content: center; }
.badge { display: flex; align-items: center; gap: 0.4rem; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 99px; padding: 0.4rem 1rem; font-size: 0.8rem; font-weight: 500; color: var(--color-text-muted); }

/* Dashboard preview */
.hero-preview { width: 100%; max-width: 760px; background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 16px; overflow: hidden; box-shadow: 0 32px 80px rgba(0,0,0,0.5); margin-top: 1rem; }
.preview-bar { display: flex; align-items: center; gap: 0.5rem; padding: 0.625rem 1rem; background: var(--color-surface-2); border-bottom: 1px solid var(--color-border); }
.dot { width: 10px; height: 10px; border-radius: 50%; }
.dot.red { background: #FF5F57; } .dot.yellow { background: #FEBC2E; } .dot.green { background: #28C840; }
.preview-url { font-size: 0.72rem; color: var(--color-text-muted); margin-left: 0.5rem; }
.preview-body { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1px; background: var(--color-border); }
.preview-stat { background: var(--color-surface); padding: 1.5rem 1rem; text-align: center; }
.ps-val   { font-size: 1.75rem; font-weight: 700; letter-spacing: -0.04em; color: var(--color-brand-light); }
.ps-label { font-size: 0.72rem; color: var(--color-text-muted); margin-top: 4px; }

/* ── Sections ── */
.section     { padding: 6rem 4rem; max-width: 1200px; margin: 0 auto; }
.section-alt { background: var(--color-surface); border-radius: 24px; margin: 2rem auto; }
.section-badge { display: inline-block; background: rgba(108,99,255,0.12); border: 1px solid rgba(108,99,255,0.25); color: var(--color-brand-light); border-radius: 99px; padding: 0.3rem 0.875rem; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem; }
.section-title { font-size: clamp(1.75rem, 3vw, 2.5rem); font-weight: 700; letter-spacing: -0.03em; margin-bottom: 3rem; max-width: 560px; }

/* ── Features ── */
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; }
.feature-card { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 16px; padding: 1.75rem; transition: all 0.2s; }
.feature-card:hover { border-color: rgba(108,99,255,0.3); transform: translateY(-3px); box-shadow: 0 16px 40px rgba(0,0,0,0.3); }
.feature-icon { width: 48px; height: 48px; border-radius: 12px; display: grid; place-items: center; margin-bottom: 1rem; }
.feature-card h3 { font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem; }
.feature-card p  { font-size: 0.875rem; color: var(--color-text-muted); line-height: 1.6; }

/* ── Steps ── */
.steps { display: flex; flex-direction: column; gap: 2rem; max-width: 640px; }
.step { display: flex; gap: 1.5rem; align-items: flex-start; }
.step-num { width: 40px; height: 40px; border-radius: 50%; background: var(--color-brand); color: #fff; display: grid; place-items: center; font-weight: 700; flex-shrink: 0; font-size: 1rem; }
.step-content h3 { font-size: 1rem; font-weight: 600; margin-bottom: 0.25rem; }
.step-content p  { font-size: 0.875rem; color: var(--color-text-muted); line-height: 1.6; }

/* ── Testimonials ── */
.testimonials { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; }
.testimonial { background: var(--color-surface); border: 1px solid var(--color-border); border-radius: 16px; padding: 1.75rem; display: flex; flex-direction: column; gap: 1.25rem; }
.t-quote  { font-size: 0.9rem; color: var(--color-text); line-height: 1.7; flex: 1; }
.t-author { display: flex; align-items: center; gap: 0.75rem; }
.t-avatar { width: 36px; height: 36px; border-radius: 50%; background: var(--color-brand-dark); color: #fff; display: grid; place-items: center; font-weight: 700; font-size: 0.875rem; flex-shrink: 0; }
.t-name   { font-size: 0.85rem; font-weight: 600; }
.t-role   { font-size: 0.75rem; color: var(--color-text-muted); }

/* ── Pricing ── */
.pricing-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; align-items: start; }
.price-card { background: var(--color-bg); border: 1px solid var(--color-border); border-radius: 16px; padding: 2rem; position: relative; transition: all 0.2s; }
.price-card.featured { background: var(--color-surface); border-color: var(--color-brand); box-shadow: 0 0 40px rgba(108,99,255,0.15); transform: scale(1.03); }
.popular-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: var(--color-brand); color: #fff; border-radius: 99px; padding: 0.2rem 0.875rem; font-size: 0.72rem; font-weight: 700; white-space: nowrap; }
.plan-name  { font-size: 1rem; font-weight: 700; margin-bottom: 0.75rem; }
.plan-price { margin-bottom: 1.5rem; }
.price-num  { font-size: 2.5rem; font-weight: 800; letter-spacing: -0.04em; }
.plan-features { list-style: none; display: flex; flex-direction: column; gap: 0.625rem; margin-bottom: 1.75rem; }
.plan-features li { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; color: var(--color-text-muted); }
.plan-cta { display: block; text-align: center; padding: 0.7rem; border-radius: 8px; border: 1px solid var(--color-border); color: var(--color-text); text-decoration: none; font-size: 0.875rem; font-weight: 600; transition: all 0.15s; }
.plan-cta:hover { border-color: var(--color-brand); color: var(--color-brand-light); }
.cta-primary { background: var(--color-brand); border-color: var(--color-brand); color: #fff; }
.cta-primary:hover { background: var(--color-brand-dark); color: #fff; }

/* ── Footer ── */
.footer { display: flex; align-items: center; justify-content: space-between; padding: 2rem 4rem; border-top: 1px solid var(--color-border); font-size: 0.8rem; color: var(--color-text-muted); }
.footer-brand { display: flex; align-items: center; gap: 0.375rem; font-weight: 700; color: var(--color-brand); }
.footer-links { display: flex; gap: 1.5rem; }
.footer-links a { color: var(--color-text-muted); text-decoration: none; transition: color 0.15s; }
.footer-links a:hover { color: var(--color-text); }
</style>
