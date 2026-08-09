import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import {
  ApiError,
  cancelTopic,
  createTopic,
  getIntroMarkdown,
  getParsed,
  listTopics,
  login,
  logout,
  proceedTopic,
  register,
} from './api'
import {
  apiUrl,
  getApiBase,
  getRefreshToken,
  getToken,
  setApiBase,
  setRefreshToken,
  setToken,
} from './session'

interface Call {
  url: string
  init: RequestInit
}

let calls: Call[] = []

function mockFetch(responder: (call: Call) => Response | Promise<Response>) {
  const impl = vi.fn(async (url: string, init: RequestInit = {}) => {
    const call = { url, init }
    calls.push(call)
    return responder(call)
  })
  vi.stubGlobal('fetch', impl)
  return impl
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

describe('session', () => {
  it('defaults to the same origin so the bundled /app mount needs no config', () => {
    expect(getApiBase()).toBe('')
    expect(apiUrl('/v1/topics')).toBe('/v1/topics')
  })

  it('strips trailing slashes from a chosen slot', () => {
    setApiBase('https://agent-test1.particletico.com///')
    expect(apiUrl('/v1/topics')).toBe('https://agent-test1.particletico.com/v1/topics')
  })

  it('appends query params and drops undefined ones', () => {
    expect(apiUrl('/x', { a: 1, b: undefined })).toBe('/x?a=1')
  })
})

describe('auth', () => {
  it('logs in with form encoding and returns both tokens', async () => {
    mockFetch(() => json({ access_token: 'tok', refresh_token: 'ref', token_type: 'bearer' }))

    expect(await login('a@b.co', 'pw')).toEqual({ accessToken: 'tok', refreshToken: 'ref' })
    const body = calls[0]!.init.body as URLSearchParams
    expect(calls[0]!.url).toBe('/auth/jwt/login')
    // The OAuth2 form takes the email in the `username` field.
    expect(body.get('username')).toBe('a@b.co')
    expect(body.get('password')).toBe('pw')
  })

  it('fails loudly when a login carries no refresh token', async () => {
    // Without it the user is back to a one-hour session and no way to renew it,
    // which is worse than a visible failure at sign-in.
    mockFetch(() => json({ access_token: 'tok', token_type: 'bearer' }))
    await expect(login('a@b.co', 'pw')).rejects.toBeInstanceOf(ApiError)
  })

  it('surfaces a bad-credentials response as an ApiError', async () => {
    mockFetch(() => json({ detail: 'LOGIN_BAD_CREDENTIALS' }, 400))
    await expect(login('a@b.co', 'nope')).rejects.toMatchObject({
      status: 400,
      detail: 'LOGIN_BAD_CREDENTIALS',
    })
  })

  it('fails loudly when a 200 login carries no access token', async () => {
    mockFetch(() => json({ token_type: 'bearer' }))
    await expect(login('a@b.co', 'pw')).rejects.toBeInstanceOf(ApiError)
  })

  it('registers with the tenant the UI minted', async () => {
    mockFetch(() => json({ id: 'u1' }, 201))
    await register({ email: 'a@b.co', password: 'pw', tenantId: 'tenant-1' })
    expect(JSON.parse(calls[0]!.init.body as string)).toEqual({
      email: 'a@b.co',
      password: 'pw',
      tenant_id: 'tenant-1',
    })
  })
})

describe('authenticated requests', () => {
  it('attaches the bearer token', async () => {
    setToken('jwt-abc')
    mockFetch(() => json({ items: [], count: 0, limit: 50, offset: 0, state: null }))

    await listTopics()
    expect(new Headers(calls[0]!.init.headers).get('Authorization')).toBe('Bearer jwt-abc')
  })

  it('sends no Authorization header when signed out', async () => {
    mockFetch(() => json({ items: [], count: 0, limit: 50, offset: 0, state: null }))
    await listTopics()
    expect(new Headers(calls[0]!.init.headers).has('Authorization')).toBe(false)
  })

  it('drops a rejected token so the UI cannot loop on it', async () => {
    setToken('stale')
    mockFetch(() => json({ detail: 'Unauthorized' }, 401))

    await expect(listTopics()).rejects.toMatchObject({ status: 401 })
    expect(getToken()).toBeNull()
  })

  it('keeps the token on a 404 — that is ownership, not authentication', async () => {
    setToken('good')
    mockFetch(() => json({ detail: 'topic not found' }, 404))

    await expect(proceedTopic('t1')).rejects.toMatchObject({ status: 404 })
    expect(getToken()).toBe('good')
  })

  it('posts a new topic as JSON and returns the created id', async () => {
    mockFetch(() => json({ topic_id: 't9', state: 'planning', events_url: '/x' }, 202))

    const created = await createTopic('  hormuz closure  ')
    expect(created.topic_id).toBe('t9')
    expect(JSON.parse(calls[0]!.init.body as string)).toEqual({ topic: '  hormuz closure  ' })
  })

  it('sends a bodyless POST for cancel', async () => {
    mockFetch(() => json({ accepted: true, state: 'cancelled' }, 202))
    await cancelTopic('t1')
    expect(calls[0]!.url).toBe('/v1/topics/t1/cancel')
    expect(calls[0]!.init.method).toBe('POST')
  })

  it('flattens FastAPI validation errors into one message', async () => {
    mockFetch(() =>
      json({ detail: [{ loc: ['body', 'topic'], msg: 'field required' }] }, 422),
    )
    await expect(createTopic('')).rejects.toMatchObject({ detail: 'field required' })
  })

  it('falls back to statusText when the error body is not JSON', async () => {
    mockFetch(() => new Response('<html>502</html>', { status: 502, statusText: 'Bad Gateway' }))
    await expect(listTopics()).rejects.toMatchObject({ detail: 'Bad Gateway' })
  })
})

describe('artifact fetches', () => {
  it('returns null for an artifact that has not been produced yet', async () => {
    mockFetch(() => json({ detail: 'parsed.json not produced yet' }, 404))
    expect(await getParsed('t1')).toBeNull()
  })

  it('returns markdown as text', async () => {
    mockFetch(() => new Response('# Intro\n\nBody.', { status: 200 }))
    expect(await getIntroMarkdown('t1')).toBe('# Intro\n\nBody.')
  })

  it('still raises on a real server error', async () => {
    mockFetch(() => json({ detail: 'boom' }, 500))
    await expect(getParsed('t1')).rejects.toBeInstanceOf(ApiError)
  })
})

describe('session renewal', () => {
  it('renews on a 401 and replays the call, so the user never sees a login screen', async () => {
    setToken('expired')
    setRefreshToken('ref-1')
    mockFetch((call) => {
      if (call.url === '/auth/jwt/refresh') {
        return json({ access_token: 'fresh', refresh_token: 'ref-2' })
      }
      const auth = new Headers(call.init.headers).get('Authorization')
      if (auth === 'Bearer fresh') {
        return json({ items: [], count: 0, limit: 50, offset: 0, state: null })
      }
      return json({ detail: 'Unauthorized' }, 401)
    })

    await expect(listTopics()).resolves.toMatchObject({ count: 0 })
    expect(getToken()).toBe('fresh')
    expect(getRefreshToken()).toBe('ref-2')
  })

  it('spends one refresh token for a burst of parallel 401s', async () => {
    // Each extra spend would reach a server that already rotated it, which
    // reads as a replay and ends every session the user has.
    setToken('expired')
    setRefreshToken('ref-1')
    mockFetch((call) => {
      if (call.url === '/auth/jwt/refresh') {
        return json({ access_token: 'fresh', refresh_token: 'ref-2' })
      }
      const auth = new Headers(call.init.headers).get('Authorization')
      return auth === 'Bearer fresh'
        ? json({ items: [], count: 0, limit: 50, offset: 0, state: null })
        : json({ detail: 'Unauthorized' }, 401)
    })

    await Promise.all([listTopics(), listTopics(), listTopics()])
    expect(calls.filter((c) => c.url === '/auth/jwt/refresh')).toHaveLength(1)
  })

  it('signs out for real when the refresh token is rejected too', async () => {
    setToken('expired')
    setRefreshToken('revoked')
    mockFetch((call) =>
      call.url === '/auth/jwt/refresh'
        ? json({ detail: 'invalid refresh token' }, 401)
        : json({ detail: 'Unauthorized' }, 401),
    )

    await expect(listTopics()).rejects.toMatchObject({ status: 401 })
    expect(getToken()).toBeNull()
    expect(getRefreshToken()).toBeNull()
  })

  it('keeps the session when the renewal fails on the network, not on auth', async () => {
    setToken('expired')
    setRefreshToken('ref-1')
    mockFetch((call) => {
      if (call.url === '/auth/jwt/refresh') throw new TypeError('Failed to fetch')
      return json({ detail: 'Unauthorized' }, 401)
    })

    await expect(listTopics()).rejects.toMatchObject({ status: 401 })
    expect(getRefreshToken()).toBe('ref-1')
  })

  it('revokes the refresh token server-side on sign-out', async () => {
    setToken('tok')
    setRefreshToken('ref-1')
    mockFetch(() => new Response(null, { status: 204 }))

    await logout()
    expect(calls[0]!.url).toBe('/auth/jwt/logout')
    expect(JSON.parse(calls[0]!.init.body as string)).toEqual({ refresh_token: 'ref-1' })
    expect(getToken()).toBeNull()
    expect(getRefreshToken()).toBeNull()
  })

  it('still signs out locally when the revoke call cannot be delivered', async () => {
    setToken('tok')
    setRefreshToken('ref-1')
    mockFetch(() => {
      throw new TypeError('Failed to fetch')
    })

    await logout()
    expect(getToken()).toBeNull()
  })
})
