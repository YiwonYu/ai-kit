# Plan

## Problem
- Goal:
- Input:
- Output:
- Constraints:
- Metric:

## Blocks

- [ ] [Web](blocks/web/BLOCK.md) — worker/admin views
  - [ ] [Login](blocks/web/login/SUB_BLOCK.md) — credentials; session
  - [ ] [Admin](blocks/web/admin/SUB_BLOCK.md) — CSV upload; all routes
  - [ ] [Worker](blocks/web/worker/SUB_BLOCK.md) — assigned route
- [ ] [Routing](blocks/routing/BLOCK.md) — calculate bus routes
  - [ ] [Data checks](blocks/routing/data-checks/SUB_BLOCK.md) — check coordinates and worker coverage
  - [ ] [Nearest stop](blocks/routing/nearest-stop/SUB_BLOCK.md) — assign the nearest stop
  - [ ] [Capacity-aware](blocks/routing/capacity-aware/SUB_BLOCK.md) — group workers within bus capacity
  - [ ] [Selected route](blocks/routing/selected-route/SUB_BLOCK.md) — save selected routes
- [ ] [Database](blocks/database/BLOCK.md) — store source records
  - [ ] [CSV import](blocks/database/csv-import/SUB_BLOCK.md) — validation; transaction
- [ ] [API](blocks/api/BLOCK.md) — access; export
  - [ ] [Login](blocks/api/login/SUB_BLOCK.md) — authentication
  - [ ] [Admin routes](blocks/api/admin-routes/SUB_BLOCK.md) — all routes
  - [ ] [Worker route](blocks/api/worker-route/SUB_BLOCK.md) — own route
  - [ ] [JSON export](blocks/api/json-export/SUB_BLOCK.md) — route schema

Example tree: replace for actual problem. Create every linked block/sub-block document during planning. All boxes initially unchecked.

## Execution
- Dependencies:
- Current block / sub-block:
- Completion / stop condition:
- Plan version / user approval / approved scope:
- Next action / approval point:
