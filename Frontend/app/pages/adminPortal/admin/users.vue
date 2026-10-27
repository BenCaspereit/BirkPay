<script setup lang="ts">
import { ref } from 'vue'

const users = ref([
  { id: 'CARD-1001', name: 'Mia Müller', class: 'Klasse 8a', balanceEuro: 12.50, limitEuro: 10, status: 'Aktiv' },
  { id: 'CARD-1002', name: 'Noah Becker', class: 'Klasse 10c', balanceEuro: 0.00, limitEuro: 5, status: 'Gesperrt' },
  { id: 'CARD-1003', name: 'Sophia Hoffmann', class: 'Klasse 6b', balanceEuro: 34.00, limitEuro: 15, status: 'Aktiv' },
])

const toggleStatus = (user: typeof users.value[0]) => {
  user.status = user.status === 'Aktiv' ? 'Gesperrt' : 'Aktiv'
}
</script>

<template>
  <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
    <div class="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-xl font-bold text-gray-900">Schüler & Kartenverwaltung</h1>
        <p class="text-xs text-gray-500">Konto-Status einsehen, Karten sperren und Tageslimits verwalten</p>
      </div>
      <button class="rounded-lg bg-teal-600 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-700">
        + Neue Karte verknüpfen
      </button>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm">
        <thead class="border-b border-gray-200 bg-gray-50 text-xs uppercase text-gray-500">
          <tr>
            <th class="py-3 px-3">Karten-ID / Name</th>
            <th class="py-3 px-3">Klasse</th>
            <th class="py-3 px-3">Guthaben</th>
            <th class="py-3 px-3">Tageslimit</th>
            <th class="py-3 px-3">Status</th>
            <th class="py-3 px-3 text-right">Aktion</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 text-gray-700">
          <tr v-for="u in users" :key="u.id" class="hover:bg-gray-50">
            <td class="py-3 px-3 font-medium text-gray-900">
              {{ u.name }}
              <div class="text-xs font-normal text-gray-400">{{ u.id }}</div>
            </td>
            <td class="py-3 px-3 text-xs">{{ u.class }}</td>
            <td class="py-3 px-3 font-semibold text-teal-700">
              {{ u.balanceEuro.toFixed(2) }}
              <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 inline-block h-4 w-4 align-[-0.2em]" />
            </td>
            <td class="py-3 px-3 text-xs">
              {{ u.limitEuro }}
              <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 inline-block h-3.5 w-3.5 align-[-0.2em]" />
              / Tag
            </td>
            <td class="py-3 px-3">
              <span 
                class="rounded-full px-2.5 py-0.5 text-xs font-medium"
                :class="u.status === 'Aktiv' ? 'bg-emerald-50 text-emerald-700' : 'bg-red-50 text-red-700'"
              >
                {{ u.status }}
              </span>
            </td>
            <td class="py-3 px-3 text-right">
              <button 
                @click="toggleStatus(u)"
                class="text-xs font-semibold underline"
                :class="u.status === 'Aktiv' ? 'text-red-600 hover:text-red-800' : 'text-emerald-600 hover:text-emerald-800'"
              >
                {{ u.status === 'Aktiv' ? 'Karte Sperren' : 'Entsperren' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>