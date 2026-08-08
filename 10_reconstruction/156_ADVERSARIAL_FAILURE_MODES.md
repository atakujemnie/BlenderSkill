# Adversarial Failure Modes

## F1 — Single-view overfit
Front idealny, side błędny.

## F2 — Hero-view distortion
Model zdeformowany pod atrakcyjny render.

## F3 — Detail distraction
Mikrodetale dodane przed poprawną sylwetką.

## F4 — Material compensation
Ciemniejszy shader ukrywa złą geometrię.

## F5 — Symmetry hallucination
Agent odbija detal, który powinien być tylko po jednej stronie.

## F6 — Hidden-side neglect
Tył/spód są puste mimo referencji.

## F7 — Invented greebles
Dodane "sci-fi" detale bez dowodu.

## F8 — Dimension drift
Bevel/solidify zmienia total dimensions.

## F9 — Camera cheating
Przesuwanie QA camera zamiast geometrii.

## F10 — Conflict averaging
Sprzeczne widoki uśrednione.

## F11 — Apply collapse
Wczesne Apply niszczy możliwość korekty.

## F12 — Optimization regression
LOD/decimate usuwa MUST.

## F13 — Text hallucination
Agent generuje błędne logo/napis.

## F14 — Lighting baked into material
Highlight z concept artu staje się albedo.

## F15 — API context thrash
Setki operatorów i zmian selection zamiast parametrycznego batchu.

Każdy benchmark powinien zawierać przynajmniej kilka z tych pułapek.
