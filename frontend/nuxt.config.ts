// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  compatibilityDate: '2025-01-01',
  devtools: { enabled: true },

  // Modules
  modules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss',
    '@nuxtjs/color-mode',
    '@vueuse/nuxt',
    'nuxt-icon',
  ],

  // Color mode config
  colorMode: {
    classSuffix: '',
    preference: 'dark',
    fallback: 'dark',
  },

  // Pinia persistence
  pinia: {
    storesDirs: ['./stores/**'],
  },

  // Runtime config — server-side secrets, client-side public vars
  runtimeConfig: {
    // Private: only available server-side (Nitro)
    fastapiBaseUrl: process.env.FASTAPI_BASE_URL || 'http://localhost:8000',
    jwtSecret: process.env.JWT_SECRET || '',

    // Public: exposed to client
    public: {
      appName: 'AutoDM',
      wsUrl:      process.env.NUXT_PUBLIC_WS_URL  || 'ws://localhost:8000/ws',
      apiBaseUrl: process.env.NUXT_PUBLIC_API_URL || 'http://localhost:8000',
    },
  },

  // Route rules — all app pages are SPA (ssr: false) to avoid
  // auth-gated server fetches during docker build / prerender.
  routeRules: {
    '/':              { ssr: false },
    '/login':         { ssr: false },
    '/signup':        { ssr: false },
    '/onboarding/**': { ssr: false },
    '/dashboard/**':  { ssr: false },
    '/campaigns/**':  { ssr: false },
    '/analytics/**':  { ssr: false },
    '/accounts/**':   { ssr: false },
    '/templates/**':  { ssr: false },
  },

  // Nitro server config
  nitro: {
    // Static SPA: only pre-render the app shell at the root.
    // All routing is handled client-side by Vue Router.
    prerender: {
      crawlLinks: false,
      routes: ['/'],
    },
    // devProxy is only active in `nuxt dev` — no effect on static builds.
    devProxy: {
      '/api/v1/**': {
        target: process.env.FASTAPI_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
        prependPath: false,
      },
    },
  },

  // TypeScript
  typescript: {
    strict: true,
  },

  // App head
  app: {
    // baseURL must match the GitHub repo name for subdirectory deployments.
    // e.g. https://username.github.io/dmMe/ → baseURL: '/dmMe/'
    // If using a custom domain or a user/org site, set to '/'.
    baseURL: process.env.NUXT_APP_BASE_URL || '/dmMe/',
    head: {
      title: 'AutoDM — Automate Your Social DMs',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Automate Instagram, X, and LinkedIn DMs at scale with AutoDM.' },
      ],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
        },
      ],
    },
    pageTransition: { name: 'page', mode: 'out-in' },
    layoutTransition: { name: 'layout', mode: 'out-in' },
  },
})
