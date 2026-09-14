# Spec-review report — 2026-09-14-composite-findings-design.md
**Mode:** default · **Budgets used:** 12 of 30 dispatches, ~2200 (estimate: 3962 s wall minus ~1780 s of user waits at the three-question ask and the two approve gates) of 3600 active seconds · **Terminal status:** `TRIAGED` · **Verdict label:** Re-reviewed (advisory) — 1 edits applied without re-review
**Spec hash (pre-loop):** 59a539a2ec232717a91aab175a4abdaa478f1d17996a2be08622b3ca5cbecb13
**Spec hash (post-loop):** db18ff3562605d44da36ca9e1ad80d8c386995b7cc6096a8767e704e1213944f
**Spec lines:** 435 → 455

Run 2 over the unchanged spec (run 1 stopped on the time budget before batch A; its report is archived as `2026-09-14-composite-findings-design-review.run1.bak`, its snapshot as `….pre-loop.run1.bak`). Flags: `--time-budget 3600 --max-dispatches 30`.

## Panel — lenses, units

- Units: the spec's `##` headings, in order: 1. Problem · 2. Goals and non-goals · 3. Definitions · 4. Report format · 5. Review side · 6. The composition pass · 7. Dispatch and the fixer · 8. Decision gate · 9. `/fix` · 10. `/qa:loop` is untouched · 11. Write-back and summaries · 12. Error handling, closed list · 13. Testing · 14. Versioning and documentation · 15. Acceptance protocol · 16. Residual risks · 17. File inventory. (The `## Composition Proposals` and `## Rejected groupings` lines inside §6.3's fenced block are not units.)
- Lenses selected (the full seven-lens roster — no cap), panel order as logged:
  - `internal-consistency` — core, always on.
  - `ambiguity-testability` — core, always on.
  - `completeness` — 17 sections, above the 3-section threshold.
  - `feasibility` — content trigger: plugin change, new agent, fix loop.
  - `doctrine-compliance` — same trigger: closed loop, agents, marketplace plugin.
  - `ux` — content trigger: user-facing flows (dissolve question, pre-flight, checklist, summaries).
  - `contracts` — content trigger: data formats (block grammar, agent return contract, payload, status vocabulary, SemVer claim).
- Panel wall time 560 s (parallel). Raw findings 49 (IC 6 · AT 11 · C 6 · F 8 · D 4 · U 8 · CT 6); 11 merges; 38 entries.
- Merges (slug equality + logged equivalence judgment):
  - SR-001 ← [internal-consistency, completeness, contracts] · the same §7.1/§7.2 payload-vs-Phase-1 contradiction; completeness graded it major and flagged needs-decision (two reconcilable directions), so the merged entry carries the flag at critical.
  - SR-002 ← [internal-consistency, ambiguity-testability] · the same bound-invariant-vs-degenerate-lone-component defect, both anchored at §3.
  - SR-003 ← [internal-consistency, ux] · the same delta-line-vs-count defect; ux adds the per-dissolve rendering and the released components' destinations.
  - SR-004 ← [internal-consistency, ambiguity-testability] · the same two senses of "persisted" in §6.6 vs §11.
  - SR-007 ← [ambiguity-testability, completeness, feasibility] · the same `/fix-all` zero-auto-path gap; feasibility graded critical (a compliant implementation violates §4.3, §6.7 and §11 on a reachable path), so the merged entry is critical.
  - SR-008 ← [ambiguity-testability, feasibility] · the same unarbitrated deciding signal for component statuses on the gate path.
  - SR-010 ← [ambiguity-testability, completeness] · the same missing review-side disjointness rule.
  - SR-015 ← [ambiguity-testability, ux] · the same undefined Fix Summary glyph vocabulary; nit + minor → minor.
  - SR-016 ← [completeness, feasibility] · the same `/fix`-runs-its-own-phases gap.
  - Not merged (different anchor slug, related): SR-005 (§2 goal) ~ SR-034 (§14 claim); SR-004 (§6.6 pre-flight) ~ SR-033 (§11 summary); SR-024 (§7, both paths) ~ SR-008 (§8, gate path only).

| SR | severity | lenses | needs-decision | outcome |
|---|---|---|---|---|
| SR-001 | critical | internal-consistency, completeness, contracts | yes — decided A | applied |
| SR-002 | major | internal-consistency, ambiguity-testability | no | applied |
| SR-003 | minor | internal-consistency, ux | no | reported-only |
| SR-004 | minor | internal-consistency, ambiguity-testability | no | reported-only |
| SR-005 | minor | internal-consistency | no | reported-only |
| SR-006 | minor | internal-consistency | no | reported-only |
| SR-007 | critical | ambiguity-testability, completeness, feasibility | no | applied |
| SR-008 | major | ambiguity-testability, feasibility | no | applied |
| SR-009 | major | ambiguity-testability | no | applied |
| SR-010 | major | ambiguity-testability, completeness | no | applied |
| SR-011 | minor | ambiguity-testability | no | reported-only |
| SR-012 | minor | ambiguity-testability | no | reported-only |
| SR-013 | minor | ambiguity-testability | no | reported-only |
| SR-014 | minor | ambiguity-testability | no | reported-only |
| SR-015 | minor | ambiguity-testability, ux | no | reported-only |
| SR-016 | major | completeness, feasibility | no | applied |
| SR-017 | minor | completeness | no | reported-only |
| SR-018 | minor | completeness | no | reported-only |
| SR-019 | major | feasibility | no | applied |
| SR-020 | major | feasibility | no | applied |
| SR-021 | minor | feasibility | no | reported-only |
| SR-022 | minor | feasibility | no | reported-only |
| SR-023 | minor | feasibility | no | reported-only |
| SR-024 | major | doctrine-compliance | yes — decided B | applied |
| SR-025 | minor | doctrine-compliance | no | reported-only |
| SR-026 | major | doctrine-compliance | yes — decided A | applied |
| SR-027 | minor | doctrine-compliance | no | reported-only |
| SR-028 | minor | ux | no | reported-only |
| SR-029 | minor | ux | no | reported-only |
| SR-030 | minor | ux | no | reported-only |
| SR-031 | nit | ux | no | reported-only |
| SR-032 | minor | ux | no | reported-only |
| SR-033 | minor | ux | no | reported-only |
| SR-034 | major | contracts | no | applied |
| SR-035 | major | contracts | no | applied |
| SR-036 | minor | contracts | no | reported-only |
| SR-037 | minor | contracts | no | reported-only |
| SR-038 | minor | contracts | no | reported-only |

## Critical challengers

| SR | verdict | note |
|---|---|---|
| SR-001 | uphold | Nothing rewrites `Composed-of` in the dispatch copy (§4.3 authored field; the stage 3 strip table is closed and does not list it); fixed/rejected IDs are not definitionally absent from it (§6.2.1 filters the derived set without editing the line; §12 "Composite unaffected"); the collision is reachable on blessed paths (three components, one fixed → dispatched with three IDs and two blocks → Failed); §12's own two rows contradict on one payload; the rejected-component half is a flat contradiction with Phase 1's skip clause and Phase 6's `skipped (rejected)`. Stands at critical. (69 s) |
| SR-007 | uphold | The path is reachable (`review.md` Step 5.5 sets needs-decision on every Documentation reinstatement, so an all-needs-decision report is ordinary; §4.1 makes the composite inherit it); `fix-all.md` Step 2.2.5 verbatim skips the rest of Step 2 and Steps 3–4 — exactly where §6.7 and §6.8 anchor the gate and the writes; no passage relocates them; §12, §2 and §16 record no deferral. On the forced reading the gate is handed a composite with no block on disk and stage 2's writes have no heading to target; on the alternative reading §8's "one finding" is unreachable. Stands at critical. (77 s) |

## Verification of batch A

The `fix-coherence` verifier received the unified diff of batch A and the SR list (id, severity, description — no proposed fix), and returned one entry per landed SR (576 s).

| SR | resolved | reason |
|---|---|---|
| SR-001 | true | §7.1 no longer excludes fixed or rejected components; §7.2 Phase 1 skips status-carrying blocks as `skipped (fixed)`/`skipped (rejected)` and fails only on an ID with no block at all; §12's colliding rows were split; §9's extraction aligned. |
| SR-002 | true | §3 binds only components of a dispatchable composite with the Step 0.4.5 exception; §6.2 item 2 unbinds the degenerate composite's lone component and puts it in the pre-flight, `total_count`, the floor, the partition and the checklist; §6.6 narrowed; §2's goal carries the exception. |
| SR-007 | true | The zero-auto path is named in §6.1, §6.7 (question at the head of Step 5.2, `yes` as commitment point), §6.8 (writes after the `yes`, before the gate loads at Step 5.4), §11, §12 and §17 with the same step numbers. |
| SR-008 | true | §8's Stage 4 bullet keys propagation on the gate's graded case, writes no component status where the composite gets none, and decides each component from its own plan check. |
| SR-009 | true | §15 specifies a Fixture, five ordered runs with each item labelled, a paging pass condition, and a Disposition rule with `N/A` and three release-blocking items. |
| SR-010 | true | §5.2's new item 2 imposes disjointness in cross-verifier return order with a matching §12 row. |
| SR-016 | true | §9 states `/fix` runs the composite through its own phases, maps §7.2's composite mode onto them including `Composite` in its Phase 1 enum; §13.1 and §17 carry the same items. |
| SR-019 | true | §6.4 requires the usability rule in full (parse, containment, existence) and drops a failing proposal as `location-unusable`; §4.1 states containment and corrects the stage 0 / Phase 1 claim on the `auto` path. |
| SR-020 | true | §13.1 names stdlib `unittest` run as `python3 …`; §13.2 adds `code-review-contract.yml` running the test and `check-prefix-sync.sh`; §15 and §17 name the same file. |
| SR-024 | true | Decision B implemented: gate path keyed to per-component plan checks with the fixer's table advisory; §7.3, §11 and §16 label the auto path's component statuses as fixer self-report. |
| SR-026 | true | Decision A implemented: §6.7 fail-closed (proposals dropped, persisted dissolved for the run, disclosure line) with a §12 row and a §16 entry. |
| SR-034 | true | §14 separates parsing (unchanged) from dispatch (changed) and re-argues MINOR; §2's goal rewritten to match. |
| SR-035 | true | §8 Stage 1 applies the per-block rules independently (nonce-wrapping every `**Source:**` component block); stage 2's render gains a `Source` row per feedback-origin component. |

Fix-induced findings (next SR ids, discovery order):

| SR | severity | introduced by | outcome |
|---|---|---|---|
| SR-039 | major | SR-002 | applied (not re-reviewed) |
| SR-040 | minor | SR-019 | reported-only |
| SR-041 | minor | SR-026 | reported-only |
| SR-042 | minor | SR-024 | reported-only |
| SR-043 | nit | SR-034, SR-007 | reported-only |

- **SR-039 · major · §6 · fix-induced by SR-002** — §3 now binds only a component of a *dispatchable* composite and §6.2 item 2 declares the degenerate composite's lone component "unbound for this run"; §6.2 item 3 and §3's `candidate` row then admit it to the candidate set, §6.3 hands the analyst only "the list of IDs already bound", and §6.4's checks pass — so the pass may bind it into a new fix-time composite while the degenerate composite still names it in `Composed-of`, violating §4.2's "at most one open composite" and "one `Part-of` line", and contradicting item 2's "dispatched alone". Reachable via §12's "Component fixed alone via `/fix` while its composite is open" row.
- **SR-040 · minor · §5 · fix-induced by SR-019** — §4.1 now says containment is enforced by "§5.2's block building at review time, which builds this field to this rule", but §5.2's procedure never validates `Location` and states no disposition for a cross-verifier `Location` that is not contained; a review-origin `auto` composite with an unusable `Location` can reach `fix-auto`, which §4.1 itself says does not test containment. *Fix:* add to §5.2 item 4 (or a new item): `Location` is validated to the §4.1 rule — parse, three-step containment, existence — and a composite failing any conjunct is not rendered as a block and stays a bullet, never repaired.
- **SR-041 · minor · §11 · fix-induced by SR-026** — §6.7 and §12 say the pre-flight and the Composition block carry `Dissolve question: unavailable — <reason>; all composites dissolved for this run`, but §11's Composition block template enumerates four line kinds with "omit any line whose value is empty", and §6.6's Composites block enumerates its lines; neither has a slot, so an implementer rendering the templates as written emits no fail-closed disclosure. *Fix:* add the line to §11's template (`<-- only where §6.7's fail-closed path applied`) and to §6.6's block under `**Composition pass:**`.
- **SR-042 · minor · §11 · fix-induced by SR-024** — §11's new sentence backticks `advisory (fixer self-report)` but the example row above it is unchanged and shows no place for the label; one implementer appends it, another prints nothing. *Fix:* update the example row to carry the suffix `— advisory (fixer self-report)` before the status cell, and state that it is omitted on the decision-gate path.
- **SR-043 · nit · §14 · fix-induced by SR-034, SR-007** — §14's MINOR justification says "no write happens before the confirmation gate", but on `/fix-all`'s zero-auto path there is no confirmation gate; the commitment point is the `yes` at Step 5.2. *Fix:* "no write happens before the run's commitment point (§6.8) — the confirmation gate, or the user's `yes` at Step 5.2 on `/fix-all`'s zero-auto path".

## Decisions

| SR | decision | edit text (verbatim) |
|---|---|---|
| SR-001 | A — accept, direction A | The payload carries every ID in `Composed-of` that still has a block in the file, already-fixed and rejected ones included, with their pre-existing `**Status:**` line (which the stage 3 strip table already lets travel). Phase 1 skips blocks carrying a status (Result `skipped (fixed)` / `skipped (rejected)`) and fails only for an ID with no block in the prompt at all. Degeneracy is still counted over unfixed components alone. One rule, no new payload line. Align §7.1, §7.2 Phase 1, Phase 4's symptom check, Phase 6's Result vocabulary, §7.3, §9's `/fix COMP-001` extraction and §12's two rows accordingly. |
| SR-024 | B — accept, variant B | On the decision-gate path a component's status is decided by that component's own check in the decided verification plan, graded on raw output exactly as the composite's own status is; the fixer's Components table is advisory and never decides a status. On the auto path the fixer's verdict remains the status, but §16 and the Fix Summary explicitly label component statuses as resting on the actor's self-report. (The same choice the user made for the equivalent entry in run 1.) |
| SR-026 | A — accept, variant A | When the dissolve question cannot be asked (`AskUserQuestion` unavailable or errors), no composite is dispatched as a unit this run: every proposed composite is dropped (nothing persisted) and every persisted composite is treated as dissolved for the run with its components dispatched individually, no dissolution status written; the pre-flight and the Composition block carry `Dissolve question: unavailable — <reason>; all composites dissolved for this run`. Add the row to §12, state the fail-closed direction in §6.7, add a §16 entry recording that the gate is not TTY-probed. |

Recorded for the reader; no run reads them back, every run asks afresh.

## Residuals

Ordered most- to least-serious.

### applied (not re-reviewed)

- **SR-039 · major · §6 · fix-induced by SR-002** — batch B's five in-place rewrites (§3 `candidate` row, §6.2 items 2 and 3, §6.3's dispatch sentence and battery check 3) exclude any ID named in an open composite's `Composed-of` from the candidate set, so a degenerate composite's lone component is dispatched alone and never re-grouped. Applied after the approve gate; by design no verifier read batch B.

### reported-only (minors and the nit — never batched)

> **Applied by hand after the run (2026-09-14, outside the pipeline, unverified by it).** Every entry below, and the four fix-induced minors and nit (SR-040–SR-043), was edited into the spec by the orchestrator at the user's request after terminalization; SR-005 needed no edit (batch A's SR-034 pair had already rewritten §2). The post-loop hash above is the hash the pipeline left; the spec on disk has moved past it, so the next run's re-run detection will treat it as changed.


- **SR-003 · minor · §6 · [internal-consistency, ux]** — §6.7's worked delta line `Dissolved COMP-002: +2 issues, 14 total` contradicts §6.6's counting rule (a two-component composite dissolves to +1 in `total_count`); whether one line prints per dissolved composite or one aggregate is undefined; released components can be dropped by the floor or routed to the skipped list, and the line never says where they went. *Fix:* one line per dissolved composite — `Dissolved COMP-002: 2 components released — <a> join the fix list, <b> require a decision, <c> below the severity floor; total to fix <new total_count>` — with the worked example corrected to §6.6's two-component COMP-002.
- **SR-004 · minor · §6 · [internal-consistency, ambiguity-testability]** — "persisted" has two senses: §6.6's pre-flight `1 proposed, 1 persisted` counts composites already on disk (nothing is written before the gate), §11's `Persisted: 1` counts proposals this run wrote. *Fix:* §6.6 `**Composition pass:** <N> proposed this run, <M> already in the report`; §11 `Proposed: N | Written this run: M | Dissolved: K`; one sentence stating that nothing this run proposes is persisted at the pre-flight.
- **SR-005 · minor · §2 · [internal-consistency]** — §2's compatibility goal was contradicted by §6.1 for old review and feedback reports. *Batch A's SR-034 pair rewrote this bullet* (`applied` via SR-034); listed here because the entry itself was graded minor and never batched.
- **SR-006 · minor · §12 · [internal-consistency]** — The closed list omits three situations the spec defines elsewhere: a proposal whose `Location` fails §6.4 (now `location-unusable`), a `Part-of` write that fails (§6.8: recorded; membership unaffected), a dissolution write that fails (§6.8: recorded; treated as dissolved for the run, offered again next run). *Fix:* add the three rows.
- **SR-011 · minor · §5 · [ambiguity-testability]** — §5.2 step 1 handles only the zero-match case; a basis title matching more than one surviving finding is undetermined. *Fix:* "A basis the challenger removed, that matches nothing, or that matches more than one surviving finding is dropped — an ambiguous title is not a resolved basis."
- **SR-012 · minor · §13 · [ambiguity-testability]** — "each is mutation-checked when written: remove the sentence, the test must fail" leaves no artifact; CI runs the assertions as written. *Fix:* each assertion carries a `# mutation:` comment quoting the sentence whose deletion must fail it, and the PR records the mutation run — or state that the mutation check is an authoring discipline outside the release gate.
- **SR-013 · minor · §6 · [ambiguity-testability]** — §6.2's zero-component close names no trigger: such a composite is never dispatched and §11 keeps the Step 4.1 recipe unchanged, so whether the housekeeping status is written, and on which runs, is undetermined. *Fix:* in §11 beside the degenerate clause: "A composite with no open components is closed by the same Step 4.1 pass as a housekeeping write, verified by Step 4.1.5; a run that never reaches write-back leaves it open."
- **SR-014 · minor · §6 · [ambiguity-testability]** — §6.8's "immediately before its first component's heading" does not say `Composed-of` order or file order; §15 inherits the ambiguity. *Fix:* "before the heading of the component that appears first in the file among its `Composed-of` members", mirrored in §15.
- **SR-015 · minor · §11 · [ambiguity-testability, ux]** — The Fix Summary's component glyphs (`✅`, `—`) are undefined against §7.2's Result values (now five); `unresolved (no location)` collapses into `—`. *Fix:* a legend beside the row — `✅ resolved · — unresolved · ❓ unresolved (no location) · 🚫 skipped (rejected) · ✔︎ skipped (fixed)` — stating the list renders each component's Phase 6 `Result`, in `Composed-of` order.
- **SR-017 · minor · §4 · [completeness]** — §4.1 carries `**Impact:**` and §5.2 takes `Impact` from the composite, but neither producer emits one: the cross-verifier's format has `Combined risk` (spent on `Problem`) and the analyst's return contract lists no Impact. *Fix:* add `Impact:` to both producers, or make `**Impact:**` optional on a composite and drop it from §5.2's list.
- **SR-018 · minor · §6 · [completeness]** — §6.3 mandates `## Rejected groupings` ("never dropped silently") but no consumer renders it; §11's Composition block has no line for the analyst's own rejections. *Fix:* add `- Rejected by the analyst: <pair> — <reason>` to §11's block (omit when empty), or state that the section is for the agent's discipline and is not rendered.
- **SR-021 · minor · §4 · [feasibility]** — §4.3's claim that `Part-of` is hashed into `**Decision-pin:**` is undeliverable: the block hash is cut from one line range (the composite's own block), so `Part-of` lines in component blocks are outside it; component blocks travel in the payload unpinned, and §8's `:ref` clause pins component *file* paths, not blocks. *Fix:* drop `Part-of` from the hashed list, state that the pin covers the composite's own block alone (membership is protected because `Composed-of` is inside it), and record the unpinned-component-block residual in §16.
- **SR-022 · minor · §7 · [feasibility]** — §7.1's trailing `User decision:` line after the component blocks collides with `fix-auto`'s field capture: Phase 1 bounds `Remediation` at the `User decision:` line and treats it as the block's own field, so a trailing line terminates the last component's Remediation and is read as that component's authoritative decision. *Fix:* place the line immediately after the composite block, before the first component heading, and state that in composite mode each block's capture ends at the next `###` heading and exactly one `User decision:` field is parsed, belonging to the composite.
- **SR-023 · minor · §13 · [feasibility]** — §9 makes `/fix` a dispatcher bound by stage 3's dispatch-copy rule, but its row in `decision-gate`'s grant-registry scope table still reads `render-only` ("Runs no stage"); `/qa:loop` is `dispatch-only` for exactly this relation. `check_execution_boundary.py` will not catch the drift. *Fix:* reclassify `fix.md` as `dispatch-only` with the `/qa:loop` rationale; add to §13.3 and §17's `decision-gate` row.
- **SR-025 · minor · §7 · [doctrine-compliance]** — Bar 3 / soft-oracle labelling: `unresolved (no location)` (a component the checker structurally cannot reach) holds the composite at `⚠️ Partially Fixed` however completely the root-cause change landed — coverage gating the verdict; no verification-coverage line exists in the Composition block, and a soft `✅ Fixed` carries no `**Verification:**` marker. *Fix:* exclude unreachable components from the Fixed/Partially Fixed test and disclose them (`- Verification coverage: 2 of 3 components checked (ARCH-001: no location)`), and write the `**Verification:** advisory — <checks run>` form beside a status that rests on a re-read.
- **SR-027 · minor · §6 · [doctrine-compliance]** — Bar 6: no time bound anywhere — §6.5 and §12 branch on a "timeout" the spec never defines or assigns; calls are `model: opus` and parallel. *Fix:* state a per-file wall-clock budget after which the orchestrator abandons the call and takes §6.5's path, plus a ceiling on concurrent calls — or record in §16 that the pass is unbounded in time and the timeout is the platform's.
- **SR-028 · minor · §6 · [ux]** — "(select none to keep all)" is false on a non-final page of the paged dissolve question, and the spec never says selections accumulate or that every page is answered. *Fix:* per-page copy — non-final page `(page X of Y — select none on this page to keep these)`, final page `(select none to keep all)` — plus "Selections accumulate across pages; every page is answered."
- **SR-029 · minor · §6 · [ux]** — The dissolve option carries ID and origin only, no title or severity, and nothing tells a persisted composite (dissolving writes `🚫 Rejected` into the report) from a proposed one (nothing written). *Fix:* label `COMP-001 · HIGH (review)`; description `<title> — <n> components: … — marks COMP-001 🚫 Rejected in the report and releases them` / `… — drops the proposal, nothing is written`.
- **SR-030 · minor · §6 · [ux]** — After a dissolve in `/fix-all` only the delta line prints; the last full rendering still shows the dissolved composites as rows and omits the released components, against Step 2.4's "always render the full list" rule. *Fix:* re-render the released components as issue-table rows with recomputed `By severity` and `Requires user decision (skipped)` lines before the gate, or state explicitly that the table is not refreshed.
- **SR-031 · nit · §6 · [ux]** — §6.9's checklist description renders two unlabelled ` · ` tails in auto-merge mode (`… · review · <basename>`) and drops the Problem sentence every other item carries. *Fix:* `src/api/validation.py:1 — 3 components (review): SEC-002, SEC-003, ARCH-001 — <first sentence of Problem>`, leaving ` · <basename>` as the auto-merge tail.
- **SR-032 · minor · §9 · [ux]** — Step 0.4.5 is three bare labels: no question text, no option descriptions, no basis for "(recommended)", no abort message. *Fix:* question `SEC-002 is part of composite COMP-001. Fix which?`; `Fix COMP-001 (recommended)` — `<composite title> — one root-cause change resolving SEC-002, SEC-003, ARCH-001`; `Fix SEC-002 alone` — `Local fix only — the shared cause stays and COMP-001 returns whole on the next bulk run`; `Abort` — `Stop now without modifying any files`, with `Aborted. No changes made.`
- **SR-033 · minor · §11 · [ux]** — The Composition block's `Persisted` and `Dissolved` conflate composites written this run, proposals merely forgotten, and persisted composites stamped `🚫 Rejected`. *Fix:* `- Proposed: 2 | Written to the report: 1 | Dropped proposals: 1 | Marked 🚫 Rejected (dissolved): 1`, listing the stamped IDs.
- **SR-036 · minor · §7 · [contracts]** — The `**Components:**` table is a new consumer contract with only the producer side specified: no read rule (row lookup by ID against `Composed-of`), nothing for a missing row, a foreign ID, or an absent/malformed table. *Fix:* "The orchestrator matches each row's `ID` against `Composed-of`; a foreign ID is ignored and noted; a component with no `resolved` row receives no `**Status:**` line"; §12 row: a report with no or an unparseable Components table is Failed per Step 3.1's malformed-response rule, nothing written.
- **SR-037 · minor · §4 · [contracts]** — `**Composed-of:**` has no one-physical-line rule (unlike every other machine-read field in this family), no token form, and no ceiling; a wrapped line silently loses members. *Fix:* "occupies exactly one physical line, no continuation; bare `PREFIX-NNN` tokens separated by `, `; a grouping too large to fit is not written — the pass caps a proposal at the members that fit and lists the remainder as rejected"; same one-line rule for `Part-of` and `Origin`.
- **SR-038 · minor · §12 · [contracts]** — A block with `**Category:** Composite` and no `**Composed-of:**` is not a composite by §3 (hence a candidate) yet puts `fix-auto` into composite mode by §7.2's Category-only switch. *Fix:* §12 row: not a composite and not a candidate — excluded from the pass and from dispatch, listed as `malformed-composite`; §7.2 enters composite mode only when the block carries a `**Composed-of:**` line, else Failed naming the missing field.

## Coverage

- Lenses not selected: none — the full seven-lens roster was dispatched.
- Lenses not returned: none.
- Verifier: returned on the first dispatch with all 13 batch-A ids present in `resolved` — no omission.
- Standing blind spots: user intent, external facts, unstated requirements. One stochastic panel pass; majors carried no challenger.

## Rejected by the panel and the verifier (self-falsification)

### internal-consistency
- [internal-consistency] §4.1 'Phase 1 refuse[s] a block without a usable location' vs §7.2 keeping a component that has none — §4.1's field rules govern the composite block, and §7.2 carves the component case out explicitly.
- [internal-consistency] §7.1 'Components that are already fixed or rejected are not included' vs §7.2 Phase 1 'A component block carrying 🚫 Rejected is skipped and listed' — reconcilable as defensive handling for §9's legacy paste mode, which can supply any block.
- [internal-consistency] §11 'A composite and each resolved component receive a **Status:** line' vs §7.3's Failed row 'no status' — §7.3 is the named status-mapping authority and §11's composite clause is equally context-scoped, so §11 reads as the recipe, not an unconditional rule.
- [internal-consistency] §6.7 'This is the one human gate on a grouping' vs §9's three-option question and /fix-report's checklist selection — the claim is scoped to the bulk run's grouping decision, which is indeed asked once.
- [internal-consistency] §15 'The dissolve question appears once' vs §6.7's four-options-per-call paging — 'once' reads as once per run, not one API call.
- [internal-consistency] §5.3 'A composite is rendered after the non-composite findings of the same severity' vs §6.8 inserting a fix-time composite immediately before its first component — §5.3 is scoped by its heading to /review Step 5.6 rendering.
- [internal-consistency] §16 'After a full run nothing is left to group and no call is made' vs released unresolved components becoming candidates again — the sentence's own qualifier 'only while unmarked candidates exist' governs.
- [internal-consistency] §4.3 'The new fields are authored fields, not loop-written ones' vs the composition pass writing them (§6.8) — the following sentence states the classification and its justification, so the two are reconciled in place.
- [internal-consistency] §9 '/fix COMP-001 … report it and stop' on degeneracy vs §6.2's bulk dispatch of the lone component — different commands, each stating its own behavior explicitly.
- [internal-consistency] §5.1's finding-falsification exemption for the cross-verifier vs §6.3's mandatory battery for the composition-analyst — different claims (member truth vs grouping validity), and §5.1 states the subsumption criterion for the review path too.
- [internal-consistency] §5.1's 'Location: (primary site of the shared fix, path:line)' vs §4.1 permitting 'path:line-range' — emitting the narrower of two permitted forms is not a contradiction.
- [internal-consistency] §8 'With no Drift-class, the analyst takes the fallback route' vs §4.1 'Components carry their own' — the gate treats the composite as the one finding being decided, so the composite's absent Drift-class governs.
- [internal-consistency] §4.3 'the composition pass writes its markers before any pin is computed in the same run' vs §6.8's Step 3.0 placement in /fix-all — the spec asserts the ordering only for /fix-report and never states where /fix-all's decision gate sits, so no spec-internal contradiction.
- [internal-consistency] §6.2's zero-component close writing '✅ Fixed when at least one component carries ✅ Fixed or ⚠️ Partially Fixed' — no stated rule forbids a composite closing Fixed over a partially fixed component.
- [internal-consistency] §6.6's single 'Composition pass:' line vs the per-file unavailability of §6.4/§6.5 — a rendering detail the spec never contradicts.
- [internal-consistency] §11's 'Dropped by validation: SEC-004 + SEC-005' reusing the pair §6.3 shows as an agent-rejected grouping — example IDs only, no rule at stake.

### ambiguity-testability
- [ambiguity-testability] §4.1 'any component carries a Fix-policy value other than auto' — silent on a component with no Fix-policy field: refuted, /fix-all Step 2.2.5 fixes 'Absent field ⇒ auto' as the plugin-wide rule.
- [ambiguity-testability] §6.1 'only over review reports (docs/reviews/, feedback reports included)' as a possible scope conflict for feedback reports: refuted, the feedback-file allocator writes into docs/reviews/, so the two clauses name one set.
- [ambiguity-testability] §6.2 'unfixed' possibly including ⚠️ Partially Fixed components: refuted, the fixed-status filter skips ✅/⚠️/🚫 alike and §6.2.2 counts ⚠️ among the fixed when closing a composite.
- [ambiguity-testability] §8 Stage 1 'A is the composite's Remediation as written, B a direction derived from the code, or A alone' — trigger for 'A alone' unstated: refuted, decision-gate's fallback route defines exactly when A is returned alone.
- [ambiguity-testability] §6.6 single `Composition pass:` line vs §6.5's per-file unavailability: refuted, both fix commands read at most one review report per run, so the per-file and per-run renderings coincide.
- [ambiguity-testability] §6.3 battery check 1 (subsumption) has no observable pass condition for a read-only agent: refuted, §16 explicitly discloses the grouping as a model judgment gated by the dissolve question.
- [ambiguity-testability] §6.4 silent on a response missing the required `## Rejected groupings` section: refuted, §12's 'returns a malformed response' row routes it to pass-unavailable.
- [ambiguity-testability] §4.3 'A `Part-of` relation binds while the composite is open' vs §4.2 'membership is decided by Composed-of alone': refuted, §4.2 arbitrates explicitly and §12 confirms a dangling Part-of is ignored.
- [ambiguity-testability] §7.2 Phase 6 verdict when verification failed but one component is `resolved`: refuted, the conditions are ordered and determinate (Partially Fixed).
- [ambiguity-testability] §4.3 'the fixers raise the composite's effective severity to the maximum for the run' — which actor: refuted, the floor and queue outcome is identical whoever computes it; only the rendered severity could differ, which is wording-level.
- [ambiguity-testability] §9 '/fix COMP-001 ... naming the remaining component as the thing to fix' with zero remaining components: refuted as wording-only, the degeneracy behaviour (report and stop) is already determined.
- [ambiguity-testability] §6.7 'Released components pass through the severity floor and the Fix-policy partition again' vs the `+2 issues, 14 total` delta example: refuted, the count after re-filtering is derivable and the example is illustrative.
- [ambiguity-testability] §6.1 placing Step 1.6 before the severity floor, so a composite can carry sub-floor components: refuted, §4.3's severity rule states the intended effect and the placement is explicit.

### completeness
- [completeness] A bound component below the severity floor rides along with its composite — §4.3's severity-maximum rule plus §6.7's "released components pass through the severity floor and the Fix-policy partition again" settle that bound ones do not.
- [completeness] A component's own persisted `**Decision:**` being silently stripped by the §7.1 dispatch copy — unreachable: §3's candidate definition excludes any finding carrying `**Decision:**` or `**Dispatch:**`, and a bound component is never dispatched alone, so it cannot acquire one while bound.
- [completeness] A stale `**Part-of:**` line left behind when a released component is re-grouped (§6.8 only inserts, never replaces) — §4.2 ("a missing or dangling `Part-of` changes nothing about what is bound") and §12's Ignored row make the leftover inert; cosmetic only.
- [completeness] A zero-component degenerate composite can never be "closed at write-back" (§6.2) when the run dispatches nothing and ends before Step 4 — benign: the composite stays open and §11's restart-safety paragraph has the next run retry it.
- [completeness] The review report double-counting a composite and its components in its headline metrics — `commands/review.md` carries no total/severity-distribution table, and §5.3 settles the only metric that exists ("Cross-analysis findings").
- [completeness] Whether `/fix` also runs a composition pass — §6.1 names `/fix-all` and `/fix-report` as the two placements, and §9 gives `/fix` only recognition of persisted composites.
- [completeness] No timeout or token budget stated for the `composition-analyst` call — §6.5 fixes the behavior on timeout (zero proposals, pass unavailable); the numeric value is implementation-plan detail this lens must not demand.
- [completeness] An `auto` finding being pulled into the decision gate because its composite inherited `needs-decision` — derivable from §4.1's inheritance rule and consistent with the fixers' documented fail-safe.
- [completeness] A component with no usable `Location` under §8's "each component's `Location` path is pinned `:ref`" clause — §7.2 already defines the location-less component's treatment and the gate already discloses unpinnable paths; low blast radius.
- [completeness] No cap on members per group or proposals per file — not load-bearing; §16's Cost bullet bounds the pass at one call per report file per run.
- [completeness] §6.4's validation list omits `Effort` — `Effort` is an optional field in the fixers' field tables, so nothing depends on validating it.
- [completeness] A dissolution chosen at `/fix-report` Step 2.1.5 being lost when Step 2.3 stops on an empty selection — §6.8's "An aborted run writes nothing" covers it, and the composite is simply offered again next run.
- [completeness] Whether `/fix-all` Step 3.0 persists needs-decision composites on the normal path — §6.7's "the run holds at least one dispatchable composite" and §6.8's unrestricted "each accepted proposal" settle that it does.

### feasibility
- [feasibility] `/fix` cannot ask §9's three-option question — refuted: CLAUDE.md states `allowed-tools` in command frontmatter pre-approves permission prompts "without affecting availability", so AskUserQuestion is reachable; 3 options is also within the 4-option ceiling.
- [feasibility] The inserted step numbers collide with existing steps — refuted: 1.6 is free in both fix commands (1.1–1.5 exist and end at the edge cases), 2.4.5 sits between fix-all's pre-flight 2.4 and confirmation 2.5, 3.0 precedes 3.1, 2.1.5 sits between fix-report's 2.1 sort and 2.2 checklist, 2.3.5 between 2.3 and the 2.4 gate, and 0.4.5 between fix.md's 0.4 and 0.5.
- [feasibility] Adding `COMP` breaks `check-prefix-sync.sh` — refuted: the canonical table is `| Category | Prefix | Reports Directory |`, the awk reads column 3 for the prefix and column 2 for the category, and `prefixes_from_alternations` matches any 2–8 uppercase token in a parenthesised alternation, so `COMP` flows to all three declared consumers exactly as §4.3 says.
- [feasibility] The new agent trips `check_agent_frontmatter.py` — refuted: `EXPECTED_AGENT_FILES = 26` is a floor that warns only when *fewer* files are scanned; `name`, `description`, `tools`, `model` are all in PERMITTED_KEYS and `Read`, `Grep`, `Glob` are all in CANONICAL_TOOLS.
- [feasibility] `composition-analyst` needs a grant-registry scope row — refuted: `check_execution_boundary.py`'s CONSUMER_GLOBS are `*/commands/*.md` and `*/skills/*/SKILL.md`; agent files are never scanned, whether or not they mention the skill.
- [feasibility] §6.7's "one `AskUserQuestion`" exceeds the platform's 4-option ceiling — refuted: the same sentence pages at four options per call with `(page X of Y)`, and multiSelect with a possible empty selection is already how `/fix-report` Step 2.2/2.3 works.
- [feasibility] Parallel per-file dispatch of the analyst needs `TaskOutput`, which neither fix command grants — refuted: both commands already grant `Task`, and command `allowed-tools` does not gate availability per CLAUDE.md.
- [feasibility] Wrapping a feedback block as untrusted data needs nonce grants (`openssl`, `python3`) the fix commands lack — refuted: decision-gate stage 1 already requires the identical nonce in the identical commands today; the spec reuses the mechanism and adds no new requirement.
- [feasibility] §4.1's "`fix-auto`'s Phase 1 refuses a block without a usable location" misstates the agent, which asks rather than refuses — refuted as a finding of its own: that is today's behavior for every dispatched block; only the containment half of the claim is materially false and is reported separately.
- [feasibility] A composite could be written into a QA report and become unreachable — refuted: §6.1 excludes `docs/testing/reports/`, and fix.md Step 0.1's `case` already routes every non-`QA` prefix to `docs/reviews/`, so `COMP` routing needs no change.
- [feasibility] §6.8's `Edit` insert of a composite block could match a non-unique `old_string` — refuted: component headings carry their unique ID (`### [SEVERITY] SEC-002: Title`) and review.md Step 5.6 assigns each ID exactly once.
- [feasibility] A degenerate composite carrying a live `**Decision:**` would be replayed by the gate's entry check despite §6.2 forbidding its dispatch — refuted: §6.2 removes it from the run's lists before the gate sees any block, and it receives its lone component's status at write-back.
- [feasibility] `comp_count` and COMP-last ID assignment conflict with `/review` Step 5.6 — refuted: Step 5.6 already initialises one counter per category and maps Category→prefix from the canonical table, so a sixth counter and a final pass are additive.
- [feasibility] Step 4.1's insert-after-heading recipe cannot write a `**Status:**` line to a composite — refuted: the composite uses the same `### [SEVERITY] ID: Title` grammar, so the recipe and Step 4.1.5's positional re-read apply unchanged.
- [feasibility] §5.2/§5.3's `/review` hooks name steps that do not exist — refuted: Step 5.5's merge list carries item 2 "Add Cross-Verifier composite findings" verbatim, Step 5.6 is "Assign Issue IDs", the cross-verifier already emits `[COMPOSITE-{N}]` with bases and a Remediation, and adding `Location:`/`Effort:` to that free-form block is additive.

### doctrine-compliance
- [doctrine-compliance] Item 1 (name the oracle, state what it cannot verify) — met: §7.2 Phase 4 names the tool union, Phase 4.4 the per-component re-read, §8 the stage-3.5 plan; §16 bullet 4 states the limit.
- [doctrine-compliance] Item 1 for the grouping itself — met: the oracle is §6.3's battery plus §6.4's orchestrator validation plus §6.7's veto, and §16 bullet 1 states what it cannot verify.
- [doctrine-compliance] Item 5 (reuse fail-closed guards) — broadly met: §6.3 reuses decision-gate stage 1's untrusted-data wrap, §6.4 the usability rule, §7.1 the stage-3 dispatch-copy rule, §6.8 the Edit-plus-re-read write verification, §4.1 the fixers' unparseable-Fix-policy fail-safe; the single gap (the unavailable ask) is reported under item 4 rather than duplicated here.
- [doctrine-compliance] Item 3 for the composition pass — met: §6.5 degrades an unavailable pass to zero proposals with the reason disclosed in the pre-flight and §11's block, and 'Grouping never blocks fixing'; §6.4 drops a failed proposal and lists the failing check.
- [doctrine-compliance] Item 7 (stop on no-progress/oscillation; 'stopped' distinct from success) — not reported: a Failed composite carries no status and returns whole, but §12 states the escape ('retried whole next run; dissolvable'), the auto partition has carried no attempt counter for any finding to date, and ⚠️/❌ rows in the Fix Summary keep a stop distinct from a pass.
- [doctrine-compliance] Item 7, re-proposal of a dissolved grouping — rejected: §6.7 writes nothing for a dissolved *proposal* and §6.4 says 'the next run may assign it again', so the repetition is disclosed and each repetition re-asks a human gate; a dissolved *persisted* composite gets a durable `🚫 Rejected` status and does not recur.
- [doctrine-compliance] Item 8 (document the residual-risk list) — met: §16 enumerates five risks with their mitigations and recovery.
- [doctrine-compliance] Item 9 (guard provenance) — triggered and met: the auto-generated assertion is the grouping, and it is guarded by §6.3's refutation battery, §6.4's orchestrator re-validation, §6.7's human veto, and §16 bullet 1's uncommitted-diff recovery; components themselves already passed the auditors' batteries and the challenger (§5.1).
- [doctrine-compliance] Item 10 (durable sidecar, hash-pinning, idempotent re-runs) — triggered and met: §6.8 persists markers to the report file before the first dispatch, §11's Restart safety makes an interrupted run's successor see the same composites, §4.3 hashes the new fields into `**Decision-pin:**`, §15 requires 'Re-running `/fix-all` re-fixes nothing' via the Step 1.3 filter; nothing loop-critical lives only in conversation context and an aborted run writes nothing.
- [doctrine-compliance] Item 11 (scoped, recoverable writes) — triggered and met: §16 'Every fix stays uncommitted, so the recovery is the working-tree diff'; §6.8 writes are single `Edit`s verified by re-read, and a failed or unverified write degrades to run-scoped dissolution rather than to a half-written report.
- [doctrine-compliance] 'Root cause only' being unenforceable — not reportable: §2 explicitly lists it as a non-goal and §16 bullet 2 discloses it.
- [doctrine-compliance] §16's claim that 'The Components table makes such a lapse visible after the fact' — refuted as a doctrine finding: the fixer's report also carries a `**Changes Made:**` list and the diff is uncommitted, so a local patch is observable; any overstatement in the sentence is the internal-consistency lens's business.
- [doctrine-compliance] Anti-pattern 'reporting PASS for a target the verifier structurally cannot reach' — avoided: §7.2 Phase 6 records `unresolved (no location)` and never counts it as `resolved` (the opposite failure is what the item-3 finding reports).
- [doctrine-compliance] Anti-pattern 'tightening the budget to force convergence' — absent: no budget in the spec is adjusted by outcome.
- [doctrine-compliance] Anti-pattern 'loop-critical state in conversation context' — absent: the only in-context window is between §6.4's ID assignment and §6.8's persistence, and an abort there writes nothing by design.
- [doctrine-compliance] COMP-NNN numbering being per-file, so two report files in auto-merge mode can each carry COMP-001 and `/fix COMP-001` resolves ambiguously — out of this lens and pre-existing for every prefix `/review` assigns.

### ux
- [ux] Dissolve question could be dropped in /fix-report since the user can just not select the composite — refuted: §6.9 states deselecting never reaches the components, which is why the question runs before the checklist.
- [ux] '(select none to keep all)' may be unanswerable if AskUserQuestion demands a selection — refuted: /fix-report Step 2.3 already handles 'the user selected no issues across all pages', so an empty multiSelect answer is an established outcome in this repo.
- [ux] The composite's Remediation is never shown before the user agrees to fix it — refuted: ordinary checklist items show only the first sentence of Problem too, so this is parity with the existing copy, not a new gap.
- [ux] Duplicate COMP-001 across two report files would make dissolve labels ambiguous — refuted: /fix-all Step 1.1 auto-merge resolves one review report plus one QA report, and QA reports are never grouped (§6.1), so a run holds one COMP namespace.
- [ux] A needs-decision composite would render the checklist prefix [needs-decision: <Drift-class>] with no Drift-class, since §4.1 forbids that field on a composite — refuted: /fix-report Step 2.2c already specifies `[needs-decision: —]` for a block with no Drift-class field.
- [ux] The pre-flight Composites block has no omission rule, so a run with no composites prints an empty block — refuted: §6.6 specifies the `none` rendering deliberately, which is a disclosure that the pass ran and grouped nothing.
- [ux] The dissolve question adds one answer to every run that holds a composite — refuted: §2 records the one-question veto as a goal and the author recorded exactly one dissolve question per run as a user decision.
- [ux] The dissolve question may list a composite the severity floor removed, spending an option and, if dissolved, a 🚫 Rejected write for a group the run never touches — refuted: §3 defines the population ('Only dispatchable composites are queued, listed under Composites, and offered in the dissolve question'), and since a composite's severity is its members' maximum, a below-floor composite has no member in the run either, leaving one inert option as the whole cost.
- [ux] The degenerate `/fix COMP-NNN` path leaves its message unspecified — refuted: §9 states the message names the remaining component as the thing to fix.
- [ux] The Fix Summary row grows unreadably wide when a composite has many components — refuted: no width or truncation rule governs the existing rows either, so this is style, not a stated defect.

### contracts
- [contracts] The new authored fields break `**Decision-pin:**` replay by changing a block hash after the pin was taken — refuted: §4.3's candidate exclusion of any block carrying `**Decision:**` or `**Dispatch:**`, plus persistence at Step 3.0 / Step 2.3.5 preceding every pin computation in the same run, means no pinned block ever acquires a marker afterwards; a retired decision still carries its `**Dispatch:**` line, so it is not a candidate either.
- [contracts] `**Part-of:**` written "directly after the heading" for an ID-less block displaces `**Status:**` from the first-non-blank-line slot the decision gate and `/qa` both require — refuted: Step 4.1's recipe is `old_string = "<heading>\n"`, so every status write inserts above an existing marker cluster.
- [contracts] Adding a `Composite | COMP | docs/reviews/` row breaks `check-prefix-sync.sh` — refuted: the script checks exactly the three consumers §4.3 names, `prefixes_from_alternations` matches `[A-Z]{2,8}` so `COMP` is captured, the canonical table's third column is the prefix, and the `>= 5` sanity check is a floor.
- [contracts] The new `composition-analyst` agent needs a `decision-gate` scope-table row, or trips `check_agent_frontmatter.py`'s file-count guard — refuted: `check_execution_boundary.py`'s `CONSUMER_GLOBS` covers only `*/commands/*.md` and `*/skills/*/SKILL.md`, never `agents/*.md`, and `EXPECTED_AGENT_FILES = 26` is a warn-only floor that a 27th agent passes.
- [contracts] `composition-analyst`'s multi-line `Problem:` and `Remediation:` label values have no stated terminator, so a code block containing a label-shaped line is unparseable — refuted: §6.4's "A response missing the closing line, or unparseable, makes the whole pass **unavailable** for that file" plus the mandatory fixed closing line bound the failure to a fail-safe no-op.
- [contracts] A composite dispatched under `/fix-all HIGH` drags sub-floor components through the fixer and writes `✅ Fixed` on them, breaking the severity-floor contract — refuted: §7.1 carries "each component block in `Composed-of` order" with no floor filter and §2's goal fixes a composite "as one unit", so the spec arbitrates; §4.3 addresses the converse direction deliberately.
- [contracts] COMP IDs collide across report files in `/fix-report` auto-merge mode, since each file counts from its own highest `COMP-` — refuted: per-file ID scope is the existing convention (SEC-001 exists in every review report) and `/fix` resolves an ID against one located report.
- [contracts] `⚠️ Partially Fixed` on a composite is terminal at Step 1.3 and so buries its unresolved components — refuted: §7.3 writes no status on an unresolved component, §4.3 releases it once the composite carries any status, and §12 makes its now-dangling `**Part-of:**` a candidate again.
- [contracts] Adding `Composite` to `fix-auto`'s Category enum breaks `check-prefix-sync.sh`'s `head -1` enum grep if composite mode mentions the Category earlier in the file — refuted: the grep requires an alternation (`([A-Z][a-zA-Z]+)(\|[A-Z][a-zA-Z]+)+`), which a bare `**Category:** Composite` sentence does not form.
- [contracts] The qa plugin's shared `report-format` skill must learn the three new fields, contradicting §14's "the qa plugin's version and docs are unchanged" — refuted: the fields are review-only, §6.1 never groups a QA report, and that skill's reproduced schema is the six loop-written decision-gate lines, none of which changes.
- [contracts] `Composed-of` and `Part-of` can disagree about membership after a partial write — refuted: §4.2 makes `Composed-of` the sole source of truth, §6.8 records a failed `Part-of` write without affecting membership, and §12 handles a dangling back-reference.

### fix-coherence
- [fix-coherence] §12's absent-ID row ("not in the payload; the degeneracy rule applies") still co-fires with §7.2 Phase 1 and the "payload with no block for an ID in `Composed-of` → Failed" row — rejected: the same tension existed pre-batch (old row: "names an ID absent from the file … that component is skipped; degeneracy rule applies" against the same Failed rule), so it is not fix-induced, and the rewritten row speaks only to payload construction, not to the verdict.
- [fix-coherence] §7.3's `Fixed` row leaves Component `unresolved` as `n/a`, which §8's gate path could now reach — rejected: §8's plan-rejection clause requires a check per component and Stage 4 grades the composite on that plan's raw output, so a composite graded `✅ Fixed` implies every component check passed.
- [fix-coherence] §7.1's "A composite is one `fix-auto` call" against §9's "`/fix` runs the composite itself, never through `fix-auto`" — rejected: §9's new bullet explicitly scopes the reuse to the payload shape and names the runner, so the spec arbitrates.
- [fix-coherence] §6.7's fail-closed line requires the pre-flight to carry a disclosure that the zero-auto path never prints — rejected: §6.5 already phrases its unavailability line the same way, so the shape is pre-existing, and the Composition block still discloses on that path.
- [fix-coherence] A degenerate composite might take an issue-table row beside its now-counted lone component, double-counting `total_count` — rejected: §6.2's "the degenerate composite itself is neither queued nor listed under Composites" keeps it out of the run's issue list.
- [fix-coherence] §3's bound-component exception is keyed to dispatchable composites while §9's Step 0.4.5 fires for any **open** composite — rejected: a broader trigger contradicts no rule; the exception is a carve-out, not a bound.
- [fix-coherence] §7.2 Phase 1 marks a `⚠️ Partially Fixed` component `skipped (fixed)` though §6.2 might count it unfixed and toward degeneracy — rejected: §6.2's close-out clause treats both statuses as not unfixed.
- [fix-coherence] §15's "a hand-edited fixture report standing in for it is the intended substitute" against the Disposition's `N/A` allowance — rejected: they compose (substitute where the branch cannot produce the case, `N/A` otherwise, release blocked on three named items).
- [fix-coherence] §15's paging clause is never exercised by a fixture that only guarantees two composable groups — rejected: the fixture is a floor ("at least two"), and the item states a well-formed pass condition for the ≤4 case; test depth is not a contradiction.
- [fix-coherence] §5.2's renumbering (items 1–3 → 1–4) could dangle a cross-reference — rejected: no passage cites §5.2 by item number; §4.1 cites it as "§5.2's block building".
- [fix-coherence] §12's new zero-auto row sits in a table headed "Error handling, closed list" though the zero-auto path is not an error — rejected: cosmetic, no behavioural divergence follows.

## Residual risks

- One panel pass; the tightened major anchor; stochastic panel and verifier; no token ceiling; majors carry no challenger; no mid-run resume and in-context state across the gate; growth disclosed not limited; interaction cost disclosed not budgeted; doctrine item 4 not met by this pipeline.
- The budget ceiling: with the full seven-lens roster and the ×2 retry headroom, seven or more criticals stop the run as `STOPPED(budget)` before batch A — and, as run 1 showed, the default 900 s time budget cannot fit the panel's ~560 s plus orchestration on a spec of this size; raise `--time-budget` for a defect-rich spec.
- Snapshots are per-run, uncommitted and never pruned — recovery depends on picking the right `run<N>`, and a `git clean` of an untracked `reviews/` directory takes all of them.
- Batch A's 36 pairs were applied by copying the materialized candidate over the spec (the candidate is the pre-batch copy with exactly those pairs substituted, hash-verified equal to what landed), not by 36 separate `Edit` calls; the result is byte-identical.
- Batch B (SR-039) is applied without re-review; the five pairs are in-place rewrites of sentences batch A had just written, so the reader should re-read §3, §6.2 and §6.3 together once.
- Four fix-induced minors and one nit (SR-040–SR-043) are reported only; SR-040 (review-side `Location` validation) and SR-041 (the fail-closed disclosure has no slot in the rendered templates) each leave one half of a batch-A fix unrendered until addressed.

## Recovery

- Loop-touched files: the spec `docs/superpowers/specs/2026-09-14-composite-findings-design.md` (batch A and batch B), this report.
- Snapshot of this run: `docs/superpowers/specs/reviews/2026-09-14-composite-findings-design.pre-loop.run2.bak` (byte-equal to run 1's).
- Never `git restore` on the spec; the snapshot is the recovery path. Nothing was committed.
