# Composite Findings Design

**Date:** 2026-09-14
**Plugin:** code-review (2.0.1 → 2.1.0)
**Status:** Draft, pending user review

## 1. Problem

A review routinely produces many findings that share one cause: five "missing input validation in endpoint X" findings that are really one missing validation layer, or a God Object with a vulnerability inside it and no tests around it, where one refactor closes all three. Today `/fix-all` and `/fix-report` hand every finding block to `fix-auto` one at a time. The fixer sees one symptom, patches it locally, and the next fixer patches the next symptom. The result is N local patches where one structural change was the right fix, and a codebase that now carries the band-aids as well as the cause.

The cross-verifier already names some of these groups as `[COMPOSITE-N]` findings, but `/review`'s merge step only says "add Cross-Verifier composite findings" and never defines how a composite reaches the saved report or what happens to its bases. Nothing in the fix commands recognises a group at all.

## 2. Goals and non-goals

**Goals**

- A composite is a first-class finding in the report: it has an ID, a location, a shared cause and a single remediation, and it names its components.
- The fixers fix a composite as one unit and never its components separately while the composite is open, with one stated exception: the user may choose to fix a component alone at `/fix`'s Step 0.4.5 (§9).
- Compositions are recognised both at review time and at fix time, and both are persisted into the report so a later run and `/fix <ID>` see the same grouping.
- The user keeps a one-question veto over every grouping the run is about to act on.
- Old reports, QA reports and feedback reports keep parsing and fixing without migration; QA reports are never grouped, while old review and feedback reports become eligible for fix-time grouping like any review report (§6.1).

**Non-goals**

- Ordering or conflict resolution between findings that touch the same code but do not share a cause. That is a separate problem.
- Grouping across report files. A composite never spans the review report and the QA report.
- Any change to `/qa:loop`.
- Machine enforcement of the fixer's "root cause only" rule. It is prose-enforced, like the execution boundary.

## 3. Definitions

| Term | Meaning |
|---|---|
| **composite** | A finding block of Category `Composite` with a `**Composed-of:**` list of at least two component IDs from the same report file. |
| **component** | A finding listed in some composite's `**Composed-of:**`. |
| **composition** | The relation: one change, described in the composite's Remediation, resolves every component's Problem without applying any component's own Remediation. |
| **origin** | Who grouped: `review` (the cross-verifier, rendered by `/review`) or `fix-time` (the composition pass in a fix command). |
| **open composite** | A composite carrying no `**Status:**` line. |
| **bound component** | A component of a **dispatchable** composite. Bound components are never dispatched on their own, with one stated exception: a component the user chooses to fix alone at `/fix`'s Step 0.4.5 (§9). |
| **released component** | A component whose composite carries any `**Status:**` line. It is treated as an ordinary finding again. |
| **degenerate composite** | An open composite with fewer than two unfixed components present in its file. |
| **candidate** | An unfixed finding in a review report that is named in no open composite's `**Composed-of:**`, is not itself a composite, and carries no `**Decision:**` or `**Dispatch:**` line. Candidates are what the composition pass may group. |
| **dispatchable composite** | An open composite that is not degenerate. Only dispatchable composites are queued, listed under Composites, and offered in the dissolve question. |

## 4. Report format

### 4.1 The composite block

A composite uses the existing issue-block grammar with a new Category and two new fields:

```markdown
### [HIGH] COMP-001: Missing input validation layer

**ID:** COMP-001
**Location:** `src/api/validation.py:1`
**Category:** Composite
**Composed-of:** SEC-002, SEC-003, ARCH-001
**Origin:** review
**Effort:** medium

**Problem:**
The shared cause, stated once. Not a list of the components' symptoms.

**Impact:**
What the combination costs.

**Remediation:**
The single change that resolves every component. May carry a code block.
```

Field rules:

- `**Location:**` is the primary site of the shared fix, in `path:line` or `path:line-range` form, and contained in the repository tree by the three-step containment test of *The usability rule* in `code-review:decision-gate`. It is required: stage 0 of the decision gate and `fix-auto`'s Phase 1 both refuse a block without a usable location. Neither of those is a containment gate on the `auto` path — stage 0 runs for needs-decision findings only, and `fix-auto`'s Phase 1 parses the field without testing containment — so for an `auto` composite containment is enforced where the value is authored: §6.4 at fix time, and §5.2's block building at review time, which builds this field to this rule.
- `**Composed-of:**` lists component IDs separated by `, `. At least two, at most twelve. Every ID belongs to the same report file as the composite. **`Composed-of` is the source of truth for membership.** It occupies exactly one physical line with no continuation line of any kind, and carries bare (unbackticked) `PREFIX-NNN` tokens: a consumer reads the IDs on that line and nothing else, so a wrapped line would silently lose members. A grouping that would exceed twelve is not written — the composition pass caps a proposal at twelve members and lists the remainder under its rejected groupings. `**Part-of:**` and `**Origin:**` are one physical line each, likewise.
- `**Origin:**` is `review` or `fix-time`.
- `**Fix-policy:** needs-decision` is present when any component carries a `**Fix-policy:**` value other than `auto` (an unparseable value counts, mirroring the fixers' fail-safe). Otherwise the field is absent.
- No `**OWASP:**`, `**CWE:**` or `**Drift-class:**` on a composite. Components carry their own.

### 4.2 The component marker

Each component carries one line, placed directly after its `**ID:**` line, or directly after the heading where the block has no `**ID:**` line:

```markdown
**Part-of:** COMP-001
```

`Part-of` is a derived back-reference for readers. It is written whenever a composite is persisted, but membership is decided by `Composed-of` alone: a missing or dangling `Part-of` changes nothing about what is bound. A component belongs to at most one open composite.

### 4.3 Rules

- **Category `Composite`, prefix `COMP`, directory `docs/reviews/`.** The row joins the canonical Category→Prefix table in `docs/plugins/code-review.md`. `check-prefix-sync.sh` then requires the three consumers to carry it: the ID regex in `commands/fix.md`, the Category enum in `agents/fix-auto.md`, and `PREFIX_RE` in `scripts/extract-issue-ids.sh`.
- **Severity is never below the maximum of the components.** The cross-verifier may escalate above it; the composition pass writes exactly the maximum. A fixer's severity floor therefore never admits a component while dropping its composite. Where a hand-edited report violates this, the fixers raise the composite's effective severity to the maximum for the run and do not rewrite the report.
- **Composites never nest.** A `COMP-` ID inside a `Composed-of` list is treated as a missing ID.
- **Binding.** A `Part-of` relation binds while the composite is open. Any `**Status:**` line on the composite, whichever value, releases its components: a released component without a status of its own is an ordinary unfixed finding on the next run.
- **The new fields are authored fields, not loop-written ones.** `Composed-of` and `Origin` sit inside the composite's own block and are hashed into its `**Decision-pin:**`; they travel in the dispatch copy, as does each component's `Part-of`. The pin's block hash covers the composite's own block alone — component blocks travel in the payload unpinned (§16) — and membership is protected because `Composed-of` is inside the hashed block. The decision gate's closed exclusion list is unchanged. This holds because the composition pass writes its markers before any pin is computed in the same run, and because a finding carrying `**Decision:**` or `**Dispatch:**` is never a candidate.

## 5. Review side

### 5.1 Cross-verifier

The `### 6. Composite Findings` task and the `### Composite Findings` output section are tightened:

- A composite is proposed **only where one change resolves every basis**. Where the bases need separate fixes, the observation is a correlation, not a composite.
- The output format gains `Location:` (primary site of the shared fix, `path:line`), `Effort:` and `Cause:` (the shared cause, one paragraph). `Remediation:` must describe the single change; `Combined risk:` is what the combination costs.
- Bases are cited by the exact finding title as the auditor wrote it; a documentation basis may cite its `DOC-NNN` ID instead, since the documentation auditor emits IDs.

The finding-falsification exemption for the cross-verifier stands: composites derive from findings that already passed the auditors' batteries and the challenger.

### 5.2 `/review` Step 5.5, item "Add Cross-Verifier composite findings"

The item gets a body. For each composite the cross-verifier returned:

1. Resolve each basis by exact title (or `DOC-NNN` ID) against the findings that survived the challenger. A basis the challenger removed, that matches nothing, or that matches more than one surviving finding is dropped — an ambiguous title is not a resolved basis.
2. Disjointness: process the composites in the order the cross-verifier returned them; a basis already resolved into an earlier composite is dropped from every later one, mirroring §6.4, so no finding is a component of two composites (§4.2). A composite left with fewer than two bases falls to the next item and stays a bullet.
3. Fewer than two bases remain → the composite is **not** rendered as a finding block. Its text stays a plain bullet under `### Cross-Analysis` in the Verification Summary, never as a `###` heading.
4. Otherwise build a finding block: severity = the greater of the cross-verifier's severity and the maximum basis severity; `Category: Composite`; `Location` and `Effort` from the composite, `Problem` from its `Cause`, `Impact` from its `Combined risk`, `Remediation` from its `Remediation`; `Origin: review`; `Fix-policy: needs-decision` per §4.1 when any basis carries a non-`auto` policy. `Location` is validated to the §4.1 rule — it parses by the two-clause read rule, is contained in the repository tree by the three-step containment test, and exists there; a composite whose `Location` fails any conjunct is **not** rendered as a finding block and stays a bullet under `### Cross-Analysis`, never repaired.

### 5.3 `/review` Step 5.6, ID assignment

- A `comp_count` counter joins the others. COMP IDs are assigned **after every other finding has its ID**, so `Composed-of` renders with final IDs.
- Each basis block gets its `**Part-of:**` line per §4.2.
- A composite is rendered after the non-composite findings of the same severity.
- The Verification Summary's "Cross-analysis findings" metric counts the composites rendered as blocks.

## 6. The composition pass

### 6.1 Placement

A new **Step 1.6** in both `/fix-all` and `/fix-report`, after the fixed-status filter (Step 1.3), the provenance flag (Step 1.4) and the edge cases (Step 1.5), before the severity floor. It runs over every unfixed finding, `auto` and `needs-decision` alike, **per source file, and only over review reports** (`docs/reviews/`, feedback reports included). A QA report under `docs/testing/reports/` is never grouped: the `COMP` prefix routes to `docs/reviews/`, so a composite written anywhere else would be unreachable by ID. Where `/fix-all`'s Step 2.2.5 takes the zero-auto path — the fix list empty, `needs_decision` non-empty — the rest of Step 2 and the whole of Steps 3–4 are skipped, so this pass still runs here but its rendering, its gate and its persistence move to Step 5 (§6.7, §6.8).

### 6.2 Marker resolution

For each source file:

1. For each open composite block, its components are the IDs in `Composed-of` that exist in the same file and are unfixed. Bound components leave the individual list.
2. A composite with fewer than two such components is **degenerate**: it is not dispatched. With one remaining component, that component is dispatched alone. It is unbound for this run: it re-enters the individual list, passes the severity floor and the Fix-policy partition, appears as an ordinary row in the pre-flight table, counts in `total_count`, and is an ordinary `/fix-report` checklist item. It is still **not** a candidate: no ID named in an open composite's `Composed-of` is ever grouped again while that composite is open (§4.2), so the composition pass leaves it alone and it is dispatched as an individual finding. The degenerate composite itself is neither queued nor listed under Composites. At write-back the composite receives the same status that component receives. With none, the composite is closed at write-back: `✅ Fixed` when at least one component carries `✅ Fixed` or `⚠️ Partially Fixed`, otherwise `🚫 Rejected (YYYY-MM-DD) — no open components`.
3. What is named in no open composite's `Composed-of`, is non-composite, and is free of `**Decision:**` and `**Dispatch:**` lines is the file's candidate set.

### 6.3 The `composition-analyst` agent

A new read-only agent, `plugins/code-review/agents/composition-analyst.md`.

```yaml
name: composition-analyst
description: Proposes composite groupings over the unfixed findings of one report file — findings that share one cause and one fix. Writes nothing. Invoked by /fix-all and /fix-report before dispatch.
tools: Read, Grep, Glob
model: opus
```

**Dispatch.** One call per source file whose candidate set has at least two members; files are dispatched in parallel. Fewer than two candidates → no call for that file. The prompt carries the candidate blocks (each with its ID), and the list of IDs named in any open composite's `Composed-of` in that file, for the disjointness test. A feedback-origin block (one with a `**Source:**` field) is wrapped as untrusted data exactly as `code-review:decision-gate` stage 1 wraps it for the decision analyst; that section is the authority for the form and is not restated.

**Return contract.** Fixed-label markdown, one `### Group N` per proposal:

```markdown
## Composition Proposals

### Group 1
Members: SEC-002, SEC-003, ARCH-001
Title: Missing input validation layer
Severity: HIGH
Location: src/api/validation.py:1
Effort: medium
Problem: <the shared cause, one paragraph>
Impact: <what the combination costs, one line>
Remediation: <the single change; may carry a code block>
Evidence:
- SEC-002 — <citation> — <why this symptom is that cause>
- SEC-003 — <citation> — <…>
- ARCH-001 — <citation> — <…>

## Rejected groupings
- SEC-004 + SEC-005 — <one-line reason>

Composition: 1 groups proposed over 7 findings
```

- `Severity` is exactly the maximum of the members' severities.
- `Location` is the primary site of the shared fix, verified against the tree.
- Every `Evidence` line carries a `tool: …` citation naming every output-determining parameter of the `Read`, `Grep` or `Glob` call, plus that call's verbatim result. This is the tool form of the two citation forms the `decision-analyst` contract defines; the command form does not apply, since this agent has no shell. A bare assertion is not evidence.
- `## Rejected groupings` is present on every run, `None` when empty.
- The closing line is fixed vocabulary: `Composition: <N> groups proposed over <M> findings`, with `N` possibly `0`. A response without it is malformed.

**The battery.** Per the `finding-falsification` skill, every proposal survives a refutation pass before it is returned. The checks are adapted to grouping:

1. **Subsumption.** The single Remediation, applied, leaves every member's Problem unreproducible **without** applying that member's own Remediation. A group whose Remediation is the members' Remediations concatenated is rejected.
2. **Same file is not same cause.** Proximity in the tree is not evidence. Each member's Evidence line must show the mechanism, not the neighbourhood.
3. **Disjointness.** A finding appears in at most one proposal and in none of the IDs handed in as named in an open composite's `Composed-of`.
4. **Minimum two members**, all from the candidate set handed in.
5. **Evidence per member**, in a citable form, as above.

Rejected groupings are listed with the failing check's reason and are never dropped silently.

### 6.4 Orchestrator validation

The fix command trusts nothing it did not verify. For every proposal:

- every member is in the candidate set of that file;
- at least two and at most twelve members (§4.1);
- no member appears in another accepted proposal;
- `Severity` is recomputed as the members' maximum (the agent's value is overwritten if it differs);
- `Location` is usable under *The usability rule* in `code-review:decision-gate` in full — it parses by the two-clause read rule, **is contained in the repository tree by that section's three-step containment test**, and exists there; a proposal whose `Location` fails any conjunct is dropped and listed with `location-unusable`, never repaired;
- the inherited `Fix-policy` is computed per §4.1.

A proposal failing any check is dropped and listed in the run's Composition block with the failing check. A response missing the closing line, or unparseable, makes the whole pass **unavailable** for that file.

**ID assignment.** Each accepted proposal is assigned the next free `COMP-NNN` in its file, counting from the highest `COMP-` number the file already carries (or `001` where it carries none), in proposal order. The ID is assigned here, before the pre-flight, so the pre-flight and the dissolve question can name the composite; it is written into the report only at persistence (§6.8). A proposal dissolved or not selected releases its number, and the next run may assign it again.

### 6.5 Fail-safe

Agent error, timeout, or an unavailable pass yields zero proposals for that file. The timeout is the platform's own agent-call timeout: the pass carries no wall-clock budget of its own (§16), and in practice at most one review file is eligible per run, so at most one analyst call is in flight. The pre-flight carries `Composition pass: unavailable — <reason>` and the run proceeds per finding, exactly as today. Grouping never blocks fixing.

### 6.6 Pre-flight rendering in `/fix-all` (Step 2.4)

- A composite is a row of the issue table like any finding: `COMP-001`, its severity, title, location. Bound components of a dispatchable composite do **not** appear in the table. `total_count` counts a composite as one issue and excludes its bound components.
- A new block under the table:

```markdown
**Composites:**
- COMP-001 (review) — Missing input validation layer — components: SEC-002, SEC-003, ARCH-001
- COMP-002 (fix-time, proposed) — Unbounded queue growth — components: PERF-001, PERF-003

**Composition pass:** 1 proposed this run, 1 already in the report
```

`proposed this run` counts the pass's accepted proposals — none of which is persisted at this point, since §6.8 writes only after the gate — and `already in the report` counts the open composite blocks the source files carry, whatever their `Origin`. The line reads `unavailable — <reason>` where §6.5 applied, and `0 proposed this run, 0 already in the report` prints as `none`. Where §6.7's fail-closed path applied, a second line follows it: `Dissolve question: unavailable — <reason>; all composites dissolved for this run`.

### 6.7 The dissolve question (Step 2.4.5 in `/fix-all`, Step 2.1.5 in `/fix-report`)

Asked **only when the run holds at least one dispatchable composite**, proposed or persisted. One `AskUserQuestion`, `multiSelect: true`:

- question, on the last or only page: `Dissolve which composites into their components? (select none to keep all)`; on a page another page follows: `Dissolve which composites into their components? (page X of Y — select none on this page to keep these)`. Four options per call, all of them composites — nothing is appended, unlike `/fix-report`'s checklist pages — so a run with Y composites costs ⌈Y/4⌉ answers; every page is answered in sequence, selections accumulate across pages, and every dispatchable composite appears on some page;
- option label: `[HIGH] COMP-001: Missing input validation layer` — severity, ID and title, under the existing 60-character title rule;
- option description, for a persisted composite: `review · 3 components: SEC-002 <title>, SEC-003 <title>, ARCH-001 <title> — <first sentence of Problem> — marks COMP-001 🚫 Rejected in the report and releases them`; for a proposed one: `fix-time, proposed · 2 components: PERF-001 <title>, PERF-003 <title> — <first sentence of Problem> — drops the proposal, nothing is written`.

Effects of dissolving:

- a **proposed** composite is dropped: nothing is written, its components return to the individual list;
- a **persisted** composite is marked for a `**Status:** 🚫 Rejected (YYYY-MM-DD) — dissolved into components` line on its block, written at persistence time (§6.8). By §4.3 the status releases its components.

Released components pass through the severity floor and the Fix-policy partition again. In `/fix-all`, which asks after the pre-flight, one line per dissolved composite is printed before the confirmation gate, naming the released components and where each went — `Dissolved COMP-002: 2 components released — 1 joins the fix list, 1 requires a decision, 0 below the severity floor; total to fix 13` — followed by a re-render of the affected part of the pre-flight: the released components as issue-table rows (`#`, ID, severity, title, location, and the Source and Report columns where shown) with recomputed `By severity` and `Requires user decision (skipped)` lines, so the full list the gate asks about is on screen. The last line's total is the `total_count` the gate's question and its `Yes — fix all <total_count>` label use. In `/fix-report`, which asks before the checklist, the checklist is simply built from the resulting list.

This is the one human gate on a grouping. A composite that passes it is fixed as a unit.

The gate is **fail-closed**. Where the question cannot be asked — `AskUserQuestion` unavailable, or it errors — no composite is dispatched as a unit this run: every proposed composite is dropped and nothing is persisted, and every persisted composite is treated as dissolved for the run with its components dispatched individually, no dissolution status written. The pre-flight and the Composition block carry `Dissolve question: unavailable — <reason>; all composites dissolved for this run`.

**On `/fix-all`'s zero-auto path** — Step 2.2.5 routes a run whose fix list is empty and whose `needs_decision` list is not straight to Step 5, skipping Step 2.4, this step and Step 3.0 — the Composites block (§6.6) is printed and this question is asked at the head of Step 5.2, beside the "Requires user decision" list that step already prints on that path, before the resolve offer. The run's commitment point is the user's `yes` at Step 5.2.

### 6.8 Persistence

Markers are written **only once the run has committed to dispatching**: in `/fix-all` at a new Step 3.0, after the confirmation gate and before the first fixer call; in `/fix-report` at a new Step 2.3.5, after selection ends and before the decision gate, so the gate's pins are computed over blocks that already carry the markers. An aborted run writes nothing, keeping `Aborted. No changes made.` true. On `/fix-all`'s zero-auto path there is no Step 3.0: the writes run immediately after the user's `yes` at Step 5.2 and before `code-review:decision-gate` is loaded at Step 5.4, so the gate's pins are again computed over blocks that already carry the markers; a `no` at Step 5.2 writes nothing. `/fix-report` persists only the proposed composites the user **selected**; an unselected proposal is forgotten and may be proposed again next run.

Writes, each with the `Edit` tool and each verified by re-reading the file, as Step 4.1.5 verifies status lines:

1. **Composite block** (`Origin: fix-time`), inserted immediately before the heading of the component that appears first **in the file** among its `Composed-of` members — not first in `Composed-of` order — so the block always precedes every member: `old_string` = that heading line, `new_string` = the composite block, a blank line, then the heading.
2. **`Part-of` line** on each component, after its `**ID:**` line, or after the heading where there is none.
3. **Dissolution status** on each persisted composite the user dissolved.

Failures:

- composite block write fails or does not verify → the group is dissolved for this run, its components are dispatched individually, and the Composition block lists it with `marker-write-failed`;
- a `Part-of` write fails → recorded in the same block; membership is unaffected (§4.2);
- a dissolution write fails → recorded; the composite is treated as dissolved for this run and will be offered again next run.

### 6.9 `/fix-report` specifics

- Step 1.6 runs at the same point as in `/fix-all`.
- The dissolve question runs at Step 2.1.5, before the checklist, because a user who does not want the composite has no other way to reach its components.
- A composite is **one checklist item**: label `[HIGH] COMP-001: Missing input validation layer`, description `src/api/validation.py:1 — 3 components (review): SEC-002, SEC-003, ARCH-001 — <first sentence of Problem>` (with ` · <basename>` appended in auto-merge mode, as today, the only dot-separated tail). Bound components are not separate items.
- A needs-decision composite sits on the needs-decision pages like any other needs-decision finding.

## 7. Dispatch and the fixer

### 7.1 Payload

A composite is one `fix-auto` call. The prompt carries the composite block first, then each component block in `Composed-of` order, each as its own `###` section. Every block passes through the dispatch-copy rule of `code-review:decision-gate` stage 3: loop-written lines are stripped, `Location` and any pre-existing `Status` travel. A `User decision:` line, where present, applies to the composite and is placed immediately after the composite block, before the first component's `###` heading — never after the last component, where the fixer's Remediation capture would take it as that component's own field. The payload carries every ID in `Composed-of` that still has a block in the file, already-fixed and rejected components included, each with the pre-existing `**Status:**` line that the same strip table lets travel. Degeneracy is counted over the unfixed components alone: fewer than two of those makes the composite degenerate (§6.2), and it is not dispatched.

A composite queues where any finding queues: severity order, then source order. No special placement.

### 7.2 `fix-auto` composite mode

**Phase 1.** When the first block's `Category` is `Composite` **and** it carries a `**Composed-of:**` line, the fixer is in composite mode; a `Composite` block without one is a **Failed** verdict naming the missing field. It parses `**Composed-of:**` and each following `###` block as a component with the same field table. In composite mode each block's field capture ends at the next `###` heading, and exactly one `User decision:` field is parsed — the one following the composite block (§7.1). An ID in `Composed-of` with no block in the prompt at all is a **Failed** verdict with an explicit error naming the ID. The fixer never guesses a component from the report on disk. A component block carrying a `**Status:**` line is skipped and listed — `skipped (fixed)` for `✅ Fixed` or `⚠️ Partially Fixed`, `skipped (rejected)` for `🚫 Rejected`; a composite block carrying `🚫 Rejected` aborts exactly as today. A component without a usable `Location` is kept, but its symptom check in Phase 4 records `unresolved (no location)`.

**Phase 2.** Reads the composite's location and every component's location, with context, before anything else.

**Phase 3.** Implements **the composite's Remediation and nothing else**. The rule, stated in the agent verbatim: *In composite mode you implement the composite's Remediation. A component's Remediation is context for understanding its symptom; it is never applied, in this phase or in Phase 5's iterations. A component the root-cause change does not cover is reported unresolved in Phase 6, not patched locally.* This is the point of the feature and it is not softened by iteration pressure.

**Phase 4.** Tool selection is the union of the rows matched by every component (a CWE on any component selects SAST, a Documentation component selects the doc re-read, and so on), plus the rows matched by the composite's own change. A new Step 4.4 runs after the tools: for each component **not skipped in Phase 1**, re-read its location with context and decide whether its Problem still holds; record `resolved` or `unresolved` with one line of evidence. A skipped component is not checked and keeps the Result Phase 1 gave it.

**Phase 5.** Iteration is unchanged, under the Phase 3 rule.

**Phase 6.** The report gains a table:

```markdown
**Components:**
| ID | Result | Evidence |
|----|--------|----------|
| SEC-002 | resolved | validation now runs in `middleware.py:14` before the handler |
| ARCH-001 | unresolved | handler still constructs the query inline at `handler.py:88` |
```

`Result` ∈ `resolved`, `unresolved`, `unresolved (no location)`, `skipped (fixed)`, `skipped (rejected)`. The verdict is computed over the components actually checked — `unresolved (no location)` and the two skipped values are excluded from the test and disclosed instead, on §11's `Verification coverage` line, so unreachable coverage never flips a verdict: **Fixed** when every checked component is `resolved` and verification passed; **Partially Fixed** when at least one checked component is `resolved`; **Failed** otherwise, or when the change could not be applied.

### 7.3 Status mapping in the orchestrator

The orchestrator reads the fixer's `**Components:**` table by matching each row's `ID` against `Composed-of`: a row naming an ID not in `Composed-of` is ignored and noted in the Composition block, and a component with no `resolved` row receives no `**Status:**` line whatever the composite's verdict — the table, never the narration around it, decides. A report with no `**Components:**` table, or one that does not parse, is **Failed** per `/fix-all` Step 3.1's malformed-response rule, and nothing is written on the composite or on any component.

| Fixer verdict | Composite | Component `resolved` | Component `unresolved` |
|---|---|---|---|
| Fixed | `✅ Fixed` | `✅ Fixed` | n/a |
| Partially Fixed | `⚠️ Partially Fixed` | `✅ Fixed` | no status; released by §4.3, returns individually next run |
| Failed | no status | no status | no status; composite returns whole next run and can be dissolved |

A component skipped in Phase 1 keeps the `**Status:**` line it already carried and is never written to. On the auto path the two component columns rest on the fixer's own Components table: the agent that applied the change is also the one that judged each symptom, so those component statuses are advisory (§16). On the decision-gate path §8 supplies the deciding signal in its place.

## 8. Decision gate

A needs-decision composite goes through the gate as **one** finding.

- **Stage 0** checks the composite block's `Location`.
- **Stage 1** hands the analyst the same payload the fixer would receive (§7.1): the composite block plus each component block. Stage 1's per-block rules apply to each block independently — every component block carrying a `**Source:**` line is sanitised and wrapped in this invocation's nonce delimiters exactly as a single feedback-origin finding is, one nonce per analyst call, while the composite block's own lines travel outside them. With no `Drift-class`, the analyst takes the fallback route: A is the composite's Remediation as written, B a direction derived from the code, or A alone.
- **Verification plan.** `code-review:decision-gate`'s plan-rejection test gains one clause: *a plan for a composite carries at least one check per component whose expected result is that component's symptom being absent; a plan without one is rejected.* The `decision-analyst` contract references that clause rather than restating it.
- **Pin.** The pinned file set is computed as today from the `Target` and the resolution text, plus one clause: *each component's `Location` path is pinned `:ref` unless the resolution already names it, in which case it keeps the `:edit` role the resolution gave it.* An edit to a symptom's file between decision and dispatch invalidates the decision like any referent edit.
- **The sweep** renders the composite's members (ID and title) under the `Target`, and stage 2's render shows a `Source` row for every component that carries one, marked feedback-origin, beside the composite's `Target`.
- **`reject`** writes `🚫 Rejected` on the composite block, releasing its components.
- **Stage 4** grades as today, and its graded case — not the fixer's verdict — is §7.3's first column on this path: a case that writes `✅ Fixed` or `⚠️ Partially Fixed` on the composite propagates per the matching row, in the same pass; a case that writes no status on the composite writes none on any component, and the composite returns whole next run. On this path a component's `resolved`/`unresolved` value is decided by that component's own check in the decided `**Verification-plan:**`, graded on its logged raw output exactly as the composite's status is; the fixer's Components table is advisory input, never the deciding signal. A component the plan carries no attributable check for receives no status and is released per §4.3.
- A persisted `**Decision:**` on a composite replays like any other decision.

## 9. `/fix`

- The ID regex gains `COMP`; the prefix routes to `docs/reviews/`. Building a composite payload makes `/fix` a consumer of stage 3's dispatch-copy rule, so its row in `code-review:decision-gate`'s consumer scope table moves from `render-only` to `dispatch-only` (§13.3).
- `/fix COMP-001`: Step 0.4 also extracts every component block named in `Composed-of` that exists in the same report — already-fixed and rejected ones included, each with its `**Status:**` line — and builds the §7.1 payload. Fewer than two **unfixed** components → the composite is degenerate; report it and stop, naming the remaining component as the thing to fix.
- `/fix SEC-002` where an **open** composite in the same report lists `SEC-002`: a new Step 0.4.5 asks one question — `SEC-002 is part of composite COMP-001. Fix which?` — with three options: `Fix COMP-001 (recommended)`, described `<composite title> — one root-cause change resolving SEC-002, SEC-003, ARCH-001`; `Fix SEC-002 alone`, described `Local fix only — the shared cause stays and COMP-001 returns whole on the next bulk run`; `Abort`, described `Stop now without modifying any files` and printing `Aborted. No changes made.`. Alone proceeds as today; its `Fixed` does not touch the composite, and the degeneracy rule applies on the next bulk run.
- Legacy paste mode with a composite block and no component blocks → Phase 1's composite-mode error; the message suggests `/fix COMP-NNN`.
- `/fix` runs the composite itself, never through `fix-auto`: its own phases carry the §7.2 composite mode — Phase 1 parses `Composed-of` and the component blocks with the same required-field, skip and missing-block rules and gains `Composite` in its Category enum; Phase 2 reads the composite's and every component's location; Phase 3's proposal names the single change and the components it must resolve; Phase 4 implements the composite's Remediation only, under the verbatim root-cause-only rule, in Phase 6's iterations too; Phase 5 selects tools by the union rule and adds the per-component symptom re-read; Phase 7's report carries the Components table and the three-verdict rule.
- Phase 8 propagates statuses per §7.3. Step 8.1.5 (never a second `**Status:**` line) applies to every block written.

## 10. `/qa:loop` is untouched

QA reports carry no composite blocks, the composition pass never runs over them (§6.1), and the dispatch-copy rule for single blocks is unchanged. In auto-merge mode the QA report's findings are dispatched exactly as today. `docs/plugins/code-review.md` says so explicitly, so nobody looks for a missing integration.

## 11. Write-back and summaries

- The Step 4.1 recipe and the Step 4.1.5 verification are unchanged. A composite and each `resolved` component receive a `**Status:**` line with the same date, each verified, each failure recorded in the same `status_write_failures` list with the same reasons. On the auto path each of those `**Status:**` lines is written together with a `**Verification:** advisory — <checks run>` line, in the form `code-review:decision-gate`'s stage 4 writes it, because the status rests on the fixer's re-read rather than on an orchestrator-run check; Step 4.1.5 verifies that line exactly as it does for the decision batch.
- A degenerate composite receives the status its lone component received. A composite with no open components is closed by the same Step 4.1 pass as a housekeeping write, verified by Step 4.1.5 like any other; a run that never reaches write-back leaves it open.
- **Fix Summary**: one row per composite, no rows for bound components:

```markdown
| 3 | [HIGH] COMP-001: Missing input validation layer — src/api/validation.py:1 (SEC-002 ✅, SEC-003 ✅, ARCH-001 —) — advisory (fixer self-report) | ⚠️ Partially Fixed |
```

The parenthesised list renders each component's Phase 6 `Result`, in `Composed-of` order: `✅` resolved · `—` unresolved · `❓` unresolved (no location) · `✔︎` skipped (fixed) · `🚫` skipped (rejected). On the auto path the row carries the suffix `— advisory (fixer self-report)` before the status cell: the marks come from the fixer's own Components table, not from an orchestrator-run check. On the decision-gate path the suffix is omitted and the marks carry §8's grading.

- A new block after `**Reports updated:**`:

```markdown
**Composition:**
- Proposed: 2 | Written to the report: 1 | Dropped proposals: 1 | Marked 🚫 Rejected (dissolved): COMP-004
- Dropped by validation: SEC-004 + SEC-005 — member not a candidate
- Rejected by the analyst: SEC-006 + SEC-007 — same file, different mechanism
- Verification coverage: 2 of 3 components checked (ARCH-001: no location)
- Marker write failures: COMP-003 — marker-write-failed
- Pass unavailable: <reason>            <-- only where §6.5 applied
- Dissolve question: unavailable — <reason>; all composites dissolved for this run   <-- only where §6.7's fail-closed path applied
```

`Written to the report` counts only the proposals this run persisted (§6.8); `Dropped proposals` the proposals dissolved before persistence, which write nothing; `Marked 🚫 Rejected (dissolved)` lists the persisted composites whose block received the dissolution status. `Rejected by the analyst` renders the analyst's `## Rejected groupings` section (§6.3), one line per grouping, so those rejections reach the user rather than the agent's discipline alone. `Verification coverage` names each component the fixer could not check (§7.2). Omit any line whose value is empty; omit the block when the run held no composite and the pass was not unavailable.

- **Restart safety.** Markers are on disk before the first dispatch — on `/fix-all`'s zero-auto path, written after the `yes` at Step 5.2 and before `code-review:decision-gate` is loaded (§6.8) — so an interrupted run leaves its successor the same composites. An open composite is retried whole. A component fixed through a composite is filtered by Step 1.3 like any fixed finding.

## 12. Error handling, closed list

| Situation | Handling |
|---|---|
| Proposal with a member outside the candidate set, from another file, in another proposal, or fewer than two members | Dropped by §6.4, listed in the Composition block. |
| `Composed-of` names an ID absent from the file | That component is not in the payload; the degeneracy rule applies over the unfixed components. |
| `Composed-of` names a component carrying a `**Status:**` line | Its block travels in the payload with that status; Phase 1 skips it as `skipped (fixed)` or `skipped (rejected)` and it is never written to. |
| `COMP-` ID inside a `Composed-of` | Treated as an absent ID. Composites never nest. |
| `Part-of` naming a composite that does not exist or is not open | Ignored; the finding is a candidate. |
| Hand-edited composite with severity below a component's | Effective severity raised to the maximum for the run; report not rewritten. |
| Fixer receives a composite payload with no block for an ID in `Composed-of` | Failed; nothing written. |
| Agent call errors, times out, or returns a malformed response | Pass unavailable for that file (§6.5). |
| Composite block persistence fails | Group dissolved for the run; components dispatched individually. |
| Proposal whose `Location` fails §6.4's usability rule | Dropped, listed with `location-unusable`; never repaired. |
| `Part-of` write fails or does not verify | Recorded in the Composition block; membership unaffected (§4.2). |
| Dissolution status write fails | Recorded; the composite is treated as dissolved for this run and offered again next run. |
| Fixer returns a composite report with no `**Components:**` table, or one that does not parse | Failed per Step 3.1's malformed-response rule; nothing written on the composite or any component (§7.3). |
| Block with `**Category:** Composite` and no `**Composed-of:**` line, or fewer than two IDs on it | Not a composite (§3) and not a candidate: excluded from the pass and from dispatch, listed in the Composition block as `malformed-composite`; dispatched by hand, the fixer returns Failed naming the missing field (§7.2). |
| Composite dispatched, run interrupted before write-back | Composite stays open; retried whole next run; dissolvable. |
| Component fixed alone via `/fix` while its composite is open | Composite unaffected; degeneracy rule on the next bulk run. |
| Two cross-verifier composites cite the same basis | The later composite loses that basis (§5.2); fewer than two leaves it a bullet. |
| `/fix-all` takes the zero-auto path (Step 2.2.5) | The Composites block and the dissolve question move to the head of Step 5.2; persistence (§6.8) runs after the user's `yes`, before the gate is loaded; a `no` writes nothing. |
| The dissolve question cannot be asked (`AskUserQuestion` unavailable or errors) | Fail-closed (§6.7): proposed composites dropped, persisted ones dissolved for the run with no status written; the pre-flight and the Composition block carry `Dissolve question: unavailable — <reason>; all composites dissolved for this run`. |

## 13. Testing

Commands and agents are prose, so verification is contract checks in CI plus an acceptance protocol, as elsewhere in this repository.

1. **Contract test** `plugins/code-review/tests/test_composite_contract.py`, stdlib `unittest`, run as `python3 plugins/code-review/tests/test_composite_contract.py`, in the shape of `scripts/test_check_*.py`. Each assertion greps one invariant across files, and each is mutation-checked when written — remove the sentence, the test must fail — with the check left as an artifact: every assertion carries a `# mutation:` comment quoting the exact sentence whose deletion fails it, and the pull request description records the mutation run; an assertion without that comment is not a contract test. Invariants:
   - `Composite` in `fix-auto`'s Category enum and in `/fix`'s Phase 1 Category enum; `COMP` in `/fix`'s ID regex and in `extract-issue-ids.sh`'s `PREFIX_RE`; the `Composite | COMP` row in the docs table;
   - the verbatim "never applied, in this phase or in Phase 5's iterations" rule in `fix-auto`, and the same root-cause-only rule in `commands/fix.md` under its own phase numbering;
   - Step 1.6 and the dissolve question in both `/fix-all` and `/fix-report`;
   - the `:ref` clause for component locations and the per-component plan clause in `decision-gate`;
   - `Location:`, `Effort:` and `Cause:` in the cross-verifier's composite format;
   - the `composition-analyst` closing line and `## Rejected groupings` section;
   - the "Composite findings" section and the `/qa:loop` untouched sentence in the docs.
2. **The contract checks in CI.** A new workflow `.github/workflows/code-review-contract.yml` runs both `python3 plugins/code-review/tests/test_composite_contract.py` and `bash plugins/code-review/scripts/check-prefix-sync.sh` on pull requests against `master`. The prefix guard exists to catch exactly this change and today runs only by hand; the contract test has no runner at all without this workflow.
3. **Frontmatter and boundary.** The new agent's `tools: Read, Grep, Glob` passes `check_agent_frontmatter.py`. The fix commands gain no `Bash(...)` grants, so the grant table `check_execution_boundary.py` diffs is unchanged. That checker scans commands and skills only (`*/commands/*.md`, `*/skills/*/SKILL.md`), so the new agent needs no scope-table row and must not be given one — a row naming a path outside those globs fails the check. `commands/fix.md`'s row in `decision-gate`'s consumer scope table moves from `render-only` to `dispatch-only`, with `/qa:loop`'s rationale: it follows stage 3's dispatch-copy rule when it builds a composite payload and runs no stage; its `Bash(git:*)` wildcard stays outside the grant diff only while its kind is not `runs-the-stage`.
4. **Acceptance protocol**, §15, run before release.
5. **Reviews.** The spec through `/superutils:spec-review`; the implementation through `/review` on the branch, with its findings fixed before merge.

## 14. Versioning and documentation

- **code-review 2.0.1 → 2.1.0.** MINOR: a new agent, a new category, new fields and steps, all additive. Pre-existing reports **parse** exactly as before — every new field is additive, no existing field's grammar changes, and the `### [SEVERITY]` block extraction, `fix-auto`'s Phase 1 field table, `extract-issue-ids.sh` and the `**Status:**` grammar all read an old report unchanged. Their **dispatch** does change: the fix-time composition pass may group an old review or feedback report's unfixed findings, persist `Composed-of`/`Part-of`/`Origin` markers into the file (§6.8) and dispatch a group as one `fix-auto` call; the dissolve question (§6.7) is the per-run veto, no write happens before the run's commitment point (§6.8) — the confirmation gate, or the user's `yes` at Step 5.2 on `/fix-all`'s zero-auto path — and the pass is fail-safe (§6.5). MINOR still holds: no command is removed, no format becomes incompatible, and the new behaviour is vetoable at the gate. All four version sites: `plugins/code-review/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, the README table row, and the `**Version:**` header of `docs/plugins/code-review.md`.
- **`docs/plugins/code-review.md`**: a new "Composite findings" section (format, rules, the pass, the dissolve question, statuses, `/fix` behaviour, `/qa:loop` untouched); the `Composite | COMP | docs/reviews/` row; updates to the `/fix-all`, `/fix-report` and `/fix` sections and to the Decision Stage section; an Upgrade Notes entry, which states the dispatch change above.
- **README**: the code-review row mentions composite findings.
- The qa plugin's version and docs are unchanged.
- The spec lives on `feat/composite-findings` and is dropped before merge, per this repository's practice for `docs/superpowers/` artifacts.

## 15. Acceptance protocol

**Fixture.** The protocol needs a branch whose review produces: at least two composable groups — one the cross-verifier groups and one it does not, so the fix-time pass still has something to propose; one cross-verifier composite with a basis the challenger removes; at least one component carrying a non-`auto` `**Fix-policy:**` inside a group, so a needs-decision composite exists; and at least one component the root-cause change will not cover, so a Partially Fixed composite with an unresolved component exists. Where the branch cannot produce one of these, a hand-edited fixture report standing in for it is the intended substitute.

**Runs.** The items belong to five runs over that fixture, in order: run 1 `/review`; run 2 `/fix-all`, dissolving one composite and fixing another; run 3 `/fix-all` re-run; run 4 `/fix-report`; run 5 `/fix`.

- [ ] **Run 1** — `/review` renders at least one `COMP-NNN` block with `Origin: review`, `Composed-of` with final IDs, and `Part-of` on each basis; a composite whose bases the challenger removed is a bullet, not a block.
- [ ] **Run 2** — the `/fix-all` pre-flight shows the composite as one row and its components under the Composites block; `total_count` excludes bound components.
- [ ] **Run 2** — the dissolve question is asked once per run, in pages of four where more than four composites exist, lists proposed and persisted composites, and dissolving one prints the delta line and updates the gate's count.
- [ ] **Run 2** — one `fix-auto` call per composite; its report carries the Components table; statuses land on the composite and on each `resolved` component; unresolved components carry none.
- [ ] **Run 2** — a fix-time composite is persisted before the first dispatch: interrupt the run while the first `fix-auto` call is in flight — the report already carries the composite block immediately before its earliest-in-file component, with `Part-of` on each component, and a re-run offers the same composite whole.
- [ ] **Run 2** — a needs-decision composite goes through the decision gate once, with a per-component check in its plan.
- [ ] **Run 3** — re-running `/fix-all` re-fixes nothing; a Partially Fixed composite's unresolved components are offered individually.
- [ ] **Run 4** — `/fix-report` shows a composite as one checklist item and asks the dissolve question before the checklist.
- [ ] **Run 5** — `/fix SEC-NNN` on a bound component asks the three-option question; `/fix COMP-NNN` fixes the composite.
- [ ] `check-prefix-sync.sh`, `check_agent_frontmatter.py`, `check_execution_boundary.py` and `python3 plugins/code-review/tests/test_composite_contract.py` pass, and `.github/workflows/code-review-contract.yml` runs the contract test and `check-prefix-sync.sh` on a pull request against `master`.

**Disposition.** An item whose fixture the branch does not produce is recorded `N/A — <reason>`, never ticked. An `N/A` on the fix-time-persistence, Partially-Fixed or needs-decision items blocks release.

## 16. Residual risks

- **The grouping is a model judgment.** The dissolve question is the human gate. A wrong group that passes it costs one structural change where N local ones were right. Every fix stays uncommitted, so the recovery is the working-tree diff, as it is for every fix today.
- **The "root cause only" rule is prose-enforced.** `fix-auto` holds unrestricted `Edit`, `Write` and `Bash`; nothing mechanical stops it patching a component locally under iteration pressure. The Components table makes such a lapse visible after the fact, not impossible.
- **Cost.** One agent call per report file per run, only while unmarked candidates exist. After a full run nothing is left to group and no call is made.
- **Verification of a composite is a re-read judgment per component** unless tests cover the symptoms. A composite's `Fixed` is only as hard as the tools its components' categories select.
- **Groups do not cross report files**, so a cause shared by a review finding and a QA finding is fixed twice. Accepted; the same-file rule is what keeps write-back and IDs simple.
- **On the auto path the fixer is its own per-component verifier.** Step 4.4's symptom check is run by the agent that made the change, and §7.3 turns its Components table into a terminal `✅ Fixed` on each `resolved` component. Those component statuses are advisory (fixer self-report) and are labelled so in the Fix Summary (§11). Only the decision-gate path removes the actor from the judgment: there each component is graded by the orchestrator on that component's own check in the decided verification plan (§8).
- **The dissolve question is not TTY-probed.** There is no interactivity probe; an `AskUserQuestion` that is unavailable or errors is handled by dissolving every composite for the run (§6.7), never by keeping them. The cost is a run that patches symptom by symptom where a grouping was right; the alternative — reading silence as consent — would fix a group as a unit with no human veto.
- **The composition pass is unbounded in time.** Its only time limit is the platform's agent-call timeout (§6.5); the spec sets no wall-clock budget for the pass or for a composite dispatch, whose work scales with the member count, capped at twelve by §4.1. Accepted for the same reason today's per-finding dispatch carries none.
- **Component blocks travel unpinned.** The `**Decision-pin:**` block hash covers the composite's own block (§4.3); an edit to a component block's text between decision and dispatch changes what the fixer receives without invalidating the pin. Membership is pinned through `Composed-of`, and each component's *file* is pinned `:ref` (§8), so the exposure is a changed description, not a changed target.

## 17. File inventory

| File | Change |
|---|---|
| `plugins/code-review/agents/composition-analyst.md` | New. |
| `plugins/code-review/agents/fix-auto.md` | Composite mode: Phase 1 parsing, Phase 3 rule, Phase 4.4 symptom check, Phase 6 Components table; `Composite` in the Category enum. |
| `plugins/code-review/agents/cross-verifier.md` | Tightened composite criterion; `Location:`, `Effort:` and `Cause:` in the format. |
| `plugins/code-review/agents/decision-analyst.md` | Composite payload noted; plan clause referenced by pointer. |
| `plugins/code-review/commands/review.md` | Step 5.5 item body; Step 5.6 COMP IDs, `Part-of`, placement; summary metric. |
| `plugins/code-review/commands/fix-all.md` | Step 1.6, pre-flight Composites block, Step 2.4.5, Step 3.0, the zero-auto hook at the head of Step 5.2 (Composites block, dissolve question, persistence after the `yes`), status mapping, Fix Summary row and Composition block. |
| `plugins/code-review/commands/fix-report.md` | Step 1.6, Step 2.1.5, checklist item, Step 2.3.5, status mapping, summary. |
| `plugins/code-review/commands/fix.md` | `COMP` in the regex and routing; Step 0.4 composite extraction; Step 0.4.5; composite mode in its own phases — Phase 1 parsing and `Composite` in the Category enum, Phase 2 locations, Phase 3 proposal, Phase 4 root-cause-only rule, Phase 5 tool union and symptom re-read, Phase 6 iterations under the same rule, Phase 7 Components table; Phase 8 propagation. |
| `plugins/code-review/skills/decision-gate/SKILL.md` | Composite through the gate; the `:ref` clause; the per-component plan clause; `fix.md`'s consumer scope row `render-only` → `dispatch-only` and the scope sentence amended. |
| `plugins/code-review/scripts/extract-issue-ids.sh` | `COMP` in `PREFIX_RE`. |
| `plugins/code-review/tests/test_composite_contract.py` | New. |
| `.github/workflows/code-review-contract.yml` | New: runs the contract test and `check-prefix-sync.sh` on pull requests against `master`. |
| `docs/plugins/code-review.md` | Composite findings section, prefix row, command sections, Decision Stage, Upgrade Notes, version header. |
| `README.md` | code-review row: version and description. |
| `.claude-plugin/marketplace.json`, `plugins/code-review/.claude-plugin/plugin.json` | Version 2.1.0. |
