import { createContext, useContext } from 'react'
import type { SourceRef } from '../../lib/widgets/types'

/**
 * What widgets may read beyond their own payload.
 *
 * Source-backed widgets (`news-card`, `source-list`) reference `news.json` by
 * id rather than inlining source data, so the agent's markdown stays small and
 * a source is described in exactly one place.
 */
export interface WidgetContextValue {
  sources: Map<string, SourceRef>
}

export const WidgetContext = createContext<WidgetContextValue>({ sources: new Map() })

export function useWidgetContext(): WidgetContextValue {
  return useContext(WidgetContext)
}
