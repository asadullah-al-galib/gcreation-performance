# P1 diagnostic instrumentation exception — Stage 1 source review only

Status: **PASS_REVIEW_READY / HUMAN REVIEW REQUIRED**. Orchestrator **HARD_BLOCKED**, P1 **BLOCKED**. This is **P1_DIAGNOSTIC_INSTRUMENTATION_EXCEPTION_STAGE1**, not REPAIR_3 or a repair-budget extension. Human authorization text is preserved in AUTHORIZATION.txt with CRLF normalized to LF. REVIEW.json records both input and stored SHA256 identities. Local static review does not grant independent human acceptance.

## Exact source identities

- Baseline: `9c1adb0884e9f88ca8771f8ddb0f5fa0c93f8fae`.
- Candidate source commit: `b060ff430854046df7490875ac402d9df909b43a`; parent `9c1adb0884e9f88ca8771f8ddb0f5fa0c93f8fae`.
- Old installed controller SHA256 (prior operator evidence): `029c5d5714a13fbdd3565901bdc08341e36319c1ab90cf30ea6d4ab7e58c4039`.
- Repository candidate controller SHA256: `be656cc95fbc3d1df09c57852577f8343401916a47aeec2b12459b4be5de414f`.
- Candidate test SHA256: `f00f54d3e61a00467bbbf4d06c7b28b883fd5b398274371921829a91be7bd8d3`.
- Exact controller patch (zero context): CONTROLLER.patch; SHA256 `4f53e0eab880adc19660eacaf91801b76ece6eed0a46b9469c8b5152aea24f0b`.
- Accepted application source remains `0ac34ba50ab3192abfe2ae425c4283879484258e`; archive SHA256 remains `958c6833da7e63d7843996a3171e540bf74b6978dcdfaf521c1eb55a39587ced`.

The source candidate commit changes only ops/dev/deploy_controller.py and tests/test_controller_health_diagnostics.py. A separate evidence/checkpoint commit records this report and the source commit, avoiding a self-referencing Git identity. No diagnostic deployment archive exists or is authorized. This candidate is NOT INSTALLED, NOT RUNTIME-VALIDATED, NOT DEPLOYMENT-AUTHORIZED and NOT ACCEPTED AS HOST CONTROLLER. Installed controller unchanged by this task; its hash was not freshly read from the protected host path.

## Minimal controller change

Add standard-library socket/urllib.error imports and one best-effort emit_health_diagnostic helper. Wrap the existing two sequential health predicates to emit one PASS/FAIL event after each completed predicate; failures use bare raise to preserve the original exception object. The first failure never runs the homepage check. Existing controller-generated RuntimeError messages, JSON parsing order, response context exits, NoRedirect, endpoints and timeouts remain equivalent. Readiness labels its same 30 attempts, numbered 1–30. The existing no-argument final health call uses default final-health/null. No Docker/network/build/rollback/retention/root guard logic changes.

No str(error), repr(error), arbitrary exception class name, traceback, response/header/body/JSON/service/environment content, URL/query, credentials or env data is emitted. HTTPError.code is accepted only as a plain integer 100–599, otherwise null. Class labels are hard-coded base families; unknown classes map to Exception. URL errors use only a timeout type check on their reason, never its string. Logger validation/serialization/time/print exceptions are swallowed; the original health result remains authoritative.

## Diagnostic schema and bounds

Fixed prefix: `GCREATION_HEALTH_DIAG ` followed by compact sorted JSON with exactly:

```json
{
  "event": "gcreation_health_diagnostic",
  "timestamp_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "phase": "readiness|final-health",
  "attempt": "1..30|null",
  "predicate": "LOCALHOST_ENGINE_HEALTH|DEV_HOMEPAGE_HEALTH",
  "result": "PASS|FAIL",
  "http_status": "100..599|null",
  "exception_class": "fixed base family|null",
  "reason": "closed reason"
}
```

The schema above describes types; REVIEW.json lists the exact allowed values. Reasons: OK, HTTP_ERROR, TIMEOUT, URL_ERROR, INVALID_JSON, IDENTITY_MISMATCH, NON_200_STATUS, NETWORK_OR_OS_ERROR, UNEXPECTED_EXCEPTION. Exception labels: HTTPError, TimeoutError, socket.timeout, URLError, JSONDecodeError, OSError, RuntimeError, AttributeError, TypeError, ValueError, Exception; all under 64 characters, or null.

UTC uses time.gmtime()/strftime(), compatible with the tested Python 3.6.8. No fromisoformat or dependency addition. Invalid JSON can retain null status because parsing still precedes the original status read. Malformed diagnostic context is omitted, not serialized.

Maximum per readiness invocation: **60 events** (30 attempts × two predicates). Final health: **2 events**. Existing deploy failure handling can invoke one rollback start_runtime: up to another 60 readiness events. **Maximum added events per deploy invocation: 122; 512 bytes per event including newline; 62464 bytes total.** The unchanged rollback readiness uses the same phase/range; no new retry layer is added. Events use the existing service StandardOutput=journal path. No persistent diagnostic file/database or privileged writable directory is introduced. No host journal settings changed.

## Tests and local static security review

Every health socket is mocked in the new regressions; unexpected socket/subprocess execution is rejected. No installed controller, real health endpoint, official deployment controller entrypoint or privileged runtime action was executed.

| Command                                                     | Tests | Result        |
| ----------------------------------------------------------- | ----- | ------------- |
| `python3 -B tests/test_controller_health_diagnostics.py -v` | 22    | PASS / exit 0 |
| `python3 -B tests/test_deployment_kit.py`                   | 12    | PASS / exit 0 |
| `python3 -B tests/test_security_review_v3.py`               | 21    | PASS / exit 0 |
| `python3 -B tests/test_security_review_v4.py`               | 13    | PASS / exit 0 |
| `python3 -B tests/test_source_permissions.py`               | 3     | PASS / exit 0 |
| `python3 -B tests/test_installer_bytecode.py`               | 4     | PASS / exit 0 |

**75 tests PASS.** The 22 new tests cover connection/identity/non200/redirect/timeout/JSON/context failures, both-pass and final-health success, exact exception rethrow, logger output/clock/serialization failure, attempts/sleeps/deadline/early stop, journal bound and information disclosure. The 53 existing tests cover deployment/V3/V4 trust, archive/dependency, source permissions and no-bytecode regressions. Synthetic ordinary-user fixture archives from those tests are not deployment artifacts.

In-memory AST/compile checks on Python 3.6.8 PASS. Removing only diagnostic statements and attribution edits yields the baseline health/start_runtime AST; every other source function/class, import/constant except the two new standard-library imports, and root entrypoint remains AST-identical. Whitespace check `scripts/repo-git.sh diff --check` PASS. No Python formatter is configured; no dependency/format configuration changed.

| #   | Required assessment                          | Result | Evidence / disposition                                                                                                                                                         |
| --- | -------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | health semantics changed?                    | PASS   | NO: normalized health AST equals baseline; predicate order/identity/status/exception regressions PASS.                                                                         |
| 2   | retry semantics changed?                     | PASS   | NO: 30 attempts, 2-second failed-attempt sleeps, original outer deadline unchanged; readiness regressions PASS.                                                                |
| 3   | timeout changed?                             | PASS   | NO: fixed localhost 10s and homepage 15s unchanged; mocked exact calls checked.                                                                                                |
| 4   | redirect behavior changed?                   | PASS   | NO: NoRedirect byte/AST logic unchanged; real urllib redirect dispatch tested for 301/302/303/307/308 without sockets.                                                         |
| 5   | security boundary changed?                   | PASS   | NO: enforcement model unchanged; all other controller functions/classes/entrypoint and source constants AST-identical; frozen files untouched.                                 |
| 6   | new filesystem write introduced?             | PASS   | NO: emitter calls only fixed serialization/time/type checks/print; existing journal stdout path used, no host evidence file/directory.                                         |
| 7   | new network operation introduced?            | PASS   | NO: the same two existing fixed HTTP operations/order are retained; no fallback or probe performed.                                                                            |
| 8   | Docker behavior changed?                     | PASS   | NO: start_runtime AST identical after only retry-attribution normalization; other Docker/build/network functions unchanged.                                                    |
| 9   | secret/env access changed?                   | PASS   | NO: no added env/file/header/body access; received JSON used only by unchanged acceptance predicate.                                                                           |
| 10  | raw exception leakage possible?              | PASS   | NO added diagnostic leakage: fixed base-family labels and closed reasons; no str/repr/traceback/type(error).**name** in emitter; opaque/custom-class sentinels PASS.           |
| 11  | response body leakage possible?              | PASS   | NO: no body, parsed JSON, service/environment values or headers appear in event; body/header/query/env sentinel tests PASS.                                                    |
| 12  | journal volume bounded?                      | PASS   | YES: <=60 events per readiness call, <=2 final-health, <=60 existing rollback readiness; <=122 per deploy invocation, <=512 bytes/event including newline, <=62464 bytes.      |
| 13  | attempt range bounded?                       | PASS   | YES: exactly 1–30; invalid/bool/out-of-range attribution rejected; final-health attempt=null.                                                                                  |
| 14  | diagnostic logger can break health behavior? | PASS   | NO for ordinary Exception failures: helper is best-effort; output/clock/serialization failures preserve original health success/error object.                                  |
| 15  | Python compatibility preserved?              | PASS   | YES: all 75 relevant tests ran on Python 3.6.8; UTC time.gmtime/strftime; no fromisoformat or new dependency.                                                                  |
| 16  | final-health behavior preserved?             | PASS   | YES: deploy final health call AST unchanged; default phase final-health/attempt=null; identical predicates.                                                                    |
| 17  | production behavior touched?                 | PASS   | NO: no production/runtime action; remote main read-only identity unchanged at c724ac3b50bc44d71f8620bb4ac0cccfae890de2.                                                        |
| 18  | installed controller touched?                | PASS   | NO: only repository candidate changed; no installed-path read/write/refresh or privileged action. Old installed hash is prior attested evidence, not a fresh host measurement. |

Static review is Codex local assessment. Human/independent acceptance remains REQUIRED. No HOLD criterion is present in the local source review. Frozen V4 enforcement boundaries and every unrelated tracked file remain unchanged.

## Exact changed files since baseline

- `.ops/ACTION_REQUIRED.md`
- `.ops/ORCHESTRATOR_STATUS.json`
- `.ops/PROJECT_STATE.md`
- `.ops/PROJECT_STATUS.md`
- `.ops/oversight/LATEST_CHECKPOINT.json`
- `.ops/oversight/LATEST_CHECKPOINT.md`
- `.ops/oversight/events/0018-P1-diagnostic-instrumentation-stage1.json`
- `.ops/reports/P1/CHECKSUMS.sha256`
- `.ops/reports/P1/EVIDENCE.json`
- `.ops/reports/P1/REPORT.md`
- `.ops/reports/P1/diagnostic-instrumentation-stage1/AUTHORIZATION.txt`
- `.ops/reports/P1/diagnostic-instrumentation-stage1/CHECKSUMS.sha256`
- `.ops/reports/P1/diagnostic-instrumentation-stage1/CONTROLLER.patch`
- `.ops/reports/P1/diagnostic-instrumentation-stage1/REPORT.md`
- `.ops/reports/P1/diagnostic-instrumentation-stage1/REVIEW.json`
- `ops/dev/deploy_controller.py`
- `tests/test_controller_health_diagnostics.py`

Only the first source commit changes functional source/tests; the recording commit changes .ops evidence/status/checkpoint documents. Original failure/review/handoff files and oversight events 0017 and earlier are preserved byte-for-byte. Product/business documentation, application/runtime sources, dependencies, immutable image inputs, privileged installer/preflight, gateway and service units are untouched.

## State and stop

INITIAL failed/consumed; REPAIR_1 failed/consumed 1/1; REPAIR_2 failed/consumed 1/1. repair_cycle=2; failed repair cycles=2; automatic retries=0; repair budget exhausted. Full P1 independent review PENDING; P2–P7 NOT_STARTED. Historical root cause and failed predicate remain NOT_ESTABLISHED. No production/main/runtime/installed controller changes. main read-only identity: `c724ac3b50bc44d71f8620bb4ac0cccfae890de2`.

HUMAN REVIEW REQUIRED: decide whether to accept the instrumentation candidate and separately authorize any future controller installation / diagnostic execution. No installation procedure or Stage 2 authority is prepared.

Stage 1 authority is consumed for source review only. No root execution recipe, installation/refresh, runtime diagnostic execution, Stage 2 authorization, deployment request, retry, REPAIR_3, budget extension/reset, image action, cleanup or P2 is prepared or performed. **NO CONTROLLER INSTALLATION, RUNTIME EXECUTION, REPAIR OR DEPLOYMENT IS AUTHORIZED.**
