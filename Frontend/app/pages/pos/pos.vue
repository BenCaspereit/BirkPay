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

// Warenkorb Logik
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

const removeFromCart = (index: number) => {
  cart.value.splice(index, 1)
}

const clearCart = () => {
  cart.value = []
}

const totalEuro = computed(() => {
  return cart.value.reduce((sum, item) => sum + item.priceEuro * item.qty, 0).toFixed(2)
})

// Simulated NFC/Card Scan State
const isProcessing = ref(false)
const scanMessage = ref('')

const processPayment = () => {
  if (cart.value.length === 0) return
  isProcessing.value = true
  scanMessage.value = 'Bitte BirkPay-Karte auflegen...'
  
  // Simulation einer Zahlung nach 1.5 Sekunden
  setTimeout(() => {
    isProcessing.value = false
    alert(`Zahlung erfolgreich! ${totalEuro.value} vom Konto abgebucht.`)
    clearCart()
  }, 1500)
}
</script>

<template>
  <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 h-[calc(100vh-6rem)]">
    
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

    <!-- Rechte Spalte: Aktueller Bon / Checkout -->
    <div class="flex flex-col justify-between rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <div>
        <div class="flex items-center justify-between border-b border-gray-100 pb-3">
          <h2 class="text-lg font-bold text-gray-900">Aktueller Bon</h2>
          <button 
            v-if="cart.length > 0"
            @click="clearCart" 
            class="text-xs font-semibold text-red-600 hover:underline"
          >
            Bon leeren
          </button>
        </div>

        <!-- Bon Einträge -->
        <div class="mt-3 divide-y divide-gray-100 overflow-y-auto max-h-[350px]">
          <div v-if="cart.length === 0" class="py-12 text-center text-sm text-gray-400">
            Warenkorb ist leer
          </div>
          <div 
            v-for="(item, idx) in cart" 
            :key="idx" 
            class="flex items-center justify-between py-2 text-sm"
          >
            <div>
              <div class="font-medium text-gray-800">{{ item.name }}</div>
              <div class="flex items-center text-xs text-gray-400">
                {{ item.qty }} x {{ item.priceEuro.toFixed(2) }}
                <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-3.5 w-3.5" />
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span class="flex items-center font-bold text-gray-900">
                {{ (item.qty * item.priceEuro).toFixed(2) }}
                <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-4 w-4" />
              </span>
              <button @click="removeFromCart(idx)" class="text-gray-400 hover:text-red-500">
                <Icon name="material-symbols:delete-outline" class="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Summe & NFC-Abrechnung -->
      <div class="border-t border-gray-200 pt-4">
        <div class="flex items-center justify-between text-base font-medium text-gray-600">
          <span>Gesamtsumme:</span>
          <span class="flex items-center text-2xl font-extrabold text-gray-900">
            {{ totalEuro }}
            <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-6 w-6" />
          </span>
        </div>

        <button
          @click="processPayment"
          :disabled="cart.length === 0 || isProcessing"
          class="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-teal-600 py-3.5 text-base font-bold text-white shadow-sm transition-colors hover:bg-teal-700 disabled:opacity-50"
        >
          <Icon name="material-symbols:contactless-outline" class="h-6 w-6" />
          <span>{{ isProcessing ? scanMessage : 'Jetzt Abbuchen (NFC Scan)' }}</span>
        </button>
      </div>
    </div>

  </div>
</template>