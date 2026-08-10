# Runtime Verification Prompt

Version: 0.18.0
Status: CURRENT PROMPT

When a task depends on Blender providers, do not infer capability from installation, documentation or familiarity.

Execution order:

1. read `_RUNTIME_INDEX.json`;
2. inspect current Blender runtime without executing provider code;
3. normalize discovered providers through the canonical provider registry;
4. resolve expected-provider constraints;
5. run only the capability probes needed for the task;
6. evaluate Blender compatibility, requested domain, license policy and quality independently;
7. preserve rejected and blocked candidates in the selection report;
8. select an eligible provider only after all stronger relevant candidates have evidence;
9. permit custom/native fallback only when no eligible stronger provider remains;
10. execute the task and run postcondition, geometry, visual and runtime QA.

Never translate `DISCOVERED` into `PASS`. Never translate an unknown add-on into `UTILITY`. Never hide a provider merely because its quality or domain gate rejected it.
