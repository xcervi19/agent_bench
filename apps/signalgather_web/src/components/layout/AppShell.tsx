import { Link, Outlet, useLocation } from 'react-router-dom'
import { Activity, Radio, Settings } from 'lucide-react'
import { useSettings } from '@/context/SettingsContext'
import { cn } from '@/lib/utils'

export function AppShell() {
  const location = useLocation()
  const { settings, baseUrl } = useSettings()

  const nav = [
    { to: '/', label: 'Topics', icon: Radio },
    { to: '/settings', label: 'Settings', icon: Settings },
  ]

  return (
    <div className="min-h-screen flex flex-col">
      <header className="sticky top-0 z-50 border-b border-border bg-surface/95 backdrop-blur-sm">
        <div className="mx-auto flex h-14 max-w-7xl items-center justify-between px-4 sm:px-6">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent">
              <Activity className="h-4 w-4 text-white" />
            </div>
            <div className="text-left">
              <span className="text-sm font-semibold text-text group-hover:text-accent transition-colors">
                SignalGather
              </span>
              <span className="hidden sm:block text-[10px] text-text-muted leading-none">
                Topic Intelligence
              </span>
            </div>
          </Link>

          <nav className="flex items-center gap-1">
            {nav.map(({ to, label, icon: Icon }) => (
              <Link
                key={to}
                to={to}
                className={cn(
                  'flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm transition-colors',
                  location.pathname === to
                    ? 'bg-accent/15 text-accent'
                    : 'text-text-muted hover:text-text hover:bg-surface-overlay',
                )}
              >
                <Icon className="h-4 w-4" />
                <span className="hidden sm:inline">{label}</span>
              </Link>
            ))}
          </nav>

          <div className="hidden md:flex items-center gap-2 text-xs text-text-muted">
            <span
              className={cn(
                'h-2 w-2 rounded-full',
                settings.apiKey ? 'bg-success' : 'bg-warning',
              )}
            />
            <span className="truncate max-w-[180px]">{baseUrl.replace('https://', '')}</span>
          </div>
        </div>
      </header>

      <main className="flex-1 mx-auto w-full max-w-7xl px-4 sm:px-6 py-6">
        <Outlet />
      </main>
    </div>
  )
}
