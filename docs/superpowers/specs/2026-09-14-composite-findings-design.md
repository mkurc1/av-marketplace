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
- The fixers fix a composite as one unit and never its components separately while the composite is open.
- Compositions are recognised both at review time and at fix time, and both are persisted into the report so a later run and `/fix <ID>` see the same grouping.
- The user keeps a one-question veto over every grouping the run is about to act on.
- Old reports, QA reports and feedback reports keep working unchanged.

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
| **bound component** | A component of an open composite. Bound components are never dispatched on their own. |
| **released component** | A component whose composite carries any `**Status:**` line. It is treated as an ordinary finding again. |
| **degenerate composite** | An open composite with fewer than two unfixed components present in its file. |
| **candidate** | An unfixed finding in a review report that is not bound, is not itself a composite, and carries no `**Decision:**` or `**Dispatch:**` line. Candidates are what the composition pass may group. |
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

- `**Location:**` is the primary site of the shared fix, in `path:line` or `path:line-range` form. It is required: stage 0 of the decision gate and `fix-auto`'s Phase 1 both refuse a block without a usable location.
- `**Composed-of:**` lists component IDs separated by `, `. At least two. Every ID belongs to the same report file as the composite. **`Composed-of` is the source of truth for membership.**
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
- **The new fields are authored fields, not loop-written ones.** `Composed-of`, `Part-of` and `Origin` are hashed into `**Decision-pin:**` and travel in the dispatch copy. The decision gate's closed exclusion list is unchanged. This holds because the composition pass writes its markers before any pin is computed in the same run, and because a finding carrying `**Decision:**` or `**Dispatch:**` is never a candidate.

## 5. Review side

### 5.1 Cross-verifier

The `### 6. Composite Findings` task and the `### Composite Findings` output section are tightened:

- A composite is proposed **only where one change resolves every basis**. Where the bases need separate fixes, the observation is a correlation, not a composite.
- The output format gains `Location:` (primary site of the shared fix, `path:line`) and `Effort:`. `Remediation:` must describe the single change.
- Bases are cited by the exact finding title as the auditor wrote it; a documentation basis may cite its `DOC-NNN` ID instead, since the documentation auditor emits IDs.

The finding-falsification exemption for the cross-verifier stands: composites derive from findings that already passed the auditors' batteries and the challenger.

### 5.2 `/review` Step 5.5, item "Add Cross-Verifier composite findings"

The item gets a body. For each composite the cross-verifier returned:

1. Resolve each basis by exact title (or `DOC-NNN` ID) against the findings that survived the challenger. A basis the challenger removed, or that matches nothing, is dropped.
2. Fewer than two bases remain → the composite is **not** rendered as a finding block. Its text stays a plain bullet under `### Cross-Analysis` in the Verification Summary, never as a `###` heading.
3. Otherwise build a finding block: severity = the greater of the cross-verifier's severity and the maximum basis severity; `Category: Composite`; `Location`, `Effort`, `Problem` (the combined risk, stated as the shared cause), `Impact`, `Remediation` from the composite; `Origin: review`; `Fix-policy: needs-decision` per §4.1 when any basis carries a non-`auto` policy.

### 5.3 `/review` Step 5.6, ID assignment

- A `comp_count` counter joins the others. COMP IDs are assigned **after every other finding has its ID**, so `Composed-of` renders with final IDs.
- Each basis block gets its `**Part-of:**` line per §4.2.
- A composite is rendered after the non-composite findings of the same severity.
- The Verification Summary's "Cross-analysis findings" metric counts the composites rendered as blocks.

## 6. The composition pass

### 6.1 Placement

A new **Step 1.6** in both `/fix-all` and `/fix-report`, after the fixed-status filter (Step 1.3), the provenance flag (Step 1.4) and the edge cases (Step 1.5), before the severity floor. It runs over every unfixed finding, `auto` and `needs-decision` alike, **per source file, and only over review reports** (`docs/reviews/`, feedback reports included). A QA report under `docs/testing/reports/` is never grouped: the `COMP` prefix routes to `docs/reviews/`, so a composite written anywhere else would be unreachable by ID.

### 6.2 Marker resolution

For each source file:

1. For each open composite block, its components are the IDs in `Composed-of` that exist in the same file and are unfixed. Bound components leave the individual list.
2. A composite with fewer than two such components is **degenerate**: it is not dispatched. With one remaining component, that component is dispatched alone and at write-back the composite receives the same status it receives. With none, the composite is closed at write-back: `✅ Fixed` when at least one component carries `✅ Fixed` or `⚠️ Partially Fixed`, otherwise `🚫 Rejected (YYYY-MM-DD) — no open components`.
3. What remains unbound, non-composite, and free of `**Decision:**` and `**Dispatch:**` lines is the file's candidate set.

### 6.3 The `composition-analyst` agent

A new read-only agent, `plugins/code-review/agents/composition-analyst.md`.

```yaml
name: composition-analyst
description: Proposes composite groupings over the unfixed findings of one report file — findings that share one cause and one fix. Writes nothing. Invoked by /fix-all and /fix-report before dispatch.
tools: Read, Grep, Glob
model: opus
```

**Dispatch.** One call per source file whose candidate set has at least two members; files are dispatched in parallel. Fewer than two candidates → no call for that file. The prompt carries the candidate blocks (each with its ID), and the list of IDs already bound in that file, for the disjointness test. A feedback-origin block (one with a `**Source:**` field) is wrapped as untrusted data exactly as `code-review:decision-gate` stage 1 wraps it for the decision analyst; that section is the authority for the form and is not restated.

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
3. **Disjointness.** A finding appears in at most one proposal and in no already-bound list.
4. **Minimum two members**, all from the candidate set handed in.
5. **Evidence per member**, in a citable form, as above.

Rejected groupings are listed with the failing check's reason and are never dropped silently.

### 6.4 Orchestrator validation

The fix command trusts nothing it did not verify. For every proposal:

- every member is in the candidate set of that file;
- at least two members;
- no member appears in another accepted proposal;
- `Severity` is recomputed as the members' maximum (the agent's value is overwritten if it differs);
- `Location` parses as `path:line` or `path:line-range` under the two-clause read rule in `code-review:decision-gate` (*The usability rule*), and the path exists in the working tree;
- the inherited `Fix-policy` is computed per §4.1.

A proposal failing any check is dropped and listed in the run's Composition block with the failing check. A response missing the closing line, or unparseable, makes the whole pass **unavailable** for that file.

**ID assignment.** Each accepted proposal is assigned the next free `COMP-NNN` in its file, counting from the highest `COMP-` number the file already carries (or `001` where it carries none), in proposal order. The ID is assigned here, before the pre-flight, so the pre-flight and the dissolve question can name the composite; it is written into the report only at persistence (§6.8). A proposal dissolved or not selected releases its number, and the next run may assign it again.

### 6.5 Fail-safe

Agent error, timeout, or an unavailable pass yields zero proposals for that file. The pre-flight carries `Composition pass: unavailable — <reason>` and the run proceeds per finding, exactly as today. Grouping never blocks fixing.

### 6.6 Pre-flight rendering in `/fix-all` (Step 2.4)

- A composite is a row of the issue table like any finding: `COMP-001`, its severity, title, location. Bound components do **not** appear in the table. `total_count` counts a composite as one issue and excludes its bound components.
- A new block under the table:

```markdown
**Composites:**
- COMP-001 (review) — Missing input validation layer — components: SEC-002, SEC-003, ARCH-001
- COMP-002 (fix-time, proposed) — Unbounded queue growth — components: PERF-001, PERF-003

**Composition pass:** 1 proposed, 1 persisted
```

The `Composition pass:` line reads `unavailable — <reason>` where §6.5 applied, and `0 proposed, 0 persisted` prints as `none`.

### 6.7 The dissolve question (Step 2.4.5 in `/fix-all`, Step 2.1.5 in `/fix-report`)

Asked **only when the run holds at least one dispatchable composite**, proposed or persisted. One `AskUserQuestion`, `multiSelect: true`:

- question: `Dissolve which composites into their components? (select none to keep all)` — with `(page X of Y)` appended when more than four composites exist, four options per call;
- option label: `COMP-001 (review)` or `COMP-002 (fix-time, proposed)`;
- option description: `<n> components: SEC-002, SEC-003, ARCH-001 — <first sentence of Problem>`.

Effects of dissolving:

- a **proposed** composite is dropped: nothing is written, its components return to the individual list;
- a **persisted** composite is marked for a `**Status:** 🚫 Rejected (YYYY-MM-DD) — dissolved into components` line on its block, written at persistence time (§6.8). By §4.3 the status releases its components.

Released components pass through the severity floor and the Fix-policy partition again. In `/fix-all`, which asks after the pre-flight, one delta line is printed before the confirmation gate: `Dissolved COMP-002: +2 issues, 14 total`, and the gate's question uses the new count. In `/fix-report`, which asks before the checklist, the checklist is simply built from the resulting list.

This is the one human gate on a grouping. A composite that passes it is fixed as a unit.

### 6.8 Persistence

Markers are written **only once the run has committed to dispatching**: in `/fix-all` at a new Step 3.0, after the confirmation gate and before the first fixer call; in `/fix-report` at a new Step 2.3.5, after selection ends and before the decision gate, so the gate's pins are computed over blocks that already carry the markers. An aborted run writes nothing, keeping `Aborted. No changes made.` true. `/fix-report` persists only the proposed composites the user **selected**; an unselected proposal is forgotten and may be proposed again next run.

Writes, each with the `Edit` tool and each verified by re-reading the file, as Step 4.1.5 verifies status lines:

1. **Composite block** (`Origin: fix-time`), inserted immediately before its first component's heading: `old_string` = that heading line, `new_string` = the composite block, a blank line, then the heading.
2. **`Part-of` line** on each component, after its `**ID:**` line, or after the heading where there is none.
3. **Dissolution status** on each persisted composite the user dissolved.

Failures:

- composite block write fails or does not verify → the group is dissolved for this run, its components are dispatched individually, and the Composition block lists it with `marker-write-failed`;
- a `Part-of` write fails → recorded in the same block; membership is unaffected (§4.2);
- a dissolution write fails → recorded; the composite is treated as dissolved for this run and will be offered again next run.

### 6.9 `/fix-report` specifics

- Step 1.6 runs at the same point as in `/fix-all`.
- The dissolve question runs at Step 2.1.5, before the checklist, because a user who does not want the composite has no other way to reach its components.
- A composite is **one checklist item**: label `[HIGH] COMP-001: Missing input validation layer`, description `src/api/validation.py:1 — components: SEC-002, SEC-003, ARCH-001 · review` (with the report basename appended in auto-merge mode, as today). Bound components are not separate items.
- A needs-decision composite sits on the needs-decision pages like any other needs-decision finding.

## 7. Dispatch and the fixer

### 7.1 Payload

A composite is one `fix-auto` call. The prompt carries the composite block first, then each component block in `Composed-of` order, each as its own `###` section. Every block passes through the dispatch-copy rule of `code-review:decision-gate` stage 3: loop-written lines are stripped, `Location` and any pre-existing `Status` travel. A trailing `User decision:` line, where present, applies to the composite. Components that are already fixed or rejected are not included; if that leaves fewer than two, the composite is degenerate (§6.2) and is not dispatched.

A composite queues where any finding queues: severity order, then source order. No special placement.

### 7.2 `fix-auto` composite mode

**Phase 1.** When the first block's `Category` is `Composite`, the fixer is in composite mode. It parses `**Composed-of:**` (required in this mode) and each following `###` block as a component with the same field table. Every ID in `Composed-of` must have a block in the prompt; a missing one is a **Failed** verdict with an explicit error naming the ID. The fixer never guesses a component from the report on disk. A component block carrying `🚫 Rejected` is skipped and listed; a composite block carrying it aborts exactly as today. A component without a usable `Location` is kept, but its symptom check in Phase 4 records `unresolved (no location)`.

**Phase 2.** Reads the composite's location and every component's location, with context, before anything else.

**Phase 3.** Implements **the composite's Remediation and nothing else**. The rule, stated in the agent verbatim: *In composite mode you implement the composite's Remediation. A component's Remediation is context for understanding its symptom; it is never applied, in this phase or in Phase 5's iterations. A component the root-cause change does not cover is reported unresolved in Phase 6, not patched locally.* This is the point of the feature and it is not softened by iteration pressure.

**Phase 4.** Tool selection is the union of the rows matched by every component (a CWE on any component selects SAST, a Documentation component selects the doc re-read, and so on), plus the rows matched by the composite's own change. A new Step 4.4 runs after the tools: for each component, re-read its location with context and decide whether its Problem still holds; record `resolved` or `unresolved` with one line of evidence.

**Phase 5.** Iteration is unchanged, under the Phase 3 rule.

**Phase 6.** The report gains a table:

```markdown
**Components:**
| ID | Result | Evidence |
|----|--------|----------|
| SEC-002 | resolved | validation now runs in `middleware.py:14` before the handler |
| ARCH-001 | unresolved | handler still constructs the query inline at `handler.py:88` |
```

`Result` ∈ `resolved`, `unresolved`, `unresolved (no location)`, `skipped (rejected)`. The verdict: **Fixed** when every non-skipped component is `resolved` and verification passed; **Partially Fixed** when at least one is `resolved`; **Failed** otherwise, or when the change could not be applied.

### 7.3 Status mapping in the orchestrator

| Fixer verdict | Composite | Component `resolved` | Component `unresolved` |
|---|---|---|---|
| Fixed | `✅ Fixed` | `✅ Fixed` | n/a |
| Partially Fixed | `⚠️ Partially Fixed` | `✅ Fixed` | no status; released by §4.3, returns individually next run |
| Failed | no status | no status | no status; composite returns whole next run and can be dissolved |

## 8. Decision gate

A needs-decision composite goes through the gate as **one** finding.

- **Stage 0** checks the composite block's `Location`.
- **Stage 1** hands the analyst the same payload the fixer would receive (§7.1). With no `Drift-class`, the analyst takes the fallback route: A is the composite's Remediation as written, B a direction derived from the code, or A alone.
- **Verification plan.** `code-review:decision-gate`'s plan-rejection test gains one clause: *a plan for a composite carries at least one check per component whose expected result is that component's symptom being absent; a plan without one is rejected.* The `decision-analyst` contract references that clause rather than restating it.
- **Pin.** The pinned file set is computed as today from the `Target` and the resolution text, plus one clause: *each component's `Location` path is pinned `:ref` unless the resolution already names it, in which case it keeps the `:edit` role the resolution gave it.* An edit to a symptom's file between decision and dispatch invalidates the decision like any referent edit.
- **The sweep** renders the composite's members (ID and title) under the `Target`.
- **`reject`** writes `🚫 Rejected` on the composite block, releasing its components.
- **Stage 4** grades as today. The write-back propagates statuses to components per §7.3 in the same pass.
- A persisted `**Decision:**` on a composite replays like any other decision.

## 9. `/fix`

- The ID regex gains `COMP`; the prefix routes to `docs/reviews/`.
- `/fix COMP-001`: Step 0.4 also extracts the unfixed component blocks named in `Composed-of` from the same report and builds the §7.1 payload. Fewer than two → the composite is degenerate; report it and stop, naming the remaining component as the thing to fix.
- `/fix SEC-002` where an **open** composite in the same report lists `SEC-002`: a new Step 0.4.5 asks one question with three options: `Fix COMP-001 instead (recommended)`, `Fix SEC-002 alone`, `Abort`. Alone proceeds as today; its `Fixed` does not touch the composite, and the degeneracy rule applies on the next bulk run.
- Legacy paste mode with a composite block and no component blocks → Phase 1's composite-mode error; the message suggests `/fix COMP-NNN`.
- Phase 8 propagates statuses per §7.3. Step 8.1.5 (never a second `**Status:**` line) applies to every block written.

## 10. `/qa:loop` is untouched

QA reports carry no composite blocks, the composition pass never runs over them (§6.1), and the dispatch-copy rule for single blocks is unchanged. In auto-merge mode the QA report's findings are dispatched exactly as today. `docs/plugins/code-review.md` says so explicitly, so nobody looks for a missing integration.

## 11. Write-back and summaries

- The Step 4.1 recipe and the Step 4.1.5 verification are unchanged. A composite and each `resolved` component receive a `**Status:**` line with the same date, each verified, each failure recorded in the same `status_write_failures` list with the same reasons.
- A degenerate composite receives the status its lone component received.
- **Fix Summary**: one row per composite, no rows for bound components:

```markdown
| 3 | [HIGH] COMP-001: Missing input validation layer — src/api/validation.py:1 (SEC-002 ✅, SEC-003 ✅, ARCH-001 —) | ⚠️ Partially Fixed |
```

- A new block after `**Reports updated:**`:

```markdown
**Composition:**
- Proposed: 2 | Persisted: 1 | Dissolved: 1
- Dropped by validation: SEC-004 + SEC-005 — member not a candidate
- Marker write failures: COMP-003 — marker-write-failed
- Pass unavailable: <reason>            <-- only where §6.5 applied
```

Omit any line whose value is empty; omit the block when the run held no composite and the pass was not unavailable.

- **Restart safety.** Markers are on disk before the first dispatch, so an interrupted run leaves its successor the same composites. An open composite is retried whole. A component fixed through a composite is filtered by Step 1.3 like any fixed finding.

## 12. Error handling, closed list

| Situation | Handling |
|---|---|
| Proposal with a member outside the candidate set, from another file, in another proposal, or fewer than two members | Dropped by §6.4, listed in the Composition block. |
| `Composed-of` names an ID absent from the file, or one carrying `🚫 Rejected` | That component is skipped; degeneracy rule applies. |
| `COMP-` ID inside a `Composed-of` | Treated as an absent ID. Composites never nest. |
| `Part-of` naming a composite that does not exist or is not open | Ignored; the finding is a candidate. |
| Hand-edited composite with severity below a component's | Effective severity raised to the maximum for the run; report not rewritten. |
| Fixer receives a composite payload missing a component block | Failed; nothing written. |
| Agent call errors, times out, or returns a malformed response | Pass unavailable for that file (§6.5). |
| Composite block persistence fails | Group dissolved for the run; components dispatched individually. |
| Composite dispatched, run interrupted before write-back | Composite stays open; retried whole next run; dissolvable. |
| Component fixed alone via `/fix` while its composite is open | Composite unaffected; degeneracy rule on the next bulk run. |

## 13. Testing

Commands and agents are prose, so verification is contract checks in CI plus an acceptance protocol, as elsewhere in this repository.

1. **Contract test** `plugins/code-review/tests/test_composite_contract.py`, pytest, in the shape of `scripts/test_check_*.py`. Each assertion greps one invariant across files, and each is mutation-checked when written: remove the sentence, the test must fail. Invariants:
   - `Composite` in `fix-auto`'s Category enum; `COMP` in `/fix`'s ID regex and in `extract-issue-ids.sh`'s `PREFIX_RE`; the `Composite | COMP` row in the docs table;
   - the verbatim "never applied, in this phase or in Phase 5's iterations" rule in `fix-auto`;
   - Step 1.6 and the dissolve question in both `/fix-all` and `/fix-report`;
   - the `:ref` clause for component locations and the per-component plan clause in `decision-gate`;
   - `Location:` and `Effort:` in the cross-verifier's composite format;
   - the `composition-analyst` closing line and `## Rejected groupings` section;
   - the "Composite findings" section and the `/qa:loop` untouched sentence in the docs.
2. **`check-prefix-sync.sh` in CI.** A new workflow `.github/workflows/prefix-sync.yml` runs the guard on pull requests against `master`. It exists to catch exactly this change and today runs only by hand.
3. **Frontmatter and boundary.** The new agent's `tools: Read, Grep, Glob` passes `check_agent_frontmatter.py`. The fix commands gain no `Bash(...)` grants, so `check_execution_boundary.py` is unaffected; the new agent does not mention `decision-gate`, so it needs no scope-table row.
4. **Acceptance protocol**, §15, run before release.
5. **Reviews.** The spec through `/superutils:spec-review`; the implementation through `/review` on the branch, with its findings fixed before merge.

## 14. Versioning and documentation

- **code-review 2.0.1 → 2.1.0.** MINOR: a new agent, a new category, new fields and steps, all additive. Pre-existing reports parse and dispatch exactly as before. All four version sites: `plugins/code-review/.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, the README table row, and the `**Version:**` header of `docs/plugins/code-review.md`.
- **`docs/plugins/code-review.md`**: a new "Composite findings" section (format, rules, the pass, the dissolve question, statuses, `/fix` behaviour, `/qa:loop` untouched); the `Composite | COMP | docs/reviews/` row; updates to the `/fix-all`, `/fix-report` and `/fix` sections and to the Decision Stage section; an Upgrade Notes entry.
- **README**: the code-review row mentions composite findings.
- The qa plugin's version and docs are unchanged.
- The spec lives on `feat/composite-findings` and is dropped before merge, per this repository's practice for `docs/superpowers/` artifacts.

## 15. Acceptance protocol

Run on a branch whose review yields at least one composable group.

- [ ] `/review` renders at least one `COMP-NNN` block with `Origin: review`, `Composed-of` with final IDs, and `Part-of` on each basis; a composite whose bases the challenger removed is a bullet, not a block.
- [ ] `/fix-all`: the pre-flight shows the composite as one row and its components under the Composites block; `total_count` excludes bound components.
- [ ] The dissolve question appears once, lists proposed and persisted composites, and dissolving one prints the delta line and updates the gate's count.
- [ ] One `fix-auto` call per composite; its report carries the Components table; statuses land on the composite and on each `resolved` component; unresolved components carry none.
- [ ] A fix-time composite is persisted before the first dispatch, immediately before its first component, with `Part-of` on each component.
- [ ] Re-running `/fix-all` re-fixes nothing; a Partially Fixed composite's unresolved components are offered individually.
- [ ] `/fix-report` shows a composite as one checklist item and asks the dissolve question before the checklist.
- [ ] `/fix SEC-NNN` on a bound component asks the three-option question; `/fix COMP-NNN` fixes the composite.
- [ ] A needs-decision composite goes through the decision gate once, with a per-component check in its plan.
- [ ] `check-prefix-sync.sh`, `check_agent_frontmatter.py`, `check_execution_boundary.py` and `test_composite_contract.py` pass.

## 16. Residual risks

- **The grouping is a model judgment.** The dissolve question is the human gate. A wrong group that passes it costs one structural change where N local ones were right. Every fix stays uncommitted, so the recovery is the working-tree diff, as it is for every fix today.
- **The "root cause only" rule is prose-enforced.** `fix-auto` holds unrestricted `Edit`, `Write` and `Bash`; nothing mechanical stops it patching a component locally under iteration pressure. The Components table makes such a lapse visible after the fact, not impossible.
- **Cost.** One agent call per report file per run, only while unmarked candidates exist. After a full run nothing is left to group and no call is made.
- **Verification of a composite is a re-read judgment per component** unless tests cover the symptoms. A composite's `Fixed` is only as hard as the tools its components' categories select.
- **Groups do not cross report files**, so a cause shared by a review finding and a QA finding is fixed twice. Accepted; the same-file rule is what keeps write-back and IDs simple.

## 17. File inventory

| File | Change |
|---|---|
| `plugins/code-review/agents/composition-analyst.md` | New. |
| `plugins/code-review/agents/fix-auto.md` | Composite mode: Phase 1 parsing, Phase 3 rule, Phase 4.4 symptom check, Phase 6 Components table; `Composite` in the Category enum. |
| `plugins/code-review/agents/cross-verifier.md` | Tightened composite criterion; `Location:` and `Effort:` in the format. |
| `plugins/code-review/agents/decision-analyst.md` | Composite payload noted; plan clause referenced by pointer. |
| `plugins/code-review/commands/review.md` | Step 5.5 item body; Step 5.6 COMP IDs, `Part-of`, placement; summary metric. |
| `plugins/code-review/commands/fix-all.md` | Step 1.6, pre-flight Composites block, Step 2.4.5, Step 3.0, status mapping, Fix Summary row and Composition block. |
| `plugins/code-review/commands/fix-report.md` | Step 1.6, Step 2.1.5, checklist item, Step 2.3.5, status mapping, summary. |
| `plugins/code-review/commands/fix.md` | `COMP` in the regex and routing; Step 0.4 composite extraction; Step 0.4.5; Phase 8 propagation. |
| `plugins/code-review/skills/decision-gate/SKILL.md` | Composite through the gate; the `:ref` clause; the per-component plan clause. |
| `plugins/code-review/scripts/extract-issue-ids.sh` | `COMP` in `PREFIX_RE`. |
| `plugins/code-review/tests/test_composite_contract.py` | New. |
| `.github/workflows/prefix-sync.yml` | New. |
| `docs/plugins/code-review.md` | Composite findings section, prefix row, command sections, Decision Stage, Upgrade Notes, version header. |
| `README.md` | code-review row: version and description. |
| `.claude-plugin/marketplace.json`, `plugins/code-review/.claude-plugin/plugin.json` | Version 2.1.0. |
