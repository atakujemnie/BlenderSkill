# v0.15 Location Skill Registry

| Skill ID | Purpose | Canonical implementation |
|---|---|---|
| `LOCATION_REFERENCE_INGEST` | classify location-level references, dimensions and composition owners | `13_environment_assembly/301` |
| `LOCATION_SCENE_GRAPH` | validate LOCATION→ZONE→SYSTEM→ASSET→INSTANCE graph | `13_environment_assembly/302`; `executors/location_scene_graph.py` |
| `LOCATION_ASSET_MANIFEST` | track required assets and proxy/final state | `13_environment_assembly/303`; `executors/location_asset_manifest.py` |
| `LOCATION_DESIGN_SYSTEM_GATE` | require persistent location design language before asset proliferation | `13_environment_assembly/304`; `executors/location_design_system_gate.py` |
| `ARCHITECTURAL_ASSEMBLY` | build and validate modular envelope | `13_environment_assembly/305` |
| `SPACE_ZONING` | define public/service/transition zones and capacity intent | `13_environment_assembly/306` |
| `SPATIAL_RELATION_GATE` | validate semantic inter-object placement relations | `13_environment_assembly/307`; `executors/spatial_relation_gate.py` |
| `LOCATION_CLEARANCE_GATE` | validate guest/service/door and object clearances | `13_environment_assembly/308`; `executors/clearance_gate.py` |
| `LOCATION_PLACEMENT_ANCHOR` | canonical position/orientation ownership | `13_environment_assembly/309` |
| `HERO_COMPOSITION` | preserve focal anchors before loose population | `13_environment_assembly/310` |
| `FURNITURE_CLUSTER_GRAMMAR` | compose table/chair/booth clusters as units | `13_environment_assembly/311` |
| `LOCATION_INTERPENETRATION_GATE` | reject architecture/asset penetrations | `13_environment_assembly/312` |
| `LOCATION_MATERIAL_LIGHTING_LANGUAGE` | apply shared material and light families | `13_environment_assembly/313` |
| `LOCATION_STAGE_BARRIER` | prevent later population before earlier closure | `13_environment_assembly/314`; `executors/location_stage_barrier.py` |
| `LOCATION_REFERENCE_FIDELITY_GATE` | validate global layout and composition against references | `13_environment_assembly/315`; `executors/location_reference_fidelity_gate.py` |
| `LOCATION_COMPLETENESS_GATE` | final non-compensating location acceptance | `13_environment_assembly/316`; `executors/location_completeness_gate.py` |
| `LOCATION_RUNTIME_PARTITION` | partition/instance accepted location for runtime | `13_environment_assembly/317` |
| `LOCATION_DEFINITION_OF_DONE` | named completion levels for environments | `13_environment_assembly/318` |
