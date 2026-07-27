import { createContext, useCallback, useEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import { ApiError, fetchCurrentUser, login as apiLogin } from './api'
import type { CurrentUser } from './api'
import { clearToken, getApiBase, getToken, setApiBase, setToken } from './session'

export interface AuthValue {
  user: CurrentUser | null
  /** True until the stored token has been validated against /users/me. */
  loading: boolean
  apiBase: string
  signIn: (email: string, password: string) => Promise<void>
  signOut: () => void
  selectApiBase: (baseUrl: string) => void
}

export const AuthContext = createContext<AuthValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<CurrentUser | null>(null)
  // Only "loading" if there is a token worth validating; a signed-out visitor
  // should get the login screen on the first paint, not a spinner.
  const [loading, setLoading] = useState(() => getToken() !== null)
  const [apiBase, setApiBaseState] = useState(getApiBase())

  // A token in localStorage is only a claim; the API decides if it is still
  // good. Re-validating on mount (and on slot change) avoids showing a shell
  // that 401s on its first real request.
  useEffect(() => {
    if (!getToken()) return
    let cancelled = false
    fetchCurrentUser()
      .then((me) => {
        if (!cancelled) setUser(me)
      })
      .catch((err) => {
        if (cancelled) return
        if (err instanceof ApiError && err.isAuthError) clearToken()
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
    const token = await apiLogin(email, password)
    setToken(token)
    setUser(await fetchCurrentUser())
  }, [])

  const signOut = useCallback(() => {
    clearToken()
    setUser(null)
  }, [])

  const selectApiBase = useCallback((baseUrl: string) => {
    // Tokens are signed per deployment — carrying one across slots only produces
    // confusing 401s, so switching slots signs you out.
    clearToken()
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
