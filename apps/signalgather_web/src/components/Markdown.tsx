import { useMemo } from 'react'
import { renderMarkdown } from '../lib/markdown'
import { cx } from './primitives'

/** Renders sanitized artifact markdown. Input is agent-written, never trusted. */
export function Markdown({ source, className }: { source: string; className?: string }) {
  const html = useMemo(() => renderMarkdown(source), [source])
  return (
    <div
      className={cx('prose-artifact text-sm text-ink', className)}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  )
}
