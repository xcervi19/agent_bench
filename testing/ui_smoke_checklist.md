# SignalGather UI — smoke checklist

Run against **test1** (`https://agent-test1.particletico.com`) unless noted.

## Setup

- [ ] Open Settings → select test1 environment
- [ ] Enter valid `X-API-Key` → Test connection shows `ready`
- [ ] Theme toggle works (dark / light / system)

## Topic list (home)

- [ ] Empty state shows onboarding copy when no topics
- [ ] Create topic from NL text → appears in list with `Planning` badge
- [ ] Topic card shows relative updated time

## Planning + gate (16a)

- [ ] Open topic workspace → SSE shows `Live` indicator
- [ ] Activity feed receives `stage.*` and `tool_use` events
- [ ] Plan review section hydrates on `intro.ready` (intro.md + query table)
- [ ] Status bar shows `Awaiting Review` + **Proceed** / **Cancel**
- [ ] Click **Proceed** → state moves to `Delivering`

## Deliver + report (16b)

- [ ] Activity feed shows deliver-stage events
- [ ] Report section hydrates on `report.ready`
- [ ] Markdown renders; `[s01]` citations link to source URLs
- [ ] Sources list shows relevance scores and external links
- [ ] Key findings and scenarios render from `report.json`

## Monitor + deltas (16c)

- [ ] Enable monitoring with interval selector
- [ ] Monitor stats update (refresh count, last refresh)
- [ ] **Refresh now** triggers `refresh.started` / `refresh.completed` in feed
- [ ] Delta timeline lists refresh cycles
- [ ] Open delta → shows updated report + new sources

## Resilience (16d)

- [ ] Reload tab mid-run → SSE reconnects, state reconciled
- [ ] Artifacts not yet available show skeletons (no crash on 404)
- [ ] API errors shown in context with retry
- [ ] Layout usable at tablet width (~768px)

## Regression

- [ ] Full curl lifecycle in `testing/app_testing_scenario.md` still passes
