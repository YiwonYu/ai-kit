# AI Kit

Codex workflow. Python 3.10+. Standard library.

## Start

```bash
git clone https://github.com/YiwonYu/ai-kit.git
cd ai-kit
# Save the problem as Prob.md
codex
```

```text
Read README.md and Prob.md, then proceed.
```

Subfolder setup:

```text
Read ai-kit/README.md and Prob.md, then proceed.
```

## Entry instructions

1. Read Prob.md. Target: its parent folder, unless specified.
2. Locate this kit: AGENTS.md, .agents/skills/solve/SKILL.md, scripts/, templates/.
3. Read AGENTS.md and the solve Skill directly.
4. Separate target: merge a short root AGENTS.md reference to the original rules and Skill. Add a local solve wrapper referencing their actual paths. Preserve existing files; report conflicting Skills. Same target: reuse existing files. Keep kit scripts and .git in place.
5. Create PLAN.md and block/sub-block planning documents. Existing project: update current documents.
6. Present problem, structure, method, checks and dependencies. Wait for explicit approval.
7. Approved scope: implement, test, update checkboxes, commit, report. Next scope: approval.

Progress: user commands, approved scope, dependencies, completion criteria. No timed plan or submission phase.

Initial setup: guidance, Skill links, planning documents. Project code, test configuration, installs, execution: after plan approval.

## Layout

```text
PLAN.md
blocks/
  web/
    BLOCK.md
    login/SUB_BLOCK.md
    admin/SUB_BLOCK.md
    worker/SUB_BLOCK.md
  routing/
    BLOCK.md
    data-checks/SUB_BLOCK.md
    nearest-stop/SUB_BLOCK.md
    capacity-aware/SUB_BLOCK.md
    selected-route/SUB_BLOCK.md
  database/
    BLOCK.md
    csv-import/SUB_BLOCK.md
  api/
    BLOCK.md
    login/SUB_BLOCK.md
    admin-routes/SUB_BLOCK.md
    worker-route/SUB_BLOCK.md
    json-export/SUB_BLOCK.md
tests/
verification.json
runs/
```

Illustration only. Match the actual problem. Existing source layout: reuse.

| File | Content |
|---|---|
| PLAN.md | Problem; block tree; dependencies; approval; next step |
| BLOCK.md | Purpose; feature checklist; child links; integration checks |
| SUB_BLOCK.md | Detailed checklist; method; tests; evidence; current choice |
| verification.json | Requirements; automatic checks; structure |
| runs/ | Original execution evidence; Git-excluded |

Short English phrases. Descriptive names. Current state updates. Method and verification: enough detail for reproduction. History: Git. No separate HANDOFF, SUBMISSION, METHOD, DECISION or EXPERIMENTS documents.

## Checkboxes

- [ ] Implementation: concrete output
- [ ] Verification: expected result; test command

Mark implementation after code inspection/execution; mark verification after observed passing results. Parent completion: child checks plus integration checks. Record failures and pending checks beside the affected feature. Store comparisons inside the relevant block: method table; performance table.

## Functions

Every function, including nested helpers and tests: leading triple-single-quoted docstring.

```python
def route_for_worker(worker_id, routes):
    '''Find a worker's assigned route.

    Args:
        worker_id: Unique worker identifier.
        routes: Mapping from worker identifiers to routes.
    Returns:
        Assigned route, or None when unassigned.
    '''
    return routes.get(worker_id)
```

## Execution

```bash
python scripts/run_experiment.py --name baseline --timeout 30 --seed 42 -- python examples/demo.py --mode success
python scripts/verify_pipeline.py --config verification.json
```

Root verification.json: kit checks. Project configuration: templates/verification.json; replace pending checks after approval. Checks: structure, unit, integration, e2e, negative, boundary. Requirements map to required checks. Pending, timeout, required failure: gate failure. Reports: runs/verification/<run>/report.md and report.json; config snapshot; original logs.

Runner exits: success 0; child failure 1; launch failure 2; timeout 124; interrupt 130. Verification exits: pass 0; failed/blocked 1; invalid config 2; interrupt 130. HARNESS_SEED: application must apply it. POSIX: process-group termination; Windows: direct child. Detached sessions: separate management.

Logs include commands and output: keep secrets in environment variables and out of output. Tests: isolated fixtures and temporary databases. Record real vs mocked dependencies.

## Git

Approved plan commit. One meaningful commit per completed sub-block or approved group. Stage specific paths; inspect diff; preserve user edits. Code revision and evidence links in block documents. No automatic push. Existing project data and logs: preserve.

CI: Python 3.10/3.12; verification reports retained 14 days.

## Reports

Current result → feature/check status → next action. Brief phrases. Detailed method and verification links in block documents.
