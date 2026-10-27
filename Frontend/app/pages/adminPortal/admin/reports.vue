<script setup lang="ts">
import { ref } from 'vue'

const selectedPeriod = ref('heute')

const summary = ref({
  totalRevenueEuro: '1.248,50',
  cashDepositsEuro: '430,00',
  transactionCount: 184,
  avgBasketEuro: '6,78'
})

const reports = ref([
  { id: 'REP-2026-09', title: 'Tagesabschluss Mensa (Kasse 1 & 2)', date: 'Heute, 14:00', type: 'PDF / Z-Bon', status: 'Bereit' },
  { id: 'REP-2026-08', title: 'Monatsabrechnung Verkäufe Gesamt', date: '01.09.2026 - 21.09.2026', type: 'CSV / Excel', status: 'Bereit' },
  { id: 'REP-2026-07', title: 'Bargeldeinzahlungen Terminal', date: '15.09.2026', type: 'PDF', status: 'Archiviert' }
])

const downloadReport = (title: string) => {
  alert(`Download gestartet: ${title}`)
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-xl font-bold text-gray-900">Abrechnung & Berichte</h1>
        <p class="text-xs text-gray-500">Tagesabschlüsse (Z-Bon), Monatsberichte und Daten-Exports für die Buchhaltung</p>
      </div>
      
      <div class="flex gap-2">
        <button 
          @click="downloadReport('Tagesabschluss_Heute.pdf')"
          class="flex items-center gap-2 rounded-lg bg-teal-600 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-700"
        >
          <Icon name="material-symbols:download" class="h-4 w-4" />
          Tagesabschluss (Z-Bon) Exportieren
        </button>
      </div>
    </div>

    <!-- Übersichtskacheln für den gewählten Zeitraum -->
    <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <p class="text-xs font-medium text-gray-500">Gesamteinnahmen Mensa</p>
        <p class="mt-1 flex items-center text-xl font-extrabold text-gray-900">
          {{ summary.totalRevenueEuro }}
          <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-5 w-5" />
        </p>
      </div>
      <div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <p class="text-xs font-medium text-gray-500">Bargeld-Einzahlungen</p>
        <p class="mt-1 flex items-center text-xl font-extrabold text-blue-600">
          {{ summary.cashDepositsEuro }}
          <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-5 w-5" />
        </p>
      </div>
      <div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <p class="text-xs font-medium text-gray-500">Anzahl Buchungen</p>
        <p class="mt-1 text-xl font-extrabold text-gray-900">{{ summary.transactionCount }}</p>
      </div>
      <div class="rounded-xl border border-gray-200 bg-white p-4 shadow-sm">
        <p class="text-xs font-medium text-gray-500">Ø Bon-Betrag</p>
        <p class="mt-1 flex items-center text-xl font-extrabold text-gray-900">
          {{ summary.avgBasketEuro }}
          <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 h-5 w-5" />
        </p>
      </div>
    </div>

    <!-- Tabelle der verfügbaren Exports -->
    <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 class="mb-4 text-base font-bold text-gray-900">Verfügbare Berichte & Dateiexporte</h2>
      
      <div class="overflow-x-auto">
        <table class="w-full text-left text-sm">
          <thead class="border-b border-gray-200 bg-gray-50 text-xs uppercase text-gray-500">
            <tr>
              <th class="py-3 px-3">Bericht</th>
              <th class="py-3 px-3">Zeitraum / Datum</th>
              <th class="py-3 px-3">Format</th>
              <th class="py-3 px-3 text-right">Aktion</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 text-gray-700">
            <tr v-for="rep in reports" :key="rep.id" class="hover:bg-gray-50">
              <td class="py-3 px-3 font-medium text-gray-900">
                {{ rep.title }}
                <div class="text-xs font-normal text-gray-400">{{ rep.id }}</div>
              </td>
              <td class="py-3 px-3 text-xs text-gray-600">{{ rep.date }}</td>
              <td class="py-3 px-3">
                <span class="rounded bg-gray-100 px-2 py-1 text-xs font-mono font-medium text-gray-700">
                  {{ rep.type }}
                </span>
              </td>
              <td class="py-3 px-3 text-right">
                <button 
                  @click="downloadReport(rep.title)"
                  class="inline-flex items-center gap-1 text-xs font-semibold text-teal-600 hover:underline"
                >
                  <Icon name="material-symbols:download" class="h-4 w-4" />
                  Herunterladen
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>