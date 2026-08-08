# Test Oracle, Exit Code and Bite-Test Integrity

## Purpose

A test result is useful only if the agent is reading the status of the **test process itself** and has evidence that the newly added assertion can actually fail.

A green-looking command is not proof of a green test.

## Core rules

```text
DISPLAY PIPELINE EXIT CODE != TEST EXIT CODE
TEST THAT NEVER BITES != VERIFIED REGRESSION TEST
PROCESS CRASH != ASSERTION FAILURE
```

## 1. Never lose the real exit status

Unsafe shell pattern:

```bash
./ModelTests.exe 2>&1 | tail -20
echo $?
```

Without `pipefail`, `$?` is normally the status of `tail`, not the test executable.

Preferred patterns:

```bash
./ModelTests.exe >test.out 2>test.err
status=$?
tail -20 test.out
tail -20 test.err
exit $status
```

or, when supported:

```bash
set -o pipefail
./ModelTests.exe 2>&1 | tail -20
status=$?
```

Better still, invoke the test process directly through a subprocess/tool API that returns its own exit code.

## 2. Classify the result

Use explicit states:

```text
PASS
ASSERTION_FAIL
LOAD_FAIL
BUILD_FAIL
CRASH
TIMEOUT
UNKNOWN
```

Do not interpret a non-zero code as a valid bite test until output shows the intended assertion failed.

Example:
- expected triangle count intentionally changed;
- process exits 1;
- stderr contains the exact bollard regression message;
- restore correct expectation;
- rebuild;
- process exits 0.

That is a valid bite test.

An `abort()`/CRT crash with exit 3 is **not** proof that the assertion bites.

## 3. Bite-test protocol

When adding a new engine/project regression assertion, perform one controlled negative proof when practical:

```text
GREEN BASELINE
-> controlled mutation of one expected value or fixture
-> rebuild only affected test target
-> run test
-> verify intended assertion fails with readable diagnostic
-> restore mutation
-> rebuild
-> verify clean PASS
```

The mutation must be:
- narrow;
- reversible;
- owned by the agent;
- never left committed;
- not destructive to production assets.

Do not run a bite test if the mutation would be unsafe or expensive; record `BITE_TEST_NOT_SAFE` instead.

## 4. Non-interactive failure requirement

Automated tests used by an agent must fail through machine-readable output/exit state rather than modal dialogs where possible.

Asset loading in a test should surface exceptions as a readable test failure. A modal CRT/error dialog that blocks automation is a test infrastructure defect.

## 5. Build/test target reuse

Before inventing commands:
1. read active Project Asset Pipeline Profile;
2. use the known build directory/configuration;
3. build the narrow test target;
4. run the known executable/test selector;
5. capture the real exit code.

Do not rediscover CMake presets, binaries and test locations every asset.

## Compact report

```yaml
test_oracle:
  build_target: ModelTests
  build_status: PASS
  command_mode: DIRECT_PROCESS
  exit_code: 0
  stderr_tail: ""
  bite_test:
    performed: true
    mutated_expectation: triangle_count_lod0
    failing_exit_code: 1
    expected_failure_message_seen: true
    restored_and_green: true
  status: PASS
```

## Completion impact

`PIPELINE_INTEGRATED` must not accept a runtime test result whose process exit status is ambiguous.

If the agent used a shell pipeline and cannot prove the executable's status:

```text
ENGINE_TEST_STATUS = UNVERIFIED
```

Rerun the test correctly; do not mark Level D PASS from the ambiguous invocation.