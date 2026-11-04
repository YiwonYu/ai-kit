# Single behavior

## Goal
- Observable behavior:
- Parent block:
- Dependencies:
- Approved scope:
- Open decisions:

One independently testable behavior per document. Split separate responsibilities into sibling sub-blocks before implementation. Replace every placeholder with concrete project details.

## Contract
| Item | Definition |
|---|---|
| Input | Field names; types; units; valid ranges |
| Output | Fields; types; ordering; example |
| Errors | Trigger; error code; response |
| State | Records/files changed; preserved values |

## Files
| File | Function / interface | Planned change |
|---|---|---|

## Steps
- [ ] Define the input contract
- [ ] Write an independent expected-output fixture
- [ ] Implement the single behavior
- [ ] Handle its specified error paths
- [ ] Add purpose/Args/Returns function docstrings
- [ ] Run the named checks
- [ ] Inspect the observable output

Replace generic steps with exact implementation actions. One action per checkbox. Explain processing order, intermediate values and state changes below.

## Method
1. Describe the input transformation.
2. Explain the processing steps and intermediate values.
3. State formulas, parameters and selection criteria.
4. Explain the result and error paths.
5. Explain the chosen approach and meaningful alternatives.

Include source/config references and an example with concrete values. Separate approved policy from assumptions. Keep enough detail to reproduce the implementation.

## Checks
- [ ] Verify the valid-input result
- [ ] Verify the missing/invalid-input response
- [ ] Verify the relevant boundary
- [ ] Verify state preservation on failure
- [ ] Verify the dependent interface

Replace each generic check with an actual input and expected outcome. Use only applicable cases; explain exclusions briefly.

| Case | Fixture / input | Independent expected result | Command | Actual / evidence | Status |
|---|---|---|---|---|---|

Describe fixture construction, oracle calculation and real/mocked dependencies. Explain execution and inspection steps. Record code/config revision and logs after execution. Failed or pending checks stay unchecked.

## Acceptance
- [ ] Implementation steps complete
- [ ] Required checks pass
- [ ] Output matches the contract
- [ ] Parent checklist updated
- [ ] Review evidence ready

## Review
- Changed behavior:
- Inspect / reproduce:
- Test result / evidence:
- Failure / pending:
- Code revision / run links:
- Next sub-block:
- User review / permission:
