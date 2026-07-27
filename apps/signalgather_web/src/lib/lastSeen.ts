/**
 * "What changed since I last looked" for the topic list (spec §A, 16d).
 *
 * The API has no per-user read state, and adding one for a badge would be a
 * schema change for a cosmetic feature. So the last-opened time is kept
 * client-side: it is advisory, per-device, and losing it only costs a badge.
 */

const KEY = 'signalgather.lastSeen'

type SeenMap = Record<string, string>

function read(): SeenMap {
  try {
    const raw = localStorage.getItem(KEY)
    if (!raw) return {}
    const parsed: unknown = JSON.parse(raw)
    return typeof parsed === 'object' && parsed !== null ? (parsed as SeenMap) : {}
  } catch {
    // Corrupt or unavailable storage must never break the list.
    return {}
  }
}

export function markTopicSeen(topicId: string, at: Date | number = Date.now()): void {
  try {
    const map = read()
    map[topicId] = new Date(at).toISOString()
    localStorage.setItem(KEY, JSON.stringify(map))
  } catch {
    /* private mode / quota — the badge is not worth failing over */
  }
}

export function lastSeenAt(topicId: string): string | undefined {
  return read()[topicId]
}

/**
 * True when the topic moved since the user last opened it. A topic never opened
 * is *not* "new" — it is simply new, and the list already conveys that with its
 * state badge; flagging both would make the flag meaningless.
 */
export function hasUnseenActivity(topicId: string, updatedAt: string): boolean {
  const seen = read()[topicId]
  if (!seen) return false
  const seenMs = Date.parse(seen)
  const updatedMs = Date.parse(updatedAt)
  if (Number.isNaN(seenMs) || Number.isNaN(updatedMs)) return false
  return updatedMs > seenMs
}
