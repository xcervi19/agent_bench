/**
 * How a `[s04]` click in the report reaches the source it cites.
 *
 * `linkCitations` renders every citation as `<a href="#src-s04">`, but the
 * anchor is emitted by `SourceCard`, which only mounts in two places: the
 * Sources tab, and a `news-card` widget inside the report body. Tabs render
 * conditionally, so while the reader is on Report the Sources panel is not in
 * the DOM at all and the plain anchor jump silently does nothing.
 *
 * So a citation whose card is already on screen (it has a widget) keeps the
 * native in-place jump, and one whose card lives on the Sources tab is
 * intercepted here: switch tab, then scroll to it once the panel has mounted.
 */
import { createContext, useCallback, useContext, useEffect, useRef } from 'react'
import { sourceAnchorId } from './citations'

export type CitationNavigate = (sourceId: string) => void

/** Undefined by default, so a surface with no tabs keeps plain anchor behaviour. */
export const CitationNavContext = createContext<CitationNavigate | undefined>(undefined)

export function useCitationNav(): CitationNavigate | undefined {
  return useContext(CitationNavContext)
}

/**
 * Wire citation clicks to a tabbed surface.
 *
 * `select` switches the tab; the scroll waits for `activeTab` to actually be the
 * sources tab, because the panel — and therefore the anchor — does not exist
 * until that render has committed.
 */
export function useCitationNavigation<T extends string>(
  sourcesTab: T,
  activeTab: T | undefined,
  select: (tab: T) => void,
): CitationNavigate {
  // A ref, not state: the tab change is what re-runs the effect, so the pending
  // target never needs to cause a render of its own.
  const pending = useRef<string | null>(null)

  const reveal = useCallback((sourceId: string): boolean => {
    const element = document.getElementById(sourceAnchorId(sourceId))
    if (!element) return false
    element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    // Which row was meant is otherwise invisible in a long list. Cleared on
    // animationend rather than a timer, so it always plays exactly once.
    element.classList.add('citation-target')
    element.addEventListener('animationend', () => element.classList.remove('citation-target'), {
      once: true,
    })
    return true
  }, [])

  const navigate = useCallback(
    (sourceId: string) => {
      // Already looking at the list (or at a card rendered inline) — just move.
      if (activeTab === sourcesTab && reveal(sourceId)) return
      pending.current = sourceId
      select(sourcesTab)
    },
    [activeTab, sourcesTab, select, reveal],
  )

  useEffect(() => {
    if (activeTab !== sourcesTab) return
    const target = pending.current
    if (!target) return
    pending.current = null
    reveal(target)
  }, [activeTab, sourcesTab, reveal])

  return navigate
}
