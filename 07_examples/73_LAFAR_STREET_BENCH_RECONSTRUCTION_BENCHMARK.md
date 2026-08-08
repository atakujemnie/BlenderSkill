# Benchmark — Lafar Street Bench / ACS-BCH-200

## Purpose

Pierwszy benchmark pełnej warstwy rekonstrukcji 1:1.

Źródło:
concept sheet `LAFAR STREET BENCH — CIVIC SEATING MODULE`.

## Explicit dimensions visible on sheet

- total width: 2000 mm,
- total depth: 550 mm,
- total height: 820 mm,
- side/seat-height dimension shown: 460 mm.

Te wartości są `HARD LOCK`, o ile nowsza zatwierdzona referencja ich nie zmieni.

## Canonical views available

- hero,
- front,
- side,
- top,
- rear,
- bottom/underside,
- detail close-up.

## Material evidence

Plansza pokazuje rodziny:
- matte graphite powder coat,
- brushed aluminum,
- dark titanium composite,
- microbead texture,
- cool-blue accent lighting.

Nazwy materiałów są evidence projektowym; fizyczna interpretacja shaderów musi zostać zwalidowana wizualnie.

## High-level MUST features

### F001
Global width/depth/height.

### F002
Masywne boczne housings pełniące rolę nóg/podłokietników.

### F003
Siedzisko pomiędzy bocznymi housings.

### F004
Pochylone oparcie o niskim, szerokim profilu.

### F005
Metaliczne/aluminiowe zewnętrzne trimy biegnące po bocznych częściach.

### F006
Wąski info strip przy górnej części frontu oparcia.

### F007
Prawostronny integrated utility panel.

### F008
Cool-blue underglow przy podstawie.

### F009
Rear panel + logo ASTERA CIVIC SYSTEMS.

### F010
Underside/service-panel layout obecny na bottom view.

### F011
Charakterystyczna otwarta negative space pod siedziskiem.

### F012
Rounded/chamfered product edge language.

## Initial object decomposition proposal

- `SM_Lafar_Bench_SeatCore`
- `SM_Lafar_Bench_BackrestCore`
- `SM_Lafar_Bench_SideHousing_L`
- `SM_Lafar_Bench_SideHousing_R`
- `SM_Lafar_Bench_Trim_L`
- `SM_Lafar_Bench_Trim_R`
- `SM_Lafar_Bench_InfoStrip`
- `SM_Lafar_Bench_UtilityPanel`
- `SM_Lafar_Bench_Underglow`
- `SM_Lafar_Bench_RearPanel`
- `SM_Lafar_Bench_Underside`
- `DEC_Lafar_Bench_AsteraRear`
- optional shared fastener instances.

To jest plan startowy, nie wymóg jednego konkretnego podziału runtime.

## View authority proposal

### Width
FRONT/TOP/REAR + numeric 2000 mm.

### Depth
SIDE/TOP + numeric 550 mm.

### Height
FRONT/SIDE/REAR + numeric 820 mm.

### 460 mm dimension
SIDE/FRONT evidence; należy precyzyjnie ustalić, do której powierzchni odnosi się marker przed użyciem jako constraint lokalny.

### Backrest angle
SIDE.

### Rear logo
REAR.

### Underside
BOTTOM.

### Edge/material character
HERO + DETAIL + palette.

## Important ambiguity list

Arkusz nie podaje bezpośrednio:
- dokładnego kąta oparcia,
- szerokości side housing,
- grubości oparcia,
- promieni wszystkich narożników,
- szerokości trimu,
- dokładnych wymiarów utility panel,
- dokładnej geometrii portów,
- dokładnej głębokości panel gaps,
- dokładnej geometrii wewnętrznej underside.

Te parametry należy mierzyć z kalibrowanych widoków i oznaczać `DERIVED`, a nie udawać jawnych wartości.

## Required reconstruction checkpoints

### B0 — Registered references
Wszystkie ortho cropy skalibrowane.

### B1 — D0
Tylko total bounds + silhouette + negative space.

### B2 — D1
Seat/back/side profiles.

### B3 — D2
Trim, info strip, utility, rear/bottom panels.

### B4 — D3
Branding, ports, fasteners.

### B5 — Surface
Material segmentation i lookdev.

### B6 — Runtime
LOD/collision/export bez utraty MUST.

## Failure traps deliberately tested

- model dopasowany tylko do hero view,
- pominięcie underside,
- mirror utility panel na obie strony,
- niewłaściwa szerokość po bevel,
- dodanie losowych sci-fi panel lines,
- logo jako błędny tekst,
- underglow użyty do maskowania złej podstawy,
- zbyt duży bevel zmieniający side silhouette.

## Benchmark metrics

- 4 explicit dimension errors,
- canonical view silhouette errors,
- MUST feature pass rate,
- landmark reprojection error,
- number of unauthorized features,
- tool calls,
- failed API calls,
- repair count,
- runtime triangle/material stats.

## Benchmark target

Nie przyjmuj wyniku "looks good".
Benchmark kończy się dopiero po przejściu reconstruction Definition of Done.
