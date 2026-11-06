<script setup lang="ts">

const { t } = useI18n({
  useScope: 'local',
  inheritLocale: true,
  messages: {
    de: {
      "history": "Verlauf",
      "entries": "Einträge",
      "transactions": "Transaktionen",
      "noTransactions": "Keine Transaktionen"
    },
    en: {
      "history": "History",
      "entries": "Entries",
      "transactions": "Transactions",
      "noTransactions": "No Transactions"
    }
  }
})

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
  <section class="rounded-[1.75rem] border border-slate-200 bg-white p-3 shadow-[0_10px_30px_rgba(15,23,42,0.04)] sm:p-4">
    <div class="mb-3 flex items-center justify-between gap-3 px-1">
      <div>
        <p class="text-[0.62rem] font-semibold uppercase tracking-[0.16em] text-slate-400">{{ t('history') }}</p>
        <h2 class="mt-1 text-lg font-bold text-slate-900">{{ t('transactions') }}</h2>
      </div>

      <span class="rounded-full bg-slate-100 px-2.5 py-1 text-[0.68rem] font-semibold text-slate-600">
        {{ transactions.length }} {{ t('entries') }}
      </span>
    </div>

    <div class="space-y-2">
      <p v-if="transactions.length === 0" class="rounded-2xl bg-slate-50 py-12 text-center text-sm text-slate-400">
        {{ t('noTransactions') }}
      </p>

      <article
        v-for="transaction in transactions"
        :key="transaction.id"
        class="rounded-2xl border border-slate-200 bg-slate-50/80 p-3 transition-colors hover:border-slate-300 hover:bg-slate-50"
      >
        <div class="flex items-center gap-3">
          <div
            class="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl"
            :class="transaction.direction === 'credit' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-600'"
          >
            <Icon
              :name="transaction.direction === 'credit' ? 'material-symbols:arrow-upward-rounded' : 'material-symbols:arrow-downward-rounded'"
              class="h-5 w-5"
            />
          </div>

          <div class="min-w-0 flex-1">
            <div class="flex items-start justify-between gap-2">
              <p class="truncate font-semibold text-slate-800">{{ transaction.description }}</p>
              <span
                class="shrink-0 text-sm font-bold tabular-nums"
                :class="transaction.direction === 'credit' ? 'text-emerald-700' : 'text-slate-800'"
              >
                <span>{{ transaction.direction === 'credit' ? '+' : '-' }}{{ formatMoney(transaction.amountEuro) }}</span>
                <Icon name="bitcoin-icons:bitcoin-filled" class="ml-0.5 inline h-4 w-4 align-[-0.15em]" aria-label="Bitcoin" />
              </span>
            </div>

            <div class="mt-1 flex items-center justify-between gap-2 text-[0.72rem] text-slate-500">
              <span>{{ transaction.time }}</span>
              <span class="font-medium">{{ transaction.id }}</span>
            </div>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>
