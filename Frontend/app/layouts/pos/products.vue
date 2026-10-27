<script setup lang="ts">
import { computed, ref } from 'vue'

const route = useRoute()
const router = useRouter()

interface Product {
  id: number
  name: string
  category: string
  priceEuro: number
  icon: string
  available: boolean
}

const products = ref<Product[]>([
  { id: 1, name: 'Tagesgericht (Fleisch)', category: 'Warmes Essen', priceEuro: 4.50, icon: 'material-symbols:lunch-dining', available: true },
  { id: 2, name: 'Tagesgericht (Veggie)', category: 'Warmes Essen', priceEuro: 4.50, icon: 'material-symbols:restaurant', available: true },
  { id: 3, name: 'Beilagensalat', category: 'Warmes Essen', priceEuro: 1.50, icon: 'material-symbols:eco', available: true },
  { id: 4, name: 'Wasser 0.5l', category: 'Getränke', priceEuro: 1.00, icon: 'material-symbols:water-drop', available: true },
  { id: 5, name: 'Apfelschorle 0.5l', category: 'Getränke', priceEuro: 1.50, icon: 'material-symbols:local-drink', available: false },
  { id: 6, name: 'Nachtisch / Joghurt', category: 'Snacks', priceEuro: 1.20, icon: 'material-symbols:icecream', available: true }
])

const categories = ['Warmes Essen', 'Getränke', 'Snacks']
const pictograms = [
  { icon: 'material-symbols:lunch-dining', label: 'Gericht' },
  { icon: 'material-symbols:restaurant', label: 'Essen' },
  { icon: 'material-symbols:eco', label: 'Vegetarisch' },
  { icon: 'material-symbols:bakery-dining', label: 'Backwaren' },
  { icon: 'material-symbols:water-drop', label: 'Wasser' },
  { icon: 'material-symbols:local-drink', label: 'Getränk' },
  { icon: 'material-symbols:coffee', label: 'Kaffee' },
  { icon: 'material-symbols:icecream', label: 'Eis & Dessert' },
  { icon: 'material-symbols:cookie', label: 'Snack' },
  { icon: 'material-symbols:nutrition', label: 'Obst' },
  { icon: 'material-symbols:shopping-bag', label: 'Sonstiges' }
]
const searchQuery = ref('')
const selectedCategory = ref('Alle Kategorien')
const isFormOpen = ref(false)
const editingProductId = ref<number | null>(null)
const formName = ref('')
const formCategory = ref(categories[0] ?? '')
const formPriceEuro = ref<number | null>(null)
const formIcon = ref(pictograms[0]?.icon ?? 'material-symbols:restaurant')
const formAvailable = ref(true)
let nextProductId = Math.max(...products.value.map(product => product.id)) + 1

const filteredProducts = computed(() => {
  const query = searchQuery.value.trim().toLocaleLowerCase('de')
  return products.value.filter((product) => {
    const matchesQuery = !query || product.name.toLocaleLowerCase('de').includes(query)
    const matchesCategory = selectedCategory.value === 'Alle Kategorien'
      || product.category === selectedCategory.value
    return matchesQuery && matchesCategory
  })
})

const availableCount = computed(() => products.value.filter(product => product.available).length)

const formatMoney = (amountEuro: number) =>
  new Intl.NumberFormat('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amountEuro)

const resetForm = () => {
  editingProductId.value = null
  formName.value = ''
  formCategory.value = categories[0] ?? ''
  formPriceEuro.value = null
  formIcon.value = pictograms[0]?.icon ?? 'material-symbols:restaurant'
  formAvailable.value = true
}

const openCreateForm = () => {
  resetForm()
  isFormOpen.value = true
}

const openEditForm = (product: Product) => {
  editingProductId.value = product.id
  formName.value = product.name
  formCategory.value = product.category
  formPriceEuro.value = product.priceEuro
  formIcon.value = product.icon
  formAvailable.value = product.available
  isFormOpen.value = true
}

const saveProduct = () => {
  const name = formName.value.trim()
  const priceEuro = formPriceEuro.value
  if (!name || priceEuro === null || !Number.isFinite(priceEuro) || priceEuro < 0) return

  if (editingProductId.value !== null) {
    const product = products.value.find(item => item.id === editingProductId.value)
    if (!product) return
    product.name = name
    product.category = formCategory.value
    product.priceEuro = priceEuro
    product.icon = formIcon.value
    product.available = formAvailable.value
  } else {
    products.value.push({
      id: nextProductId++,
      name,
      category: formCategory.value,
      priceEuro,
      icon: formIcon.value,
      available: formAvailable.value
    })
  }

  isFormOpen.value = false
  resetForm()
}

const toggleAvailability = (product: Product) => {
  product.available = !product.available
}

const goBack = () => {
  if (import.meta.client && window.history.state.back) {
    router.back()
    return
  }

  navigateTo(route.path.startsWith('/adminPortal') ? '/adminPortal/pos' : '/pos')
}
</script>

<template>
  <main class="min-h-full bg-gray-50 px-3 py-4 sm:px-5 sm:py-6 lg:px-8">
    <div class="mx-auto max-w-7xl">
      <header class="mb-5 flex flex-col gap-4 rounded-2xl border border-purple-100 bg-purple-50 p-4 sm:flex-row sm:items-center sm:justify-between sm:p-6">
        <div>
          <p class="text-xs font-bold uppercase tracking-wide text-purple-700">Kasse &amp; Mensa</p>
          <h1 class="mt-1 text-2xl font-bold text-gray-950">Speisen &amp; Artikel</h1>
          <p class="mt-1 text-sm text-gray-600">Produkte, Preise und Verfügbarkeit verwalten.</p>
        </div>
        <div class="grid gap-2 sm:flex sm:shrink-0">
          <button
            type="button"
            class="inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-lg border border-purple-200 bg-white px-4 py-2.5 text-sm font-semibold text-purple-700 transition-colors hover:bg-purple-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500 focus-visible:ring-offset-2 sm:w-auto"
            @click="goBack"
          >
            <Icon name="material-symbols:arrow-back" class="h-5 w-5" />
            Zurück
          </button>
          <button
            type="button"
            class="inline-flex min-h-11 w-full items-center justify-center gap-2 rounded-lg bg-purple-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-purple-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500 focus-visible:ring-offset-2 sm:w-auto"
            @click="openCreateForm"
          >
            <Icon name="material-symbols:add" class="h-5 w-5" />
            Neuen Artikel anlegen
          </button>
        </div>
      </header>

      <section class="rounded-2xl border border-gray-200 bg-white shadow-sm">
        <div class="flex flex-col gap-4 border-b border-gray-100 p-4 sm:p-5 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h2 class="text-lg font-bold text-gray-900">Artikelübersicht</h2>
            <p class="mt-1 text-sm text-gray-500">
              {{ availableCount }} von {{ products.length }} Artikeln verfügbar
            </p>
          </div>

          <div class="grid gap-3 sm:grid-cols-2 lg:w-[min(100%,32rem)]">
            <label class="block">
              <span class="mb-1.5 block text-xs font-semibold text-gray-600">Artikel suchen</span>
              <span class="relative block">
                <Icon name="material-symbols:search" class="pointer-events-none absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
                <input
                  v-model="searchQuery"
                  type="search"
                  placeholder="Name eingeben"
                  class="h-11 w-full rounded-lg border border-gray-300 bg-white pl-10 pr-3 text-sm text-gray-800 outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
                >
              </span>
            </label>
            <label class="block">
              <span class="mb-1.5 block text-xs font-semibold text-gray-600">Kategorie</span>
              <select
                v-model="selectedCategory"
                class="h-11 w-full rounded-lg border border-gray-300 bg-white px-3 text-sm text-gray-800 outline-none transition focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
              >
                <option>Alle Kategorien</option>
                <option v-for="category in categories" :key="category">{{ category }}</option>
              </select>
            </label>
          </div>
        </div>

        <div v-if="filteredProducts.length" class="grid gap-3 p-3 sm:grid-cols-2 sm:p-4 xl:grid-cols-3">
          <article
            v-for="product in filteredProducts"
            :key="product.id"
            class="flex min-w-0 flex-col justify-between rounded-xl border border-gray-200 p-4 transition-shadow hover:shadow-md"
          >
            <div>
              <div class="flex items-start justify-between gap-3">
                <div class="flex min-w-0 items-center gap-3">
                  <span class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-purple-50 text-purple-700">
                    <Icon :name="product.icon" class="h-6 w-6" />
                  </span>
                  <div class="min-w-0">
                    <p class="text-xs font-medium text-gray-500">{{ product.category }}</p>
                    <h3 class="mt-1 break-words font-semibold text-gray-900">{{ product.name }}</h3>
                  </div>
                </div>
                <span
                  class="shrink-0 rounded-full px-2.5 py-1 text-xs font-semibold"
                  :class="product.available ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'"
                >
                  {{ product.available ? 'Verfügbar' : 'Pausiert' }}
                </span>
              </div>
              <p class="mt-4 flex items-center text-2xl font-bold tabular-nums text-gray-900">
                {{ formatMoney(product.priceEuro) }}
                <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-6 w-6" />
              </p>
            </div>

            <div class="mt-4 grid grid-cols-2 gap-2 border-t border-gray-100 pt-3">
              <button
                type="button"
                class="inline-flex min-h-10 items-center justify-center gap-1.5 rounded-lg border border-purple-200 px-3 text-sm font-semibold text-purple-700 transition-colors hover:bg-purple-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500"
                @click="openEditForm(product)"
              >
                <Icon name="material-symbols:edit-outline" class="h-4 w-4" />
                Bearbeiten
              </button>
              <button
                type="button"
                class="inline-flex min-h-10 items-center justify-center rounded-lg px-2 text-sm font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500"
                :class="product.available ? 'text-red-600 hover:bg-red-50' : 'text-emerald-700 hover:bg-emerald-50'"
                :aria-label="product.available ? `${product.name} pausieren` : `${product.name} aktivieren`"
                @click="toggleAvailability(product)"
              >
                {{ product.available ? 'Pausieren' : 'Aktivieren' }}
              </button>
            </div>
          </article>
        </div>
        <div v-else class="px-4 py-12 text-center">
          <Icon name="material-symbols:search-off" class="mx-auto h-9 w-9 text-gray-400" />
          <p class="mt-3 font-semibold text-gray-800">Keine Artikel gefunden</p>
          <p class="mt-1 text-sm text-gray-500">Passe die Suche oder den Kategorie-Filter an.</p>
        </div>
      </section>
    </div>

    <div
      v-if="isFormOpen"
      class="fixed inset-0 z-50 flex items-end justify-center bg-gray-950/40 p-0 sm:items-center sm:p-4"
      @click.self="isFormOpen = false"
    >
      <section
        role="dialog"
        aria-modal="true"
        aria-labelledby="product-form-title"
        class="max-h-[92dvh] w-full overflow-y-auto rounded-t-2xl bg-white p-5 shadow-xl sm:max-w-lg sm:rounded-2xl sm:p-6"
      >
        <div class="flex items-start justify-between gap-4">
          <div>
            <h2 id="product-form-title" class="text-xl font-bold text-gray-900">
              {{ editingProductId === null ? 'Neuen Artikel anlegen' : 'Artikel bearbeiten' }}
            </h2>
            <p class="mt-1 text-sm text-gray-500">Name, Kategorie und Preis festlegen.</p>
          </div>
          <button
            type="button"
            aria-label="Dialog schließen"
            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-gray-500 hover:bg-gray-100"
            @click="isFormOpen = false"
          >
            <Icon name="material-symbols:close" class="h-5 w-5" />
          </button>
        </div>

        <form class="mt-5 space-y-4" @submit.prevent="saveProduct">
          <label class="block text-sm font-semibold text-gray-700">
            Artikelname
            <input
              v-model="formName"
              required
              maxlength="80"
              autofocus
              placeholder="z. B. Apfelsaft 0,5 l"
              class="mt-1.5 h-12 w-full rounded-lg border border-gray-300 px-3 text-base font-normal text-gray-900 outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
            >
          </label>
          <label class="block text-sm font-semibold text-gray-700">
            Kategorie
            <select
              v-model="formCategory"
              class="mt-1.5 h-12 w-full rounded-lg border border-gray-300 bg-white px-3 text-base font-normal text-gray-900 outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
            >
              <option v-for="category in categories" :key="category">{{ category }}</option>
            </select>
          </label>
          <fieldset>
            <legend class="text-sm font-semibold text-gray-700">Piktogramm</legend>
            <p class="mt-1 text-xs font-normal text-gray-500">Wähle ein passendes Google Material Symbol.</p>
            <div class="mt-2 grid grid-cols-3 gap-2 sm:grid-cols-4">
              <button
                v-for="pictogram in pictograms"
                :key="pictogram.icon"
                type="button"
                :aria-pressed="formIcon === pictogram.icon"
                :aria-label="`Piktogramm auswählen: ${pictogram.label}`"
                class="flex min-h-16 flex-col items-center justify-center gap-1 rounded-lg border px-2 py-2 text-xs font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500"
                :class="formIcon === pictogram.icon
                  ? 'border-purple-500 bg-purple-50 text-purple-700 ring-1 ring-purple-500'
                  : 'border-gray-200 bg-white text-gray-600 hover:border-purple-200 hover:bg-purple-50'"
                @click="formIcon = pictogram.icon"
              >
                <Icon :name="pictogram.icon" class="h-6 w-6" />
                <span>{{ pictogram.label }}</span>
              </button>
            </div>
          </fieldset>
          <label class="block text-sm font-semibold text-gray-700">
            Preis
            <span class="relative mt-1.5 block">
              <input
                v-model.number="formPrice"
                type="number"
                min="0"
                step="0.01"
                required
                placeholder="0,00"
                class="h-12 w-full rounded-lg border border-gray-300 px-3 pr-10 text-base font-normal text-gray-900 outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-100"
              >
              <Icon name="bitcoin-icons:bitcoin-filled" class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
            </span>
          </label>
          <label class="flex min-h-12 cursor-pointer items-center justify-between rounded-lg border border-gray-200 px-3">
            <span>
              <span class="block text-sm font-semibold text-gray-800">Artikel verfügbar</span>
              <span class="block text-xs text-gray-500">In der Kasse zum Verkauf anzeigen</span>
            </span>
            <input
              v-model="formAvailable"
              type="checkbox"
              class="h-5 w-5 rounded border-gray-300 text-purple-600 focus:ring-purple-500"
            >
          </label>
          <div class="flex flex-col-reverse gap-2 border-t border-gray-100 pt-4 sm:flex-row sm:justify-end">
            <button
              type="button"
              class="min-h-11 rounded-lg px-4 text-sm font-semibold text-gray-600 hover:bg-gray-100"
              @click="isFormOpen = false"
            >
              Abbrechen
            </button>
            <button
              type="submit"
              class="min-h-11 rounded-lg bg-purple-600 px-5 text-sm font-semibold text-white transition-colors hover:bg-purple-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500 focus-visible:ring-offset-2"
            >
              {{ editingProductId === null ? 'Artikel anlegen' : 'Änderungen speichern' }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </main>
</template>
