<script setup lang="ts">
import { ref } from 'vue'

const nfcScanned = ref(false)
const student = ref({
  id: 'CARD-8832',
  name: 'Lukas Weber',
  class: 'Klasse 9b',
  balanceEuro: 14.50
})

const selectedAmountEuro = ref<number | null>(null)
const amountsEuro = [5, 10, 20, 50]

const scanCardSim = () => {
  nfcScanned.value = true
}

const depositMoney = () => {
  if (!selectedAmountEuro.value) return
  student.value.balanceEuro += selectedAmountEuro.value
  alert(`${selectedAmountEuro.value} erfolgreich aufgeladen! Neues Guthaben: ${student.value.balanceEuro.toFixed(2)}`)
  reset()
}

const reset = () => {
  nfcScanned.value = false
  selectedAmountEuro.value = null
}
</script>

<template>
  <div class="mx-auto max-w-2xl rounded-2xl border border-gray-200 bg-white p-8 shadow-sm">
    <div class="flex items-center gap-3">
      <img src="/birkling.svg" alt="" class="h-10 w-10 shrink-0" />
      <div>
        <p class="text-xs font-bold uppercase tracking-wide text-purple-700">BirkPay</p>
        <h1 class="text-xl font-bold text-gray-900">Bank Terminal</h1>
      </div>
    </div>
    <p class="text-sm text-gray-500">Bargeld aufladen oder Guthaben abfragen</p>

    <!-- Schritt 1: Karte auflegen -->
    <div v-if="!nfcScanned" class="my-10 text-center">
      <div class="mx-auto flex h-24 w-24 items-center justify-center rounded-full bg-blue-50 text-blue-600 animate-pulse">
        <Icon name="material-symbols:contactless-outline" class="h-12 w-12" />
      </div>
      <p class="mt-4 text-base font-semibold text-gray-800">Bitte BirkPay-Karte auflegen</p>
      <button 
        @click="scanCardSim"
        class="mt-6 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
      >
        (Simuliere NFC-Scan)
      </button>
    </div>

    <!-- Schritt 2: Account-Details & Betrag wähle -->
    <div v-else class="mt-6 space-y-6">
      <div class="flex items-center justify-between rounded-xl bg-gray-50 p-4 border border-gray-100">
        <div>
          <h2 class="text-lg font-bold text-gray-900">{{ student.name }}</h2>
          <p class="text-xs text-gray-500">{{ student.class }} • ID: {{ student.id }}</p>
        </div>
        <div class="text-right">
          <p class="text-xs text-gray-500">Aktuelles Guthaben</p>
          <p class="flex items-center text-2xl font-black text-teal-600">
            {{ student.balanceEuro.toFixed(2) }}
            <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-6 w-6" />
          </p>
        </div>
      </div>

      <div>
        <label class="block text-sm font-semibold text-gray-700 mb-3">Aufladebetrag wählen:</label>
        <div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <button
            v-for="amountEuro in amountsEuro"
            :key="amountEuro"
            @click="selectedAmountEuro = amountEuro"
            class="rounded-xl border p-4 text-center text-lg font-bold transition-all"
            :class="selectedAmountEuro === amountEuro ? 'border-blue-600 bg-blue-50 text-blue-700' : 'border-gray-200 hover:border-gray-300'"
          >
            +{{ amountEuro }}
            <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 inline-block h-5 w-5 align-[-0.2em]" />
          </button>
        </div>
      </div>

      <div class="flex gap-3 pt-4">
        <button 
          @click="reset" 
          class="w-1/3 rounded-xl border border-gray-300 py-3 text-sm font-semibold text-gray-700 hover:bg-gray-50"
        >
          Abbrechen
        </button>
        <button 
          @click="depositMoney" 
          :disabled="!selectedAmountEuro"
          class="w-2/3 rounded-xl bg-blue-600 py-3 text-sm font-bold text-white hover:bg-blue-700 disabled:opacity-50"
        >
          Einzahlung bestätigen
        </button>
      </div>
    </div>
  </div>
</template>