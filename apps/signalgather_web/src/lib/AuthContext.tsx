import { createContext, useCallback, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import { ApiError, fetchCurrentUser, login as apiLogin, logout as apiLogout } from './api'
import type { CurrentUser } from './api'
import {
  clearSession,
  getApiBase,
  getRefreshToken,
  getToken,
  setApiBase,
  setRefreshToken,
  setToken,
} from './session'

export interface AuthValue {
  user: CurrentUser | null
  /** True until the stored token has been validated against /users/me. */
  loading: boolean
  apiBase: string
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
  selectApiBase: (baseUrl: string) => void
}

export const AuthContext = createContext<AuthValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null)
  // Only "loading" if there is a session worth validating; a signed-out visitor
  // should get the login screen on the first paint, not a spinner. A refresh
  // token on its own counts: the access token beside it may have expired hours
  // ago, and renewing it is exactly what saves the user a password prompt.
  const [loading, setLoading] = useState(() => getToken() !== null || getRefreshToken() !== null)
  const [apiBase, setApiBaseState] = useState(getApiBase())

  // A token in localStorage is only a claim; the API decides if it is still
  // good. Re-validating on mount (and on slot change) avoids showing a shell
  // that 401s on its first real request. An expired access token is renewed
  // inside this call rather than failing it — see `request` in api.ts.
  useEffect(() => {
    if (!getToken() && !getRefreshToken()) return
    let cancelled = false
    fetchCurrentUser()
      .then((me) => {
        if (!cancelled) setUser(me)
      })
      .catch((err) => {
        if (cancelled) return
        if (err instanceof ApiError && err.isAuthError) clearSession()
        setUser(null)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [apiBase])

  const signIn = useCallback(async (email: string, password: string) => {
    const tokens = await apiLogin(email, password)
    setToken(tokens.accessToken)
    setRefreshToken(tokens.refreshToken)
    setUser(await fetchCurrentUser())
  }, [])

  const signOut = useCallback(async () => {
    // Revokes the row server-side before forgetting it here, so the session is
    // actually over rather than merely out of sight.
    await apiLogout()
    setUser(null)
  }, [])

  const selectApiBase = useCallback((baseUrl: string) => {
    // Tokens are issued per deployment — carrying one across slots only produces
    // confusing 401s, so switching slots signs you out.
    clearSession()
    setUser(null)
    setApiBase(baseUrl)
    setApiBaseState(getApiBase())
  }, [])

  const value = useMemo<AuthValue>(
    () => ({ user, loading, apiBase, signIn, signOut, selectApiBase }),
    [user, loading, apiBase, signIn, signOut, selectApiBase],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
