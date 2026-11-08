import { ref, onUnmounted } from 'vue'
import { KeyboardWedgeScanner, type ScanError } from '@/utils/scanners/keyboardWedge'

export function usePaymentScanner(onSuccess: (uid: string) => void, customRegex?: RegExp) {
  const statusText = ref('Bitte NFC-Karte anhalten...')
  const errorMessage = ref<string | null>(null)
  const isListening = ref(false)

  const scanner = new KeyboardWedgeScanner({
    ...(customRegex ? { uidPattern: customRegex } : {})
  })

  let cleanupScan: (() => void) | null = null
  let cleanupError: (() => void) | null = null

  const start = () => {
    isListening.value = true
    statusText.value = 'Warte auf NFC-Karte...'
    errorMessage.value = null

    cleanupScan = scanner.onScan((uid) => {
      statusText.value = `Erkannt: ${uid}`
      onSuccess(uid)
      stop()
    })

    cleanupError = scanner.onError((err: ScanError) => {
      if (err === 'incomplete') {
        errorMessage.value = 'Übertragung unvollständig. Bitte nochmal.'
      } else {
        errorMessage.value = 'Ungültige Karte!'
      }
    })

    scanner.attach()
  }

  const stop = () => {
    isListening.value = false
    scanner.detach()
    if (cleanupScan) cleanupScan()
    if (cleanupError) cleanupError()
  }

  onUnmounted(() => {
    stop()
  })

  return {
    statusText,
    errorMessage,
    isListening,
    handleKey: scanner.handleKey, // Für das iPad-Input-Feld
    start,
    stop
  }
}