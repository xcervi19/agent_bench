/** Small presentation helpers shared by the list and workspace screens. */

const RELATIVE = new Intl.RelativeTimeFormat(undefined, { numeric: 'auto' })

const UNITS: [Intl.RelativeTimeFormatUnit, number][] = [
  ['second', 60],
  ['minute', 60],
  ['hour', 24],
  ['day', 7],
  ['week', 4.348],
  ['month', 12],
  ['year', Number.POSITIVE_INFINITY],
]

/** "3 minutes ago" — the list is scanned, not read, so absolute stamps go in `title`. */
export function relativeTime(iso: string, now: number = Date.now()): string {
  const then = Date.parse(iso)
  if (Number.isNaN(then)) return '—'
  let delta = (then - now) / 1000
  for (const [unit, span] of UNITS) {
    if (Math.abs(delta) < span) return RELATIVE.format(Math.round(delta), unit)
    delta /= span
  }
  return RELATIVE.format(Math.round(delta), 'year')
}

export function absoluteTime(iso: string): string {
  const parsed = Date.parse(iso)
  return Number.isNaN(parsed) ? iso : new Date(parsed).toLocaleString()
}

/** Elapsed wall-clock in a compact form ("4m 12s"). */
export function elapsed(fromIso: string, toIso?: string): string {
  const start = Date.parse(fromIso)
  const end = toIso ? Date.parse(toIso) : Date.now()
  if (Number.isNaN(start) || Number.isNaN(end) || end < start) return '—'
  const total = Math.floor((end - start) / 1000)
  const hours = Math.floor(total / 3600)
  const minutes = Math.floor((total % 3600) / 60)
  const seconds = total % 60
  if (hours) return `${hours}h ${minutes}m`
  if (minutes) return `${minutes}m ${seconds}s`
  return `${seconds}s`
}

export function formatUsd(value: unknown): string | null {
  return typeof value === 'number' && Number.isFinite(value) ? `$${value.toFixed(2)}` : null
}

export function formatDuration(ms: unknown): string | null {
  if (typeof ms !== 'number' || !Number.isFinite(ms)) return null
  return ms < 1000 ? `${Math.round(ms)}ms` : `${(ms / 1000).toFixed(1)}s`
}
