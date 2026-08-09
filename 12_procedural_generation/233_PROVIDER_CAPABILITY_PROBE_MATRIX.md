# Provider Capability Probe Matrix

## Separation

For every relevant provider keep these states independent:

```text
discovered/enabled
runtime execution probe
requested-domain support
quality tier
license/use policy
selection result
```

A provider may therefore be:

```yaml
provider_id: sapling_tree_gen
discovered: true
enabled: true
runtime_probe_status: PASS
domain_match: false
quality_tier: B
selection: REJECTED
reason: REQUESTED_DOMAIN_GRASS_NOT_SUPPORTED
```

That provider still appears in the final report.

## Probe requirements

A production-capable probe should verify, where applicable:
- expected Python module/operator/API symbol exists;
- required context can be satisfied;
- minimal disposable operation can execute;
- output type is valid;
- deterministic seed behavior when claimed;
- cleanup succeeds.

If a specialized adapter does not yet exist, use `PROBE_REQUIRED`, not `UNAVAILABLE`.

## Failure semantics

- discovery miss: `NOT_DISCOVERED`;
- discovered but untested: `PROBE_REQUIRED`;
- probe executed and failed: `FAIL`;
- probe passed but wrong domain: `DOMAIN_MISMATCH`;
- correct domain but insufficient quality: `QUALITY_REJECTED`;
- usable candidate: `ELIGIBLE`.

Do not collapse these states into a single boolean.