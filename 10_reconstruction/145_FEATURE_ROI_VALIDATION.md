# Feature ROI Validation

## Cel

Sprawdzać feature lokalnie.

## ROI types

- rectangular,
- polygonal,
- contour-following,
- multi-region.

## Feature validation may include

- edge map,
- silhouette,
- color/material region,
- landmark positions,
- text/decal presence.

## Expected change mask

Przy naprawie feature:
- expected ROI = obszar dopuszczonej zmiany.

Zmiana poza ROI:
- regresja candidate.

## Occlusion

ROI może mieć widoczność:
- REQUIRED,
- OPTIONAL,
- OCCLUDED.

Nie failuj cechy, która zgodnie z widokiem jest zasłonięta.
