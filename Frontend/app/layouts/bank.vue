<script setup lang="ts">
import { ref } from 'vue'

const mobileMenuOpen = ref(false)
</script>

<template>
  <div class="flex h-screen bg-gray-50">
    <LayoutAppSidebar :mobile-open="mobileMenuOpen" @close-mobile-menu="mobileMenuOpen = false" />

    <div class="flex min-w-0 flex-1 flex-col overflow-hidden">
      <LayoutAppNavbar @toggle-mobile-menu="mobileMenuOpen = !mobileMenuOpen" />

      <main class="flex-1 overflow-y-auto p-3 sm:p-4 md:p-6">
        <slot />
      </main>
    </div>
  </div>
</template>
