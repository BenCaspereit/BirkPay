interface CheckoutPayload {
  nfc_uid: string
  items: Array<{
    product_id: number
    quantity: number
  }>
}

const isCheckoutPayload = (value: unknown): value is CheckoutPayload => {
  if (typeof value !== 'object' || value === null || !('nfc_uid' in value) || !('items' in value)) {
    return false
  }

  const payload = value as { nfc_uid: unknown; items: unknown }
  return typeof payload.nfc_uid === 'string'
    && payload.nfc_uid.trim().length > 0
    && Array.isArray(payload.items)
    && payload.items.length > 0
    && payload.items.every(item =>
      typeof item === 'object'
      && item !== null
      && 'product_id' in item
      && 'quantity' in item
      && Number.isInteger(item.product_id)
      && Number.isInteger(item.quantity)
      && item.product_id > 0
      && item.quantity > 0
    )
}

const getUpstreamMessage = (error: unknown): string => {
  if (typeof error === 'object' && error !== null && '_data' in error) {
    const data = error._data
    if (typeof data === 'object' && data !== null && 'detail' in data) {
      const detail = data.detail
      if (typeof detail === 'string') return detail
      if (typeof detail === 'object' && detail !== null && 'message' in detail) {
        const message = detail.message
        if (typeof message === 'string') return message
      }
    }
  }

  return error instanceof Error ? error.message : 'Der Zahlungsdienst konnte nicht kontaktiert werden.'
}

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig(event)
  const backendBaseUrl = config.backendBaseUrl.trim().replace(/\/+$/, '')
  const cashierNfcUid = config.cashierNfcUid.trim()

  if (!backendBaseUrl || !cashierNfcUid) {
    throw createError({
      statusCode: 503,
      statusMessage: 'Der Zahlungsdienst ist nicht konfiguriert.'
    })
  }

  const payload: unknown = await readBody(event)
  if (!isCheckoutPayload(payload)) {
    throw createError({
      statusCode: 400,
      statusMessage: 'Ungültige Zahlungsdaten.'
    })
  }

  try {
    return await $fetch(`${backendBaseUrl}/api/v1/transactions/checkout`, {
      method: 'POST',
      headers: {
        'X-NFC-Key': cashierNfcUid
      },
      body: payload
    })
  } catch (error) {
    throw createError({
      statusCode: 502,
      statusMessage: getUpstreamMessage(error)
    })
  }
})
