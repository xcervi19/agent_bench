import { cleanup, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import { SourceMixNote } from './SourceMixNote'
import type { SourceMixPayload } from '../../lib/types'
import type { SourceRef } from '../../lib/widgets/types'

const source = (over: Partial<SourceRef> = {}): SourceRef => ({
  id: 's01',
  source_class: 'specialist_outlet',
  ...over,
})

const payload = (over: Partial<SourceMixPayload> = {}): SourceMixPayload => ({
  total: 10,
  authoritative: 6,
  whitelisted: 4,
  authoritative_ratio: 0.6,
  entirely_secondary: false,
  ...over,
})

afterEach(cleanup)

describe('SourceMixNote — the emitted payload', () => {
  it('renders the backend count', () => {
    render(<SourceMixNote mix={payload()} sources={undefined} />)
    expect(screen.getByText(/6 of 10 sources are primary or official/)).toBeTruthy()
  })

  it('warns when the backend says every source is secondary', () => {
    render(<SourceMixNote mix={payload({ authoritative: 0, entirely_secondary: true })} sources={[]} />)
    expect(screen.getByText(/No primary sources/)).toBeTruthy()
  })

  it('renders the payload even when the local count would disagree', () => {
    // The whole point of #51: the backend also counts a whitelisted host, so a
    // source the analyst classed `unknown` can still be authoritative. If this
    // rendered 0, the customer would be reading the narrower number again.
    render(
      <SourceMixNote
        mix={payload({ total: 1, authoritative: 1, whitelisted: 1, authoritative_ratio: 1 })}
        sources={[source({ source_class: 'unknown' })]}
      />,
    )
    expect(screen.getByText(/1 of 1 sources are primary or official/)).toBeTruthy()
  })

  it('renders nothing for a run with no sources at all', () => {
    const { container } = render(<SourceMixNote mix={payload({ total: 0 })} sources={[]} />)
    expect(container.textContent).toBe('')
  })
})

describe('SourceMixNote — legacy artefacts with no payload', () => {
  it('falls back to counting the classes it can see', () => {
    render(
      <SourceMixNote
        mix={null}
        sources={[source({ source_class: 'primary_official' }), source(), source()]}
      />,
    )
    expect(screen.getByText(/1 of 3 sources are primary or official/)).toBeTruthy()
  })

  it('flags the observed prod refresh, which had no primary source at all', () => {
    const observed = ['Al Hadath', 'France 24', 'Sputnik', 'Bloomberg', 'Al Jazeera'].map(
      (publisher) => source({ publisher, source_class: 'specialist_outlet' }),
    )
    render(<SourceMixNote mix={undefined} sources={observed} />)
    expect(screen.getByText(/No primary sources/)).toBeTruthy()
  })

  it('counts data_feed as authoritative, as the backend does', () => {
    render(<SourceMixNote mix={null} sources={[source({ source_class: 'data_feed' })]} />)
    expect(screen.getByText(/1 of 1 sources are primary or official/)).toBeTruthy()
  })

  it('renders nothing when there is neither a payload nor a source', () => {
    const { container } = render(<SourceMixNote mix={null} sources={undefined} />)
    expect(container.textContent).toBe('')
  })
})
