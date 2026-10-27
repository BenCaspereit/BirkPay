<script setup lang="ts">
import { ref } from 'vue'
import BankAccountCard from '../../components/bank/accountcard.vue'
import BankDepositCard from '../../components/bank/depositcard.vue'
import BankTranshistory from '../../components/bank/transhistory.vue'

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
  <main class="min-h-dvh bg-gray-50 px-3 py-4 sm:px-5 sm:py-6 lg:px-8">
    <div class="mx-auto max-w-7xl">
      <header class="mb-5 flex items-center justify-between gap-3">
        <div class="flex items-center gap-2">
          <img src="/birkling.svg" alt="" class="h-9 w-9" />
          <p class="text-xs font-bold uppercase tracking-wide text-teal-800">BirkPay</p>
        </div>
        <button
          type="button"
          class="inline-flex min-h-11 shrink-0 items-center justify-center gap-2 rounded-lg bg-teal-700 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-teal-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-600 focus-visible:ring-offset-2"
        >
          <Icon name="material-symbols:nfc" class="h-5 w-5" />
          <span>Neue Karte scannen</span>
        </button>
      </header>

      <div class="grid items-stretch gap-4 sm:gap-5 min-[900px]:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
        <div class="space-y-4 sm:space-y-5">
          <BankAccountCard
            :name="account.name"
            :account-number="account.accountNumber"
            :role="account.role"
            :class-name="account.className"
            :balance-euro="account.balanceEuro"
            :active="account.active"
          />
          <BankDepositCard @deposit="depositMoney" />
        </div>

        <BankTranshistory :transactions="transactions" />
      </div>
    </div>
  </main>
</template>
