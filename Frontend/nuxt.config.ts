import tailwindcss from '@tailwindcss/vite'
import { createResolver } from '@nuxt/kit'
const { resolve } = createResolver(import.meta.url)

export default defineNuxtConfig({
  compatibilityDate: '2026-10-05',

  modules: [
    '@nuxt/icon',
    '@nuxt/ui',
    '@nuxtjs/i18n'
  ],

  css: ['~/assets/css/main.css'],

  vite: {
    plugins: [tailwindcss()]
  },

  devtools: { enabled: true },

  devServer: {
    host: '0.0.0.0',
    port: 3000      
  },

  i18n: {
    defaultLocale: 'de',
    strategy: 'prefix_except_default',
    
    // Verwende den Resolver, um den absoluten Pfad zu erzwingen:
    langDir: resolve('./app/locales'),

    locales: [
      {
        code: 'de',
        name: 'Deutsch',
        file: 'de/auth.json' // WIChtig: Nutze "file" (Singular) bei lazy: true pro Locale oder behalte files bei, je nach Struktur
      },
      {
        code: 'en',
        name: 'English',
        file: 'en/auth.json'
      }
    ],

    lazy: true
  }
})