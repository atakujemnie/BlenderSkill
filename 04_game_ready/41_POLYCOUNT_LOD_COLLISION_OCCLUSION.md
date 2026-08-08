# Polycount, LOD, Collision and Occlusion

## Polycount

Licz trójkąty, nie tylko quady/polygons.
Runtime rasteryzacyjny finalnie operuje na trójkątach.

## LOD

LOD powinien usuwać detal według kolejności:
1. niewidoczne mikrodetale,
2. małe bevel segments,
3. drobne recess,
4. elementy niezmieniające silhouette,
5. upraszczanie dużych zakrzywień dopiero później.

Każdy LOD powinien zachować:
- globalną sylwetkę,
- pivot,
- bounds,
- główne material regions.

## Collision

Collision mesh:
- prostszy niż render mesh,
- bez drobnych szczelin,
- zgodny z funkcją gameplay.

Nie twórz perfect collision, jeżeli gameplay tego nie potrzebuje.

## Occlusion

Dla dużych obiektów rozważ:
- rozdzielenie geometryczne umożliwiające culling,
- logiczne segmenty,
- bounding volumes.

## Instancing

Asset występujący setki razy wymaga ostrzejszego budżetu niż unikalny hero prop.
