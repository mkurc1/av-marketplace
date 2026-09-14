#!/usr/bin/env python3
"""Contract test for code-review's composite findings.

Spec: docs/superpowers/specs/2026-09-14-composite-findings-design.md, §13.
Run:  python3 plugins/code-review/tests/test_composite_contract.py

Each test greps one invariant across the plugin's prose files. Each carries a
`# mutation:` comment quoting the sentence whose deletion must make it fail;
the mutation run (delete the sentence, watch the test fail, restore it) is
recorded in the pull request description. An assertion without that comment
is not a contract test.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

FIX_AUTO = "plugins/code-review/agents/fix-auto.md"
FIX = "plugins/code-review/commands/fix.md"
FIX_ALL = "plugins/code-review/commands/fix-all.md"
FIX_REPORT = "plugins/code-review/commands/fix-report.md"
REVIEW = "plugins/code-review/commands/review.md"
CROSS = "plugins/code-review/agents/cross-verifier.md"
ANALYST = "plugins/code-review/agents/composition-analyst.md"
GATE = "plugins/code-review/skills/decision-gate/SKILL.md"
DECISION_ANALYST = "plugins/code-review/agents/decision-analyst.md"
DOCS = "docs/plugins/code-review.md"
EXTRACT = "plugins/code-review/scripts/extract-issue-ids.sh"


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.is_file():
        raise AssertionError(f"missing file: {rel}")
    return path.read_text(encoding="utf-8")


class CompositeContract(unittest.TestCase):
    # ---- Task 1: prefix and category ------------------------------------

    def test_docs_prefix_table_has_composite_row(self):
        # mutation: delete the `| Composite | COMP | docs/reviews/ |` row in docs/plugins/code-review.md
        self.assertRegex(
            read(DOCS), r"(?m)^\|\s*Composite\s*\|\s*COMP\s*\|\s*`docs/reviews/`\s*\|", "docs table lacks the Composite | COMP row"
        )

    def test_fix_id_regex_has_comp(self):
        # mutation: remove `COMP` from fix.md's `^(SEC|PERF|ARCH|MAINT|DOC|QA|COMP)-\d{3}$` pattern
        self.assertRegex(read(FIX), r"\^\(SEC\|PERF\|ARCH\|MAINT\|DOC\|QA\|COMP\)-\\d\{3\}\$")

    def test_fix_auto_category_enum_has_composite(self):
        # mutation: remove `\|Composite` from fix-auto.md's `**Category:**` alternation
        self.assertRegex(read(FIX_AUTO), r"\*\*Category:\*\* Security\\\|Performance\\\|Architecture\\\|Maintainability\\\|Documentation\\\|Testing\\\|Composite")

    def test_extract_issue_ids_has_comp(self):
        # mutation: remove `|COMP` from extract-issue-ids.sh's PREFIX_RE
        self.assertIn("PREFIX_RE='(SEC|PERF|ARCH|MAINT|DOC|COMP)'", read(EXTRACT))

    # ---- Task 2: fix-auto composite mode ---------------------------------

    def test_fix_auto_composite_mode_switch(self):
        # mutation: delete the sentence "When the first block's `Category` is `Composite` **and** it carries a `**Composed-of:**` line, you are in composite mode" from fix-auto.md
        self.assertIn(
            "When the first block's `Category` is `Composite` **and** it carries a `**Composed-of:**` line, you are in composite mode",
            read(FIX_AUTO),
        )

    def test_fix_auto_root_cause_only_rule_verbatim(self):
        # mutation: delete the italic rule "In composite mode you implement the composite's Remediation. …" from fix-auto.md Phase 3
        self.assertIn(
            "it is never applied, in this phase or in Phase 5's iterations",
            read(FIX_AUTO),
        )

    def test_fix_auto_components_table_and_results(self):
        # mutation: delete the `**Components:**` table or any of the five Result values from fix-auto.md Phase 6
        text = read(FIX_AUTO)
        self.assertIn("**Components:**", text)
        for value in ("resolved", "unresolved (no location)", "skipped (fixed)", "skipped (rejected)"):
            self.assertIn(f"`{value}`", text, f"Result value {value} missing")

    def test_fix_auto_verdict_over_checked_components(self):
        # mutation: delete "The verdict is computed over the components actually checked" from fix-auto.md Phase 6
        self.assertIn("The verdict is computed over the components actually checked", read(FIX_AUTO))


if __name__ == "__main__":
    unittest.main(argv=[sys.argv[0]] + sys.argv[1:], verbosity=2)
