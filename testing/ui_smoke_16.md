# UI smoke — SignalGather frontend (#16, phases a–d)

Manual checklist for the full journey the UI replaces in
`app_testing_scenario.md`. Run it against **test1** before prod.

Covers sign-in, topic list, create, live plan, gate, report, sources,
monitoring, and deltas.

**Time:** ~30 min plus one real plan+deliver run (15–30 min of agent work).

---

## 0. Target

| Slot | UI | API |
|---|---|---|
| test1 | `https://agent-test1.particletico.com/app` | same origin |
| local | `http://localhost:5173/app/` (`npm run dev`) | proxied to `:8002` |

Deploy on the VPS (test1 slot, from `~/agent_bench_test1`):

```bash
git pull
docker compose -f docker-compose.yml -f infra/docker-compose.test1.yml \
  -f infra/docker-compose.slot-minimal.yml build claude_agent
docker compose -f docker-compose.yml -f infra/docker-compose.test1.yml \
  -f infra/docker-compose.slot-minimal.yml up -d claude_agent
curl -s -o /dev/null -w '%{http_code}\n' https://agent-test1.particletico.com/app   # 200
```

The SPA is baked into the image (`web` stage in
`docker/Dockerfile.claude_agent`) and served from `CLAUDE_AGENT_WEB_DIST`.
No Caddy change is needed — the existing `agent-test1` vhost already proxies it.

**Product-mode note.** With `CLAUDE_AGENT_ALLOW_SERVICE_KEY_BYPASS=true`
(the harness default) an unauthenticated browser is treated as the service
principal and would see *every* topic. Set it to `false` on any slot where the
UI is exercised as a real user, and re-run §2.

---

## 1. Sign in / register

- [ ] `/app` loads; no console errors; sign-in card renders
- [ ] **Environment** picker lists same-origin / local / test1 / test2 / prod
- [ ] Wrong password → “Email or password is incorrect.”, no crash
- [ ] **Create account** with a fresh email + 8-char password → auto sign-in
- [ ] Registering the same email twice → “account … already exists”
- [ ] Header shows the account email and the environment chip
- [ ] Hard reload keeps you signed in (token restored from localStorage)
- [ ] **Sign out** returns to the sign-in card; reload stays signed out

## 2. Ownership (needs a second account)

- [ ] New account's topic list is **empty** — no other user's topics leak
- [ ] Paste account A's topic URL while signed in as B → “Topic not found”
- [ ] Sign back in as A → the topic is there

## 3. Create a topic

- [ ] Empty account shows the “No topics yet” empty state
- [ ] **Start planning** is disabled until text is entered
- [ ] Type a real topic (e.g. `Hormuz strait closure — options to lower price`)
- [ ] ⌘/Ctrl + Enter submits
- [ ] Redirects to the workspace; badge reads **Planning** with a spinner
- [ ] Back on the list, the topic appears with relative timestamps

## 4. Live activity (SSE)

- [ ] Stream badge turns **Live** within a few seconds
- [ ] `Finding trusted sources` then `Building the query plan` appear as stages
- [ ] Tool rows accumulate; `details` expands input/output previews
- [ ] Feed auto-scrolls; scrolling up unticks **Follow** and stops the jump
- [ ] “Running for” counter ticks while the topic is active
- [ ] Event `#seq` numbers are strictly increasing with **no gaps and no repeats**

## 5. Reconnect (the resilience criterion)

- [ ] Sleep the tab (or switch away) for ≥60 s, return → badge back to **Live**
- [ ] Turn Wi-Fi off ~20 s → badge shows **Reconnecting…**; back on → **Live**
- [ ] After reconnect the feed has **no duplicated and no missing seq numbers**
- [ ] Hard reload mid-run → full event history is replayed, run continues
- [ ] DevTools → Network: exactly **one** open `events` request; no repeating
      polls of `/report`, `/parsed`, `/intro` while nothing is happening

## 6. Plan review gate

- [ ] On `intro.ready` the **Plan review** panel fills in on its own (no reload)
- [ ] Badge becomes **Awaiting your review**; feed shows the “waiting for you” line
- [ ] **Brief** tab renders `intro.md` (headings, bullets, chips)
- [ ] **Queries** tab shows the count and one row per planned query
- [ ] Non-English queries render in native script
- [ ] Clicking a query row expands rationale / sources / covered entities
- [ ] Before the gate is reached, **Proceed** is disabled and **Cancel** is not

## 7. Proceed and deliver

- [ ] **Proceed** → button shows a busy state, then badge → **Researching**
- [ ] Deliver-stage events keep streaming into the feed
- [ ] On completion the badge reads **Report ready** and the stream badge closes
- [ ] **Report** and **Sources** tabs appear; the view switches to Report on its own

## 7a. Report (16b)

- [ ] Executive summary and report body render with headings and bullets
- [ ] Thesis badge shows supported / weakened / invalidated / inconclusive
- [ ] **Citations `[s01]` are links** — clicking one jumps to that source
- [ ] A citation with no matching source is shown dimmed/dashed, not as a link
- [ ] Key findings show confidence and their source ids
- [ ] Scenario table shows before/after probabilities and a verdict
- [ ] Open questions and suggested next-cycle queries appear

## 7b. Adaptive widgets (16b)

This is the point of the widget registry — check it actually fired.

- [ ] `intro.md` renders **entity chips** and a **highlights** block as UI, not
      as the literal text `<EntityChips>…`
- [ ] `report.md` renders any `news-card` the agent emitted as a full source card
- [ ] No "Cannot display …" disclosure appears. If one does, note the widget type
      and reason — it means the agent emitted a type the registry does not know
- [ ] Grep the artifacts on the server to confirm the agent used the new form:
      ```bash
      grep -l 'markdown-ui-widget' /state/news/*/runs/*/intro.md | head
      ```
      An older run using `<EntityChips>` must still render correctly (legacy path)

## 7c. Sources (16b)

- [ ] Every source shows publisher, class, relevance meter, date
- [ ] Sort **Relevance** / **Newest** both reorder the list
- [ ] **Official only** filters to primary-official sources; count in the heading updates
- [ ] Search budget / drop counts appear at the bottom
- [ ] Source links open in a new tab

## 7d. Monitoring and deltas (16c)

- [ ] **Monitoring** tab appears only once the topic is `reported`
- [ ] **Enable monitoring** → panel switches to Active with a query count
- [ ] Freshness window buttons (24/48/72/168h) change and persist across reload
- [ ] Schedule **Off → Every 6h** sets a "Next scheduled" time; **Off** clears it
- [ ] Pause → status shows Paused and **Refresh now** is disabled; Resume restores
- [ ] **Refresh now** → confirmation appears and `refresh.started` shows in the feed
- [ ] Pressing **Refresh now** twice reports "already running" as info, not an error
- [ ] On `refresh.completed` a new row appears in **Refresh history** with no reload
- [ ] Opening a cycle loads its detail; a cycle that found nothing says so
- [ ] Delta detail shows new sources, key changes, and trigger terms hit
- [ ] DevTools → Network: delta artifacts are fetched **only** when a row is opened

## 7e. Sharing (#40)

The one section to run in **two windows**: signed in, and a private/incognito
window with no account at all.

- [ ] **Share** tab appears once the topic is `reported`
- [ ] Before publishing it names the trade-off: monitoring pauses, actions stop
- [ ] **Share publicly** → badge flips to Shared, a banner appears on every tab
- [ ] **Copy link** yields `…/app/shared/<topic-id>`
- [ ] Monitoring tab now explains the freeze instead of showing controls
- [ ] Plan tab's Proceed/Cancel stay disabled and say why
- [ ] `curl -X POST .../v1/topics/<id>/refresh` with the owner's JWT → **409**
- [ ] Topic list shows a **Shared** badge on the row
- [ ] **Incognito:** open the copied link → report, sources, plan and updates all
      render; the page says Read-only
- [ ] **Incognito:** DevTools → Network shows only `GET /v1/public/topics/*`, no
      `Authorization` header, and no request to `/v1/topics/*`
- [ ] **Incognito:** nothing on the page runs anything — no Proceed, Cancel,
      Refresh, monitoring or Share control anywhere
- [ ] **Incognito:** `/app/shared` lists the topic and its search finds it
- [ ] **Stop sharing** → incognito reload shows "not shared", `/app/shared` no
      longer lists it, owner actions work again, monitoring stays paused
- [ ] Publishing a topic that is not `reported` is refused (button disabled)

## 8. Cancel (second topic)

- [ ] Create another topic, hit **Cancel topic** while it is planning
- [ ] Badge → **Cancelled**; both actions become disabled
- [ ] Reload → still cancelled

## 9. Failure & recovery

- [ ] Stop `claude_agent`, reload the UI → an error is shown, not a blank page
- [ ] Restart it, hit **Retry** on the list → topics load again
- [ ] Open `/app/topics/<random-uuid>` → “Topic not found”, with a link home
- [ ] Delete the token in devtools localStorage and act → returns to sign-in

## 10. Return-use

- [ ] Leave the workspace, wait for a scheduled refresh, return to the list
- [ ] The topic carries a **New since your last visit** badge
- [ ] Opening it and going back clears the badge

## 11. Responsive & appearance

- [ ] Desktop (≥1280 px): content and activity feed side by side
- [ ] Tablet (~820 px): single column, feed below content, nothing clipped
- [ ] No horizontal page scroll at 768 px; query, source and scenario tables
      scroll inside their own boxes
- [ ] Light and dark OS themes both readable (dark is the default)

---

## Result

| Field | |
|---|---|
| Date | |
| Slot / commit | |
| `ALLOW_SERVICE_KEY_BYPASS` | |
| Topic used | |
| Plan → gate duration | |
| Failures | |

Record failures in `STATUS.md` → Known bugs.
