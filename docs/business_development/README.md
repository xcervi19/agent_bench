# Business development — plans and product features ahead of the build queue

This folder holds **where the product could go**, written down before it is a ticket.
It is the step before `docs/specs/`: an idea lives here until someone decides to build
it, then it gets a number in `docs/specs/TICKET_REGISTRY.md` and a spec, and the entry
here links to it.

What belongs here:

- product feature ideas, with the evidence that suggested them;
- commercial angles — what a trading desk would pay for, and how we show it;
- pilot and engagement shapes for prospective customers.

What does not: the current product definition (`docs/product/README.md`), the
requirements already agreed (`docs/specs/business_requirements/`), and the first-customer
plan (`docs/specs/business_requirements/go_to_market_first_customer.md`).

## Documents

| File | What it is |
|---|---|
| [`product_feature_ideas.md`](product_feature_ideas.md) | Feature and positioning ideas from the review of the three test2 topics (Japan nuclear, India gas, India coal), 2026-10-10 |

## How to use an entry

Each idea carries a **status**: `idea` (written down, not discussed), `agreed` (the owner
wants it), `ticketed` (has a spec number — link it), `dropped` (with the reason). Change
the status in place; do not delete an entry, because the reason something was not built
is context too.
