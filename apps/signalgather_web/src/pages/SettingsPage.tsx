import { useState } from 'react'
import { Check, Eye, EyeOff, Server } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { useSettings } from '@/context/SettingsContext'
import { checkHealth } from '@/lib/api'
import type { ApiEnvironment } from '@/lib/types'
import { API_ENVIRONMENTS } from '@/lib/types'

export function SettingsPage() {
  const { settings, baseUrl, updateSettings } = useSettings()
  const [apiKey, setApiKey] = useState(settings.apiKey)
  const [showKey, setShowKey] = useState(false)
  const [testing, setTesting] = useState(false)
  const [testResult, setTestResult] = useState<{
    ok: boolean
    message: string
  } | null>(null)

  const handleSave = () => {
    updateSettings({ apiKey })
    setTestResult({ ok: true, message: 'Settings saved' })
  }

  const handleTest = async () => {
    setTesting(true)
    setTestResult(null)
    try {
      const patched = { ...settings, apiKey }
      const result = await checkHealth(patched)
      setTestResult({
        ok: result.status === 'ready' || result.status === 'ok',
        message: `API status: ${result.status}`,
      })
    } catch (e) {
      setTestResult({
        ok: false,
        message: e instanceof Error ? e.message : 'Connection failed',
      })
    } finally {
      setTesting(false)
    }
  }

  return (
    <div className="max-w-xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-text">Settings</h1>
        <p className="text-sm text-text-muted mt-1">
          Configure API connection and appearance
        </p>
      </div>

      <section className="rounded-xl border border-border bg-surface-raised p-5 space-y-4 text-left">
        <div className="flex items-center gap-2">
          <Server className="h-4 w-4 text-accent" />
          <h2 className="text-sm font-medium text-text">API Environment</h2>
        </div>

        <div className="grid grid-cols-2 gap-2">
          {(Object.keys(API_ENVIRONMENTS) as Array<keyof typeof API_ENVIRONMENTS>).map(
            (env) => (
              <button
                key={env}
                type="button"
                onClick={() => updateSettings({ environment: env })}
                className={`rounded-lg border px-3 py-2.5 text-left text-sm transition-colors ${
                  settings.environment === env
                    ? 'border-accent bg-accent/10 text-accent'
                    : 'border-border text-text-muted hover:border-accent/30'
                }`}
              >
                <span className="font-medium capitalize">{env}</span>
                <span className="block text-[10px] mt-0.5 opacity-70 truncate">
                  {API_ENVIRONMENTS[env]}
                </span>
              </button>
            ),
          )}
          <button
            type="button"
            onClick={() => updateSettings({ environment: 'custom' as ApiEnvironment })}
            className={`rounded-lg border px-3 py-2.5 text-left text-sm transition-colors ${
              settings.environment === 'custom'
                ? 'border-accent bg-accent/10 text-accent'
                : 'border-border text-text-muted hover:border-accent/30'
            }`}
          >
            <span className="font-medium">Custom</span>
            <span className="block text-[10px] mt-0.5 opacity-70">Your own URL</span>
          </button>
        </div>

        {settings.environment === 'custom' && (
          <input
            type="url"
            value={settings.customBaseUrl}
            onChange={(e) => updateSettings({ customBaseUrl: e.target.value })}
            placeholder="https://agent-test1.particletico.com"
            className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-sm text-text focus:outline-none focus:ring-2 focus:ring-accent/40"
          />
        )}

        <p className="text-xs text-text-muted">
          Current: <code className="font-mono">{baseUrl}</code>
        </p>
      </section>

      <section className="rounded-xl border border-border bg-surface-raised p-5 space-y-4 text-left">
        <h2 className="text-sm font-medium text-text">API Key</h2>
        <p className="text-xs text-text-muted">
          Sent as <code className="font-mono">X-API-Key</code> header. Leave empty if the
          server has no key configured.
        </p>
        <div className="relative">
          <input
            type={showKey ? 'text' : 'password'}
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="CLAUDE_AGENT_API_KEY"
            className="w-full rounded-lg border border-border bg-surface px-3 py-2 pr-10 text-sm text-text font-mono focus:outline-none focus:ring-2 focus:ring-accent/40"
          />
          <button
            type="button"
            onClick={() => setShowKey(!showKey)}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-text-muted hover:text-text"
          >
            {showKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        </div>
        <div className="flex gap-2">
          <Button onClick={handleSave}>Save</Button>
          <Button variant="secondary" onClick={() => void handleTest()} loading={testing}>
            Test connection
          </Button>
        </div>
        {testResult && (
          <p
            className={`text-xs flex items-center gap-1 ${
              testResult.ok ? 'text-success' : 'text-danger'
            }`}
          >
            {testResult.ok && <Check className="h-3.5 w-3.5" />}
            {testResult.message}
          </p>
        )}
      </section>

      <section className="rounded-xl border border-border bg-surface-raised p-5 space-y-3 text-left">
        <h2 className="text-sm font-medium text-text">Appearance</h2>
        <div className="flex gap-2">
          {(['dark', 'light', 'system'] as const).map((theme) => (
            <button
              key={theme}
              type="button"
              onClick={() => updateSettings({ theme })}
              className={`rounded-lg border px-4 py-2 text-sm capitalize transition-colors ${
                settings.theme === theme
                  ? 'border-accent bg-accent/10 text-accent'
                  : 'border-border text-text-muted hover:border-accent/30'
              }`}
            >
              {theme}
            </button>
          ))}
        </div>
      </section>
    </div>
  )
}
