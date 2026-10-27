<script setup lang="ts">
interface Transaction {
  id: string
  description: string
  amountEuro: number
  direction: 'credit' | 'debit'
  time: string
}

defineProps<{
  transactions: Transaction[]
}>()

const formatMoney = (amountEuro: number) =>
  new Intl.NumberFormat('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amountEuro)
</script>

<template>
  <section class="flex min-w-0 flex-col rounded-xl border border-gray-200 bg-white p-4 shadow-sm sm:p-5 min-[900px]:h-full min-[900px]:min-h-0">
    <div class="border-b border-gray-100 pb-3">
      <h2 class="text-lg font-bold text-gray-900">Transaktionen</h2>
    </div>

    <div class="mt-2 max-h-[min(65dvh,640px)] divide-y divide-gray-100 overflow-y-auto min-[900px]:max-h-none min-[900px]:min-h-0 min-[900px]:flex-1">
      <p v-if="transactions.length === 0" class="py-12 text-center text-sm text-gray-400">
        Keine Transaktionen vorhanden
      </p>

      <article v-for="transaction in transactions" :key="transaction.id" class="py-3">
        <div class="flex items-center justify-between gap-2 sm:gap-3">
          <div class="min-w-0 flex-1">
            <p class="truncate font-medium text-gray-800">{{ transaction.description }}</p>
            <p class="mt-1 text-xs text-gray-400">{{ transaction.time }} · {{ transaction.id }}</p>
          </div>

          <div class="flex shrink-0 items-center gap-1.5 sm:gap-2">
            <span
              class="font-bold"
              :class="transaction.direction === 'credit' ? 'text-emerald-700' : 'text-red-600'"
            >
              {{ transaction.direction === 'credit' ? '+' : '−' }}{{ formatMoney(transaction.amountEuro) }}
              <Icon name="bitcoin-icons:bitcoin-filled" class="h-4 w-4 shrink-0" />
            </span>
            <button
              type="button"
              class="flex h-10 w-10 items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 hover:text-gray-600"
              :aria-label="`Weitere Informationen zu ${transaction.id}`"
              title="Weitere Informationen (später verfügbar)"
            >
              <Icon name="material-symbols:info-outline" class="h-5 w-5" />
            </button>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>
