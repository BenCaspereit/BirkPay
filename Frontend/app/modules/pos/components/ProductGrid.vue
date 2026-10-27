<script setup lang="ts">
import { ref, computed } from 'vue'

// Produkt-Kategorien
const activeCategory = ref('alle')
const categories = [
  { id: 'alle', name: 'Alle Artikel' },
  { id: 'essen', name: 'Warmes Essen' },
  { id: 'getraenke', name: 'Getränke' },
  { id: 'snacks', name: 'Snacks & Nachtisch' }
]

// Produkte mit Dummy-Daten
const products = [
  { id: 1, name: 'Tagesgericht (Fleisch)', priceEuro: 4.50, category: 'essen', color: 'bg-amber-100 text-amber-900 border-amber-300' },
  { id: 2, name: 'Tagesgericht (Veggie)', priceEuro: 4.50, category: 'essen', color: 'bg-emerald-100 text-emerald-900 border-emerald-300' },
  { id: 3, name: 'Beilagensalat', priceEuro: 1.50, category: 'essen', color: 'bg-green-100 text-green-900 border-green-300' },
  { id: 4, name: 'Wasser 0.5l', priceEuro: 1.00, category: 'getraenke', color: 'bg-blue-100 text-blue-900 border-blue-300' },
  { id: 5, name: 'Apfelschorle 0.5l', priceEuro: 1.50, category: 'getraenke', color: 'bg-yellow-100 text-yellow-900 border-yellow-300' },
  { id: 6, name: 'Nachtisch / Joghurt', priceEuro: 1.20, category: 'snacks', color: 'bg-pink-100 text-pink-900 border-pink-300' },
  { id: 7, name: 'Apfel / Banane', priceEuro: 0.60, category: 'snacks', color: 'bg-orange-100 text-orange-900 border-orange-300' }
]
const cart = ref<{ id: number; name: string; priceEuro: number; qty: number }[]>([])

const filteredProducts = computed(() => {
  if (activeCategory.value === 'alle') return products
  return products.filter(p => p.category === activeCategory.value)
})

const addToCart = (product: typeof products[0]) => {
  const existing = cart.value.find(item => item.id === product.id)
  if (existing) {
    existing.qty++
  } else {
    cart.value.push({ id: product.id, name: product.name, priceEuro: product.priceEuro, qty: 1 })
  }
}
</script>

<template>
    
    <!-- Linke 2 Spalten: Produkt-Schnellauswahl -->
    <div class="lg:col-span-2 flex flex-col justify-between rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      
      <!-- Kategorien-Filter (Buttons) -->
      <div>
        <div class="flex items-center gap-2 overflow-x-auto pb-3">
          <button
            v-for="cat in categories"
            :key="cat.id"
            @click="activeCategory = cat.id"
            class="rounded-lg px-4 py-2 text-sm font-semibold transition-colors shrink-0"
            :class="activeCategory === cat.id ? 'bg-teal-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
          >
            {{ cat.name }}
          </button>
        </div>

        <!-- Produkt-Raster (Große Touch-Buttons) -->
        <div class="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4">
          <button
            v-for="prod in filteredProducts"
            :key="prod.id"
            @click="addToCart(prod)"
            class="flex flex-col justify-between rounded-xl border p-4 text-left shadow-xs transition-transform active:scale-95 hover:shadow-md h-32"
            :class="prod.color"
          >
            <span class="text-sm font-bold leading-tight">{{ prod.name }}</span>
            <span class="flex items-center text-lg font-extrabold">
              {{ prod.priceEuro.toFixed(2) }}
              <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-5 w-5" />
            </span>
          </button>
        </div>
      </div>

      <div class="mt-4 text-xs text-gray-400">
        💡 Tipp: Klicke auf die Artikel, um sie dem Bon hinzuzufügen.
      </div>
    </div>


</template>