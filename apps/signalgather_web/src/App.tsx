import { Link, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './lib/AuthContext'
import { useAuth } from './lib/useAuth'
import { API_ENVS } from './lib/session'
import { LoginPage } from './pages/LoginPage'
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

function Shell() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex min-h-full items-center justify-center">
        <Spinner className="size-6 text-ink-faint" />
        <span className="sr-only">Restoring your session…</span>
      </div>
    )
  }

  if (!user) return <LoginPage />

  return (
    <div className="flex min-h-full flex-col">
      <TopBar />
      <Routes>
        <Route path="/" element={<TopicListPage />} />
        <Route path="/topics/:topicId" element={<TopicWorkspacePage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
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
        <Link to="/" className="text-sm font-semibold tracking-tight text-ink">
          SignalGather
        </Link>
        <div className="flex items-center gap-3 text-xs text-ink-muted">
          <span className="rounded-full border border-line px-2 py-0.5" title={apiBase || 'same origin'}>
            {env?.label ?? apiBase}
          </span>
          <span className="hidden sm:inline">{user?.email}</span>
          <Button variant="ghost" onClick={signOut} className="px-2 py-1">
            Sign out
          </Button>
        </div>
      </div>
    </header>
  )
}
