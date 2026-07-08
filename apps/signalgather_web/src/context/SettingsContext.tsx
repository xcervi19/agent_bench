import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import type { AppSettings } from '@/lib/types'
import { loadSettings, saveSettings } from '@/lib/storage'
import { resolveBaseUrl } from '@/lib/api'

interface SettingsContextValue {
  settings: AppSettings
  baseUrl: string
  updateSettings: (patch: Partial<AppSettings>) => void
}

const SettingsContext = createContext<SettingsContextValue | null>(null)

export function SettingsProvider({ children }: { children: ReactNode }) {
  const [settings, setSettings] = useState<AppSettings>(() => loadSettings())

  useEffect(() => {
    saveSettings(settings)
  }, [settings])

  useEffect(() => {
    const root = document.documentElement
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    const isDark =
      settings.theme === 'dark' || (settings.theme === 'system' && prefersDark)
    root.classList.toggle('light', !isDark)
  }, [settings.theme])

  const updateSettings = useCallback((patch: Partial<AppSettings>) => {
    setSettings((prev) => ({ ...prev, ...patch }))
  }, [])

  const value = useMemo(
    () => ({
      settings,
      baseUrl: resolveBaseUrl(settings),
      updateSettings,
    }),
    [settings, updateSettings],
  )

  return <SettingsContext.Provider value={value}>{children}</SettingsContext.Provider>
}

export function useSettings() {
  const ctx = useContext(SettingsContext)
  if (!ctx) throw new Error('useSettings must be used within SettingsProvider')
  return ctx
}
