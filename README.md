# Medicare Decoded Guide

A warm, plain-English Medicare paperwork manual — education and admin
help only: what Medicare is in one picture, enrollment windows without
panic, Parts A–D translated, Advantage vs. Supplement trade tables in
round numbers, how to read a plan's fine print, Extra Help programs,
avoiding plan-switching scams, and your own enrollment binder, with
printable decision worksheets and a glossary.

**Education and paperwork help only.** Nothing in this project is
medical, legal, or financial advice — and it is never *plan* advice. It
explains paperwork; it never picks plans, never advises about health,
and never asks for personal information (because it can't: it's a book).

## Why

Medicare paperwork arrives as letters, windows, and twenty fall mail
pieces, usually all at once and usually accompanied by television ads.
This manual translates the whole system "like a friend would": plain
English, step by step, never condescending, with round made-up numbers
($100 premiums, $500 copays) so the *idea* stays clear while your real
numbers always come from your own plan papers.

## Read it

- **On GitHub-style readers:** just open the files in
  [`docs/`](docs/index.md) — they're plain Markdown.
- **As a local website (recommended):**

  ```bash
  python3 build.py          # builds the static site into site/
  python3 build.py --check  # build + verify every internal link
  ```

  Then open `site/index.html` in a browser. Works fully offline; no
  network, no accounts, nothing leaves your machine.

## What's inside

| Part | What it covers |
| --- | --- |
| [Start Here](docs/index.md) | The whole guide in six sentences |
| Ch. 1 — Medicare in One Picture | The two doors: Original vs. Advantage |
| Ch. 2 — Enrollment Windows, Calmly | The four windows (and two situational ones), penalties without panic |
| Ch. 3 — Parts A–D, Translated | Hospital, doctors, the Advantage delivery, drugs — with round numbers |
| Ch. 4 — Advantage vs. Supplement | Trade tables in round numbers: Plan Alpha vs. Plan Beta, honestly |
| Ch. 5 — Reading the Fine Print | The six papers, the three pages to actually read, phrase decoder |
| Ch. 6 — Extra Help Programs | Extra Help, Medicare Savings Programs, Medicaid, and where to apply |
| Ch. 7 — Avoiding Plan-Switching Scams | Scam shapes, illegal switches, first aid, a scam-proofing checklist |
| Ch. 8 — Your Enrollment Binder | Six tabs, a yearly one-hour ritual, privacy rules |
| Ch. 9 — Glossary | Plain words for Medicare paper |
| [The Education-Only Promise](docs/disclaimer.md) | What this guide is, and is not |
| Worksheets | [Advantage or Supplement?](docs/worksheets/decision-worksheet-advantage-or-supplement.md), [Fine-Print Comparison](docs/worksheets/plan-fine-print-comparison-worksheet.md), [My Deadlines](docs/worksheets/enrollment-deadlines-worksheet.md), [Binder Inventory](docs/worksheets/binder-inventory-worksheet.md), [Plan Call Notes](docs/worksheets/plan-call-notes-worksheet.md) |

## Testing

```bash
python3 -m unittest discover -s tests -v
```

The test suite builds the site, checks every internal link and anchor,
verifies all chapters/worksheets render, guards converter regressions,
and enforces the education-only guardrails (no personal-data-shaped
strings, no secrets, the exact LICENSE copyright, the LLC credit).
Run after any edit.

## Companion projects

- **medical-bills-comfort-guide** — what happens *after* care, when the
  bill and the EOB arrive. This guide hands off there.
- **hospital-stay-companion-guide** — planned and surprise stays, from
  packing to homecoming.
- This guide covers the insurance side: the letters, the windows, and
  the plans — so the paperwork has a home in every season.

## Project details

- **License:** MIT — see [LICENSE](LICENSE).
- **Copyright (c) 2026 Asdale Dynamics, LLC** of Indiana — plain-English
  AI education, books, and practical life-admin tools
  (dylanasdale.github.io, *The Massive AI Manual*).
- **Local-first and private:** static HTML from your own Markdown; no
  services, no trackers, no secrets, no personal data anywhere in the
  repo.
