# Plan

## Problem
- Goal:
- Input:
- Output:
- Constraints:
- Metric:

## Blocks

- [ ] [Web](blocks/web/BLOCK.md) — user views
  - [ ] [Login form](blocks/web/login-form/SUB_BLOCK.md) — show credentials form
  - [ ] [Login input checks](blocks/web/login-input/SUB_BLOCK.md) — show field errors
  - [ ] [CSV upload](blocks/web/csv-upload/SUB_BLOCK.md) — send roster file
  - [ ] [Admin route list](blocks/web/admin-list/SUB_BLOCK.md) — show all routes
  - [ ] [Worker route view](blocks/web/worker-view/SUB_BLOCK.md) — show assigned route
- [ ] [Routing](blocks/routing/BLOCK.md) — calculate bus routes
  - [ ] [Coordinate checks](blocks/routing/coordinates/SUB_BLOCK.md) — reject invalid coordinates
  - [ ] [Stop candidates](blocks/routing/stop-candidates/SUB_BLOCK.md) — find walkable stops
  - [ ] [Baseline assignment](blocks/routing/baseline/SUB_BLOCK.md) — assign nearest stop
  - [ ] [Capacity grouping](blocks/routing/capacity/SUB_BLOCK.md) — enforce passenger limit
  - [ ] [Stop ordering](blocks/routing/stop-order/SUB_BLOCK.md) — compare visit sequences
  - [ ] [Route audit](blocks/routing/audit/SUB_BLOCK.md) — check assignment constraints
  - [ ] [Route save](blocks/routing/save/SUB_BLOCK.md) — store selected routes
- [ ] [Database](blocks/database/BLOCK.md) — import source records
  - [ ] [CSV headers](blocks/database/headers/SUB_BLOCK.md) — check required columns
  - [ ] [CSV row values](blocks/database/row-values/SUB_BLOCK.md) — check required fields
  - [ ] [Worker identity](blocks/database/identity/SUB_BLOCK.md) — detect duplicate identifiers
  - [ ] [Record mapping](blocks/database/mapping/SUB_BLOCK.md) — map source fields
  - [ ] [Import transaction](blocks/database/transaction/SUB_BLOCK.md) — save or roll back
- [ ] [API](blocks/api/BLOCK.md) — access and export
  - [ ] [Credential lookup](blocks/api/credential-lookup/SUB_BLOCK.md) — find account
  - [ ] [Password verification](blocks/api/password-check/SUB_BLOCK.md) — verify password
  - [ ] [Session creation](blocks/api/session/SUB_BLOCK.md) — issue session
  - [ ] [Logout](blocks/api/logout/SUB_BLOCK.md) — invalidate session
  - [ ] [Admin access](blocks/api/admin-access/SUB_BLOCK.md) — enforce admin role
  - [ ] [Worker access](blocks/api/worker-access/SUB_BLOCK.md) — restrict own records
  - [ ] [JSON export](blocks/api/json-export/SUB_BLOCK.md) — serialize approved schema

Example only. Match the actual problem. Add missing behaviors and split remaining bundles. Create one document per linked block/sub-block. All boxes initially unchecked.

## Execution
- Dependency order:
- Current block / sub-block:
- Plan version / actual approval / approved scope:
- Current review point:
- Next action / permission:

Each sub-block: detailed contract, files/functions, steps, method, checks and acceptance. Default: implement one sub-block; show evidence; wait for user review. Grouped approval: report each result separately.
