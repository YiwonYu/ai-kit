# Workflow

## Plan
- Read problem, source, environment, rules.
- Short English phrases in Markdown. Detailed method and verification where needed.
- PLAN.md: problem; named block/sub-block tree; dependencies; current approval.
- Each block: blocks/<name>/BLOCK.md. Each sub-block: blocks/<name>/<name>/SUB_BLOCK.md.
- Before approval: read-only inspection, root guidance/Skill connections, planning documents.
- Present plan; wait for explicit approval. Revisions: update plan, then approval.
- Default scope: one sub-block. Explicit multi-block approval: that scope only.
- Significant goal, structure, data, metric changes: revised plan and approval.

- Progress: user commands and approved scope. No time allocation, timed stages or submission phase.

## Blocks
- Each document: concrete implementation and verification checkboxes.
- Before work: purpose, inputs/outputs, tasks, method and expected tests.
- During work: tick completed tasks; attach commands, observed results, code/config/fixture references.
- Verification ticks: actual passing results only. Failures/pending: local status plus next action.
- Parent completion: child implementation/verification plus block integration tests.
- Algorithm alternatives: relevant routing/research block; descriptive method names, method/performance tables; detailed comparison inside child documents.
- Selected/rejected approach and reason: relevant block document. History: Git.
- Current state updates. No dated appendices or abbreviation-only descriptions.
- No separate HANDOFF.md, SUBMISSION.md, METHOD.md, DECISION.md or EXPERIMENTS.md.
- Existing projects: preserve evidence; consolidate legacy documents with user authorization.

## Code
- Every function: leading triple-single-quoted docstring; purpose, Args, Returns. Include exceptions/side effects when relevant.
- Existing source layout: reuse. New paths: agree in PLAN/block documents and structure checks.
- APIs/DB/web contracts: explicit inputs, outputs, errors, fixtures.

## Verification
- Approved checks: verification.json; requirement-to-check mapping; independent expected values.
- Structure, unit, integration, e2e, error and boundary checks as applicable.
- Tests and block documents: same feature names and reproducible commands.
- After approved changes: run relevant checks; before block completion: integration and regression checks.
- Required failure, pending or timeout: incomplete verification checkbox.
- Logs: unique run paths; config, seed, code revision, dirty state, elapsed time.
- Real vs mocked dependencies: label. Secrets: environment variables; redact outputs. Test DB: isolated.

## Git and continuity
- Actual target repository: inspect root/status; preserve user changes. Keep kit repository separate when nested.
- Approved plan; sub-block code/tests/docs: local commits. Stage explicit paths; review staged diff.
- No secrets, sensitive data, weights or large logs in commits. Push only when requested.
- Report completed commit; reference previous code revisions in documents. No self-hash requirement.
- New session: PLAN → current BLOCK → current SUB_BLOCK → tests/logs/Git as needed.
- End of scope: update checklists; report result/tests/commit/next action; wait for next approval.
- Reports: brief current results. Actual failures/pending conditions: once, beside affected feature.
- Parallel agents: only on explicit request.
