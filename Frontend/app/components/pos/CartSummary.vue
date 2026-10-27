<script setup lang="ts">
interface CartItem {
  id: number
  name: string
  priceEuro: number
  qty: number
}

defineProps<{
  cart: CartItem[]
  totalEuro: string
  isProcessing: boolean
  scanMessage: string
}>()

const emit = defineEmits<{
  (event: 'decrement', index: number): void
  (event: 'remove', index: number): void
  (event: 'clear'): void
  (event: 'checkout'): void
}>()
</script>

<template>
  <div class="flex flex-col justify-between rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
    <div>
      <div class="flex items-center justify-between border-b border-gray-100 pb-3">
        <h2 class="text-lg font-bold text-gray-900">Aktuelle Bestellung</h2>
        <button
          v-if="cart.length > 0"
          @click="emit('clear')"
          class="text-xs font-semibold text-red-600 hover:underline"
        >
          Alles leeren
        </button>
      </div>

      <div class="mt-3 max-h-[350px] divide-y divide-gray-100 overflow-y-auto">
        <div v-if="cart.length === 0" class="py-12 text-center text-sm text-gray-400">
          Warenkorb ist leer
        </div>
        <div
          v-for="(item, index) in cart"
          :key="item.id"
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
            <button
              @click="emit('decrement', index)"
              class="flex h-8 w-8 items-center justify-center text-xl font-bold text-gray-400 hover:text-red-500"
              :aria-label="`${item.name} Menge verringern`"
            >
              -
            </button>
            <span class="flex items-center font-bold text-gray-900">
              {{ (item.qty * item.priceEuro).toFixed(2) }}
              <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-4 w-4" />
            </span>
            <button
              @click="emit('remove', index)"
              class="text-gray-400 hover:text-red-500"
              :aria-label="`${item.name} aus dem Warenkorb entfernen`"
            >
              <Icon name="material-symbols:delete-outline" class="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="border-t border-gray-200 pt-4">
      <div class="flex items-center justify-between text-base font-medium text-gray-600">
        <span>Gesamtsumme:</span>
        <span class="flex items-center text-2xl font-extrabold text-gray-900">
          {{ totalEuro }}
          <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-6 w-6" />
        </span>
      </div>

      <button
        @click="emit('checkout')"
        :disabled="cart.length === 0 || isProcessing"
        class="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-teal-600 py-3.5 text-base font-bold text-white shadow-sm transition-colors hover:bg-teal-700 disabled:opacity-50"
      >
        <Icon name="material-symbols:contactless-outline" class="h-6 w-6" />
        <span>{{ isProcessing ? scanMessage : 'Jetzt Abbuchen (NFC Scan)' }}</span>
      </button>
    </div>
  </div>
</template>