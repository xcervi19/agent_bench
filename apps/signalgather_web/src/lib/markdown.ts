/**
 * Markdown → sanitized HTML for agent-written artifacts (`intro.md`).
 *
 * The content is produced by an LLM, so it is untrusted input by definition and
 * always goes through DOMPurify.
 *
 * This handles **prose only**. Widgets are extracted before this runs and
 * rendered as React components — see `components/ArtifactMarkdown.tsx`. Do not
 * whitelist component tags here to make them render: that re-creates the
 * per-output-type coupling the widget registry exists to remove.
 */

import DOMPurify from 'dompurify'
import { marked } from 'marked'

marked.setOptions({ gfm: true, breaks: false })

export function renderMarkdown(source: string): string {
  const html = marked.parse(source, { async: false })
  return DOMPurify.sanitize(html, {
    ADD_ATTR: ['target', 'rel'],
    FORBID_TAGS: ['style', 'form', 'input', 'button'],
    FORBID_ATTR: ['style'],
  })
}
