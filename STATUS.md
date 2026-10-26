# STATUS — Medicare Decoded Guide

As of 2026-10-26.

## What was built

A complete, education-only Medicare paperwork manual (never plan or
medical advice), in the house style of the sibling guides (plain English,
warm, step by step, round teaching numbers):

- `docs/index.md` — Start Here: the whole guide in six sentences, who
  it's for, a route table, and the standing disclaimer.
- `docs/01-one-picture.md` — what Medicare is in one ASCII picture (the
  two doors: Original Medicare vs. Medicare Advantage), the four letters
  in one breath, what Original typically does not cover (custodial
  long-term care, most dental/hearing/vision, care abroad), the cast of
  characters (CMS, SSA, private plans, SHIP, 1-800-MEDICARE), and the
  five round-number vocabulary words (premium, deductible, copay,
  coinsurance, out-of-pocket maximum).
- `docs/02-enrollment-windows.md` — enrollment windows without panic:
  the four windows everyone should know (IEP, Fall Open Enrollment,
  Advantage Open Enrollment, SEPs), the two situational ones (General
  Enrollment, Medigap open enrollment), the IEP start-date logic, the
  employer-coverage detour, late penalties in round numbers, five panic
  killers, and a phone sentence for SEPs.
- `docs/03-parts-a-through-d.md` — Parts A–D translated with teaching
  numbers each (A: hospital, premium-free for most, benefit periods,
  observation-status surprise; B: doctors, the open-ended 20%; C: a
  delivery, not a benefit — networks, prior auth, out-of-pocket max;
  D: formularies, tiers, the yearly drug cap, creditable coverage), plus
  a pretend-$10,000-stay table and what each part does not do.
- `docs/04-advantage-vs-supplement.md` — three honest trade tables in
  round numbers: headline trade-offs; a pretend year (Plan Alpha
  Advantage vs. Plan Beta Original + Medigap G + Part D, quiet year and
  rough year); and a "$0 premium" decoder. Medigap specifics (letter
  plans, F vs. G, the 6-month window, underwriting), who-tends-to-pick-
  what patterns (explicitly not advice), and a one-sentence summary.
- `docs/05-reading-fine-print.md` — the six official papers, the three
  pages to read if you read nothing else, a copay-row decoder table, a
  fine-print-phrase translation table, the five questions before
  comparing plans, star ratings in one honest paragraph, and red-flag
  fine print.
- `docs/06-extra-help-programs.md` — Extra Help (LIS), Medicare Savings
  Programs (QMB/SLMB/QI), Medicaid dual coverage, PACE flagged, a
  where-to-apply table, a worked round-number example, and three
  applying-safely rules (applying is free; offices never call first;
  keep approval letters).
- `docs/07-avoiding-scams.md` — the three golden rules, six scam shapes
  in a table, illegal-switching symptoms, a five-step first-aid list
  (anchored by the 1-800-MEDICARE "what plan am I in, and who authorized
  it" call), and a printable scam-proofing checklist.
- `docs/08-enrollment-binder.md` — the six-tab enrollment binder:
  shopping list (~$15), tab-by-tab contents, the twice-yearly one-hour
  ritual, privacy/shredding rules, offline digital backup, and a
  low-energy mode (15 minutes a month, one tab at a time).
- `docs/09-glossary.md` — 45 plain-words definitions, alphabetical,
  plus "words that sound scarier than they are."
- `docs/disclaimer.md` — the education-only promise, including what the
  guide is not, where real decisions happen (a table), and the guide's
  one set of capital letters.
- `docs/worksheets/` — five printable worksheets: the Advantage-or-
  Supplement decision worksheet (values → facts → round-number math →
  SHIP questions → one-line summary), the side-by-side fine-print
  comparison, the personal deadlines calendar, the binder inventory
  checklist, and the plan-call notes log with confirmation numbers.
- `build.py` (+ `build.sh`) — zero-dependency Python 3 stdlib static
  site builder: Markdown → HTML with sidebar nav, print-friendly CSS in
  `assets/style.css`, and a `--check` mode verifying every internal link
  and anchor.
- `tests/test_build.py` (+ `test.sh`) — 39 tests, described below.
- `README.md`, `LICENSE` (MIT), `.gitignore`.

Every doc carries the line "never medical, legal, financial, or plan
advice"; the guide consistently points real decisions to 1-800-MEDICARE,
Social Security, SHIP, and plan papers.

## How to run it

```bash
python3 build.py --check   # build site/ + verify all internal links
./test.sh                  # full test suite (also builds the site)
```

Then open `site/index.html` in a browser. Fully offline afterwards; no
network, accounts, or trackers. Python 3 standard library only.

## Verification results

- `python3 build.py --check` → builds all 17 files (16 pages + CSS);
  "Link check: all internal links resolve."
- `./test.sh` → **39 tests, all OK**:
  - build produces every chapter/worksheet/disclaimer page plus the
    stylesheet; every page has the 16-entry nav, the education-only
    sidebar notice, and 1-800-MEDICARE;
  - no `file://` URLs or absolute local paths in output; footer
    copyright present on every page;
  - all internal links and anchors resolve, and the checker provably
    flags a deliberately broken link;
  - converter regressions guarded (headings/IDs, paragraphs, lists
    incl. checkbox items and wrapped-item continuation, tables, fenced
    code escaping, blockquotes, inline bold/italic/nested emphasis,
    bold across wrapped lines, escaping, hr);
  - content guards: the one-picture diagram, all six enrollment windows,
    Parts A–D coverage, the three trade tables with invented-number
    notice, fine-print terms, Extra Help program names, scam guards
    (1-800-MEDICARE, gift card, permission slip), six binder tabs, 45-
    term glossary anchors, the capitalized disclaimer promise, all five
    worksheets, and the education-only line in every single doc;
  - repo hygiene: LICENSE copyright is exactly
    "Copyright (c) 2026 Asdale Dynamics, LLC", README credits the LLC,
    no secret-shaped or SSN-shaped strings anywhere.
- HTTP smoke test (local `http.server`): `/`, one chapter page, one
  worksheet, and `style.css` all return 200.
- Fixes made during this pass: corrected an arithmetic inconsistency in
  the chapter 4 pretend-year table (Plan Beta's quiet-year total now
  matches its rows: $2,740), replaced a self-referential glossary link
  with a Start Here link, and made three content guards
  whitespace/case-robust (the wrapped disclaimer line, lowercased
  fine-print markers, "Every number is invented").

## Known gaps

- **By design:** every dollar figure is an invented teaching number
  (premiums, copays, penalties, the worked Extra Help example) — the
  guide deliberately avoids quoting current-year official amounts, which
  change annually; it points to Social Security, 1-800-MEDICARE, and
  plan papers for the real numbers. Rules like the 7-month IEP and the
  Oct 15–Dec 7 window are described in their stable federal shapes, with
  "confirm with SHIP / the official offices" standing instructions.
- No search function or dark mode on the built site; sidebar nav only
  (consistent with sibling guides).
- US-specific by nature (Medicare, SHIP, Medicaid); other regions would
  need their own guide.
- The site is static HTML; the worksheets print via the browser's print
  dialog (print CSS included), not generated PDFs.
- Companion-project links (medical-bills-comfort-guide,
  hospital-stay-companion-guide, free-health-admin-kit) are by name, not
  URL, since they are sibling repositories with no fixed relationship
  in-repo.
- The Part D yearly drug cap is described by shape ("in the low
  thousands; the official number changes") rather than by exact current
  amount, for the same durability reason as above.
