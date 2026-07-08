import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { formatDistanceToNow, parseISO } from 'date-fns'
import type { NewsSource } from './types'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatRelativeTime(iso: string | null | undefined): string {
  if (!iso) return '—'
  try {
    return formatDistanceToNow(parseISO(iso), { addSuffix: true })
  } catch {
    return iso
  }
}

export function truncate(text: string, max = 120): string {
  if (text.length <= max) return text
  return `${text.slice(0, max).trim()}…`
}

export function buildSourceMap(sources: NewsSource[]): Map<string, NewsSource> {
  return new Map(sources.map((s) => [s.id, s]))
}

export function resolveCitations(
  markdown: string,
  sourceMap: Map<string, NewsSource>,
): string {
  return markdown.replace(/\[([a-z]\d+)\]/gi, (_match, id: string) => {
    const source = sourceMap.get(id.toLowerCase()) ?? sourceMap.get(id)
    if (!source) return `[${id}]`
    const label = source.publisher ?? source.title.slice(0, 30)
    return `[${label}](${source.url})`
  })
}

export function scorePercent(score: number | undefined): string {
  if (score === undefined || score === null) return '—'
  return `${Math.round(score * 100)}%`
}

export function elapsedSince(iso: string): string {
  try {
    const start = parseISO(iso)
    const ms = Date.now() - start.getTime()
    const mins = Math.floor(ms / 60000)
    if (mins < 1) return '<1m'
    if (mins < 60) return `${mins}m`
    const hours = Math.floor(mins / 60)
    if (hours < 24) return `${hours}h ${mins % 60}m`
    return `${Math.floor(hours / 24)}d`
  } catch {
    return '—'
  }
}
