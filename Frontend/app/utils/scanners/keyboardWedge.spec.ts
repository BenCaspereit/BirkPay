import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { KeyboardWedgeScanner } from './keyboardWedge'

// Statt des Browser-KeyboardEvents nutzen wir ein simples Objekt mit der key-Eigenschaft
const key = (k: string) => ({ key: k } as KeyboardEvent)

const type = (s: string, sc: KeyboardWedgeScanner) =>
  [...s].forEach(c => sc.handleKey(key(c)))

describe('KeyboardWedgeScanner', () => {
  beforeEach(() => vi.useFakeTimers())
  afterEach(() => vi.useRealTimers())

  it('liefert gültige UID', () => {
    const sc = new KeyboardWedgeScanner()
    const onScan = vi.fn()
    sc.onScan(onScan)
    type('04A1B2C3', sc); sc.handleKey(key('Enter'))
    expect(onScan).toHaveBeenCalledWith('04A1B2C3')
  })

  it('meldet incomplete, wenn nur die Hälfte ankommt', () => {
    const sc = new KeyboardWedgeScanner()
    const onError = vi.fn()
    sc.onError(onError)
    type('04A1', sc)
    vi.advanceTimersByTime(150)
    expect(onError).toHaveBeenCalledWith('incomplete', '04A1')
  })

  it('verwirft den Buffer, sodass der nächste Scan sauber ist', () => {
    const sc = new KeyboardWedgeScanner()
    const onScan = vi.fn()
    sc.onScan(onScan)
    type('04A1', sc)
    vi.advanceTimersByTime(150)
    type('04A1B2C3', sc); sc.handleKey(key('Enter'))
    expect(onScan).toHaveBeenCalledWith('04A1B2C3')  // nicht '04A104A1B2C3'
  })

  it('meldet invalid bei falscher Länge mit Enter', () => {
    const sc = new KeyboardWedgeScanner()
    const onError = vi.fn()
    sc.onError(onError)
    type('04A1B2', sc); sc.handleKey(key('Enter'))
    expect(onError).toHaveBeenCalledWith('invalid', '04A1B2')
  })
})