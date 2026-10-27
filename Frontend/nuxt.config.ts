import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2026-10-05',

  modules: [
    '@nuxt/icon',
    '@nuxt/ui'
  ],

  css: ['~/assets/css/main.css'],

  vite: {
    plugins: [tailwindcss()]
  },

  devtools: { enabled: true },

  devServer: {
    host: '0.0.0.0',
    port: 3000       
  }
})