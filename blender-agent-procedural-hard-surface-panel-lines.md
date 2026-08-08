# Blender Agent Skill: Procedural Hard-Surface Panel Lines and Grooves

## Purpose

This skill defines how a Blender AI agent creates, updates, validates, and repairs hard-surface panel lines, seams, and narrow grooves procedurally through the Blender Python API.

The skill is intended for reconstruction workflows in which an AI agent must reproduce concept-art details with deterministic geometry instead of simulating manual UI actions.

The core technique implemented here is based on a non-destructive modifier stack:

```text
semantic panel-line path
        ->
mesh edges representing the path
        ->
Sharp edge marking
        ->
Edge Split
        ->
Solidify
        ->
Bevel
        ->
Subdivision Surface: SIMPLE
        ->
Subdivision Surface: CATMULL_CLARK
        ->
validated high-poly groove geometry
```

The primary target is high-poly/detail geometry suitable for rendering or baking normal maps. It must not be assumed to be appropriate as final game-export topology.

---

## Skill name

`blender-agent-procedural-hard-surface-panel-lines.md`

---

## When the agent should use this skill

Use this skill when the requested or detected geometry contains any of the following:

- panel separation lines;
- cosmetic seams;
- structural shell seams;
- narrow recessed hard-surface lines;
- sci-fi panel lines;
- technical grooves whose visual width is small relative to the parent surface;
- continuous L-shaped, U-shaped, rectangular, polygonal, or segmented seam paths;
- high-poly detail that should later be baked into a normal map;
- concept-art details that are better represented as a path than as a Boolean volume.

Typical semantic requests:

```text
Create a 3 mm structural seam along the left casing.

Reconstruct the visible L-shaped groove from the concept-art side view.

Add a cosmetic panel line 18% from the top edge and continue it vertically downward.

Match this seam to the reference image without permanently cutting the export mesh.
```

---

## When the agent should NOT use this skill

Do not use this technique by default when:

- the feature is a wide recess rather than a narrow seam;
- the groove must remove substantial physical volume;
- the feature changes the silhouette;
- the feature is a through-hole;
- the panel is physically detached from the surrounding shell;
- the final topology itself must contain the recess for gameplay or collision reasons;
- a Boolean cutter expresses the design intent more accurately;
- the detail is purely material-based and does not require geometry;
- the requested result is a final low-poly game mesh and the generated subdivision density would be excessive.

Preferred alternatives:

```text
wide recess       -> HS_RECESS
through opening   -> HS_CUTOUT
slot              -> HS_SLOT
vent array        -> HS_VENT
raised panel      -> HS_RAISED_PANEL
silhouette detail -> direct base-mesh modeling
```

---

# 1. Agent mental model

The agent must reason about a panel line as a semantic geometric object, not as a sequence of Blender clicks.

Wrong abstraction:

```text
Enter Edit Mode.
Press K.
Click four times.
Press Enter.
Select edges.
Mark Sharp.
Add modifiers.
```

Correct abstraction:

```python
PanelLine(
    id="side_shell_seam_01",
    surface="LEFT_SHELL",
    path=[
        (0.18, 0.77),
        (0.43, 0.77),
        (0.43, 0.39),
        (0.81, 0.39),
    ],
    profile="STRUCTURAL_SMALL",
)
```

The execution layer is responsible for translating this intent into Blender geometry.

The agent should reason at three levels:

```text
LEVEL 1: INTENT
"There is a narrow structural seam visible on the left shell."

LEVEL 2: SEMANTIC GEOMETRY
PanelLine(surface, normalized_path, profile)

LEVEL 3: BLENDER EXECUTION
projection -> topology -> sharp edges -> modifiers -> validation
```

The agent must keep Level 2 independent of temporary Blender edge indices.

---

# 2. Hard rules

## 2.1 Never treat edge indices as persistent identity

Do not store semantic intent as:

```python
edge_indices = [124, 125, 131, 140]
```

Edge indices can change after topology edits, modifiers are applied, geometry is rebuilt, objects are joined, meshes are triangulated, or another reconstruction step modifies connectivity.

Edge indices may be used only as short-lived execution data inside one atomic operation.

Persistent intent must be stored as one or more of:

- normalized path coordinates;
- local-space 3D path coordinates;
- stable semantic surface identifier;
- mesh edge-domain custom attribute;
- custom object metadata describing the panel line.

---

## 2.2 Prefer a dedicated detail shell

By default the agent must not run this Sharp/Edge Split technique on the only production copy of the base mesh.

Reason:

```text
Edge Split with use_edge_sharp=True
```

acts on all edges marked Sharp on that mesh. Other sharp edges may exist for shading or unrelated hard-surface treatment.

Default structure:

```text
ASSET_ROOT
|
+-- Asset_BASE
|
+-- Asset_PANEL_HIGH
|
+-- Asset_BOOLEAN_HIGH
|
+-- Asset_EXPORT
```

Recommended panel-line target:

```text
Asset_PANEL_HIGH
```

The detail shell may be:

- a controlled duplicate of the relevant surface;
- a separated copy of selected faces;
- a reconstruction-only high-poly object;
- a disposable bake source.

Only use the primary mesh directly if the agent has verified that Sharp edge semantics are dedicated exclusively to this subsystem.

---

## 2.3 Prefer data API and BMesh over UI operators

Preferred:

```python
obj.data.edges[i].use_edge_sharp = True
obj.modifiers.new(...)
bmesh.new()
bmesh.ops...
```

Avoid as the default automation mechanism:

```python
bpy.ops.mesh.mark_sharp()
bpy.ops.object.modifier_add(...)
```

Reason:

`bpy.ops` is often context-sensitive and can depend on selection state, active object, editor state, mode, or current area. A reconstruction agent should minimize hidden UI state.

Use operators only when a specific Blender operation has no sufficiently reliable data API or BMesh equivalent, and isolate such use behind a tested adapter.

---

## 2.4 Use meters internally

All geometric profile dimensions must be represented internally in meters.

Examples:

```text
0.0005 m = 0.5 mm
0.0010 m = 1.0 mm
0.0020 m = 2.0 mm
0.0040 m = 4.0 mm
```

The asset may be displayed in any unit system, but the skill contract must remain numerically unambiguous.

---

## 2.5 Do not apply modifiers prematurely

Keep the stack non-destructive until one of the following explicitly requires application:

- baking pipeline;
- export preparation;
- downstream topology operation requiring evaluated geometry;
- explicit finalization request.

The semantic reconstruction data must remain editable even if modifiers are later applied.

---

# 3. Semantic data contract

The recommended input object is:

```python
panel_line = {
    "id": "side_shell_seam_01",
    "target_object": "Bench_SidePanel_PANEL_HIGH",
    "surface_id": "LEFT_SHELL",
    "coordinate_space": "SURFACE_NORMALIZED_2D",
    "path": [
        (0.18, 0.77),
        (0.43, 0.77),
        (0.43, 0.39),
        (0.81, 0.39),
    ],
    "profile": "STRUCTURAL_SMALL",
    "closed": False,
    "source": "concept_art",
    "confidence": 0.93,
}
```

Required fields:

```text
id
surface_id or an explicit local surface frame
path
profile or explicit dimensions
```

Recommended fields:

```text
target_object
coordinate_space
closed
source
confidence
reference_view
reference_feature_id
```

---

# 4. Coordinate spaces

## 4.1 Preferred representation: surface-normalized 2D

For mostly planar hard-surface panels, represent points in a normalized local 2D frame:

```text
u: 0.0 -> 1.0 across the usable surface width
v: 0.0 -> 1.0 across the usable surface height
```

Example:

```python
path = [
    (0.20, 0.75),
    (0.45, 0.75),
    (0.45, 0.35),
    (0.80, 0.35),
]
```

This representation survives asset resizing better than absolute edge indices or arbitrary global coordinates.

---

## 4.2 Surface frame

A planar surface frame should contain:

```python
surface_frame = {
    "origin": (x, y, z),
    "u_axis": (ux, uy, uz),
    "v_axis": (vx, vy, vz),
    "normal": (nx, ny, nz),
    "u_size": 0.80,
    "v_size": 0.42,
}
```

Conversion:

```text
P = origin
  + u_axis * (u * u_size)
  + v_axis * (v * v_size)
```

The agent must define whether `origin` corresponds to lower-left, upper-left, center, or another explicit anchor. Do not infer silently.

Recommended convention:

```text
origin = lower-left of the semantic surface frame
u      = left -> right
v      = bottom -> top
```

---

## 4.3 Curved surfaces

For curved shells, normalized points describe the intended path approximately in a reference frame, then each point or sampled segment must be projected onto evaluated surface geometry.

Preferred tools:

```python
Object.ray_cast(...)
Object.closest_point_on_mesh(...)
```

Use ray casting when the expected projection direction is known.

Use closest-point projection as a fallback when ray direction is ambiguous or the source point is already near the target surface.

Do not project through the object onto an unintended rear surface without checking hit normal and distance.

---

# 5. Panel-line profiles

Use named profiles instead of inventing dimensions separately for every operation.

Initial library:

```python
PANEL_PROFILES = {
    "COSMETIC_MICRO": {
        "depth": 0.0006,
        "bevel_width": 0.00020,
        "bevel_segments": 2,
        "simple_levels": 1,
        "smooth_levels": 1,
    },
    "COSMETIC_SMALL": {
        "depth": 0.0010,
        "bevel_width": 0.00035,
        "bevel_segments": 2,
        "simple_levels": 1,
        "smooth_levels": 2,
    },
    "STRUCTURAL_SMALL": {
        "depth": 0.0015,
        "bevel_width": 0.00050,
        "bevel_segments": 3,
        "simple_levels": 1,
        "smooth_levels": 2,
    },
    "STRUCTURAL_MEDIUM": {
        "depth": 0.0030,
        "bevel_width": 0.00100,
        "bevel_segments": 3,
        "simple_levels": 1,
        "smooth_levels": 2,
    },
    "HEAVY_PANEL": {
        "depth": 0.0060,
        "bevel_width": 0.00150,
        "bevel_segments": 4,
        "simple_levels": 1,
        "smooth_levels": 2,
    },
}
```

These are starting presets, not universal physical standards.

For 1:1 reconstruction, reference-derived dimensions override preset defaults.

The profile system exists to provide:

- consistent style;
- deterministic defaults;
- controlled parameter search;
- easier visual comparison;
- reusable asset-family standards.

---

# 6. Execution strategies

The agent must select one of three strategies.

## Strategy A: reuse an existing edge path

Use when the intended panel-line path already follows mesh edges closely enough.

Procedure:

```text
find candidate edges
-> verify continuity
-> verify geometric deviation
-> tag them as panel-line edges
-> set Sharp
-> build/reuse modifier stack
-> validate evaluated result
```

This is the cheapest and preferred route.

---

## Strategy B: create missing topology on the detail shell

Use when the path is on the target surface but corresponding edges do not yet exist.

Procedure:

```text
project semantic path to surface
-> find containing/intersected faces
-> create/split vertices and edges
-> preserve valid face topology
-> record resulting semantic edge attribute
-> set Sharp
-> modifier stack
-> validate
```

Implementation should use `bmesh` whenever practical.

Relevant BMesh concepts:

```text
bmesh.new()
bm.from_mesh(mesh)
bmesh.ops.bisect_edges(...)
bmesh.ops.subdivide_edges(...)
bmesh.ops.connect_verts(...)
bm.to_mesh(mesh)
bm.free()
```

The exact topology operation depends on whether projected path points land on vertices, edges, or face interiors.

---

## Strategy C: rebuild a dedicated path-friendly shell

Use when the source topology is unsuitable for deterministic cutting, for example:

- dense triangulated import;
- poor Meshy/AI-generated topology;
- many tiny irregular faces;
- non-manifold local region;
- uncontrolled overlapping surfaces;
- projection creates unstable topology;
- the panel-line detail only exists for bake/render purposes.

Procedure:

```text
extract/reconstruct clean surface shell
-> establish stable local surface frame
-> create panel-line topology on clean shell
-> run modifier stack
-> bake or render
```

For reconstruction agents this is often better than attempting to preserve unusable source topology.

---

# 7. Modifier stack specification

The canonical stack is:

```text
01 PANEL_EdgeSplit
02 PANEL_Solidify
03 PANEL_Bevel
04 PANEL_SubdivisionSimple
05 PANEL_SubdivisionSmooth
```

The order is part of the skill contract.

---

## 7.1 Edge Split

Required configuration:

```python
edge_split = obj.modifiers.new(
    name="PANEL_EdgeSplit",
    type='EDGE_SPLIT',
)

edge_split.use_edge_angle = False
edge_split.use_edge_sharp = True
```

Intent:

```text
split only explicitly Sharp-marked semantic panel-line edges
```

Do not enable angle-based splitting for this subsystem unless the reconstruction specifically requires it.

---

## 7.2 Solidify

Required baseline:

```python
solidify = obj.modifiers.new(
    name="PANEL_Solidify",
    type='SOLIDIFY',
)

solidify.thickness = depth
solidify.use_even_offset = True
solidify.use_rim = True
solidify.use_rim_only = True
```

The exact sign of `thickness` depends on shell orientation and expected groove direction.

The agent must visually/geometrically validate direction rather than assuming positive thickness always means inward.

If the groove is generated on the wrong side:

```text
first inspect normals and shell orientation
then invert thickness or correct normals
```

Do not hide reversed normals by randomly changing thickness signs across assets.

---

## 7.3 Bevel

Baseline:

```python
bevel = obj.modifiers.new(
    name="PANEL_Bevel",
    type='BEVEL',
)

bevel.width = bevel_width
bevel.segments = bevel_segments
bevel.limit_method = 'NONE'
bevel.use_clamp_overlap = True
```

`limit_method='NONE'` is acceptable on the dedicated panel-line shell because the shell exists for this detail treatment.

If the modifier unexpectedly bevels unrelated geometry, this is evidence that the target object is insufficiently isolated. Prefer isolating the shell rather than accumulating brittle modifier exceptions.

---

## 7.4 Simple subdivision

```python
subdiv_simple = obj.modifiers.new(
    name="PANEL_SubdivisionSimple",
    type='SUBSURF',
)

subdiv_simple.subdivision_type = 'SIMPLE'
subdiv_simple.levels = simple_levels
subdiv_simple.render_levels = simple_levels
```

Purpose:

- add supporting geometry;
- preserve overall shape;
- improve the next smoothing stage.

---

## 7.5 Catmull-Clark subdivision

```python
subdiv_smooth = obj.modifiers.new(
    name="PANEL_SubdivisionSmooth",
    type='SUBSURF',
)

subdiv_smooth.subdivision_type = 'CATMULL_CLARK'
subdiv_smooth.levels = smooth_levels
subdiv_smooth.render_levels = smooth_levels
```

Purpose:

- smooth the generated groove profile;
- improve high-poly shading and bake quality.

Do not raise subdivision levels automatically to fix an incorrect cross-section. Repair geometry/profile settings first.

---

# 8. Idempotent Python implementation

The execution code must be safe to run repeatedly.

Repeated execution must not create:

```text
PANEL_Bevel
PANEL_Bevel.001
PANEL_Bevel.002
...
```

Use deterministic modifier names and create-or-reuse behavior.

```python
import bpy


def ensure_modifier(obj, name, modifier_type):
    existing = obj.modifiers.get(name)

    if existing is not None:
        if existing.type != modifier_type:
            raise TypeError(
                f"Modifier {name!r} exists on {obj.name!r} "
                f"but has type {existing.type!r}, expected {modifier_type!r}."
            )
        return existing

    return obj.modifiers.new(name=name, type=modifier_type)
```

---

# 9. Reference implementation: build modifier stack

```python
import bpy


def ensure_modifier(obj, name, modifier_type):
    modifier = obj.modifiers.get(name)

    if modifier is not None:
        if modifier.type != modifier_type:
            raise TypeError(
                f"Modifier {name!r} on {obj.name!r} has type "
                f"{modifier.type!r}, expected {modifier_type!r}."
            )
        return modifier

    return obj.modifiers.new(name=name, type=modifier_type)


def ensure_panel_line_stack(
    obj,
    *,
    depth=0.0015,
    bevel_width=0.0005,
    bevel_segments=3,
    simple_levels=1,
    smooth_levels=2,
):
    if obj is None:
        raise ValueError("Panel-line target object is None.")

    if obj.type != 'MESH':
        raise TypeError(
            f"Panel-line target {obj.name!r} must be a MESH, got {obj.type!r}."
        )

    edge_split = ensure_modifier(
        obj,
        "PANEL_EdgeSplit",
        'EDGE_SPLIT',
    )
    edge_split.use_edge_angle = False
    edge_split.use_edge_sharp = True

    solidify = ensure_modifier(
        obj,
        "PANEL_Solidify",
        'SOLIDIFY',
    )
    solidify.thickness = float(depth)
    solidify.use_even_offset = True
    solidify.use_rim = True
    solidify.use_rim_only = True

    bevel = ensure_modifier(
        obj,
        "PANEL_Bevel",
        'BEVEL',
    )
    bevel.width = float(bevel_width)
    bevel.segments = int(bevel_segments)
    bevel.limit_method = 'NONE'
    bevel.use_clamp_overlap = True

    subdiv_simple = ensure_modifier(
        obj,
        "PANEL_SubdivisionSimple",
        'SUBSURF',
    )
    subdiv_simple.subdivision_type = 'SIMPLE'
    subdiv_simple.levels = int(simple_levels)
    subdiv_simple.render_levels = int(simple_levels)

    subdiv_smooth = ensure_modifier(
        obj,
        "PANEL_SubdivisionSmooth",
        'SUBSURF',
    )
    subdiv_smooth.subdivision_type = 'CATMULL_CLARK'
    subdiv_smooth.levels = int(smooth_levels)
    subdiv_smooth.render_levels = int(smooth_levels)

    return {
        "edge_split": edge_split,
        "solidify": solidify,
        "bevel": bevel,
        "subdiv_simple": subdiv_simple,
        "subdiv_smooth": subdiv_smooth,
    }
```

---

# 10. Enforce modifier order

Creating modifiers by name is not enough if the object already contains other modifiers or the stack was manually reordered.

The agent must verify canonical relative order:

```text
PANEL_EdgeSplit
before
PANEL_Solidify
before
PANEL_Bevel
before
PANEL_SubdivisionSimple
before
PANEL_SubdivisionSmooth
```

If the API/version-specific implementation for moving modifiers is available and tested, reorder them programmatically.

Otherwise fail validation explicitly rather than silently accepting a wrong stack.

Pseudo-contract:

```python
validate_modifier_order(
    obj,
    [
        "PANEL_EdgeSplit",
        "PANEL_Solidify",
        "PANEL_Bevel",
        "PANEL_SubdivisionSimple",
        "PANEL_SubdivisionSmooth",
    ],
)
```

---

# 11. Marking existing edges as panel-line edges

Short-lived execution helper:

```python
def mark_edges_sharp(obj, edge_indices, clear_existing=False):
    if obj.type != 'MESH':
        raise TypeError("Target must be a mesh.")

    mesh = obj.data

    if clear_existing:
        for edge in mesh.edges:
            edge.use_edge_sharp = False

    for index in edge_indices:
        if not 0 <= index < len(mesh.edges):
            raise IndexError(
                f"Edge index {index} out of range for {obj.name!r}."
            )

        mesh.edges[index].use_edge_sharp = True

    mesh.update()
```

This helper is not a semantic persistence layer.

The caller must already have determined which temporary edge indices represent the requested semantic path.

---

# 12. Semantic edge attribute

Use an edge-domain boolean attribute to record which edges belong to this subsystem whenever possible.

Recommended attribute name:

```text
agent_panel_line
```

Optional multi-line classification attributes:

```text
agent_panel_line
agent_panel_line_group
agent_panel_line_profile
```

A simple boolean attribute can be created as:

```python
def ensure_panel_line_edge_attribute(mesh, name="agent_panel_line"):
    attr = mesh.attributes.get(name)

    if attr is None:
        attr = mesh.attributes.new(
            name=name,
            type='BOOLEAN',
            domain='EDGE',
        )

    if attr.domain != 'EDGE':
        raise TypeError(f"Attribute {name!r} must use EDGE domain.")

    return attr
```

The Sharp state remains the mechanism consumed by Edge Split, while the custom attribute is the agent's semantic bookkeeping layer.

After any topology-changing operation, validate whether the attribute still maps correctly to the intended edge path.

Never assume attribute propagation is perfect across every topology operation.

---

# 13. Path reconstruction pipeline

For a normalized path:

```python
[
    (0.18, 0.77),
    (0.43, 0.77),
    (0.43, 0.39),
    (0.81, 0.39),
]
```

use the following pipeline.

## Step 1: resolve target surface

Identify a semantic surface frame or the exact source faces.

Output:

```python
surface = {
    "object": obj,
    "face_indices": [...],
    "origin": ...,
    "u_axis": ...,
    "v_axis": ...,
    "normal": ...,
    "u_size": ...,
    "v_size": ...,
}
```

---

## Step 2: convert normalized points to 3D candidates

```python
from mathutils import Vector


def surface_uv_to_local_point(surface, u, v):
    origin = Vector(surface["origin"])
    u_axis = Vector(surface["u_axis"]).normalized()
    v_axis = Vector(surface["v_axis"]).normalized()

    return (
        origin
        + u_axis * (float(u) * float(surface["u_size"]))
        + v_axis * (float(v) * float(surface["v_size"]))
    )
```

---

## Step 3: project onto the actual mesh

For curved or imperfect surfaces, project candidate points onto evaluated geometry.

Example fallback using closest point:

```python
def project_local_point_to_mesh(obj, point_local, depsgraph=None):
    if depsgraph is None:
        depsgraph = bpy.context.evaluated_depsgraph_get()

    hit, location, normal, face_index = obj.closest_point_on_mesh(
        point_local,
        depsgraph=depsgraph,
    )

    if not hit:
        raise RuntimeError(
            f"Could not project point {tuple(point_local)} onto {obj.name!r}."
        )

    return {
        "location": location,
        "normal": normal,
        "face_index": face_index,
    }
```

Projection validation must include:

```text
maximum allowed projection distance
expected normal orientation
allowed face set / semantic surface region
front/back ambiguity check
```

---

## Step 4: determine whether path already exists

Search nearby vertices and edges using a scale-aware tolerance.

Do not use a fixed arbitrary tolerance such as `0.01` for every asset.

Recommended tolerance basis:

```text
tolerance = max(
    absolute_minimum,
    object_diagonal * relative_tolerance
)
```

Example:

```text
absolute_minimum = 0.0001 m
relative_tolerance = 1e-4
```

If an existing continuous edge chain is within tolerance, reuse it.

---

## Step 5: create topology if missing

The topology builder must classify each projected point as approximately:

```text
EXISTING_VERTEX
ON_EDGE
INSIDE_FACE
```

Then:

```text
EXISTING_VERTEX -> reuse vertex
ON_EDGE         -> split/bisect edge
INSIDE_FACE     -> create face split topology
```

Do not create overlapping duplicate vertices or edges.

BMesh validity requirements:

- no duplicate edges;
- no duplicate faces;
- all faces contain at least 3 vertices;
- selection state is irrelevant unless a UI operator is invoked;
- write BMesh back to the mesh after topology changes;
- free standalone BMesh data when finished.

---

# 14. BMesh skeleton

```python
import bmesh


def edit_mesh_with_bmesh(obj, edit_callback):
    if obj.type != 'MESH':
        raise TypeError("Target must be a mesh object.")

    mesh = obj.data
    bm = bmesh.new()

    try:
        bm.from_mesh(mesh)
        bm.verts.ensure_lookup_table()
        bm.edges.ensure_lookup_table()
        bm.faces.ensure_lookup_table()

        result = edit_callback(bm)

        bm.normal_update()
        bm.to_mesh(mesh)
        mesh.update()

        return result

    finally:
        bm.free()
```

This isolates BMesh lifecycle management from the geometry-specific operation.

---

# 15. Path creation is not equivalent to creating wire edges

A panel line running through an existing surface must become part of the surface topology.

Wrong:

```text
create free-floating vertices
connect them with wire edges
place them visually on top of the surface
```

This does not correctly split the underlying faces and may not produce the intended Edge Split/Solidify behavior.

Correct:

```text
new path vertices become vertices of affected faces
new path edges split affected faces
surface topology remains valid
```

Use face-aware BMesh operations.

---

# 16. Existing-edge path resolver

The resolver receives projected path segments and returns a continuous mesh edge chain.

Required checks:

```text
1. Candidate edges are near the requested path.
2. Candidate edges form a connected chain.
3. Chain ordering matches semantic path ordering.
4. Maximum perpendicular deviation is below tolerance.
5. Chain does not leave the allowed semantic surface.
6. Chain does not contain large unintended detours.
```

Suggested output:

```python
{
    "status": "REUSED_EXISTING_TOPOLOGY",
    "edge_indices": [...],
    "max_path_deviation": 0.00018,
    "path_length_requested": 0.412,
    "path_length_actual": 0.413,
}
```

---

# 17. Visual-intent preservation

The agent must distinguish three concepts:

```text
path location
profile dimensions
surface relationship
```

A concept-art seam can be positioned correctly but still look wrong because:

- groove is too deep;
- bevel is too round;
- groove is too wide;
- smoothing changes corner shape;
- projection drifts around curved surfaces;
- line is offset from a nearby panel boundary;
- line terminates too early or too late.

Validation must therefore include both path geometry and cross-section appearance.

---

# 18. Corner handling

Panel lines commonly contain corners:

```text
L
U
rectangle
stepped path
polygon
```

The agent should preserve semantic corner locations exactly unless a rounded corner is explicitly visible in the reference.

Do not smooth path coordinates merely because the final modifier stack contains subdivision.

The path is the design skeleton.

The modifier stack controls the groove profile.

These are different layers of geometry.

---

# 19. Closed panel lines

A closed path:

```text
+-------------+
|             |
|             |
+-------------+
```

must be represented explicitly:

```python
{
    "closed": True,
    "path": [P0, P1, P2, P3]
}
```

Do not require the final point to be duplicated as `P0` unless the implementation contract explicitly uses that representation.

The executor should close the final segment internally.

Validate:

```text
last -> first connection exists
no duplicate zero-length closing segment
consistent winding
no self intersection
```

---

# 20. Self-intersection handling

Before cutting topology, detect path self-intersections in the semantic surface frame.

Example invalid path:

```text
\ /
 X
/ \
```

Default behavior:

```text
FAIL
```

Do not silently create ambiguous panel topology.

Allowed exception:

A deliberate crossing is explicitly represented as separate panel-line features with defined depth/priority behavior.

---

# 21. Multiple panel lines on one detail shell

Preferred:

```text
one semantic registry
one controlled Sharp state
one canonical modifier stack
many panel-line paths
```

Do not create five identical modifier stacks for five seams unless they require genuinely different cross-sections.

If different profiles are required on one object, prefer one of:

```text
A. separate detail-shell objects by profile
B. separate semantic material/detail layer
C. a more advanced geometry-node/custom system
```

The basic Sharp/Edge Split modifier stack does not natively encode a different Solidify thickness for every individual Sharp edge set.

---

# 22. Object naming

Recommended deterministic naming:

```text
<BaseName>_BASE
<BaseName>_PANEL_HIGH
<BaseName>_BOOLEAN_HIGH
<BaseName>_EXPORT
```

Examples:

```text
Bench_Frame_BASE
Bench_Frame_PANEL_HIGH
Bench_Frame_EXPORT

TamudaWall_Module06_BASE
TamudaWall_Module06_PANEL_HIGH
```

Do not use names such as:

```text
Cube.017
Cube_copy_final2
panelnew
```

for semantically important reconstruction objects.

---

# 23. Semantic metadata persistence

Store enough metadata to regenerate the detail after destructive changes.

Example:

```python
import json


def save_panel_line_registry(obj, registry):
    obj["agent_panel_lines"] = json.dumps(
        registry,
        separators=(",", ":"),
        sort_keys=True,
    )
```

Example stored structure:

```json
{
  "version": 1,
  "lines": [
    {
      "id": "side_shell_seam_01",
      "surface_id": "LEFT_SHELL",
      "coordinate_space": "SURFACE_NORMALIZED_2D",
      "path": [[0.18, 0.77], [0.43, 0.77], [0.43, 0.39], [0.81, 0.39]],
      "profile": "STRUCTURAL_SMALL",
      "closed": false
    }
  ]
}
```

The registry is the source of semantic truth.

Temporary mesh edge indices are execution artifacts.

---

# 24. Updating an existing panel line

Agent command:

```python
update_panel_line(
    id="side_shell_seam_01",
    path=new_path,
)
```

Expected behavior:

```text
1. Resolve registry entry.
2. Remove/clear previous panel-line topology or regenerate the detail shell.
3. Reconstruct the path from semantic data.
4. Reapply semantic edge attributes and Sharp state.
5. Reuse canonical modifier stack.
6. Validate.
7. Replace registry entry only after successful validation.
```

For reconstruction assets, regenerating a dedicated detail shell from clean source geometry may be safer than surgically deleting an old path.

Prefer determinism over clever local mutation.

---

# 25. Deleting a panel line

Deletion by semantic ID:

```python
delete_panel_line("side_shell_seam_01")
```

must not mean:

```text
clear an arbitrary list of remembered edge indices
```

The executor should either:

- rebuild the detail shell without that semantic line; or
- resolve the currently tagged edge group safely and remove its effect.

If geometry surgery risks corrupting topology, rebuild from semantic source data.

---

# 26. Evaluated-geometry validation

Modifier parameters alone do not prove the result is correct.

The agent must inspect evaluated geometry.

Conceptual pattern:

```python
depsgraph = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(depsgraph)
```

Depending on the Blender version and geometry-access path used by the runtime, the agent may inspect an evaluated mesh or evaluated geometry set.

Validation must operate on the final evaluated result whenever the measurement concerns visible post-modifier geometry.

Do not measure only the original cage and claim the groove output is correct.

---

# 27. Required validation report

Every autonomous panel-line operation should produce a machine-readable report.

Minimum:

```python
{
    "operation": "panel_line",
    "feature_id": "side_shell_seam_01",
    "status": "PASS",
    "target": "Bench_SidePanel_PANEL_HIGH",
    "profile": "STRUCTURAL_SMALL",
    "path_segments": 3,
    "closed": False,
    "max_path_deviation_m": 0.00018,
    "self_intersections": 0,
    "non_manifold_edges": 0,
    "modifier_order_valid": True,
    "sharp_path_continuous": True,
}
```

Recommended additional metrics:

```text
requested path length
actual path length
projection max distance
projection mean distance
requested groove depth
measured groove depth
requested bevel width
measured/estimated visible width
triangle count before modifiers
triangle count after evaluated stack
normal consistency
number of disconnected sharp components
```

---

# 28. Pass/fail conditions

## PASS

All must be true:

```text
semantic path resolved
path is continuous
path is on intended surface
no unintended Sharp edges are consumed by this subsystem
modifier stack exists
modifier order is valid
no invalid self intersection
no newly introduced non-manifold topology unless explicitly allowed
visual profile direction is correct
geometric deviation is within tolerance
```

## FAIL

Fail explicitly if any of the following occurs:

```text
surface cannot be resolved
projection hits wrong shell repeatedly
requested path leaves the semantic surface
path is self-intersecting without explicit crossing semantics
topology operation creates duplicate/invalid faces
edge chain is discontinuous
Sharp classification leaks to unrelated edges
modifier stack order cannot be guaranteed
result points outward when an inward seam is required and cannot be safely corrected
required path tolerance cannot be met
```

Do not return PASS merely because Blender did not throw an exception.

---

# 29. Repair strategy hierarchy

When validation fails, repair in this order.

```text
1. Re-evaluate surface frame and projection.
2. Re-resolve existing topology with adjusted scale-aware tolerance.
3. Rebuild local detail topology.
4. Rebuild dedicated detail shell from clean source.
5. Switch to a different hard-surface operation if panel-line semantics are incorrect.
```

Do not immediately increase subdivision levels.

Do not randomly perturb geometry until the validator passes.

---

# 30. Performance rules

The stack can become expensive because subdivision multiplies geometry.

Rules:

```text
Viewport smooth levels should normally remain <= 2.
Use SIMPLE level 1 unless measurement proves more is required.
Prefer Bevel segments 2-3 for most reconstruction work.
Use 4+ bevel segments only for close high-poly requirements.
Disable expensive high-poly detail objects outside reconstruction/bake views when practical.
Do not export the evaluated high-poly stack as the game mesh by default.
```

Track evaluated geometry growth.

Example warning threshold:

```text
if evaluated_triangles > base_triangles * 100:
    issue PERFORMANCE_WARNING
```

The exact threshold may be asset-specific.

---

# 31. High-poly versus game mesh

Default production flow:

```text
CONCEPT ART
    ->
BASE RECONSTRUCTION
    ->
PANEL_HIGH
    ->
high-poly panel-line geometry
    ->
NORMAL/AO BAKE
    ->
EXPORT mesh + baked maps
```

The presence of a valid high-poly groove does not imply that the same geometry should be exported into the runtime.

The reconstruction layer and game-optimization layer are separate concerns.

---

# 32. Profile-selection reasoning

The agent should estimate panel-line class from reference scale.

Example heuristic:

```text
visible hairline / cosmetic separation
-> COSMETIC_MICRO or COSMETIC_SMALL

clear manufactured shell seam
-> STRUCTURAL_SMALL

prominent equipment casing channel
-> STRUCTURAL_MEDIUM

large armored panel separation
-> HEAVY_PANEL or switch to HS_RECESS
```

If the feature width exceeds approximately a few percent of the local surface dimension, question whether it is still semantically a panel line.

Do not force every elongated recess into this skill.

---

# 33. Concept-art reconstruction integration

When the panel line comes from an image, store measurement provenance.

Example:

```python
{
    "id": "front_panel_seam_02",
    "source": {
        "type": "concept_art",
        "view": "FRONT",
        "reference_id": "concept_front_v03",
        "pixel_polyline": [
            [412, 188],
            [612, 188],
            [612, 366],
            [801, 366]
        ]
    },
    "surface_path": [...],
    "confidence": 0.91
}
```

This permits later comparison between rendered output and the original reference.

---

# 34. Multi-view reconstruction rule

If the same seam is visible in multiple orthographic/reference views, do not independently reconstruct two different 3D paths.

Instead:

```text
all views constrain one semantic 3D feature
```

Procedure:

```text
infer candidate 3D path
-> project candidate into each reference view
-> measure reprojection error
-> optimize/repair one 3D path
```

The semantic feature ID remains single and stable.

---

# 35. Example agent request

Input:

```json
{
  "operation": "HS_PANEL_LINE",
  "target_object": "Bench_LeftShell_PANEL_HIGH",
  "feature_id": "left_shell_seam_01",
  "surface_id": "LEFT_OUTER_SURFACE",
  "coordinate_space": "SURFACE_NORMALIZED_2D",
  "path": [
    [0.16, 0.78],
    [0.46, 0.78],
    [0.46, 0.42],
    [0.83, 0.42]
  ],
  "profile": "STRUCTURAL_SMALL",
  "closed": false
}
```

Expected execution:

```text
resolve LEFT_OUTER_SURFACE
-> convert normalized path to surface coordinates
-> project to real mesh
-> search existing edge chain
-> if absent, create topology in BMesh
-> tag semantic edges
-> mark semantic edges Sharp
-> ensure canonical panel modifier stack
-> evaluate result
-> validate path, topology, direction and profile
-> persist semantic registry
-> return report
```

---

# 36. Example high-level Python API

The reconstruction agent should ultimately call a compact interface such as:

```python
result = hs.panel_line.create(
    target="Bench_LeftShell_PANEL_HIGH",
    feature_id="left_shell_seam_01",
    surface="LEFT_OUTER_SURFACE",
    path=[
        (0.16, 0.78),
        (0.46, 0.78),
        (0.46, 0.42),
        (0.83, 0.42),
    ],
    coordinate_space="SURFACE_NORMALIZED_2D",
    profile="STRUCTURAL_SMALL",
    closed=False,
)
```

The LLM should not normally generate the underlying BMesh implementation for every asset.

The underlying library should be deterministic, versioned, tested, and reusable.

---

# 37. Suggested Python package layout

```text
blender_agent/
|
+-- geometry/
|   +-- mesh_access.py
|   +-- topology.py
|   +-- projection.py
|   +-- surface_frames.py
|   +-- metrics.py
|
+-- hard_surface/
|   +-- panel_lines.py
|   +-- recesses.py
|   +-- grooves.py
|   +-- cutouts.py
|   +-- slots.py
|   +-- vents.py
|   +-- seams.py
|
+-- reconstruction/
|   +-- feature_registry.py
|   +-- concept_projection.py
|   +-- semantic_surfaces.py
|
+-- validation/
|   +-- topology.py
|   +-- geometry.py
|   +-- modifiers.py
|   +-- reconstruction_error.py
|
+-- profiles/
    +-- panel_lines.py
```

This skill defines the behavior expected from:

```text
hard_surface/panel_lines.py
```

---

# 38. Suggested public interface

```python
class PanelLineService:
    def create(self, *, target, feature_id, surface, path,
               profile, coordinate_space, closed=False):
        ...

    def update(self, feature_id, **changes):
        ...

    def delete(self, feature_id):
        ...

    def rebuild(self, feature_id):
        ...

    def validate(self, feature_id):
        ...

    def rebuild_all(self, target):
        ...
```

Important property:

```text
rebuild_all(target)
```

must be able to reconstruct all panel lines from semantic registry data without relying on historical edge indices.

This is the determinism test for the subsystem.

---

# 39. Determinism test

A valid implementation should pass:

```text
1. Start from clean BASE shell.
2. Load semantic panel-line registry.
3. Generate PANEL_HIGH.
4. Save validation metrics.
5. Delete generated PANEL_HIGH.
6. Generate it again from the same inputs.
7. Compare geometry/metrics.
```

Expected:

```text
same semantic paths
same profile settings
same modifier ordering
same topology class
same validation result within numeric tolerance
```

If reconstruction depends on random UI state or undocumented selection history, the skill implementation is not acceptable.

---

# 40. Transaction rule

Complex topology edits should behave transactionally.

Preferred pattern:

```text
snapshot semantic registry
-> operate on disposable/generated detail shell
-> validate
-> commit generated result
```

If validation fails:

```text
preserve previous valid generated object
return FAIL report
```

Do not leave partially edited production geometry as the only version of the asset.

---

# 41. Error taxonomy

Use explicit error codes.

```text
PL001 TARGET_NOT_MESH
PL002 TARGET_NOT_FOUND
PL003 SURFACE_NOT_RESOLVED
PL004 PATH_PROJECTION_FAILED
PL005 PATH_OUTSIDE_SURFACE
PL006 PATH_SELF_INTERSECTION
PL007 EDGE_CHAIN_DISCONTINUOUS
PL008 TOPOLOGY_BUILD_FAILED
PL009 UNINTENDED_SHARP_EDGE_CONFLICT
PL010 MODIFIER_STACK_INVALID
PL011 GROOVE_DIRECTION_WRONG
PL012 NON_MANIFOLD_RESULT
PL013 PROFILE_TOLERANCE_FAILED
PL014 PERFORMANCE_LIMIT_EXCEEDED
PL015 SEMANTIC_REGISTRY_INVALID
```

Warnings:

```text
PLW01 REUSED_APPROXIMATE_EXISTING_EDGE_CHAIN
PLW02 HIGH_EVALUATED_POLYCOUNT
PLW03 REFERENCE_CONFIDENCE_LOW
PLW04 SOURCE_TOPOLOGY_POOR
PLW05 CURVED_SURFACE_PROJECTION_APPROXIMATE
```

---

# 42. Minimum logging

Each operation should log:

```text
feature ID
target object
selected strategy A/B/C
profile
path point count
projection tolerance
number of reused edges
number of created vertices/edges/faces
modifier creation/reuse
validation metrics
final status
```

Do not log every individual Blender RNA assignment unless debug mode is enabled.

---

# 43. Agent decision table

| Condition | Action |
|---|---|
| Correct edge chain already exists | Strategy A: reuse |
| Clean quad/ngon shell, path missing | Strategy B: create topology |
| Imported triangulated/noisy shell | Strategy C: rebuild detail shell |
| Feature is wide/deep | Switch to recess/Boolean skill |
| Feature changes silhouette | Edit base mesh, not panel-line detail |
| Sharp edges already have unrelated semantic use | Dedicated PANEL_HIGH shell required |
| Multiple line widths required | Separate shells/profile groups or advanced system |
| Final asset is low-poly export | Bake high-poly detail; do not export stack by default |

---

# 44. Anti-patterns

The agent must not:

```text
simulate keyboard/mouse steps when data API is sufficient;
store panel identity only as edge indices;
apply modifiers immediately after creating them;
use one arbitrary numeric tolerance for all asset scales;
add more subdivision to hide broken topology;
run Edge Split on unrelated Sharp shading edges without isolation;
create free-floating wire paths instead of splitting surface topology;
claim success without evaluating the resulting geometry;
export high-poly subdivision geometry automatically;
reconstruct the same seam independently from each concept-art view;
mutate the only good production mesh without a recoverable semantic source;
randomly invert thickness instead of checking normals and groove direction.
```

---

# 45. Completion criteria

A panel-line feature is complete only when:

```text
[ ] semantic feature has stable ID
[ ] target semantic surface is known
[ ] path is stored independently of temporary edge indices
[ ] path is projected/resolved onto correct surface
[ ] topology contains a continuous edge representation
[ ] panel-line edges are semantically tagged
[ ] required edges are Sharp
[ ] unrelated Sharp edges are not consumed unintentionally
[ ] canonical modifier stack exists
[ ] modifier order is correct
[ ] profile parameters match requested/preset values
[ ] evaluated groove points in intended direction
[ ] topology is valid
[ ] path deviation is within tolerance
[ ] performance is within the asset budget or explicitly warned
[ ] semantic registry can regenerate the feature
[ ] validation report is PASS
```

---

# 46. Compact execution instruction for an autonomous agent

When asked to create a hard-surface panel line:

```text
1. Classify the feature as a narrow panel-line/seam rather than a wide recess.
2. Resolve the semantic target surface.
3. Represent the path in persistent surface-relative coordinates.
4. Prefer a dedicated PANEL_HIGH detail shell.
5. Reuse an existing matching edge chain if one exists.
6. Otherwise create valid face-splitting topology with BMesh.
7. Tag generated/reused edges semantically.
8. Mark only the intended panel-line edges Sharp.
9. Ensure this modifier stack in this order:
   Edge Split -> Solidify -> Bevel -> SIMPLE Subdivision -> CATMULL_CLARK Subdivision.
10. Evaluate the post-modifier geometry.
11. Validate path, topology, modifier order, groove direction, dimensions and performance.
12. Persist semantic reconstruction data only after success.
13. Return an explicit PASS/FAIL report with measurements.
14. Keep high-poly panel geometry separate from final game-export topology unless explicitly required.
```

---

# 47. API notes

The implementation relies on Blender Python capabilities including:

```text
bpy.types.MeshEdge.use_edge_sharp
bpy.types.EdgeSplitModifier.use_edge_angle
bpy.types.EdgeSplitModifier.use_edge_sharp
bpy.types.SolidifyModifier
bpy.types.BevelModifier
bpy.types.SubsurfModifier
bmesh
bmesh.ops
Object.ray_cast
Object.closest_point_on_mesh
Blender dependency-graph/evaluated geometry access
```

The runtime implementation should perform feature/property checks where practical when supporting multiple Blender versions.

Example:

```python
if not hasattr(edge_split, "use_edge_sharp"):
    raise RuntimeError(
        "This Blender build does not expose EdgeSplitModifier.use_edge_sharp."
    )
```

Do not silently substitute a different geometric technique when a required API capability is absent. Return a capability error or explicitly invoke a defined fallback implementation.

---

# 48. Source references for implementation verification

Official Blender Python API documentation should be treated as the implementation source of truth for API names and version behavior:

- Blender Python API: MeshEdge
- Blender Python API: EdgeSplitModifier
- Blender Python API: SolidifyModifier
- Blender Python API: BevelModifier
- Blender Python API: SubsurfModifier
- Blender Python API: BMesh Module
- Blender Python API: BMesh Operators
- Blender Python API: Object evaluated geometry, ray casting, and closest-point queries

When the Blender runtime version differs from the version used to write this skill, verify the affected RNA properties before changing the skill contract.

---

# 49. Architectural conclusion

This skill is not a tutorial for reproducing manual Blender actions.

It defines a reconstruction primitive:

```text
HS_PANEL_LINE
```

The AI agent provides semantic intent:

```text
where the panel line is
what surface it belongs to
what profile it has
how it relates to reference geometry
```

The deterministic Blender layer decides:

```text
which current edges represent the path
whether topology must be created
how the edges are tagged
how the modifier stack is configured
how the evaluated result is validated
```

The semantic reconstruction record, not the temporary Blender selection or edge index list, is the durable source of truth.

This separation is mandatory for an agent expected to reconstruct hard-surface assets repeatedly, update them after concept-art corrections, and reproduce the same result after topology or scene changes.
