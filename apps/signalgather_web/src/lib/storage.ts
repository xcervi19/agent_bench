import type { AppSettings } from './types'

const SETTINGS_KEY = 'signalgather_settings'
const VISITS_KEY = 'signalgather_last_visits'

const DEFAULT_SETTINGS: AppSettings = {
  apiKey: '',
  environment: 'test1',
  customBaseUrl: '',
  theme: 'dark',
}

export function loadSettings(): AppSettings {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY)
    if (!raw) return { ...DEFAULT_SETTINGS }
    return { ...DEFAULT_SETTINGS, ...JSON.parse(raw) }
  } catch {
    return { ...DEFAULT_SETTINGS }
  }
}

export function saveSettings(settings: AppSettings): void {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings))
}

export function loadLastVisits(): Record<string, string> {
  try {
    const raw = localStorage.getItem(VISITS_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

export function markTopicVisited(topicId: string): void {
  const visits = loadLastVisits()
  visits[topicId] = new Date().toISOString()
  localStorage.setItem(VISITS_KEY, JSON.stringify(visits))
}

export function hasNewActivity(
  topicId: string,
  updatedAt: string,
  deltaCreatedAt?: string | null,
): boolean {
  const visits = loadLastVisits()
  const lastVisit = visits[topicId]
  if (!lastVisit) return false
  const compareTime = deltaCreatedAt ?? updatedAt
  try {
    return new Date(compareTime) > new Date(lastVisit)
  } catch {
    return false
  }
}
