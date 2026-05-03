<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    <AppToast />
  </div>
</template>

<script setup lang="ts">
useHead({
  htmlAttrs: { lang: 'en' },
})
</script>

<style>
/* ── Global Styles ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --font-sans: 'Inter', system-ui, sans-serif;

  /* Brand palette */
  --color-brand:       #6C63FF;
  --color-brand-light: #A89CFF;
  --color-brand-dark:  #4B44CC;

  /* Neutrals (dark mode base) */
  --color-bg:        #0E0E16;
  --color-surface:   #16161F;
  --color-surface-2: #1E1E2C;
  --color-border:    rgba(255,255,255,0.08);

  /* Text */
  --color-text:       #F0EFF8;
  --color-text-muted: #8B8AA8;

  /* Status */
  --color-success: #22C55E;
  --color-error:   #EF4444;
  --color-warning: #F59E0B;

  /* Spacing */
  --sidebar-w: 240px;
  --topbar-h:  60px;
  --radius:    12px;
}

html, body { height: 100%; font-family: var(--font-sans); }
body { background: var(--color-bg); color: var(--color-text); }

/* ── Page transitions ── */
.page-enter-active,
.page-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.page-enter-from   { opacity: 0; transform: translateY(6px); }
.page-leave-to     { opacity: 0; transform: translateY(-6px); }

/* ── Layout transitions ── */
.layout-enter-active,
.layout-leave-active { transition: opacity 0.15s ease; }
.layout-enter-from,
.layout-leave-to     { opacity: 0; }

/* ── Scrollbar ── */
::-webkit-scrollbar       { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--color-border); border-radius: 99px; }
</style>
