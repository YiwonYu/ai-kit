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
- Each feature: detailed implementation checklist and separate verification checklist.
- Include method, alternatives, data contracts, tests, expected results and completion criteria.
- Functional hierarchy and execution order: separate. Example: web block can appear first while database/API dependencies run first.
- Needed harness and project checks: propose in relevant block documents.
- Present plan; stop for user review and explicit approval.

## Approved scope
1. Announce current sub-block, tasks, tests.
2. Implement approved checklist items; purpose/Args/Returns docstring per function.
3. Test normal/error/boundary paths against independent expected values. Add regression and actual integration checks.
4. Execute runner/verification pipeline; keep original evidence under runs/.
5. Update the same block/sub-block document: implementation ticks, verification ticks, command, fixture, expected/actual result, logs, code revision, next action.
6. Alternative methods: local method/performance tables. Selection/rejection reasons: same relevant document.
7. Parent checklist: update after child and integration completion. PLAN: current summary only.
8. Commit relevant code/tests/block documents; report results and commit. Stop when approved scope ends.

## Continuity
- Read PLAN and active block documents; inspect real code/logs/Git.
- Plan changes: update affected blocks; obtain approval for changed scope.
- No separate handoff, submission, method, decision or experiment documents.
- Short English labels; method and verification details sufficient for reproduction.
