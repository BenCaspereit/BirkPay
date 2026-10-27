<script setup lang="ts">
// Dummydaten für das Dashboard (später durch API-Calls / Pinia Store ersetzbar)

const stats = ref([
  {
    title: 'Tagesumsatz Mensa & Kasse',
    value: '1.248,50',
    isMoney: true,
    subtitle: '184 Verkäufe heute',
    subtitleColor: 'text-emerald-600',
    icon: 'material-symbols:point-of-sale',
    bgIcon: 'bg-emerald-50 text-emerald-600',
    to: '/pos/sales'
  },
  {
    title: 'Gesamtguthaben im System',
    value: '14.820,00',
    isMoney: true,
    subtitle: 'Verteilt auf 620 Konten',
    subtitleColor: 'text-teal-600',
    icon: 'material-symbols:account-balance-wallet-outline',
    bgIcon: 'bg-teal-50 text-teal-600',
    to: '/admin/users'
  },
  {
    title: 'Bank-Auszahlungen heute',
    value: '430,00',
    isMoney: true,
    subtitle: '12 Gehälter / Einzahlungen',
    subtitleColor: 'text-blue-600',
    icon: 'material-symbols:payments-outline',
    bgIcon: 'bg-blue-50 text-blue-600',
    to: '/bank/payout'
  },
  {
    title: 'Inaktive / Gesperrte Karten',
    value: '3',
    isMoney: false,
    subtitle: 'Handlungsbedarf bei 3 Konten',
    subtitleColor: 'text-amber-600',
    icon: 'material-symbols:credit-card-off-outline',
    bgIcon: 'bg-amber-50 text-amber-600',
    to: '/admin/users'
  }
])

const recentTransactions = ref([
  { id: 'TX-9021', terminal: 'Mensa Kasse 1', item: 'Tagesgericht (Pasta)', amountEuro: '-4,50', time: 'Vor 3 Min.', status: 'Erfolgreich' },
  { id: 'TX-9020', terminal: 'Kiosk / Snack', item: 'Apfelschorle 0.5l', amountEuro: '-1,50', time: 'Vor 8 Min.', status: 'Erfolgreich' },
  { id: 'TX-9019', terminal: 'Mensa Kasse 2', item: 'Vegetarisches Menü', amountEuro: '-4,50', time: 'Vor 12 Min.', status: 'Erfolgreich' },
  { id: 'TX-9018', terminal: 'Mensa Kasse 1', item: 'NFC-Karte nicht ausreichend gedeckt', amountEuro: '0,00', time: 'Vor 25 Min.', status: 'Fehlgeschlagen' }
])

const bankPayouts = ref([
  { id: 'BK-4401', user: 'Max Mustermann (Schüler-GmbH)', purpose: 'Gehaltsauszahlung', amountEuro: '+25,00', date: 'Heute, 11:20 Uhr' },
  { id: 'BK-4400', user: 'Anna Schmidt (Klasse 9b)', purpose: 'Bareinzahlung Terminal', amountEuro: '+50,00', date: 'Heute, 10:05 Uhr' },
  { id: 'BK-4399', user: 'Leon Weber (Klasse 10a)', purpose: 'Rückzahlung Restguthaben', amountEuro: '-15,00', date: 'Gestern' }
])
</script>

<template>
  <div>
    <header class="mb-6 flex items-center gap-3 rounded-2xl border border-purple-100 bg-purple-50 p-4 sm:p-5">
      <img src="/birkling.svg" alt="" class="h-12 w-12 shrink-0" />
      <div>
        <p class="text-xs font-bold uppercase tracking-wide text-purple-700">BirkPay</p>
        <h1 class="mt-0.5 text-xl font-bold text-gray-950">Verwaltungsübersicht</h1>
      </div>
    </header>

    <!-- KPI-Kacheln Grid -->
    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
      <NuxtLink 
        v-for="stat in stats"
        :key="stat.title"
        :to="stat.to" 
        class="flex items-center justify-between rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition-shadow hover:shadow-md"
      >
        <div>
          <p class="text-xs font-semibold uppercase tracking-wider text-gray-500">{{ stat.title }}</p>
          <p class="mt-1 flex items-center text-2xl font-bold text-gray-900">
            {{ stat.value }}
            <Icon v-if="stat.isMoney" name="bitcoin-icons:bitcoin-filled" class="ml-1 h-6 w-6" />
          </p>
          <div class="mt-2 flex items-center text-xs font-medium" :class="stat.subtitleColor">
            <span>{{ stat.subtitle }}</span>
          </div>
        </div>
        <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg" :class="stat.bgIcon">
          <Icon :name="stat.icon" class="h-6 w-6" />
        </div>
      </NuxtLink>
    </div>

    <!-- Listen- / Tabellen-Bereich -->
    <div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
      
      <!-- Linke Spalte: Letchte Kassen-Transaktionen -->
      <div class="flex flex-col justify-between rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <div>
          <div class="mb-4 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <h2 class="text-base font-bold text-gray-900">Letzte Verkäufe & Kasse</h2>
              <span class="rounded-full bg-teal-50 px-2 py-0.5 text-xs font-semibold text-teal-700">Echtzeit</span>
            </div>
            <NuxtLink to="/pos/sales" class="text-xs font-semibold text-teal-600 hover:underline">
              Alle Umsätze
            </NuxtLink>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
              <thead class="border-b border-gray-100 bg-gray-50/50 text-xs uppercase text-gray-400">
                <tr>
                  <th class="py-2.5 px-2 font-medium">Terminal</th>
                  <th class="py-2.5 px-2 font-medium">Posten</th>
                  <th class="py-2.5 px-2 font-medium">Zeit</th>
                  <th class="py-2.5 px-2 font-medium text-right">Betrag</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 text-gray-600">
                <tr 
                  v-for="tx in recentTransactions" 
                  :key="tx.id"
                  class="group transition-colors hover:bg-gray-50/80"
                >
                  <td class="py-3 px-2 font-medium text-gray-900">
                    {{ tx.terminal }}
                  </td>
                  <td class="py-3 px-2 text-xs text-gray-600">
                    {{ tx.item }}
                  </td>
                  <td class="py-3 px-2 whitespace-nowrap text-xs text-gray-400">
                    {{ tx.time }}
                  </td>
                  <td class="py-3 px-2 text-right font-semibold whitespace-nowrap" :class="tx.status === 'Fehlgeschlagen' ? 'text-red-500 line-through' : 'text-gray-900'">
                    {{ tx.amountEuro }}
                    <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 inline-block h-4 w-4 align-[-0.2em]" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="mt-4 border-t border-gray-100 pt-3 text-right">
          <NuxtLink to="/pos" class="inline-flex items-center text-xs font-semibold text-teal-600 hover:text-teal-800">
            <Icon name="material-symbols:point-of-sale" class="mr-1 h-4 w-4" /> Kassen-Terminal öffnen
          </NuxtLink>
        </div>
      </div>

      <!-- Rechte Spalte: Bank & Transaktionen -->
      <div class="flex flex-col justify-between rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
        <div>
          <div class="mb-4 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <h2 class="text-base font-bold text-gray-900">Bank-Aktivitäten & Einzahlungen</h2>
              <span class="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-700">Bank</span>
            </div>
            <NuxtLink to="/bank/accounts" class="text-xs font-semibold text-blue-600 hover:underline">
              Kontenübersicht
            </NuxtLink>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
              <thead class="border-b border-gray-100 bg-gray-50/50 text-xs uppercase text-gray-400">
                <tr>
                  <th class="py-2.5 px-2 font-medium">Inhaber / Ziel</th>
                  <th class="py-2.5 px-2 font-medium">Zweck</th>
                  <th class="py-2.5 px-2 font-medium text-right">Betrag</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 text-gray-600">
                <tr 
                  v-for="payout in bankPayouts" 
                  :key="payout.id"
                  class="group transition-colors hover:bg-gray-50/80"
                >
                  <td class="py-3 px-2 font-medium text-gray-900">
                    {{ payout.user }}
                    <div class="text-[10px] text-gray-400 font-normal">{{ payout.date }}</div>
                  </td>
                  <td class="py-3 px-2 text-xs text-gray-500">
                    {{ payout.purpose }}
                  </td>
                  <td class="py-3 px-2 text-right font-semibold whitespace-nowrap" :class="payout.amountEuro.startsWith('+') ? 'text-emerald-600' : 'text-gray-900'">
                    {{ payout.amountEuro }}
                    <Icon name="bitcoin-icons:bitcoin-filled" class="ml-1 inline-block h-4 w-4 align-[-0.2em]" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="mt-4 border-t border-gray-100 pt-3 text-right">
          <NuxtLink to="/bank/payout" class="inline-flex items-center text-xs font-semibold text-blue-600 hover:text-blue-800">
            <Icon name="material-symbols:payments-outline" class="mr-1 h-4 w-4" /> Neue Auszahlung vornehmen
          </NuxtLink>
        </div>
      </div>

    </div>
  </div>
</template>