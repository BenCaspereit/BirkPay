<script setup lang="ts">
import { computed, ref } from 'vue'

const emit = defineEmits<{
  (event: 'deposit', payload: { amountEuro: number; purpose: string }): void
}>()

const amountEuro = ref<number | null>(null)
const purpose = ref('Bargeldeinzahlung')
const purposes = ['Bargeldeinzahlung', 'Gutschrift', 'Sonstiges']
const canDeposit = computed(() =>
  amountEuro.value !== null && Number.isFinite(amountEuro.value) && amountEuro.value > 0
)

const submitDeposit = () => {
  if (!canDeposit.value || amountEuro.value === null) return

  emit('deposit', { amountEuro: amountEuro.value, purpose: purpose.value })
  amountEuro.value = null
}
</script>

<template>
  <section class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
    <div class="flex items-center gap-2">
      <Icon name="material-symbols:add-card-outline" class="h-5 w-5 text-teal-700" />
      <h2 class="text-lg font-bold text-gray-900">Geld aufladen</h2>
    </div>

    <form class="mt-4 space-y-3" @submit.prevent="submitDeposit">
      <label class="block text-sm font-medium text-gray-700">
        Betrag
        <div class="relative mt-1">
          <input
            v-model.number="amountEuro"
            type="number"
            min="0.01"
            step="0.01"
            required
            placeholder="0,00"
            class="h-11 w-full rounded-lg border border-gray-300 bg-white px-3 pr-9 text-sm outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
          >
          <Icon name="bitcoin-icons:bitcoin-filled" class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
        </div>
      </label>

      <label class="block text-sm font-medium text-gray-700">
        Zweck
        <select
          v-model="purpose"
          class="mt-1 h-11 w-full rounded-lg border border-gray-300 bg-white px-3 text-sm outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
        >
          <option v-for="option in purposes" :key="option" :value="option">{{ option }}</option>
        </select>
      </label>

      <button
        type="submit"
        :disabled="!canDeposit"
        class="flex h-11 w-full items-center justify-center gap-2 rounded-lg bg-teal-700 px-4 text-sm font-bold text-white transition-colors hover:bg-teal-800 disabled:cursor-not-allowed disabled:opacity-50"
      >
        <Icon name="material-symbols:add" class="h-5 w-5" />
        Betrag aufladen
      </button>
    </form>
  </section>
</template>
