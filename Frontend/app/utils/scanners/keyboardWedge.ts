// app/utils/scanners/keyboardWedge.ts
export type ScanError = 'incomplete' | 'invalid'

interface Options {
  terminator?: string          // 'Enter'
  interCharTimeoutMs?: number  // max. Pause zwischen Zeichen
  uidPattern?: RegExp          // z. B. /^[0-9A-F]{8}$|^[0-9A-F]{14}$/
}

export class KeyboardWedgeScanner {
  private buffer = ''
  private timer?: ReturnType<typeof setTimeout>
  private scanCbs = new Set<(uid: string) => void>()
  private errorCbs = new Set<(e: ScanError, partial: string) => void>()

  constructor(private opts: Options = {}) {
    this.opts = {
      terminator: 'Enter',
      interCharTimeoutMs: 150,
      uidPattern: /^(?:[0-9A-F]{8}|[0-9A-F]{14})$/,
      ...opts,
    }
  }

  handleKey = (e: KeyboardEvent) => {
    if (e.key === this.opts.terminator) {
      this.finish()
      return
    }
    if (e.key.length !== 1) return   // Shift, Ctrl etc. ignorieren
    this.buffer += e.key.toUpperCase()
    clearTimeout(this.timer)
    this.timer = setTimeout(() => this.abort(), this.opts.interCharTimeoutMs)
  }

  private finish() {
    clearTimeout(this.timer)
    const value = this.buffer
    this.buffer = ''
    if (!value) return
    if (this.opts.uidPattern!.test(value)) this.scanCbs.forEach(cb => cb(value))
    else this.errorCbs.forEach(cb => cb('invalid', value))
  }

  private abort() {
    const partial = this.buffer
    this.buffer = ''
    if (partial) this.errorCbs.forEach(cb => cb('incomplete', partial))
  }

  onScan(cb: (uid: string) => void) { this.scanCbs.add(cb); return () => this.scanCbs.delete(cb) }
  onError(cb: (e: ScanError, partial: string) => void) { this.errorCbs.add(cb); return () => this.errorCbs.delete(cb) }

  attach() { 
    if (typeof window !== 'undefined') {
      window.addEventListener('keydown', this.handleKey) 
    }
  }
  
  detach() { 
    if (typeof window !== 'undefined') {
      window.removeEventListener('keydown', this.handleKey) 
    }
  }
}