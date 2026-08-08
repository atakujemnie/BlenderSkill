# Asset Brief Schema

Przed modelowaniem utwórz krótki brief.

## 1. Identity
- Asset name:
- Category:
- Function:
- Environment:
- Hero / midground / background:
- Static / animated / deformable:
- Unique / modular / instanced:

## 2. Scale
- Real/world dimensions:
- Blender units:
- Character scale reference:
- Required clearances:

## 3. Viewing conditions
- Typical camera distance:
- Closest camera distance:
- Primary view angles:
- Can player walk around it:
- Can player see back/bottom/top:

## 4. Visual language
- Dominant shapes:
- Edge language:
- Symmetry:
- Repetition:
- Material families:
- Wear level:
- Manufacturing logic:

## 5. Functional decomposition
Lista części:
- structural shell,
- insert,
- panel,
- trim,
- mechanical detail,
- interactive element,
- collision volume.

## 6. Runtime constraints
- Target triangle budget:
- LOD count:
- Texture budget:
- Material slot budget:
- Collision strategy:
- Lightmap requirement:
- Export format:

## 7. Unknowns
Każdą niewiadomą oznacz:
- `BLOCKING`
- `NON_BLOCKING`
- `CAN_INFER`

Agent może rozpocząć blockout, jeśli nie istnieje `BLOCKING`.
