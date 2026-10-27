<script setup lang="ts">
import { onBeforeUnmount, ref, computed } from 'vue'
import ProductGrid from '../../components/pos/ProductGrid.vue'
import CartSummary from '../../components/pos/CartSummary.vue'
import PaymentModal from '../../components/pos/PaymentModal.vue'

// Produkt-Kategorien
const activeCategory = ref('alle')
const categories = [
  { id: 'alle', name: 'Alle Artikel', icon: 'material-symbols:grid-view' },
  { id: 'essen', name: 'Warmes Essen', icon: 'material-symbols:restaurant' },
  { id: 'getraenke', name: 'Getränke', icon: 'material-symbols:local-drink' },
  { id: 'snacks', name: 'Snacks & Nachtisch', icon: 'material-symbols:cookie' }
]

// Produkte mit Dummy-Daten
const products = ref([
  { id: 1, name: 'Tagesgericht (Fleisch)', priceEuro: 4.50, category: 'essen', icon: 'material-symbols:lunch-dining', color: 'bg-amber-100 text-amber-900 border-amber-300', disabled: false },
  { id: 2, name: 'Tagesgericht (Veggie)', priceEuro: 4.50, category: 'essen', icon: 'material-symbols:wheat', color: 'bg-emerald-100 text-emerald-900 border-emerald-300', disabled: false },
  { id: 3, name: 'Beilagensalat', priceEuro: 1.50, category: 'essen', icon: 'material-symbols:eco', color: 'bg-green-100 text-green-900 border-green-300', disabled: false },
  { id: 4, name: 'Wasser 0.5l', priceEuro: 1.00, category: 'getraenke', icon: 'material-symbols:water-drop', color: 'bg-blue-100 text-blue-900 border-blue-300', disabled: false },
  { id: 5, name: 'Apfelschorle 0.5l', priceEuro: 1.50, category: 'getraenke', icon: 'material-symbols:local-drink', color: 'bg-yellow-100 text-yellow-900 border-yellow-300', disabled: false },
  { id: 6, name: 'Nachtisch / Joghurt', priceEuro: 1.20, category: 'snacks', icon: 'material-symbols:icecream', color: 'bg-pink-100 text-pink-900 border-pink-300', disabled: false },
  { id: 7, name: 'Apfel / Banane', priceEuro: 0.60, category: 'snacks', icon: 'material-symbols:nutrition', color: 'bg-orange-100 text-orange-900 border-orange-300', disabled: false }
])

// Warenkorb Logik
const cart = ref<{ id: number; name: string; priceEuro: number; qty: number }[]>([])

const filteredProducts = computed(() => {
  if (activeCategory.value === 'alle') return products.value
  return products.value.filter(p => p.category === activeCategory.value)
})

const addToCart = (product: typeof products.value[number]) => {
  if (product.disabled) return

  const existing = cart.value.find(item => item.id === product.id)
  if (existing) {
    existing.qty++
  } else {
    cart.value.push({ id: product.id, name: product.name, priceEuro: product.priceEuro, qty: 1 })
  }
}

const toggleProductAvailability = (productId: number) => {
  const product = products.value.find(item => item.id === productId)
  if (!product) return

  product.disabled = !product.disabled
  if (product.disabled) {
    cart.value = cart.value.filter(item => item.id !== productId)
  }
}

const decreaseCartItem = (index: number) => {
  const item = cart.value[index]
  if (!item) return

  if (item.qty > 1) {
    item.qty--
  } else {
    cart.value.splice(index, 1)
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
const showPaymentModal = ref(false)
const successAmountEuro = ref('0.00')
const paymentState = ref<'waiting' | 'success' | 'error'>('waiting')
const paymentErrorMessage = ref('')
const isPosMenuOpen = ref(false)
let paymentTimeout: ReturnType<typeof setTimeout> | undefined

const processPayment = () => {
  if (cart.value.length === 0) return
  if (paymentTimeout) clearTimeout(paymentTimeout)

  isProcessing.value = true
  scanMessage.value = 'Warte auf Karte...'
  successAmountEuro.value = totalEuro.value
  paymentErrorMessage.value = ''
  paymentState.value = 'waiting'
  showPaymentModal.value = true

  paymentTimeout = setTimeout(() => {
    paymentTimeout = undefined
    isProcessing.value = false
    paymentState.value = 'success'
    clearCart()
  }, 2000)
}

const cancelPayment = () => {
  if (paymentTimeout) clearTimeout(paymentTimeout)
  paymentTimeout = undefined
  isProcessing.value = false
  showPaymentModal.value = false
}

const closePaymentModal = () => {
  showPaymentModal.value = false
}

onBeforeUnmount(() => {
  if (paymentTimeout) clearTimeout(paymentTimeout)
})
</script>

<template>
  <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 h-[calc(100vh-6rem)]">
    <ProductGrid
      :categories="categories"
      :active-category="activeCategory"
      :products="filteredProducts"
      @select-category="activeCategory = $event"
      @add-to-cart="addToCart"
      @toggle-availability="toggleProductAvailability"
    >
      <template #toolbar>
        <div class="relative shrink-0 ml-auto">
          <button
            type="button"
            class="ml-auto flex h-9 w-9 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-600 hover:bg-gray-50 hover:text-teal-700"
            aria-label="POS-Unterseiten öffnen"
            title="POS-Unterseiten"
            :aria-expanded="isPosMenuOpen"
            @click="isPosMenuOpen = !isPosMenuOpen"
          >
            <Icon name="material-symbols:settings-outline" class="h-5 w-5" />
          </button>
          <div
            v-if="isPosMenuOpen"
            class="absolute right-0 top-full z-30 mt-2 w-44 rounded-lg border border-gray-200 bg-white p-1 shadow-lg"
          >
            <NuxtLink
              to="/pos/products"
              class="flex items-center gap-2 rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-gray-100"
              @click="isPosMenuOpen = false"
            >
              <Icon name="material-symbols:restaurant" class="h-4 w-4" />
              Products
            </NuxtLink>
            <NuxtLink
              to="/pos/sales"
              class="flex items-center gap-2 rounded-md px-3 py-2 text-sm text-gray-700 hover:bg-gray-100"
              @click="isPosMenuOpen = false"
            >
              <Icon name="material-symbols:receipt-long-outline" class="h-4 w-4" />
              Sales
            </NuxtLink>
          </div>
        </div>
      </template>
    </ProductGrid>
    <CartSummary
      :cart="cart"
      :total-euro="totalEuro"
      :is-processing="isProcessing"
      :scan-message="scanMessage"
      @decrement="decreaseCartItem"
      @remove="removeFromCart"
      @clear="clearCart"
      @checkout="processPayment"
    />
    <PaymentModal
      :open="showPaymentModal"
      :state="paymentState"
      :amount-euro="successAmountEuro"
      :error-message="paymentErrorMessage"
      @cancel="cancelPayment"
      @retry="processPayment"
      @close="closePaymentModal"
    />
  </div>
</template>