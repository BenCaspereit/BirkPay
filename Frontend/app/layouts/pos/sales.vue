<script setup lang="ts">
import { computed, ref } from 'vue'

const route = useRoute()
const router = useRouter()

const topSellers = ref([
  { name: 'Tagesgericht (Fleisch)', count: 92, revenueEuro: 414 },
  { name: 'Tagesgericht (Veggie)', count: 54, revenueEuro: 243 },
  { name: 'Apfelschorle 0.5l', count: 78, revenueEuro: 117 },
  { name: 'Wasser 0.5l', count: 45, revenueEuro: 45 }
])

const salesByPeak = ref([
  { time: '09:30–09:50', label: '1. Große Pause', count: 68, totalEuro: 380.50 },
  { time: '11:30–12:15', label: 'Mittagspause 1', count: 84, totalEuro: 620 },
  { time: '13:00–13:30', label: 'Mittagspause 2', count: 32, totalEuro: 248 }
])

const dailyRevenueEuro = computed(() => salesByPeak.value.reduce((sum, peak) => sum + peak.totalEuro, 0))
const transactionCount = computed(() => salesByPeak.value.reduce((sum, peak) => sum + peak.count, 0))
const averageTransactionEuro = computed(() => transactionCount.value ? dailyRevenueEuro.value / transactionCount.value : 0)
const bestSeller = computed(() => [...topSellers.value].sort((a, b) => b.count - a.count)[0])
const busiestPeakRevenueEuro = computed(() => Math.max(...salesByPeak.value.map(peak => peak.totalEuro), 0))

const formatMoney = (amountEuro: number) =>
  new Intl.NumberFormat('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amountEuro)

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
    <div class="mx-auto max-w-7xl space-y-5 sm:space-y-6">
      <header class="flex flex-col gap-4 rounded-2xl border border-purple-100 bg-purple-50 p-4 sm:flex-row sm:items-center sm:justify-between sm:p-6">
        <div class="flex items-start gap-3">
          <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-purple-100 text-purple-700">
            <Icon name="material-symbols:monitoring" class="h-6 w-6" />
          </div>
          <div>
            <p class="text-xs font-bold uppercase tracking-wide text-purple-700">Kasse &amp; Mensa</p>
            <h1 class="mt-1 text-xl font-bold text-gray-950 sm:text-2xl">Tagesumsatz &amp; Verkaufsanalyse</h1>
            <p class="mt-1 text-sm text-gray-600">Verkäufe und Stoßzeiten auf einen Blick.</p>
          </div>
        </div>
        <button
          type="button"
          class="inline-flex min-h-11 w-full shrink-0 items-center justify-center gap-2 rounded-lg border border-purple-200 bg-white px-4 py-2.5 text-sm font-semibold text-purple-700 transition-colors hover:bg-purple-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-purple-500 focus-visible:ring-offset-2 sm:w-auto"
          @click="goBack"
        >
          <Icon name="material-symbols:arrow-back" class="h-5 w-5" />
          Zurück
        </button>
      </header>

      <section class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <article class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5">
          <div class="flex items-center gap-2 text-sm font-medium text-gray-500">
            <Icon name="material-symbols:payments-outline" class="h-5 w-5 text-purple-600" />
            Umsatz heute
          </div>
          <p class="mt-3 flex items-center text-2xl font-extrabold tabular-nums text-gray-950">
            {{ formatMoney(dailyRevenueEuro) }}
            <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-6 w-6" />
          </p>
          <p class="mt-1 text-xs text-gray-500">Gesamtumsatz des Tages</p>
        </article>

        <article class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5">
          <div class="flex items-center gap-2 text-sm font-medium text-gray-500">
            <Icon name="material-symbols:receipt-long-outline" class="h-5 w-5 text-purple-600" />
            Verkäufe heute
          </div>
          <p class="mt-3 text-2xl font-extrabold tabular-nums text-gray-950">{{ transactionCount }}</p>
          <p class="mt-1 text-xs text-gray-500">Abgeschlossene Transaktionen</p>
        </article>

        <article class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5">
          <div class="flex items-center gap-2 text-sm font-medium text-gray-500">
            <Icon name="material-symbols:account-balance-wallet-outline" class="h-5 w-5 text-emerald-600" />
            Durchschnittsbon
          </div>
          <p class="mt-3 flex items-center text-2xl font-extrabold tabular-nums text-gray-950">
            {{ formatMoney(averageTransactionEuro) }}
            <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-6 w-6" />
          </p>
          <p class="mt-1 text-xs text-gray-500">Umsatz pro Transaktion</p>
        </article>

        <article class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5">
          <div class="flex items-center gap-2 text-sm font-medium text-gray-500">
            <Icon name="material-symbols:star-outline" class="h-5 w-5 text-amber-500" />
            Meistverkauft
          </div>
          <p class="mt-3 truncate text-lg font-extrabold text-gray-950">{{ bestSeller?.name ?? 'Noch keine Verkäufe' }}</p>
          <p v-if="bestSeller" class="mt-1 text-xs text-gray-500">{{ bestSeller.count }} Stück verkauft</p>
        </article>
      </section>

      <section class="grid items-start gap-4 lg:grid-cols-2 lg:gap-5">
        <article class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5">
          <div class="mb-2">
            <h2 class="text-lg font-bold text-gray-900">Meistverkaufte Artikel</h2>
            <p class="mt-1 text-sm text-gray-500">Nach Verkaufsmenge sortiert</p>
          </div>

          <ol class="divide-y divide-gray-100">
            <li
              v-for="(item, index) in [...topSellers].sort((a, b) => b.count - a.count)"
              :key="item.name"
              class="flex items-center gap-3 py-4"
            >
              <span
                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-sm font-bold"
                :class="index === 0 ? 'bg-purple-100 text-purple-700' : 'bg-gray-100 text-gray-600'"
              >
                {{ index + 1 }}
              </span>
              <div class="min-w-0 flex-1">
                <p class="truncate text-sm font-semibold text-gray-900">{{ item.name }}</p>
                <p class="mt-0.5 text-xs text-gray-500">{{ item.count }} Stück verkauft</p>
              </div>
              <p class="flex shrink-0 items-center text-sm font-bold tabular-nums text-emerald-700">
                {{ formatMoney(item.revenueEuro) }}
                <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-4 w-4" />
              </p>
            </li>
          </ol>
        </article>

        <article class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5">
          <div class="mb-2">
            <h2 class="text-lg font-bold text-gray-900">Umsatz nach Pausenzeit</h2>
            <p class="mt-1 text-sm text-gray-500">Erkenne die stärksten Verkaufszeiten des Tages</p>
          </div>

          <ul class="divide-y divide-gray-100">
            <li v-for="peak in salesByPeak" :key="peak.time" class="py-4">
              <div class="flex items-start justify-between gap-3">
                <div>
                  <p class="text-sm font-semibold text-gray-900">{{ peak.label }}</p>
                  <p class="mt-0.5 text-xs text-gray-500">{{ peak.time }} · {{ peak.count }} Transaktionen</p>
                </div>
                <p class="flex shrink-0 items-center text-sm font-bold tabular-nums text-emerald-700">
                  {{ formatMoney(peak.totalEuro) }}
                  <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-4 w-4" />
                </p>
              </div>
              <div
                class="mt-3 h-2 overflow-hidden rounded-full bg-purple-50"
                role="progressbar"
                :aria-label="`Umsatzanteil ${peak.label}`"
                aria-valuemin="0"
                :aria-valuemax="dailyRevenueEuro"
                :aria-valuenow="peak.totalEuro"
              >
                <div
                  class="h-full rounded-full bg-purple-500 transition-all"
                  :style="{ width: `${busiestPeakRevenueEuro ? (peak.totalEuro / busiestPeakRevenueEuro) * 100 : 0}%` }"
                />
              </div>
            </li>
          </ul>
        </article>
      </section>
    </div>
  </main>
</template>
