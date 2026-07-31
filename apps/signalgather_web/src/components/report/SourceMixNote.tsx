import type { SourceRef } from '../../lib/widgets/types'
import { summarizeSources } from '../../lib/sourceQuality'
import { cx } from '../primitives'

export function SourceMixNote({
  sources,
  className,
}: {
  sources: SourceRef[] | undefined
  className?: string
}) {
  const mix = summarizeSources(sources)
  if (mix.total === 0) return null

  return (
    <p
      role={mix.entirelySecondary ? 'note' : undefined}
      className={cx(
        'rounded-lg border px-3 py-2 text-xs',
        mix.entirelySecondary
          ? 'border-warning/50 bg-warning/10 text-warning'
          : 'border-line bg-surface-sunken text-ink-muted',
        className,
      )}
    >
      {mix.entirelySecondary ? (
        <>
          <strong className="font-semibold">No primary sources.</strong> All {mix.total} sources are
          secondary reporting — treat every finding here as unconfirmed by an official or
          first-party source.
        </>
      ) : (
        <>
          {mix.authoritative} of {mix.total} sources are primary or official.
        </>
      )}
    </p>
  )
}
