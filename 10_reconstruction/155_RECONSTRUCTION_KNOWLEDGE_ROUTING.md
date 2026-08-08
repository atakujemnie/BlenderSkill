# Reconstruction Knowledge Routing

Maksymalna biblioteka nie oznacza ładowania wszystkiego.

## Stage packs

### Ingest pack
103–109

### Geometry solve pack
110–123

### Surface pack
124–127

### Build pack
128–140

### QA pack
141–148

### Governance pack
149–159

## Asset-specific packs

Do tego:
- właściwy `11_playbooks`,
- engine profile,
- standard API modules.

## Token rule

Agent ładuje:
1. Reconstruction Index,
2. State Machine,
3. odpowiedni stage pack,
4. tylko playbook klasy.

Nie należy wrzucać całego `_FULL_LIBRARY.md` do każdego tool-call.
