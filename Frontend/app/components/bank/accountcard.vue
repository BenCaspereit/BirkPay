<script setup lang="ts">
defineProps<{
  name: string
  accountNumber: string
  role: string
  className: string
  balanceEuro: number
  active: boolean
}>()

const formatMoney = (amountEuro: number) =>
  new Intl.NumberFormat('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amountEuro)
</script>

<template>
  <section class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
    <div class="flex items-start justify-between gap-3">
      <div>
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-500">Kontodaten</p>
        <h2 class="mt-1 text-lg font-bold text-gray-900">{{ name }}</h2>
      </div>
      <span
        class="rounded-full px-2.5 py-1 text-xs font-semibold"
        :class="active ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'"
      >
        {{ active ? 'Aktiv' : 'Gesperrt' }}
      </span>
    </div>

    <div class="mt-4 grid grid-cols-2 gap-3 text-sm">
      <div class="rounded-lg bg-gray-50 p-3">
        <p class="text-xs text-gray-500">Kontonummer</p>
        <p class="mt-1 font-mono font-semibold text-gray-800">{{ accountNumber }}</p>
      </div>
      <div class="rounded-lg bg-gray-50 p-3">
        <p class="text-xs text-gray-500">Kontotyp</p>
        <p class="mt-1 font-semibold text-gray-800">{{ role }}</p>
      </div>
      <div class="col-span-2 rounded-lg bg-gray-50 p-3">
        <p class="text-xs text-gray-500">Klasse / Bereich</p>
        <p class="mt-1 font-semibold text-gray-800">{{ className }}</p>
      </div>
    </div>

    <div class="mt-4 rounded-lg bg-teal-50 p-4">
      <p class="text-sm font-medium text-teal-800">Aktueller Kontostand</p>
      <p
        class="mt-1 text-3xl font-extrabold tabular-nums"
        :class="balanceEuro > 0 ? 'text-teal-950' : 'text-red-600'"
      >
        {{ formatMoney(balanceEuro) }}
        <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 inline-block h-6 w-6 align-[-0.2em]" />
      </p>
    </div>
  </section>
</template>
