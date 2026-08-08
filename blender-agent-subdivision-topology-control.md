# Blender Agent Skill: Subdivision-Surface Topology Control

## Purpose

This skill defines how a Blender AI agent designs, repairs, validates, and maintains topology intended to survive a Catmull-Clark Subdivision Surface workflow.

The source technique set comes from the supplied transcript of the tutorial at:

`https://www.youtube.com/watch?v=zSLELihVi6I`

The tutorial presents seven topology techniques for keeping SubD meshes clean. This skill converts those manual modeling ideas into reusable semantic operations for an autonomous Blender agent.

The agent must reason about **topology flow**, **support-loop density**, **curvature continuity**, **pole placement**, **local tessellation**, and **post-subdivision behavior** rather than reproducing keyboard and mouse actions.

This skill is primarily for:

- high-poly hard-surface modeling;
- VFX-style SubD control cages;
- reconstruction assets that require smooth manufactured surfaces;
- game-asset high-poly sources used for baking;
- curved hard-surface shells with integrated recesses, ports, buttons, tubes, or transitions.

It must not be assumed that the resulting control cage is the final runtime game mesh.

---

# 1. Core mental model

Subdivision Surface does not repair topology. It amplifies the consequences of topology.

The agent must separate four layers:

```text
DESIGN INTENT
    ->
CONTROL-CAGE TOPOLOGY
    ->
SUBDIVISION BEHAVIOR
    ->
EVALUATED SURFACE QUALITY
```

A valid cage is not merely a mesh with quads. A valid cage must produce the intended evaluated surface under the configured Subdivision Surface modifier.

The agent must therefore inspect both:

```text
base/control mesh
and
evaluated subdivided mesh
```

before returning PASS.

---

# 2. Skill primitives

This skill defines the following semantic operations:

```text
SUBD_REDIRECT_CORNER_SUPPORT
SUBD_BUILD_SUPPORT_BEVEL
SUBD_REPAIR_CURVED_PINCHING
SUBD_TERMINATE_LOCAL_DENSITY
SUBD_CURVED_CYLINDER_RECESS
SUBD_BUILD_POLE_SAFE_SPHERE
SUBD_REPAIR_BRANCH_JUNCTION
SUBD_CURVED_CYLINDER_PROTRUSION
SUBD_TOPOLOGY_AUDIT
```

These are not Blender operators. They are agent-level intentions translated into Blender API/BMesh operations.

---

# 3. General SubD rules

## 3.1 Support geometry is intentional geometry

Supporting edge loops exist to control the limit surface.

They must not be added globally by habit.

The agent should ask:

```text
Which feature requires support?
Which side of the feature requires support?
How far from the feature should the support lie?
Can the support terminate or redirect before crossing unrelated curvature?
```

---

## 3.2 Avoid unnecessary clusters of parallel loops

A common failure mode is:

```text
feature edge
support loop
support loop
another nearby structural loop
```

all traveling through the entire object.

This produces:

- dense local tessellation;
- difficult editing;
- poor deformation behavior;
- uneven displacement response;
- needless evaluated geometry;
- pinching when those loops enter curved regions.

The agent should redirect or terminate support topology when the extra density is no longer needed.

---

## 3.3 Even spacing matters on curved surfaces

On planar surfaces, irregular edge spacing may have little visible consequence.

On curved surfaces, uneven spacing changes the way Catmull-Clark distributes the limit surface and can create:

- pinching;
- flattening;
- waviness;
- visible shading discontinuity;
- uneven displacement tessellation.

The agent should measure local edge-length variance and loop spacing when a failure occurs on a curved area.

---

## 3.4 Do not use subdivision level as a substitute for correct topology

Increasing subdivision can reduce some visible artifacts because the sampled surface becomes denser, but this is not the first repair strategy.

Repair order:

```text
1. inspect topology flow
2. inspect support-loop placement
3. inspect pole location and valence
4. inspect local tessellation density
5. increase base resolution only when the curved feature genuinely lacks enough control points
6. increase render subdivision only after the cage is structurally sound
```

---

## 3.5 Creases are not the default portability strategy

The source tutorial prefers supporting edge loops over creasing for VFX portability and surface quality.

This skill adopts the following policy:

```text
portable/high-poly reconstruction -> prefer support geometry
Blender-only temporary control     -> crease may be acceptable
pipeline explicitly supports it    -> crease may be acceptable
```

Do not claim that creases are universally invalid. Blender supports weighted edge creases. The reason to avoid them by default here is pipeline portability and predictable explicit topology, not an absence of Blender support.

---

# 4. SUBD_REDIRECT_CORNER_SUPPORT

## Source idea

When two support loops approach a corner, allowing both to continue around the entire mesh creates an unnecessary three-loop cluster.

Instead, the support flow can be redirected diagonally through the corner so the excess inner loops dissolve and the topology exits the corner cleanly.

## Semantic operation

```python
SUBD_REDIRECT_CORNER_SUPPORT(
    feature_id,
    corner_region,
    incoming_support_loops,
    outgoing_support_path,
)
```

## Goal

Transform:

```text
three dense parallel loops near corner
```

into:

```text
one intentional support-flow turn
with unnecessary interior loops terminated
```

## Agent procedure

1. Identify the actual feature edge being supported.
2. Identify the two support loops surrounding it.
3. Find the corner vertex/region where all loops currently continue unnecessarily.
4. Build a diagonal connection across the corner.
5. Dissolve only the redundant interior loop sections.
6. Preserve the feature-support distance.
7. Validate the surrounding curved region after SubD.

## API strategy

Prefer BMesh topology editing:

```text
resolve semantic vertices
-> create/connect diagonal edge
-> split affected faces if required
-> dissolve redundant edges
-> update normals
```

Do not depend on the Knife tool UI unless an adapter is explicitly required.

## Validation

PASS requires:

- feature edge unchanged;
- support width unchanged within tolerance;
- no accidental n-gon self-intersection;
- redirected topology remains manifold;
- evaluated corner preserves intended sharpness;
- edge density outside the feature region is reduced;
- no new visible pinch is introduced.

---

# 5. SUBD_BUILD_SUPPORT_BEVEL

## Source idea

Instead of manually inserting support loops one by one around a hard boundary, selected feature edges can be beveled with a controlled profile to generate two support edges.

The tutorial uses approximately:

```text
segments = 2
profile/shape = 1
outer miter = ARC
```

then manually connects/cleans the corner topology.

## Semantic operation

```python
SUBD_BUILD_SUPPORT_BEVEL(
    feature_edges,
    support_distance,
    segments=2,
    profile=1.0,
    outer_miter="ARC",
)
```

## Interpretation

This bevel is not primarily a cosmetic bevel.

It is a **support-loop generator**.

The produced edges control the Catmull-Clark transition around a feature boundary.

## Agent rules

- Use a width derived from target edge softness, not an arbitrary default.
- Preserve original feature position.
- Avoid bevel widths that collide with nearby topology.
- Prefer a consistent support width within one manufactured edge family.
- After beveling a corner, inspect whether Arc miter topology should be simplified or redirected.

## API strategy

Preferred:

- BMesh bevel operation where suitable;
- direct mesh reconstruction for deterministic cases;
- operator fallback only behind a tested adapter.

## Important

A successful bevel operation is not a successful SubD result.

Always evaluate the post-Subdivision surface.

---

# 6. SUBD_REPAIR_CURVED_PINCHING

## Source idea

Pinching around a hard detail embedded in a curved surface is often caused by insufficient or uneven base tessellation.

The tutorial demonstrates that the same feature on a denser sphere produces less obvious pinching.

## Diagnostic model

Potential causes:

```text
P1 insufficient radial tessellation
P2 support loops too close together
P3 support loops enter curvature at poor angles
P4 high-valence pole too close to visible curvature
P5 asymmetric vertex spacing
P6 feature topology too dense relative to host surface
P7 normals/topology errors
```

## Agent procedure

1. Render/evaluate without changing subdivision level.
2. Locate the pinch region.
3. Measure host-surface edge spacing around it.
4. Compare detail-loop spacing to surrounding cage spacing.
5. Inspect extraordinary vertices and valence.
6. If the host surface is genuinely under-resolved, add controlled base tessellation.
7. Reproject/relax vertices to preserve the original curvature.
8. Re-evaluate.

## Base-resolution increase

Allowed when:

- a curved surface has too few vertices to accommodate the requested feature;
- the added topology remains reasonably even;
- the increase improves curvature rather than simply hiding broken connectivity.

## Material and distance criterion

The agent may accept residual low-level pinching if:

- it is below the asset's visual tolerance;
- it is invisible at intended screen size;
- the material does not reveal it under expected highlights;
- the reference does not require closer fidelity.

This decision must be reported, not silently ignored.

---

# 7. SUBD_TERMINATE_LOCAL_DENSITY

## Source idea

A local feature may require several extra loops, but those loops should not necessarily continue through the entire mesh.

The tutorial terminates extra topology by moving neighboring vertices, connecting outer vertices, and dissolving the interior edges.

## Semantic operation

```python
SUBD_TERMINATE_LOCAL_DENSITY(
    dense_region,
    termination_direction,
    target_loop_count,
)
```

## Purpose

Transition from:

```text
high local loop density
```

to:

```text
lower background loop density
```

without visible deformation.

## Topological concept

This is a controlled edge-flow reduction.

The agent should create a transition topology rather than allowing every loop to propagate globally.

## Rules

- Place termination away from the strongest highlight/curvature when possible.
- Do not stack many poles in a tiny area.
- Keep edge-length change gradual.
- Prefer termination on flatter regions.
- Preserve the host silhouette.

## Repetition

The technique may be applied multiple times if several density reductions are required.

Each reduction must be individually validated.

## Example use cases

- button cluster on a control panel;
- local screw recesses;
- dense vent area;
- switch array;
- connector plate;
- local embossed feature.

---

# 8. SUBD_CURVED_CYLINDER_RECESS

## Source idea

A high-sided cylinder Booleaned directly into a curved surface may look acceptable before SubD but creates unsuitable topology for a clean subdivision cage.

The tutorial instead uses a lower-sided cylinder with edge spacing comparable to the host surface, performs the Boolean as a construction aid, then manually reconnects the resulting circular boundary into the surrounding edge flow.

## Semantic operation

```python
SUBD_CURVED_CYLINDER_RECESS(
    host_surface,
    center,
    axis,
    radius,
    depth,
    radial_segments,
)
```

## Primary principle

**Match feature resolution to host-surface resolution.**

Do not create a 64-sided circular boundary inside a host region containing only a few broad quads.

## Segment selection

The tutorial prefers powers of two as a practical modeling habit.

This skill treats that as a heuristic, not a mathematical requirement.

Preferred segment candidates may include:

```text
8, 16, 32
```

when they fit:

- feature size;
- host edge spacing;
- visible roundness;
- intended SubD level.

## Procedure

1. Estimate average host edge spacing near the recess.
2. Choose the smallest radial segment count that can represent the circular feature after SubD.
3. Create/position the cylindrical construction primitive.
4. Use Boolean Difference only as an intermediate geometric intersection if useful.
5. Capture the resulting boundary loop.
6. Remove unusable Boolean topology if necessary.
7. Route boundary vertices into nearby host loops.
8. Send left-side vertices toward compatible left-going flow, top vertices toward top-going flow, etc.
9. Reduce unnecessary edges.
10. Prefer quads where they improve predictable SubD flow, but do not distort the surface purely to avoid every triangle.
11. Add support topology around the recess.
12. Fill/repair the center or surrounding region with a predictable grid when appropriate.
13. Evaluate with SubD.

## Important

Boolean is not the final topology solution in this operation.

It is an intersection/construction aid.

## Quad policy

The source tutorial prefers keeping the region in quads when easy.

This skill uses a stricter rule:

```text
prefer clean predictable quads in deformation/highlight-critical regions;
allow controlled triangles where they do not create visible SubD artifacts and pipeline policy permits them.
```

Do not create tortured quads solely to satisfy an all-quad ideology.

## Grid Fill

Grid Fill may be used when the boundary conditions are appropriate.

The agent must verify:

- boundary continuity;
- compatible vertex count;
- resulting grid orientation;
- preservation of curvature.

---

# 9. SUBD_BUILD_POLE_SAFE_SPHERE

## Source idea

A conventional UV sphere concentrates many edges at the top and bottom poles. Under SubD and especially displacement, this can produce visible star-like artifacts.

The tutorial proposes two alternatives:

```text
icosphere -> subdivide -> spherize
```

or

```text
cube -> subdivide -> spherize
```

for more even tessellation.

## Semantic operation

```python
SUBD_BUILD_POLE_SAFE_SPHERE(
    radius,
    topology="CUBE_SPHERE" | "ICO_SPHERE",
    base_resolution,
)
```

## Decision

### UV sphere

Use only when:

- poles are hidden or irrelevant;
- the downstream operation tolerates poles;
- UV layout or latitude/longitude topology is specifically desired.

### Icosphere-derived sphere

Use when:

- distributed tessellation is desired;
- triangular starting topology is acceptable;
- subsequent subdivision/spherization fits the pipeline.

### Cube-sphere

Use when:

- relatively even quad distribution is desired;
- displacement quality matters;
- six-patch topology is acceptable.

## Spherization

The agent may use:

- To Sphere behavior;
- Cast-to-sphere logic;
- direct mathematical normalization of vertices to radius.

For autonomous code, direct deterministic geometry math is preferred when equivalent.

Example concept:

```python
p = vertex.co
vertex.co = p.normalized() * radius
```

subject to object-space and transform correctness.

## Validation

Evaluate:

- radial error;
- edge-length variance;
- pole artifact presence;
- displacement test if displacement is part of the intended workflow.

---

# 10. SUBD_REPAIR_BRANCH_JUNCTION

## Source idea

When one region splits into two branches, support loops can create three nearby directions of edge flow and a messy dense junction.

The tutorial resolves the junction by making two edges meet centrally, removing redundant edges, then introducing a better-spaced center loop and redirecting the flow.

## Semantic operation

```python
SUBD_REPAIR_BRANCH_JUNCTION(
    junction_region,
    branch_a,
    branch_b,
    support_family,
)
```

## Goal

Convert an uncontrolled multi-direction loop collision into a readable topology junction.

## Rules

- Preserve the two actual branches.
- Merge or redirect only support topology, not primary shape topology.
- Avoid two nearly coincident support loops after the junction.
- Introduce a central transition loop if it improves spacing.
- Place extraordinary vertices away from the strongest visible curvature when possible.

## Validation

Inspect:

- branch symmetry/asymmetry required by reference;
- support width through junction;
- limit-surface smoothness;
- local valence;
- no accidental crease or flattening.

---

# 11. SUBD_CURVED_CYLINDER_PROTRUSION

## Source idea

A cylindrical shape protruding from a surface can be created with Boolean Union, but the resulting topology generally requires cleanup for SubD.

The tutorial shows a cleaner construction approach:

```text
select region
-> inset
-> circularize
-> extrude
-> add supporting loops
```

On curved surfaces, the circularization operation must not flatten the host surface.

## Semantic operation

```python
SUBD_CURVED_CYLINDER_PROTRUSION(
    host_region,
    center,
    radius,
    height,
    axis,
    support_width,
)
```

## Preferred construction

1. Resolve a sufficiently regular host face region.
2. Create an inset boundary.
3. Circularize the boundary while preserving host curvature.
4. Extrude along intended local axis/normal.
5. Add radial/axial supporting topology.
6. Validate transition into the host surface.

## LoopTools note

The source tutorial uses the LoopTools Circle function and says to disable flattening on a curved surface.

For this AI skill:

- LoopTools is an optional capability, not a required dependency;
- current Blender distribution may expose LoopTools through the Blender Extensions ecosystem rather than guaranteeing it is already enabled;
- the agent must capability-check it before use;
- a deterministic mathematical/BMesh circularization fallback is preferred for portable automation.

## Circularization fallback

Given boundary vertices and a fitted local plane/frame:

```text
1. estimate center
2. estimate local normal
3. project boundary to local 2D frame
4. compute target angular positions
5. move vertices toward target radius
6. preserve/restitch the host curvature component rather than flattening the full region
```

On curved hosts, preserve each vertex's signed offset along the host surface normal or reproject the circularized boundary back to the evaluated host surface.

## Boolean fallback

Boolean Union remains allowed when:

- speed matters more than clean SubD topology;
- the asset will not use SubD;
- a later retopology pass is planned;
- the Boolean result is only a guide.

It is not the default for a final clean SubD cage.

---

# 12. SUBD_TOPOLOGY_AUDIT

The agent must not assess topology only by counting quads.

A SubD audit should inspect at least:

```text
control-cage manifold state
face degeneracy
edge-length distribution
support-loop spacing
local density ratio
extraordinary-vertex valence
pole placement
surface curvature around poles
triangle/ngon placement
feature-boundary continuity
modifier configuration
evaluated surface deviation
visible pinching
```

## Recommended report

```python
{
    "operation": "SUBD_TOPOLOGY_AUDIT",
    "object": "Asset_HIGH",
    "subdivision_levels": 2,
    "non_manifold_edges": 0,
    "degenerate_faces": 0,
    "extraordinary_vertices": 14,
    "high_valence_visible_region": 0,
    "max_local_edge_length_ratio": 2.1,
    "support_loop_collisions": 0,
    "visible_pinching_regions": [],
    "status": "PASS"
}
```

The exact thresholds are project/asset dependent.

---

# 13. Evaluated-surface validation

The base cage can appear clean while the final surface is wrong.

Validation should use the evaluated dependency-graph result when possible.

Conceptual Blender API pattern:

```python
depsgraph = bpy.context.evaluated_depsgraph_get()
obj_eval = obj.evaluated_get(depsgraph)
```

Measure visible results on evaluated geometry rather than assuming modifier settings guarantee quality.

---

# 14. Curvature and highlight validation

Many SubD defects are most obvious under grazing highlights.

The QA layer should support a neutral diagnostic material and light rig.

Recommended modes:

```text
MATCAP / neutral glossy
wireframe-over-shaded
flat color + grazing light
curvature-sensitive studio light
```

A topology change is rejected if it creates a visible highlight kink not present in the reference or approved checkpoint.

---

# 15. Displacement stress test

The source tutorial points out that dense local tessellation and UV-sphere poles become especially visible under displacement.

For assets intended for displacement, the agent should optionally perform a diagnostic test using a controlled procedural displacement.

Purpose:

- expose uneven tessellation;
- expose pole artifacts;
- expose pinching;
- reveal abrupt density changes.

This diagnostic displacement is not part of the final asset unless explicitly requested.

---

# 16. Local density metric

Define a local edge-density estimate from average edge length in a region.

Example conceptual metric:

```text
density ~= 1 / mean_edge_length
```

Compare:

```text
feature region density
vs
neighboring host density
```

A very high ratio is not automatically wrong, but it triggers review.

The objective is not uniform tessellation everywhere.

The objective is **controlled and justified density**.

---

# 17. Pole policy

An extraordinary vertex is not automatically a topology error.

## Acceptable pole

- on relatively flat surface;
- away from silhouette;
- away from sharp specular highlight path;
- away from deformation-critical zone;
- necessary for clean density transition.

## Risky pole

- on tight curvature;
- directly next to a support loop;
- at a feature corner;
- inside a circular recess transition;
- where several density transitions collide.

## Agent rule

Do not optimize for zero poles.

Optimize for **well-placed poles**.

---

# 18. Triangle and n-gon policy

The tutorial often prefers quads because of predictable SubD flow.

This skill defines:

```text
QUAD        preferred in curved/highlight-critical SubD regions
TRIANGLE    allowed when its evaluated effect is validated
N-GON       allowed only when planar/stable or when subdivision behavior is explicitly verified
```

Do not automatically rewrite a stable solution into worse geometry merely to satisfy an all-quad metric.

---

# 19. Edge-flow decision table

| Condition | Preferred action |
|---|---|
| two support loops continue unnecessarily around a corner | `SUBD_REDIRECT_CORNER_SUPPORT` |
| need support loops around selected hard boundary | `SUBD_BUILD_SUPPORT_BEVEL` |
| curved region pinches around detail | `SUBD_REPAIR_CURVED_PINCHING` |
| local detail creates global unnecessary loops | `SUBD_TERMINATE_LOCAL_DENSITY` |
| circular recess enters curved surface | `SUBD_CURVED_CYLINDER_RECESS` |
| sphere poles produce star/displacement artifacts | `SUBD_BUILD_POLE_SAFE_SPHERE` |
| support flow collides at Y/branch junction | `SUBD_REPAIR_BRANCH_JUNCTION` |
| cylinder protrudes from surface | `SUBD_CURVED_CYLINDER_PROTRUSION` |
| unsure if cage is production-safe | `SUBD_TOPOLOGY_AUDIT` |

---

# 20. Reconstruction integration

When used with the Reconstruction Layer, topology is subordinate to reference fidelity.

The agent must never move a locked silhouette or dimension simply to obtain prettier topology.

Priority:

```text
1. explicit dimensional constraints
2. canonical-view shape
3. MUST features
4. surface continuity
5. topology elegance
```

If a clean topology solution cannot preserve the locked shape, report the conflict rather than altering the reference-derived form silently.

---

# 21. Integration with panel-line skill

The existing skill:

`blender-agent-procedural-hard-surface-panel-lines.md`

creates high-poly grooves and seams.

This SubD skill should be invoked when such detail:

- sits on a curved SubD shell;
- creates pinching;
- requires local density changes;
- must terminate support loops;
- interacts with a circular recess/protrusion.

The panel-line semantic feature remains the source of design intent.

This skill controls the surrounding SubD topology needed to support it.

---

# 22. Suggested service API

```python
class SubDTopologyService:
    def redirect_corner_support(self, *, target, feature_id, region, params):
        ...

    def build_support_bevel(self, *, target, edges, width, params):
        ...

    def repair_curved_pinching(self, *, target, region, tolerance):
        ...

    def terminate_local_density(self, *, target, region, target_density):
        ...

    def curved_cylinder_recess(self, *, target, center, axis,
                               radius, depth, radial_segments=None):
        ...

    def build_pole_safe_sphere(self, *, radius, topology, resolution):
        ...

    def repair_branch_junction(self, *, target, region, branches):
        ...

    def curved_cylinder_protrusion(self, *, target, region, radius,
                                   height, axis):
        ...

    def audit(self, *, target, subdivision_levels=2):
        ...
```

The LLM should call semantic operations instead of regenerating low-level BMesh code for every asset.

---

# 23. Suggested Python package layout

```text
blender_agent/
|
+-- topology/
|   +-- subd_analysis.py
|   +-- edge_flow.py
|   +-- density.py
|   +-- poles.py
|   +-- curvature.py
|
+-- hard_surface/
|   +-- subd_support.py
|   +-- circular_features.py
|   +-- branch_junctions.py
|
+-- primitives/
|   +-- cube_sphere.py
|   +-- ico_sphere.py
|
+-- validation/
    +-- subd_surface.py
    +-- pinching.py
    +-- tessellation.py
```

---

# 24. Transaction rule

Topology rewrites can be destructive.

Preferred workflow:

```text
accepted checkpoint
-> duplicate/generated working cage
-> perform topology rewrite
-> evaluate SubD
-> compare against locked geometry/reference
-> validate topology
-> commit replacement only if PASS
```

If validation fails, preserve the previous accepted cage.

---

# 25. Error taxonomy

```text
SD001 TARGET_NOT_MESH
SD002 SUBD_MODIFIER_MISSING_OR_UNRESOLVED
SD003 CORNER_FLOW_NOT_RESOLVED
SD004 SUPPORT_WIDTH_COLLISION
SD005 PINCHING_ABOVE_TOLERANCE
SD006 LOCAL_DENSITY_TRANSITION_FAILED
SD007 RECESS_BOUNDARY_FLOW_FAILED
SD008 POLE_ARTIFACT_FAILED
SD009 BRANCH_JUNCTION_FLOW_FAILED
SD010 CIRCULARIZATION_FAILED
SD011 CURVATURE_LOST
SD012 NON_MANIFOLD_RESULT
SD013 LOCKED_SHAPE_REGRESSION
SD014 EVALUATED_SURFACE_INVALID
SD015 PERFORMANCE_BUDGET_EXCEEDED
```

Warnings:

```text
SDW01 HIGH_LOCAL_DENSITY_RATIO
SDW02 HIGH_VALENCE_POLE_NEAR_VISIBLE_CURVATURE
SDW03 RESIDUAL_PINCHING_ACCEPTED_BY_SCREEN_TOLERANCE
SDW04 CREASE_USED_IN_PORTABLE_PIPELINE
SDW05 LOOPTOOLS_UNAVAILABLE_USING_FALLBACK
SDW06 BOOLEAN_USED_AS_INTERMEDIATE_CONSTRUCTION
```

---

# 26. Required validation gates

## Cage gate

```text
[ ] manifold unless explicitly intended otherwise
[ ] no degenerate faces
[ ] no accidental duplicate geometry
[ ] support loops correspond to real features
[ ] local density is justified
[ ] no uncontrolled dense loop propagation
[ ] pole placement reviewed
```

## Evaluated SubD gate

```text
[ ] silhouette preserved
[ ] explicit dimensions preserved
[ ] feature edge softness correct
[ ] no visible unacceptable pinching
[ ] no star-like pole artifact in relevant view
[ ] no unwanted flattening of curved host
[ ] no highlight kink introduced
```

## Runtime/high-poly gate

```text
[ ] subdivision density is appropriate for intended use
[ ] high-poly cage is not exported as runtime mesh by accident
[ ] bake source remains reproducible
[ ] control cage remains editable or reconstructable
```

---

# 27. Anti-patterns

The agent must not:

```text
add support loops through the entire mesh just because Loop Cut can do it;
judge topology only from the unsmoothed cage;
increase SubD levels to hide bad topology;
use extremely high-sided Boolean cylinders on low-density curved hosts;
place multiple density-termination poles in the same highlight-critical area;
use UV-sphere poles in displacement-critical hero regions without review;
flatten curved host surfaces while circularizing an extrusion boundary;
assume LoopTools is installed and enabled;
use crease as the default solution for every hard edge;
force every triangle into a distorted quad;
move reference-locked geometry only to make topology prettier;
accept a Boolean result as clean SubD topology without validation;
return PASS only because Blender completed the operation without an exception.
```

---

# 28. Compact autonomous-agent instruction

When working on a SubD hard-surface mesh:

```text
1. Identify which edges define real shape and which are only support topology.
2. Evaluate the current mesh under the intended Subdivision Surface level.
3. Detect unnecessary support-loop propagation, density clusters, poles and pinching.
4. Redirect support loops around corners instead of carrying every loop globally.
5. Generate support pairs with a controlled bevel when appropriate.
6. Terminate local density away from strong curvature/highlights.
7. Match circular-feature resolution to host-surface resolution.
8. For curved cylindrical recesses, treat Boolean as a construction aid and rebuild clean surrounding flow.
9. Prefer pole-safe sphere topology when poles/displacement would be visible.
10. Repair branch junctions so support flow does not collide in dense three-way clusters.
11. For cylindrical protrusions, prefer inset -> curvature-preserving circularization -> extrusion over an unclean Boolean union.
12. Inspect both cage and evaluated surface.
13. Validate silhouette, dimensions, curvature, pinching, edge spacing, poles and performance.
14. Preserve the previous accepted cage if the rewrite fails.
```

---

# 29. What comes directly from the supplied tutorial

The following ideas are directly derived from the supplied transcript:

- redirecting support loops diagonally around corners and dissolving redundant loops;
- generating support loops with a two-segment bevel using a strong profile and Arc outer miter;
- increasing host tessellation when a curved surface does not have enough topology to support a detail cleanly;
- terminating extra local loops instead of carrying them through the entire model;
- rebuilding cylindrical recess topology manually after using a lower-resolution Boolean cutter;
- preferring lower, controlled cylinder segment counts and matching their spacing to the surrounding mesh;
- using icosphere- or cube-derived spheres to avoid UV-sphere pole artifacts under SubD/displacement;
- cleaning three-way support-loop junctions by redirecting/merging the flow;
- creating cylindrical protrusions from inset and circularized host topology instead of relying on Boolean Union;
- preserving curvature when circularizing a region on a curved host surface.

---

# 30. Project adaptation beyond the tutorial

The following parts are deliberate agent/pipeline extensions rather than claims made explicitly in the tutorial:

- semantic `SUBD_*` operations;
- BMesh/data-API-first execution;
- evaluated-geometry QA;
- dimension/reference regression protection;
- topology audit metrics;
- transaction/checkpoint behavior;
- explicit pole and triangle policies;
- capability check and non-LoopTools circularization fallback;
- error taxonomy;
- high-poly/game-runtime separation;
- integration with the project's Reconstruction Layer and panel-line skill.

These adaptations are required because an autonomous agent needs deterministic contracts and validators rather than manual modeling intuition alone.

---

# 31. Blender implementation notes

Current Blender documentation confirms the core mechanisms used by this skill:

- Subdivision Surface uses Catmull-Clark or Simple subdivision and support edge loops can control sharpness;
- weighted edge creases are supported by Blender;
- bevel supports outer miter modes including Arc;
- Grid Fill creates structured quad grids from appropriate boundaries;
- To Sphere / sphere-casting operations exist for producing spherical distributions;
- LoopTools exists in the Blender Extensions ecosystem, so an automated agent must not assume it is enabled in every runtime.

Before relying on exact RNA/operator names, verify them against the Blender version targeted by the project.

Target project version for this repository: Blender 5.1.x.

---

# 32. Architectural conclusion

This skill teaches the agent that SubD topology is not a cosmetic cleanup pass.

It is a **surface-control system**.

The durable reasoning should be:

```text
feature requires a surface behavior
        ->
choose topology flow
        ->
place support density only where needed
        ->
redirect/terminate loops intentionally
        ->
place poles in low-risk regions
        ->
match local feature resolution to host curvature
        ->
evaluate Catmull-Clark result
        ->
repair measurable artifacts
```

The goal is not the prettiest wireframe screenshot.

The goal is the simplest controllable cage that reproduces the intended shape, survives subdivision predictably, remains editable, and does not create unnecessary tessellation or visible surface artifacts.