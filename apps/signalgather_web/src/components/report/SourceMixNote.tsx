import type { SourceMixPayload } from '../../lib/types'
import type { SourceRef } from '../../lib/widgets/types'
import { cx } from '../primitives'

/**
 * How much of this run rests on primary sources — the backend's number (#51).
 *
 * There used to be a second definition here. `sourceQuality.ts` counted a source
 * authoritative on its `source_class` alone, while the backend also counts a host
 * on the register, so the figure a customer read was narrower than the figure the
 * system measured and neither could be called *the* source mix. The definition now
 * lives in `apps/claude_agent/topics/source_quality.py`, is written to
 * `source_mix.json` by the run, and is rendered here as it arrives.
 *
 * `legacyMix` is not that definition returning by the back door. It is the only
 * thing that can be said about a run that finished before the file existed, and it
 * runs only when `mix` is absent.
 */
export function SourceMixNote({
  mix,
  sources,
  className,
}: {
  mix: SourceMixPayload | null | undefined
  sources: SourceRef[] | undefined
  className?: string
}) {
  const resolved = mix ?? legacyMix(sources)
  if (!resolved || resolved.total === 0) return null

  return (
    <p
      role={resolved.entirely_secondary ? 'note' : undefined}
      className={cx(
        'rounded-lg border px-3 py-2 text-xs',
        resolved.entirely_secondary
          ? 'border-warning/50 bg-warning/10 text-warning'
          : 'border-line bg-surface-sunken text-ink-muted',
        className,
      )}
    >
      {resolved.entirely_secondary ? (
        <>
          <strong className="font-semibold">No primary sources.</strong> All {resolved.total}{' '}
          sources are secondary reporting — treat every finding here as unconfirmed by an
          official or first-party source.
        </>
      ) : (
        <>
          {resolved.authoritative} of {resolved.total} sources are primary or official.
        </>
      )}
    </p>
  )
}

const AUTHORITATIVE_CLASSES = new Set(['primary_official', 'data_feed'])

/**
 * What can be counted in the browser for a run with no `source_mix.json`.
 *
 * Class only: the register of authoritative domains is a server-side file and is
 * not shipped here, so this undercounts a ministry page the analyst classed
 * `unknown`. That is the reason it is a fallback and not the definition.
 */
function legacyMix(sources: SourceRef[] | undefined): SourceMixPayload | null {
  const rows = sources ?? []
  if (rows.length === 0) return null
  const authoritative = rows.filter((row) =>
    AUTHORITATIVE_CLASSES.has(row.source_class ?? ''),
  ).length
  return {
    total: rows.length,
    authoritative,
    whitelisted: 0,
    authoritative_ratio: authoritative / rows.length,
    entirely_secondary: authoritative === 0,
  }
}
