<script setup lang="ts">
import { ref } from 'vue'

const userMenuOpen = ref(false)
const searchQuery = ref('')
const hasUnread = ref(false) // later
const searchInput = ref<HTMLInputElement | null>(null)

const emit = defineEmits<{
  (event: 'toggle-mobile-menu'): void
}>()

const createNewEntry = () => {
  // Ihre Logik zum Erstellen einer neuen Einwahl (z. B. Modal öffnen oder Navigieren)
  console.log('Neue Einwahl erstellen...')
  navigateTo('/elect/new')
}

defineShortcuts({
  meta_k: {
    usingInput: true, // Reagiert auch, wenn der Fokus bereits in einem Input liegt
    handler: () => {
      searchInput.value?.focus()
    }
  },

  meta_n: {
    usingInput: true,
    handler: () => {
      createNewEntry()
    }
  }
/*  enter: {
    usingInput: 'queryInput',
    handler: () => performSearch()
  },
  escape: {
    usingInput: true,
    handler: () => clearSearch()
  }*/

})
</script>

<template>
  <header class="flex min-h-16 flex-wrap items-center gap-3 border-b border-purple-100 bg-purple-100 px-3 py-2 text-gray-900 shadow-sm sm:px-4 md:grid md:grid-cols-3 md:gap-0 md:px-6 md:py-0">

    <div class="flex items-center md:block">
      <button
        type="button"
        aria-label="Navigation öffnen"
        class="rounded-lg p-2 text-gray-600 hover:bg-purple-50 hover:text-purple-700 md:hidden"
        @click="emit('toggle-mobile-menu')"
      >
        <Icon name="material-symbols:menu-rounded" size="22" />
      </button>
    </div>

    <div class="order-3 mt-1 w-full md:order-none md:mt-0 md:flex md:justify-center">
      <div class="relative w-full md:w-144 md:max-w-full">
        <Icon
          name="material-symbols:search"
          class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500"
          size="18"
        />

        <input
          ref="searchInput"
          v-model="searchQuery"
          type="text"
          placeholder="Suchen..."
          class="w-full rounded-lg border border-gray-400 bg-gray-100 py-2 pl-9 pr-12 text-sm text-gray-700 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-100"
        />
      </div>
    </div>

    <div class="ml-auto flex items-center gap-1.5 sm:gap-3 md:gap-4">

      <button type="button" aria-label="Benachrichtigungen" class="relative rounded-full p-2 text-gray-500 hover:bg-purple-50 hover:text-purple-700">
        <Icon
            :name="hasUnread ? 'material-symbols:notifications-outline-rounded' : 'material-symbols:notifications-outline-rounded'"
            class="text-gray-500"
            size="22"
        />
        <span
            v-if="hasUnread"
            class="absolute right-1.5 top-1.5 h-2 w-2 rounded-full bg-red-500"
        ></span>
      </button>

      <div class="relative">
        <button
          type="button"
          aria-label="Benutzermenü öffnen"
          class="flex items-center gap-2 rounded-full bg-gray-100 px-2 py-1.5 text-sm font-medium text-gray-700 hover:bg-purple-50 hover:text-purple-700 sm:px-3"
          @click="userMenuOpen = !userMenuOpen"
        >
          <span class="h-6 w-6 rounded-full bg-gray-400"></span>
          <span class="hidden sm:inline">Admin</span>
        </button>

      <div
        v-if="userMenuOpen"
        class="absolute right-0 mt-2 w-40 rounded-md border border-gray-200 bg-white py-1 shadow-lg"
      >
        <NuxtLink to="/settings" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
          Einstellungen
        </NuxtLink>
        <button class="block w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100">
          Abmelden
        </button>
      </div>
    </div>
    </div>
  </header>
</template>