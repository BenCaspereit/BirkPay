<script setup lang="ts">
import SmallAccountCard from '~/components/SmallAccountCard.vue'

const { t } = useI18n({
  useScope: 'local',
  inheritLocale: true,
  messages: {
    de: {
      title: 'Mein Konto'
    },
    en: {
      title: 'My Account'
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

const account = ref({
  name: 'Lukas Weber',
  accountNumber: 'CARD-8832',
  role: 'Schüler',
  className: '9b',
  balanceEuro: 14.50,
  active: true
})

const transactions = ref<Transaction[]>([
  { id: 'TX-10508', description: 'Tagesgericht (Fleisch)', amountEuro: 4.50, direction: 'debit', time: 'Heute, 10:42' },
  { id: 'TX-10507', description: 'Gutschrift Taschengeld', amountEuro: 15.00, direction: 'credit', time: 'Heute, 10:18' },
  { id: 'TX-10506', description: 'Apfelschorle 0.5l', amountEuro: 1.50, direction: 'debit', time: 'Heute, 09:56' },
  { id: 'TX-10505', description: 'Bargeldeinzahlung', amountEuro: 20.00, direction: 'credit', time: 'Heute, 09:31' },
  { id: 'TX-10504', description: 'Beilagensalat', amountEuro: 2.20, direction: 'debit', time: 'Heute, 09:12' },
  { id: 'TX-10503', description: 'Brötchen', amountEuro: 1.20, direction: 'debit', time: 'Gestern, 12:04' },
  { id: 'TX-10502', description: 'Aufladung', amountEuro: 10.00, direction: 'credit', time: 'Gestern, 08:45' },
  { id: 'TX-10501', description: 'Wasser 0.5l', amountEuro: 0.80, direction: 'debit', time: 'Gestern, 08:22' }
])

let nextTransactionNumber = 10509

const addTransaction = (transaction: Omit<Transaction, 'id' | 'time'>) => {
  transactions.value.unshift({
    ...transaction,
    id: `TX-${nextTransactionNumber++}`,
    time: `Heute, ${new Intl.DateTimeFormat('de-DE', { hour: '2-digit', minute: '2-digit' }).format(new Date())}`
  })
  account.value.balanceEuro += transaction.direction === 'credit' ? transaction.amountEuro : -transaction.amountEuro
}

const depositMoney = ({ amountEuro, purpose }: { amountEuro: number; purpose: string }) => {
  if (!account.value.active || !Number.isFinite(amountEuro) || amountEuro <= 0) return
  addTransaction({ description: purpose, amountEuro, direction: 'credit' })
}
</script>

<template>
  <main class="mx-auto min-h-screen bg-slate-100 px-4 pb-8 pt-5 sm:max-w-xl sm:px-6 lg:max-w-3xl">
    <div class="space-y-4">
      <header class="flex items-center justify-between gap-3 pt-1">
        <div>
          <h1 class="mt-1 text-2xl font-black tracking-tight text-slate-900">{{ t('title') }}</h1>
        </div>
      </header>

      <small-account-card :name="account.name" :balance-euro="account.balanceEuro" />

      <transhistory :transactions="transactions" />
    </div>
  </main>
</template>