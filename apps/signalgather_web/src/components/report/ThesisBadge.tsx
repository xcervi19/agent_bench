import type { ThesisStatus } from '../../lib/types'
import { cx } from '../primitives'

/**
 * The single most decision-relevant field in a report: did the news support the
 * working thesis or break it? Given its own badge so it survives skim-reading.
 */
const STYLES: Record<string, { label: string; className: string }> = {
  supported: { label: 'Thesis supported', className: 'border-positive/50 bg-positive/10 text-positive' },
  weakened: { label: 'Thesis weakened', className: 'border-warning/50 bg-warning/10 text-warning' },
  invalidated: { label: 'Thesis invalidated', className: 'border-danger/50 bg-danger/10 text-danger' },
  inconclusive: { label: 'Inconclusive', className: 'border-line bg-surface-sunken text-ink-muted' },
  unchanged: { label: 'Unchanged', className: 'border-line bg-surface-sunken text-ink-muted' },
}

export function ThesisBadge({
  status,
  className,
}: {
  status: ThesisStatus | string | undefined
  className?: string
}) {
  if (!status) return null
  const style = STYLES[status] ?? {
    label: status,
    className: 'border-line bg-surface-sunken text-ink-muted',
  }
  return (
    <span
      className={cx(
        'inline-flex items-center rounded-full border px-2.5 py-1 text-xs font-medium whitespace-nowrap',
        style.className,
        className,
      )}
    >
      {style.label}
    </span>
  )
}
