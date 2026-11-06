<script setup lang="ts">

const { t } = useI18n({
  useScope: 'local',
  inheritLocale: true,
  messages: {
    de: {
      account: 'Konto',
      accountbalance: 'Kontostand'
    },
    en: {
      account: 'Account',
      accountbalance: 'Balance'
    }
  }
})

const props = withDefaults(
  defineProps<{
    name?: string
    balanceEuro?: number
  }>(),
  {
    name: 'Unbekannt',
    balanceEuro: 0
  }
)

const formattedName = computed(() => {
  const parts = props.name.trim().split(/\s+/).filter(Boolean)
  const firstName = parts[0]
  if (!firstName || parts.length <= 1) return props.name
  const lastName = parts.at(-1)
  if (!lastName) return firstName
  const lastNameInitial = lastName.charAt(0)
  return `${firstName} ${lastNameInitial}.`
})

const formatMoney = (amountEuro: number) =>
  new Intl.NumberFormat('de-DE', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amountEuro)
</script>

<template>
  <section class="overflow-hidden rounded-[1.75rem] bg-gradient-to-br from-indigo-600 via-violet-600 to-purple-500 p-[1px] shadow-[0_18px_40px_rgba(91,92,226,0.25)]">
    <div class="rounded-[1.7rem] bg-[radial-gradient(circle_at_top_left,rgba(255,255,255,0.28),transparent_38%),linear-gradient(135deg,rgba(91,92,226,0.97),rgba(139,109,255,0.93))] p-4 text-white sm:p-5">
      <div class="flex items-start justify-between gap-3">
        <div>
          <p class="text-[0.62rem] font-semibold uppercase tracking-[0.18em] text-white/70">{{ t('account') }}</p>
          <h2 class="mt-2 text-xl font-bold leading-tight">{{ formattedName }}</h2>
        </div>

      </div>

      <div class="mt-5 flex items-end justify-between gap-3">
        <div>
          <p class="text-[0.62rem] uppercase tracking-[0.16em] text-white/70">{{ t('accountbalance') }}</p>
          <p class="mt-2 flex items-center gap-1.5 text-3xl font-black tracking-tight tabular-nums">
            {{ formatMoney(balanceEuro) }}
            <Icon name="bitcoin-icons:bitcoin-filled" class="h-7 w-7 shrink-0" aria-label="Bitcoin" />
          </p>
        </div>
      </div>
    </div>
  </section>
</template>
