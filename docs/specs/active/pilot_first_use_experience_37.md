# Pilot first-use experience — #37

**Status:** planned  
**Depends on:** #16 phase 16a (authenticated topic setup and plan review), #16 phase 16b (report reader)  
**Blocks:** Pilot user acquisition beyond assisted demos  
**Lane:** Product / frontend — *make the completed topic journey understandable and trustworthy for a first professional user*

## Goal

Make the SignalGather topic workflow self-explanatory for a first commodity-market
professional: sign in, understand what a topic produces, create one, recognize
work in progress, review the plan, read the delivered report, and return later
to their own topics without operator help.

## Core question

*"Can a first-time user complete and resume the plan → approval → report workflow
without curl, a product walkthrough, or guessing what the system is doing?"*

## Why this is a separate slice

#16 supplies the product workflow and workspace. This ticket supplies the
first-use and return-use clarity needed before treating that workflow as a
customer-acquisition surface. It must not become a generic dashboard or a
second implementation of #16.

## Scope

1. **First-use entry and orientation**
   - Explain, in concise product copy, that a topic produces a reviewable
     research plan followed by an evidence-backed strategic report.
   - Provide a clear signed-out entry (sign in / create account) and a
     logged-in empty state with one primary action: create a topic.
   - Use an example topic only as assistive placeholder/help, never as a
     required template or unverified promise.

2. **Actionable workflow states**
   - In the topic list and workspace, make the current state and next user
     action explicit: planning → review plan → generating report → report
     ready / failed / cancelled.
   - Give useful loading, waiting, empty, and recoverable-error copy. Preserve
     the topic and tell the user whether to wait, retry, or contact support;
     do not expose raw API/SSE errors as the primary message.
   - At the plan gate, state what approving does and that cancelling only
     reliably stops work at a gate until the known backend cancellation gap is
     fixed.

3. **Return and account continuity**
   - Make the authenticated user's identity and sign-out action visible.
   - Make “My topics” the return home and show each topic's meaningful next
     action or most recent completed outcome, not only an internal state code.
   - After report delivery, give a clear next action: return to topics or,
     once #16c ships, enable monitoring from that workspace.

4. **Pilot readiness validation**
   - Add a short manual test script for a new account on test1 covering:
     register/login → understand empty state → create topic → observe planning
     → review and proceed → read report → sign out/in → reopen own topic.
   - Test keyboard-operable primary actions, visible focus, non-color-only
     state meaning, and tablet-width usability for this flow.
   - Validate wording and flow with 3–5 target pilot users or structured
     founder-led sessions. Record observed confusion and completion blockers;
     do not claim research results before those sessions occur.

## Out of scope

- New topic/research/report/monitoring API behavior — #16 and backend tickets.
- A cross-topic market-signals dashboard, dense scheduler table, or admin view
  — #34 / later product work.
- Monitoring controls and delta timeline — #16c after #22 live verification.
- Browser environment switching for customers; pilot users use the designated
  product URL, while test-slot selection remains an operator concern.
- Password reset, OAuth, account profile editing, notification preferences, and
  billing. The MVP account surface is identity visibility plus sign out.
- Fixing cancellation of in-flight plan/deliver work; document its limitation
  until its backend ticket exists.

## Acceptance criteria

- [ ] A new user can state, before creating a topic, what they will review and
  receive.
- [ ] The empty state gives one unambiguous next action and the create form has
  a concrete example/helpful prompt.
- [ ] Every primary workflow state tells the user what is happening and what
  they can do next without relying on internal state names alone.
- [ ] Loading, SSE disconnect, API error, failed, and cancelled states preserve
  context and offer an understandable recovery path.
- [ ] A returning user can find only their own topics and resume the next
  meaningful action after a new login.
- [ ] The report-ready screen makes the delivered report and sources the visual
  outcome, with a clear next action.
- [ ] The new-account manual smoke and basic accessibility checks pass on
  test1.
- [ ] At least one structured pilot-session result is recorded before broad
  self-serve acquisition is claimed.

## Related

- `docs/specs/active/signalgather_frontend_v1_16.md` — UI shell, workspace,
  report reader, monitoring
- `docs/specs/done/topic_user_ownership_24.md` — JWT user scoping
- `docs/specs/active/topic_ops_table_frontend_34.md` — later ops dashboard
- `STATUS.md` — product build sequence
- `testing/app_testing_scenario.md` — API lifecycle to translate into a UI smoke
