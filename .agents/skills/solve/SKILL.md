---
name: solve
description: Plan research or service tasks as blocks and sub-blocks; wait for approval; implement, verify, update checklists and commit each approved scope.
---

# Solve

## Setup
- Read README.md, AGENTS.md, Prob.md and existing code.
- Target: Prob.md parent or user-specified folder.
- Separate target: preserve root guidance; add original kit rule/Skill links and a local solve wrapper with actual relative paths. Avoid duplicate links, overwrites and self-reference.
- Keep kit scripts/templates/.git in place. Commands: explicit target cwd and kit paths.
- Initial setup: guidance and planning documents only.

## Plan
- templates/PLAN.md: short problem summary, full block/sub-block tree, dependency order, scope, approval.
- templates/BLOCK.md and SUB_BLOCK.md: one document per block/sub-block, descriptive folder names.
- Decompose every feature into the smallest independently testable behavior. One folder/document per sub-block; link each in PLAN and its BLOCK.
- Before implementation: exact files/functions, typed inputs, output/error contract, ordered steps, test data, expected values and acceptance checklist. Explain algorithm choices and verification procedures in detail.
- If a planned sub-block still bundles independent behaviors, split it and present the revised scope before execution.
- Each feature: separate task and check lists. One verb-led action per checkbox.
- Replace abstract labels with concrete objects and expected outputs. Use AGENTS.md writing rules.
- Include method, alternatives, data contracts, tests, expected results and completion criteria.
- Functional hierarchy and execution order: separate. Example: web block can appear first while database/API dependencies run first.
- Needed harness and project checks: propose in relevant block documents.
- Present plan; stop for user review and explicit approval.

## Approved scope
1. Present the detailed current sub-block plan, tasks and tests. Resolve open decisions; confirm the applicable user approval.
2. Implement approved checklist items; purpose/Args/Returns docstring per function.
3. Test normal/error/boundary paths against independent expected values. Add regression and actual integration checks.
4. Execute runner/verification pipeline; keep original evidence under runs/.
5. Update the same block/sub-block document: implementation ticks, verification ticks, command, fixture, expected/actual result, logs, code revision, next action.
6. Alternative methods: local method/performance tables. Selection/rejection reasons: same relevant document.
7. Parent checklist: update after child and integration completion. PLAN: current summary only.
8. Commit relevant code/tests/block documents. Report this sub-block: changed behavior, test results, inspection command and next part. Default: stop for user review; grouped approval: continue only within that scope.

## Continuity
- Read PLAN and active block documents; inspect real code/logs/Git.
- Plan changes: update affected blocks; obtain approval for changed scope.
- No separate handoff, submission, method, decision or experiment documents.
- Short English labels; method and verification details sufficient for reproduction.
