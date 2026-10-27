<script setup lang="ts">
import { ref, computed } from 'vue'

// Warenkorb Logik
const cart = ref<{ id: number; name: string; priceEuro: number; qty: number }[]>([])



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
</template>