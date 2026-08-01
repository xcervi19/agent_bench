import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { ApiError } from './api'
import {
  getPublicDelta,
  getPublicIntroMarkdown,
  getPublicReport,
  getPublicTopic,
  listPublicDeltas,
  listPublicTopics,
  shareUrl,
} from './publicApi'
import { setToken } from './session'

interface Call {
  url: string
  init: RequestInit
}

let calls: Call[] = []

/** The request under test; failing loudly beats an `undefined` assertion. */
function firstCall(): Call {
  const call = calls[0]
  if (!call) throw new Error('expected a fetch call')
  return call
}

function mockFetch(responder: (call: Call) => Response) {
  vi.stubGlobal(
    'fetch',
    vi.fn(async (url: string, init: RequestInit = {}) => {
      const call = { url, init }
      calls.push(call)
      return responder(call)
    }),
  )
}

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  })
}

beforeEach(() => {
  calls = []
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('the public client is read-only', () => {
  it('never sends the signed-in user’s token', async () => {
    // A reader may well be signed in — a shared page must still be the same
    // page for them as for a stranger, and must not leak a bearer token to a
    // route that has no use for one.
    setToken('a-real-looking-jwt')
    mockFetch(() => json({ id: 't1' }))

    await getPublicTopic('t1')

    const headers = new Headers(firstCall().init.headers)
    expect(headers.get('Authorization')).toBeNull()
    localStorage.clear()
  })

  it('only ever issues GETs', async () => {
    mockFetch(() => json({ items: [], count: 0, limit: 50, offset: 0, q: null }))

    await listPublicTopics()
    await getPublicTopic('t1').catch(() => null)
    await listPublicDeltas('t1')

    for (const call of calls) {
      expect(call.init.method).toBe('GET')
      expect(call.init.body).toBeUndefined()
    }
  })

  it('reads from the public router, not the owner routes', async () => {
    mockFetch(() => json({ items: [], count: 0, limit: 50, offset: 0, q: null }))

    await listPublicTopics('hormuz')

    expect(firstCall().url).toContain('/v1/public/topics')
    expect(firstCall().url).toContain('q=hormuz')
    expect(firstCall().url).not.toContain('/v1/topics?')
  })
})

describe('missing artifacts', () => {
  it('resolves a 404 artifact to null rather than throwing', async () => {
    mockFetch(() => new Response('{"detail":"report.json not produced yet"}', { status: 404 }))
    await expect(getPublicReport('t1')).resolves.toBeNull()
    await expect(getPublicIntroMarkdown('t1')).resolves.toBeNull()
    await expect(getPublicDelta('t1', 2)).resolves.toBeNull()
  })

  it('surfaces a withdrawn share as a 404 on the topic itself', async () => {
    mockFetch(() => new Response('{"detail":"topic not found"}', { status: 404 }))
    await expect(getPublicTopic('t1')).rejects.toBeInstanceOf(ApiError)
  })

  it('keeps a real failure a failure', async () => {
    mockFetch(() => new Response('{"detail":"boom"}', { status: 500 }))
    await expect(getPublicReport('t1')).rejects.toMatchObject({ status: 500 })
  })
})

describe('share links', () => {
  it('points at the SPA route, absolute so it survives a paste', () => {
    expect(shareUrl('abc')).toBe(`${window.location.origin}/shared/abc`)
  })
})
