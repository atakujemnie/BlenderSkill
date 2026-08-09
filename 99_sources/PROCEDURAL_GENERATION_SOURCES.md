# Procedural Generation Sources — v0.13

Research snapshot: 2026-08-09. Runtime probe always overrides this document.

## Directly relevant Blender 5.1-capable tools

### NodeToPython
- Repository: https://github.com/BrendanParmer/NodeToPython
- Release line 4.1.x states support for Blender 4.2–5.1.
- License: GPL-3.0 from v3.5.0 onward.
- v0.13 role: node-graph compiler/tooling provider; generated Python should preferably remove runtime dependency.

### Sverchok
- Repository: https://github.com/nortikin/sverchok
- README explicitly lists Blender 5.1 among supported versions.
- License: GPL-3.0.
- v0.13 role: optional parametric/computational-geometry provider, never mandatory for vegetation.

### geonodes
- Repository: https://github.com/al1brn/geonodes
- Project states Blender 5.1 support.
- v0.13 role: optional Python-first Geometry Nodes authoring provider after license/capability probe.

## Blender Extensions to probe

Blender Extensions lists Sapling Tree Gen, IvyGen, A.N.T. Landscape and Archimesh. Their presence is not treated as proof of the exact operator/API surface in the active Blender 5.1 session.

- https://extensions.blender.org/
- Sapling: optional tree provider.
- IvyGen: optional surface-growth provider.
- A.N.T. Landscape: future terrain provider.
- Archimesh: future architectural-blockout provider.

## Optional asset/scatter provider

### engon / botaniq
- Repository: https://github.com/polygoniq/engon
- extension manifest currently declares Blender minimum 4.2.0; recent releases include Blender 5.0 fixes, but 5.1 must be locally probed.
- code license: GPL-3.0-or-later; commercial asset-pack licenses remain separate.

## Source/reference systems, not v0.13 runtime dependencies

### Infinigen
- Repository: https://github.com/princeton-vl/infinigen
- BSD-3-Clause.
- Includes procedural natural-world generation and node-transpiler tooling.
- v0.13 policy: study/extract architecture and algorithms; do not import the whole framework for one asset generator.

### ProcFunc
- Repository: https://github.com/princeton-vl/procfunc
- BSD-3-Clause.
- Current installation requires `bpy==4.2.0` and Python 3.11; 5.1 support is a stated future direction.
- v0.13 policy: function-oriented procedural design reference only.

### BlenderProc
- Repository: https://github.com/DLR-RM/BlenderProc
- GPL-3.0.
- Release 2.8.0 upgraded its managed Blender runtime to 4.2.1.
- Useful source for physics-aware placement patterns; not an in-process Blender 5.1 dependency.

### The Grove
- Documentation: https://www.thegrove3d.com/learn/
- Grove Core exposes Python-driven growth; Blender add-on documentation currently lists Blender 4.2 LTS, 4.3 and 4.4.
- v0.13 policy: `VERSION_BLOCKED` on Blender 5.1 until newer compatibility is proven.

## Licensing rule

Never copy third-party source, node graphs or commercial asset packs into BlenderSkill merely because they can be called from Python. Study, adapter invocation and redistribution are distinct legal/technical actions.
