<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { usePaymentScanner } from '@/composables/usePaymentScanner'

type PaymentState = 'waiting' | 'success' | 'error'

const props = withDefaults(defineProps<{
  open: boolean
  state: PaymentState
  amountEuro: string
  errorMessage: string
  testMode: boolean
}>(), {
  testMode: false
})

const emit = defineEmits<{
  (event: 'cancel'): void
  (event: 'retry'): void
  (event: 'close'): void
  (event: 'scan', uid: string): void // Neu: Überträgt die Kartennummer nach oben
}>()

const hiddenInputRef = ref<HTMLInputElement | null>(null)

// Scanner-Composable einbinden
const { handleKey, start, stop } = usePaymentScanner((uid) => {
  emit('scan', uid)
})

// Überwachen, ob das Modal sich öffnet und im 'waiting'-Status ist
watch(
  () => [props.open, props.state],
  async ([isOpen, currentState]) => {
    if (isOpen && currentState === 'waiting') {
      start()
      await nextTick()
      // Verstecktes Input-Feld fokussieren, damit das iPad die Bluetooth-Tastatur-Events abfängt
      hiddenInputRef.value?.focus()
    } else {
      stop()
    }
  },
  { immediate: true }
)
</script>

<template>
  <div
    v-if="open"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
    role="presentation"
  >
    <!-- WICHTIG FÜR IPAD / SAFARI:
         Dieses unsichtbare Input-Feld fängt die Bluetooth-HID-Signale ab, 
         ohne dass eine störende Bildschirmtastatur auf dem iPad hochklappt. -->
    <input
      ref="hiddenInputRef"
      type="text"
      class="opacity-0 absolute -left-[9999px]"
      @keydown.stop="handleKey"
      tabindex="-1"
      aria-hidden="true"
    />

    <section
      class="w-full max-w-sm rounded-xl bg-white p-6 text-center shadow-xl"
      role="dialog"
      aria-modal="true"
      aria-labelledby="payment-modal-title"
      aria-live="polite"
    >
      <template v-if="state === 'waiting'">
        <Icon name="material-symbols:contactless" class="mx-auto h-14 w-14 animate-pulse text-teal-600" />
        <h2 id="payment-modal-title" class="mt-3 text-xl font-bold text-gray-900">
          Warte auf Karte
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          Bitte halte die BirkPay-Karte an das Terminal.
        </p>
        <p v-if="testMode" class="mt-2 text-xs font-medium text-amber-700">
          Testmodus: Die Zahlung wird ohne Karten-Scan simuliert.
        </p>
        <button
          @click="emit('cancel')"
          class="mt-6 w-full rounded-lg border border-gray-300 px-4 py-3 font-semibold text-gray-700 hover:bg-gray-50"
        >
          Abbrechen
        </button>
      </template>

      <template v-else-if="state === 'success'">
        <Icon name="material-symbols:check-circle" class="mx-auto h-14 w-14 text-emerald-600" />
        <h2 id="payment-modal-title" class="mt-3 text-xl font-bold text-gray-900">
          Zahlung erfolgreich!
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          {{ amountEuro }}
          <Icon name="bitcoin-icons:bitcoin-filled" class="mx-1 inline-block h-4 w-4 align-[-0.2em]" />
          wurden vom Konto abgebucht.
        </p>
        <button
          @click="emit('close')"
          class="mt-6 w-full rounded-lg bg-teal-600 px-4 py-3 font-semibold text-white hover:bg-teal-700"
        >
          Schließen
        </button>
      </template>

      <template v-else>
        <Icon name="material-symbols:error" class="mx-auto h-14 w-14 text-red-600" />
        <h2 id="payment-modal-title" class="mt-3 text-xl font-bold text-gray-900">
          Zahlung fehlgeschlagen
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          {{ errorMessage || 'Die Zahlung konnte nicht verarbeitet werden.' }}
        </p>
        <div class="mt-6 flex gap-3">
          <button
            @click="emit('close')"
            class="flex-1 rounded-lg border border-gray-300 px-4 py-3 font-semibold text-gray-700 hover:bg-gray-50"
          >
            Schließen
          </button>
          <button
            @click="emit('retry')"
            class="flex-1 rounded-lg bg-teal-600 px-4 py-3 font-semibold text-white hover:bg-teal-700"
          >
            Erneut versuchen
          </button>
        </div>
      </template>
    </section>
  </div>
</template>