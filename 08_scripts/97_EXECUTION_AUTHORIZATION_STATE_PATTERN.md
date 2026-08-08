# Execution Authorization and State Pattern

Canonical pure-Python sequence:

```python
import execution_authorization_gate as auth
import node_state_store as state

issued = auth.issue_authorization(graph, node_id, node_revision='n_004')
assert issued['status'] == 'PASS'

transition = state.validate_transition(
    'CONSTRAINED', 'READY_TO_BUILD', evidence=issued
)
assert transition['status'] == 'PASS'

# persist READY_TO_BUILD here

permit = auth.can_mutate(graph_with_ready_state, node_id, issued)
assert permit['can_mutate_geometry']

# mutate only this node
# persist BUILT_UNVERIFIED
# canonical QA + RECONSTRUCTION_NODE_GATE
```

Do not replace this with an asset-local boolean such as `can_build=True`.
