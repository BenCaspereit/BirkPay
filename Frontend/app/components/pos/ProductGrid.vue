<script setup lang="ts">
interface Category {
  id: string
  name: string
  icon: string
}

interface Product {
  id: number
  name: string
  priceEuro: number
  category: string
  icon: string
  color: string
  disabled: boolean
}

defineProps<{
  categories: Category[]
  activeCategory: string
  products: Product[]
}>()

const emit = defineEmits<{
  (event: 'select-category', categoryId: string): void
  (event: 'add-to-cart', product: Product): void
  (event: 'toggle-availability', productId: number): void
}>()

let longPressTimer: ReturnType<typeof setTimeout> | undefined
let suppressNextClick = false

const cancelLongPress = () => {
  if (longPressTimer) clearTimeout(longPressTimer)
  longPressTimer = undefined
}

const startLongPress = (productId: number) => {
  cancelLongPress()
  suppressNextClick = false
  longPressTimer = setTimeout(() => {
    longPressTimer = undefined
    suppressNextClick = true
    emit('toggle-availability', productId)
  }, 600)
}

const selectProduct = (product: Product) => {
  if (suppressNextClick) {
    suppressNextClick = false
    return
  }
  if (product.disabled) return
  emit('add-to-cart', product)
}
</script>

<template>
  <div class="lg:col-span-2 flex flex-col justify-between rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
    <div>
      <div class="flex items-center gap-2 pb-3">
        <div class="flex min-w-0 items-center gap-2 overflow-x-auto">
          <button
            v-for="category in categories"
            :key="category.id"
            @click="emit('select-category', category.id)"
            class="rounded-lg px-4 py-2 text-sm font-semibold transition-colors shrink-0"
            :class="activeCategory === category.id ? 'bg-teal-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
          >
            <Icon :name="category.icon" class="mr-2 inline-block h-5 w-5 align-middle" />
            {{ category.name }}
          </button>
        </div>
        <slot name="toolbar" />
      </div>

      <div class="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4">
        <button
          v-for="product in products"
          :key="product.id"
          @pointerdown="startLongPress(product.id)"
          @pointerup="cancelLongPress"
          @pointerleave="cancelLongPress"
          @pointercancel="cancelLongPress"
          @contextmenu.prevent
          @click="selectProduct(product)"
          :aria-disabled="product.disabled"
          :title="product.disabled ? 'Gedrückt halten, um den Artikel zu aktivieren' : 'Gedrückt halten, um den Artikel zu deaktivieren'"
          class="relative flex h-32 flex-col justify-between rounded-xl border p-4 text-left shadow-xs transition-transform active:scale-95 hover:shadow-md select-none"
          :class="[product.color, product.disabled ? 'cursor-not-allowed opacity-40 grayscale' : '']"
        >
          <Icon v-if="product.disabled" name="material-symbols:lock-outline" class="absolute right-2 top-2 h-4 w-4" />
          <Icon :name="product.icon" class="h-7 w-7" />
          <span class="text-sm font-bold leading-tight">{{ product.name }}</span>
          <span class="flex items-center text-lg font-extrabold">
            {{ product.priceEuro.toFixed(2) }}
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