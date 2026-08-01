import { Link, Navigate, Route, Routes, useLocation } from 'react-router-dom'
import { AuthProvider } from './lib/AuthContext'
import { useAuth } from './lib/useAuth'
import { API_ENVS } from './lib/session'
import { LoginPage } from './pages/LoginPage'
import { PublicTopicListPage } from './pages/PublicTopicListPage'
import { PublicTopicPage } from './pages/PublicTopicPage'
import { TopicListPage } from './pages/TopicListPage'
import { TopicWorkspacePage } from './pages/TopicWorkspacePage'
import { Button, Spinner } from './components/primitives'

export default function App() {
  return (
    <AuthProvider>
      <Shell />
    </AuthProvider>
  )
}

/** Shared topics (#40) are readable with no account, so they route before the gate. */
const PUBLIC_PREFIX = '/shared'

function Shell() {
  const { user, loading } = useAuth()
  const location = useLocation()
  const isPublicRoute = location.pathname.startsWith(PUBLIC_PREFIX)

  // Only the signed-in half of the app waits on the session: a shared link must
  // open for a visitor who has no token to validate.
  if (loading && !isPublicRoute) {
    return (
      <div className="flex min-h-full items-center justify-center">
        <Spinner className="size-6 text-ink-faint" />
        <span className="sr-only">Restoring your session…</span>
      </div>
    )
  }

  if (!user && !isPublicRoute) return <LoginPage />

  return (
    <div className="flex min-h-full flex-col">
      <TopBar />
      <Routes>
        <Route path={PUBLIC_PREFIX} element={<PublicTopicListPage />} />
        <Route path={`${PUBLIC_PREFIX}/:topicId`} element={<PublicTopicPage />} />
        {user && <Route path="/" element={<TopicListPage />} />}
        {user && <Route path="/topics/:topicId" element={<TopicWorkspacePage />} />}
        <Route path="*" element={<Navigate to={user ? '/' : PUBLIC_PREFIX} replace />} />
      </Routes>
    </div>
  )
}

function TopBar() {
  const { user, signOut, apiBase } = useAuth()
  const env = API_ENVS.find((candidate) => candidate.baseUrl === apiBase)

  return (
    <header className="sticky top-0 z-10 border-b border-line bg-surface/85 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl flex-wrap items-center justify-between gap-2 px-4 py-3 sm:px-6">
        <div className="flex items-center gap-4">
          <Link to={user ? '/' : PUBLIC_PREFIX} className="text-sm font-semibold tracking-tight text-ink">
            SignalGather
          </Link>
          <Link to={PUBLIC_PREFIX} className="text-xs text-ink-muted hover:text-ink">
            Shared topics
          </Link>
        </div>
        <div className="flex items-center gap-3 text-xs text-ink-muted">
          <span className="rounded-full border border-line px-2 py-0.5" title={apiBase || 'same origin'}>
            {env?.label ?? apiBase}
          </span>
          {user ? (
            <>
              <span className="hidden sm:inline">{user.email}</span>
              <Button variant="ghost" onClick={signOut} className="px-2 py-1">
                Sign out
              </Button>
            </>
          ) : (
            // A reader with no account gets a way in, not a sign-out button for
            // a session they do not have.
            <Link to="/" className="text-accent hover:underline">
              Sign in
            </Link>
          )}
        </div>
      </div>
    </header>
  )
}
