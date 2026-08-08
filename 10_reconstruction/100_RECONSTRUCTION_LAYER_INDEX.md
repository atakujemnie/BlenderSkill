# Reconstruction Layer Index

Warstwa `10_reconstruction` służy do ścisłego odtwarzania obiektu 3D na podstawie:
- concept sheet,
- blueprintów,
- rzutów ortograficznych,
- zdjęć,
- renderów,
- detail close-upów,
- wymiarów,
- opisów funkcjonalnych i materiałowych.

Nie jest to warstwa "inspiracji".
Celem jest maksymalnie wierna rekonstrukcja przy jawnej obsłudze niepewności.

## Pipeline

`INGEST -> SEGMENT -> CLASSIFY -> AUTHORITY -> REGISTER -> CONSTRAIN -> DECOMPOSE -> PLAN -> BLOCKOUT -> MATCH -> DETAIL -> SHADE -> MULTIVIEW_QA -> RUNTIME`

## Pakiety wiedzy

### Evidence
100–109

### Geometry constraints
110–123

### Surface/material evidence
124–127

### Construction planning
128–140

### Validation
141–148

### Governance
149–159

### Specialized reconstruction
160–169

## Fundamental rule

Rekonstrukcja 1:1 nie oznacza "model wygląda podobnie".
Oznacza:
- wszystkie znane wymiary są respektowane,
- wszystkie kanoniczne widoki są równocześnie zgodne,
- cechy rozpoznawcze nie giną,
- niepewne obszary są oznaczone jako niepewne,
- agent nie inventuje szczegółów, których nie da się obronić dowodem.
