/**
 * Turn `[s01]` / `[s03, s09]` markers into links to the source list.
 *
 * This closes open decision #4 of the spec ("resolve [s01] to source URLs in
 * UI"). `report.md` cites `news.json#sources[].id`, and until now those markers
 * were dead text.
 *
 * It runs on **sanitized** HTML, walking text nodes only, so it cannot
 * reintroduce markup DOMPurify removed and cannot rewrite anything inside
 * `<code>`, `<pre>` or an existing link.
 */

import type { SourceRef } from './widgets/types'

/** `[s01]`, `[s01, s03]`, `[s01; s03]` — ids are `s` + digits, per the contract. */
const CITATION = /\[((?:s\d{1,3})(?:\s*[,;]\s*s\d{1,3})*)\]/gi

const SKIP_INSIDE = new Set(['CODE', 'PRE', 'A', 'SCRIPT', 'STYLE', 'TEXTAREA'])

/** DOM id for a source row, so a citation can link to it. */
export function sourceAnchorId(sourceId: string): string {
  return `src-${sourceId.toLowerCase()}`
}

export interface CitationOptions {
  /** Known sources. A citation with no matching source renders unlinked. */
  sources?: Map<string, SourceRef>
}

export function linkCitations(html: string, options: CitationOptions = {}): string {
  const { sources } = options
  const doc = new DOMParser().parseFromString(`<div id="root">${html}</div>`, 'text/html')
  const root = doc.getElementById('root')
  if (!root) return html

  const walker = doc.createTreeWalker(root, NodeFilter.SHOW_TEXT)
  const targets: Text[] = []
  let node = walker.nextNode()
  while (node) {
    const text = node as Text
    if (CITATION.test(text.data) && !hasAncestor(text, SKIP_INSIDE)) targets.push(text)
    CITATION.lastIndex = 0
    node = walker.nextNode()
  }

  for (const text of targets) replaceIn(doc, text, sources)
  return root.innerHTML
}

function hasAncestor(node: Node, tags: Set<string>): boolean {
  let current = node.parentElement
  while (current) {
    if (tags.has(current.tagName)) return true
    current = current.parentElement
  }
  return false
}

function replaceIn(doc: Document, text: Text, sources?: Map<string, SourceRef>): void {
  const fragment = doc.createDocumentFragment()
  let cursor = 0
  CITATION.lastIndex = 0

  for (const match of text.data.matchAll(CITATION)) {
    const start = match.index
    if (start > cursor) {
      fragment.appendChild(doc.createTextNode(text.data.slice(cursor, start)))
    }
    fragment.appendChild(doc.createTextNode('['))
    const ids = (match[1] ?? '').split(/[,;]/).map((id) => id.trim())
    ids.forEach((id, index) => {
      if (index > 0) fragment.appendChild(doc.createTextNode(', '))
      fragment.appendChild(citationNode(doc, id, sources))
    })
    fragment.appendChild(doc.createTextNode(']'))
    cursor = start + match[0].length
  }

  if (cursor < text.data.length) {
    fragment.appendChild(doc.createTextNode(text.data.slice(cursor)))
  }
  text.replaceWith(fragment)
}

function citationNode(doc: Document, id: string, sources?: Map<string, SourceRef>): Node {
  const source = sources?.get(id.toLowerCase())
  if (!source) {
    // Cited but absent from news.json — show it, don't pretend it resolves.
    const span = doc.createElement('span')
    span.className = 'citation citation-missing'
    span.setAttribute('title', `${id} is cited but not present in this run's sources`)
    span.textContent = id
    return span
  }
  const link = doc.createElement('a')
  link.className = 'citation'
  link.setAttribute('href', `#${sourceAnchorId(id)}`)
  link.setAttribute('title', [source.title, source.publisher].filter(Boolean).join(' — ') || id)
  link.textContent = id
  return link
}

/** Index news.json sources by lowercased id for citation and widget lookup. */
export function indexSources(sources: SourceRef[] | undefined): Map<string, SourceRef> {
  const map = new Map<string, SourceRef>()
  for (const source of sources ?? []) {
    if (source?.id) map.set(source.id.toLowerCase(), source)
  }
  return map
}
