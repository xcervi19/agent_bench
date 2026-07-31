import type { SourceRef } from './widgets/types'

const AUTHORITATIVE_CLASSES = new Set(['primary_official', 'data_feed'])

export interface SourceMix {
  total: number
  authoritative: number
  entirelySecondary: boolean
}

export function isAuthoritative(source: SourceRef): boolean {
  return AUTHORITATIVE_CLASSES.has(source.source_class ?? '')
}

export function summarizeSources(sources: SourceRef[] | undefined): SourceMix {
  const rows = sources ?? []
  const authoritative = rows.filter(isAuthoritative).length
  return {
    total: rows.length,
    authoritative,
    entirelySecondary: rows.length > 0 && authoritative === 0,
  }
}
