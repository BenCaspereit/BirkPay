<script setup lang="ts">
import { ref } from 'vue'

interface NavChild {
  label: string
  to: string
  icon: string
}

interface NavSection {
  title: string
  icon: string
  to?: string
  isOpen: boolean
  children: NavChild[]
}

const props = withDefaults(defineProps<{
  mobileOpen?: boolean
}>(), {
  mobileOpen: false
})

const emit = defineEmits<{
  (event: 'close-mobile-menu'): void
}>()

// Navigations-Struktur mit Untermenüs für BirkPay
const navSections = ref<NavSection[]>([
  {
    title: 'Kasse & Mensa',
    icon: 'material-symbols:point-of-sale',
    isOpen: true,
    children: [
      { label: 'Kassen-Terminal', to: '/adminPortal/pos', icon: 'material-symbols:contactless-outline' },
      { label: 'Speiseplan / Artikel', to: '/adminPortal/pos/products', icon: 'material-symbols:restaurant' },
      { label: 'Tagesumsatz', to: '/adminPortal/pos/sales', icon: 'material-symbols:receipt-long-outline' },
    ]
  },
  {
    title: 'Bank & Gehälter',
    icon: 'material-symbols:account-balance-outline',
    to: '/adminPortal/bank',
    isOpen: false,
    children: []
  },
  {
    title: 'Administration',
    icon: 'material-symbols:admin-panel-settings-outline',
    isOpen: true,
    children: [
      { label: 'Dashboard', to: '/adminPortal/admin', icon: 'material-symbols:dashboard-outline' },
      { label: 'Schüler & Karten', to: '/adminPortal/users', icon: 'material-symbols:group-outline' },
      { label: 'Transaktionen Log', to: '/adminPortal/transactions', icon: 'material-symbols:history' },
      { label: 'System-Einstellungen', to: '/adminPortal/settings', icon: 'material-symbols:tune' },
    ]
  }
])

const toggleSection = (index: number) => {
  const section = navSections.value[index]
  if (!section || section.to || section.children.length === 0) return

  section.isOpen = !section.isOpen
}
</script>

<template>
  <!-- Mobile Overlay -->
  <div 
    v-if="props.mobileOpen" 
    class="fixed inset-0 z-40 bg-gray-900/30 md:hidden" 
    @click="emit('close-mobile-menu')"
  ></div>

  <!-- Sidebar -->
  <aside
    class="fixed inset-y-0 left-0 z-50 flex h-screen w-64 flex-col border-r border-purple-100 bg-violet-200 text-gray-900 transition-transform duration-200 md:static md:z-auto md:translate-x-0 md:transition-none"
    :class="props.mobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'"
  >
    <!-- Header / Brand -->
    <div class="flex h-16 items-center justify-between border-b border-purple-100 px-6">
      <div class="flex items-center gap-2">
        <img src="/birkling.svg" alt="" class="h-9 w-9 shrink-0" />
        <span class="text-xl font-bold text-gray-900">BirkPay</span>
      </div>

      <button 
        type="button" 
        aria-label="Navigation schließen" 
        class="rounded-lg p-1.5 text-gray-500 hover:bg-gray-100 hover:text-gray-900 md:hidden"
        @click="emit('close-mobile-menu')"
      >
        <Icon name="material-symbols:close-rounded" class="h-5 w-5" />
      </button>
    </div>

    <!-- Navigation Area -->
    <nav class="flex flex-1 flex-col justify-between overflow-y-auto px-3 py-4">
      <div class="space-y-4">
        
        <!-- Einzelner Link: Schnelleinsatz / Start -->
        <NuxtLink
          to="/"
          @click="emit('close-mobile-menu')"
          class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-semibold text-gray-700 transition-colors hover:bg-purple-50 hover:text-purple-700"
          active-class="bg-purple-100 text-purple-700 font-bold"
        >
          <Icon name="material-symbols:home-outline" class="h-5 w-5 shrink-0" />
          <span>Übersicht</span>
        </NuxtLink>

        <hr class="border-gray-200" />

        <!-- Haupt-Kategorien mit Untermenüs -->
        <div v-for="(section, idx) in navSections" :key="section.title" class="space-y-1">
          
          <!-- Haupt-Button / Kategorie Header -->
          <NuxtLink
            v-if="section.to"
            :to="section.to"
            @click="emit('close-mobile-menu')"
            class="flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm font-semibold text-gray-800 transition-colors hover:bg-purple-50"
            active-class="bg-purple-100 text-purple-700 font-bold"
          >
            <span class="flex items-center gap-3">
              <Icon :name="section.icon" class="h-5 w-5 shrink-0 text-gray-500" />
              <span>{{ section.title }}</span>
            </span>
          </NuxtLink>
          <button
            v-else
            type="button"
            @click="toggleSection(idx)"
            class="flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm font-semibold text-gray-800 transition-colors hover:bg-purple-50"
          >
            <div class="flex items-center gap-3">
              <Icon :name="section.icon" class="h-5 w-5 shrink-0 text-gray-500" />
              <span>{{ section.title }}</span>
            </div>
            <Icon 
              name="material-symbols:keyboard-arrow-down-rounded" 
              class="h-5 w-5 text-gray-400 transition-transform duration-200"
              :class="{ 'rotate-180': section.isOpen }"
            />
          </button>

          <!-- Untermenü Einträge -->
          <div v-if="!section.to" v-show="section.isOpen" class="ml-4 space-y-1 border-l-2 border-gray-200 pl-2">
            <NuxtLink
              v-for="child in section.children"
              :key="child.to"
              :to="child.to"
              @click="emit('close-mobile-menu')"
              class="flex items-center gap-2.5 rounded-md px-2.5 py-1.5 text-xs font-medium text-gray-600 transition-colors hover:bg-purple-50 hover:text-purple-700"
              active-class="bg-purple-50 text-purple-700 font-semibold border-r-2 border-purple-500"
            >
              <Icon :name="child.icon" class="h-4 w-4 shrink-0" />
              <span>{{ child.label }}</span>
            </NuxtLink>
          </div>

        </div>
      </div>

      <!-- Unteres Menü -->
      <div class="space-y-1 border-t border-gray-200 pt-3">
        <NuxtLink
          to="/settings"
          @click="emit('close-mobile-menu')"
          class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-purple-50 hover:text-purple-700"
          active-class="bg-purple-50 text-purple-700 font-semibold"
        >
          <Icon name="material-symbols:settings-outline" class="h-5 w-5 shrink-0" />
          <span>Einstellungen</span>
        </NuxtLink>
      </div>
    </nav>
  </aside>
</template>