"""Tests for the Medicare Decoded Guide.

Run with:  python3 -m unittest discover -s tests -v

Covers: building the static site, the Markdown converter's documented
subset, presence of all chapters/worksheets, internal link integrity,
education-only guardrails, and repo hygiene (no secrets/personal-data-
looking strings, exact LICENSE copyright, README credit).
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import build as build_mod  # noqa: E402


class BuildSiteTests(unittest.TestCase):
    """Actually build the site, then check the outputs."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.written = build_mod.build()

    def test_build_succeeds_and_creates_all_pages(self):
        expected = {
            Path("site") / Path(f).with_suffix(".html") for f, _ in build_mod.CHAPTERS
        }
        written = {Path(p) for p in self.written}
        self.assertEqual(
            written & expected, expected, "missing generated pages"
        )

    def test_style_sheet_is_copied(self):
        self.assertTrue((build_mod.SITE / "style.css").exists())

    def test_pages_have_nav_and_disclaimer(self):
        for f, label in build_mod.CHAPTERS:
            page = (build_mod.SITE / f).with_suffix(".html")
            text = page.read_text(encoding="utf-8")
            self.assertIn(label, text, f"nav missing entry for {f}")
            self.assertIn("Education and paperwork help only", text)
            self.assertIn("1-800-MEDICARE", text)

    def test_no_absolute_paths_or_file_urls(self):
        for html_file in build_mod.SITE.rglob("*.html"):
            text = html_file.read_text(encoding="utf-8")
            self.assertNotIn("file://", text)
            self.assertNotIn(str(build_mod.ROOT), text)

    def test_footer_copyright_present(self):
        index = (build_mod.SITE / "index.html").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", index)

    def test_built_site_is_uptodate(self):
        """The repo copy of site/ (if present) matches a fresh rebuild."""
        for src in (ROOT / "docs").rglob("*.md"):
            rel = src.relative_to(build_mod.DOCS).with_suffix(".html")
            freshest = build_mod.SITE / rel
            if not freshest.exists():
                continue
            mtime_src = src.stat().st_mtime
            mtime_out = freshest.stat().st_mtime
            self.assertGreaterEqual(
                mtime_out, mtime_src, f"site/ stale for {rel} — rerun build.py"
            )


class LinkIntegrityTests(unittest.TestCase):
    def test_internal_links_resolve(self):
        build_mod.build()
        broken = build_mod.check_links()
        self.assertEqual(broken, [], "broken internal links found")

    def test_link_check_actually_works(self):
        # sanity: the checker should flag a deliberately broken link
        target = build_mod.SITE / "index.html"
        original = target.read_text(encoding="utf-8")
        marker = 'href="01-one-picture.html"'
        self.assertIn(marker, original)
        try:
            target.write_text(original.replace(marker, 'href="no-such-file.html"'), encoding="utf-8")
            broken = build_mod.check_links()
            self.assertTrue(any("no-such-file.html" in b for b in broken))
        finally:
            target.write_text(original, encoding="utf-8")
            build_mod.build()


class ConverterTests(unittest.TestCase):
    def conv(self, md: str) -> str:
        return build_mod.convert_markdown(md)

    def test_headings_get_ids(self):
        html_out = self.conv("## Enrollment Windows, Calmly and Unhurried")
        self.assertIn('id="enrollment-windows-calmly-and-unhurried"', html_out)

    def test_paragraph(self):
        html_out = self.conv("Just a paragraph.")
        self.assertEqual(html_out, "<p>Just a paragraph.</p>")

    def test_lists(self):
        html_out = self.conv("- one\n- two\n1. first\n2. second")
        self.assertIn("<ul>\n<li>one</li>\n<li>two</li>\n</ul>", html_out)
        self.assertIn("<ol>\n<li>first</li>\n<li>second</li>\n</ol>", html_out)

    def test_wrapped_list_item_joins(self):
        html_out = self.conv("- hospital\n  care bucket\n- doctors bucket")
        self.assertNotIn("<p>care bucket</p>", html_out)
        self.assertIn("<li>hospital care bucket</li>", html_out)

    def test_checkbox_list(self):
        html_out = self.conv("- [ ] task one\n- [ ] task two")
        self.assertIn("<li>[ ] task one</li>", html_out)

    def test_table(self):
        html_out = self.conv("| A | B |\n| --- | --- |\n| 1 | 2 |")
        self.assertIn("<table>", html_out)
        self.assertIn("<th>A</th>", html_out)
        self.assertIn("<td>2</td>", html_out)

    def test_fenced_code_escapes_brackets(self):
        html_out = self.conv("```\n[ ] checkbox\n```\n")
        self.assertIn("[ ] checkbox", html_out)
        self.assertNotIn("<ble", html_out)

    def test_blockquote(self):
        html_out = self.conv("> Hello there.\n> This is a quote.")
        self.assertIn("<blockquote>", html_out)
        self.assertIn("This is a quote.", html_out)

    def test_inline_elements(self):
        html_out = self.conv("**bold** and *soft* and `code`")
        self.assertIn("<strong>bold</strong>", html_out)
        self.assertIn("<em>soft</em>", html_out)
        self.assertIn("<code>code</code>", html_out)

    def test_bold_and_nested_emphasis(self):
        html_out = self.conv("**bold *nested* text** stays")
        self.assertIn("<strong>bold <em>nested</em> text</strong>", html_out)

    def test_bold_across_wrapped_lines(self):
        html_out = self.conv("a **bold\nphrase** here")
        self.assertIn("<strong>bold<br />phrase</strong>", html_out)

    def test_html_is_escaped(self):
        html_out = self.conv("Angle <brackets> & ampersands")
        self.assertIn("&lt;brackets&gt;", html_out)
        self.assertIn("&amp;", html_out)

    def test_hr(self):
        self.assertIn("<hr />", self.conv("---"))


class ContentPresenceTests(unittest.TestCase):
    DOCS = ROOT / "docs"

    def doc(self, name: str) -> str:
        return (self.DOCS / name).read_text(encoding="utf-8")

    def test_all_chapters_exist(self):
        for f, _ in build_mod.CHAPTERS:
            self.assertTrue((self.DOCS / f).exists(), f"missing doc {f}")

    def test_one_picture_diagram_present(self):
        text = self.doc("01-one-picture.md")
        self.assertIn("ORIGINAL MEDICARE", text)
        self.assertIn("MEDICARE ADVANTAGE", text)

    def test_enrollment_windows_covered(self):
        text = self.doc("02-enrollment-windows.md")
        for marker in [
            "Initial Enrollment Period",
            "Fall Open Enrollment",
            "Advantage Open Enrollment",
            "Special Enrollment Period",
            "General Enrollment Period",
            "Medigap Open Enrollment",
        ]:
            self.assertIn(marker, text)

    def test_parts_translated(self):
        text = self.doc("03-parts-a-through-d.md")
        for marker in ["Part A", "Part B", "Part C", "Part D", "hospital", "doctors", "drugs"]:
            self.assertIn(marker, text)

    def test_trade_tables_in_round_numbers(self):
        text = self.doc("04-advantage-vs-supplement.md")
        for marker in ["Plan Alpha", "Plan Beta", "$0", "out-of-pocket maximum", "$140"]:
            self.assertIn(marker, text)
        self.assertIn("Every number is invented", text)

    def test_fine_print_terms(self):
        text = self.doc("05-reading-fine-print.md").lower()
        for marker in [
            "summary of benefits",
            "evidence of coverage",
            "anoc",
            "formulary",
            "prior authorization",
            "star ratings",
        ]:
            self.assertIn(marker, text)

    def test_extra_help_programs(self):
        text = self.doc("06-extra-help-programs.md")
        for marker in ["Extra Help", "Low-Income Subsidy", "Medicare Savings Program", "QMB", "SLMB", "QI", "Medicaid", "PACE"]:
            self.assertIn(marker, text)

    def test_scam_guards(self):
        text = self.doc("07-avoiding-scams.md")
        for marker in ["1-800-MEDICARE", "gift card", "permission slip", "confirmation number"]:
            self.assertIn(marker, text)

    def test_binder_six_tabs(self):
        text = self.doc("08-enrollment-binder.md")
        for marker in ["Contacts", "Current plan", "Enrollment records", "Money papers", "Notes & worksheets", "six tabs"]:
            self.assertIn(marker, text)

    def test_glossary_defines_key_terms(self):
        text = self.doc("09-glossary.md")
        for marker in [
            "Accepts assignment",
            "ANOC (Annual Notice of Change)",
            "Formulary",
            "Prior authorization",
            "SHIP",
            "Out-of-pocket maximum",
            "Underwriting",
        ]:
            self.assertIn(marker, text)

    def test_disclaimer_promise_present(self):
        text = self.doc("disclaimer.md")
        self.assertIn("THIS GUIDE EXPLAINS PAPER", text)

    def test_decision_worksheet_present(self):
        text = self.doc("worksheets/decision-worksheet-advantage-or-supplement.md")
        for marker in ["Step 1", "Step 4", "SHIP", "My one-line summary"]:
            self.assertIn(marker, text)

    def test_all_five_worksheets_exist(self):
        names = [f for f, _ in build_mod.CHAPTERS if f.startswith("worksheets/")]
        self.assertEqual(len(names), 5)

    def test_disclaimer_in_every_doc(self):
        needle = "never medical, legal, financial, or plan advice"
        for f in self.DOCS.rglob("*.md"):
            text = re.sub(r"\s+", " ", f.read_text(encoding="utf-8"))
            self.assertIn(needle, text, f"education-only line missing in {f.name}")

    def test_no_personal_looking_data(self):
        pattern = re.compile(r"\b(\d{3}-\d{2}-\d{4})\b")  # SSN-shaped strings
        for f in self.DOCS.rglob("*.md"):
            self.assertIsNone(pattern.search(f.read_text()), f"SSN-like string in {f.name}")


class RepoHygieneTests(unittest.TestCase):
    def test_license_exact_copyright(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", text)

    def test_readme_credits_llc(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", text)

    def test_no_obvious_secrets(self):
        pattern = re.compile(
            r"(api[_-]?key\s*[:=]\s*['\"]?[A-Za-z0-9]{16,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,})",
            re.IGNORECASE,
        )
        for f in ROOT.rglob("*"):
            if not f.is_file() or f.name.startswith(".git"):
                continue
            if f.suffix not in {".py", ".md", ".css", ".txt"}:
                continue
            self.assertIsNone(pattern.search(f.read_text(errors="ignore")), f"secret-like string in {f}")


if __name__ == "__main__":
    unittest.main()
