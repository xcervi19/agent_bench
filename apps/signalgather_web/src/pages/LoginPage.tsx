import { useState } from 'react'
import { ApiError, register } from '../lib/api'
import { API_ENVS } from '../lib/session'
import { useAuth } from '../lib/useAuth'
import { Button, Card, ErrorNote } from '../components/primitives'

type Mode = 'signin' | 'register'

/**
 * Sign-in against `POST /auth/jwt/login` (#24), plus self-registration so a
 * pilot account can be created without shell access.
 *
 * The environment picker lives here because it decides which deployment the
 * credentials are checked against — switching it after login would be a lie.
 */
export function LoginPage() {
  const { signIn, apiBase, selectApiBase } = useAuth()
  const [mode, setMode] = useState<Mode>('signin')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [notice, setNotice] = useState<string | null>(null)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setBusy(true)
    setError(null)
    setNotice(null)
    try {
      if (mode === 'register') {
        // agentic_core requires a tenant on every user; a self-serve pilot
        // account gets its own tenant rather than joining someone else's.
        await register({ email, password, tenantId: crypto.randomUUID() })
        setNotice('Account created. Signing you in…')
      }
      await signIn(email, password)
    } catch (err) {
      setError(describeAuthError(err, mode))
      setNotice(null)
    } finally {
      setBusy(false)
    }
  }

  return (
    <main className="flex min-h-full items-center justify-center px-4 py-12">
      <div className="w-full max-w-sm">
        <header className="mb-6 text-center">
          <h1 className="text-2xl font-semibold tracking-tight text-ink">SignalGather</h1>
          <p className="mt-1 text-sm text-ink-muted">Topic intelligence for trading desks</p>
        </header>

        <Card className="p-6">
          <div className="mb-5 flex gap-1 rounded-lg bg-surface-sunken p-1">
            <ModeTab active={mode === 'signin'} onClick={() => setMode('signin')}>
              Sign in
            </ModeTab>
            <ModeTab active={mode === 'register'} onClick={() => setMode('register')}>
              Create account
            </ModeTab>
          </div>

          <form onSubmit={onSubmit} className="space-y-4">
            <Field label="Email" htmlFor="email">
              <input
                id="email"
                type="email"
                required
                autoComplete="username"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={INPUT}
              />
            </Field>

            <Field label="Password" htmlFor="password">
              <input
                id="password"
                type="password"
                required
                minLength={8}
                autoComplete={mode === 'signin' ? 'current-password' : 'new-password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className={INPUT}
              />
            </Field>

            <Field label="Environment" htmlFor="env">
              <select
                id="env"
                value={apiBase}
                onChange={(e) => selectApiBase(e.target.value)}
                className={INPUT}
              >
                {API_ENVS.map((env) => (
                  <option key={env.id} value={env.baseUrl}>
                    {env.label}
                  </option>
                ))}
                {!API_ENVS.some((env) => env.baseUrl === apiBase) && (
                  <option value={apiBase}>{apiBase}</option>
                )}
              </select>
            </Field>

            {notice && <p className="text-sm text-positive">{notice}</p>}
            {error && <ErrorNote>{error}</ErrorNote>}

            <Button type="submit" variant="primary" busy={busy} className="w-full">
              {mode === 'signin' ? 'Sign in' : 'Create account and sign in'}
            </Button>
          </form>
        </Card>

        <p className="mt-4 text-center text-xs text-ink-faint">
          Topics are private to your account.
        </p>
      </div>
    </main>
  )
}

const INPUT =
  'w-full rounded-lg border border-line bg-surface-sunken px-3 py-2 text-sm text-ink ' +
  'placeholder:text-ink-faint focus-visible:outline-2 focus-visible:outline-offset-1 focus-visible:outline-accent'

function Field({
  label,
  htmlFor,
  children,
}: {
  label: string
  htmlFor: string
  children: React.ReactNode
}) {
  return (
    <div>
      <label htmlFor={htmlFor} className="mb-1.5 block text-xs font-medium text-ink-muted">
        {label}
      </label>
      {children}
    </div>
  )
}

function ModeTab({
  active,
  onClick,
  children,
}: {
  active: boolean
  onClick: () => void
  children: React.ReactNode
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-pressed={active}
      className={`flex-1 rounded-md px-3 py-1.5 text-sm font-medium transition-colors ${
        active ? 'bg-surface-raised text-ink shadow-sm' : 'text-ink-muted hover:text-ink'
      }`}
    >
      {children}
    </button>
  )
}

function describeAuthError(err: unknown, mode: Mode): string {
  if (err instanceof ApiError) {
    if (err.status === 400 && mode === 'register') {
      return err.detail === 'REGISTER_USER_ALREADY_EXISTS'
        ? 'An account with that email already exists — sign in instead.'
        : `Registration rejected: ${err.detail}`
    }
    if (err.status === 400 || err.status === 401) return 'Email or password is incorrect.'
    if (err.status === 404) {
      return 'This deployment has no auth routes — check the selected environment.'
    }
    return err.detail
  }
  if (err instanceof TypeError) {
    return 'Could not reach the API. Check the selected environment and your connection.'
  }
  return err instanceof Error ? err.message : String(err)
}
