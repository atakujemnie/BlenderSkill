# Source of Truth

## Kolejność nadrzędności

### 1. User intent
Jawne polecenie użytkownika jest nadrzędne.

### 2. Approved reference
Jeżeli użytkownik zaakceptował konkretny wygląd, staje się on referencją kanoniczną.

### 3. Project asset contract
Wymiary, skala świata, texel density, naming, pivot, format eksportu, limity i standardy silnika.

### 4. Current Blender scene
Rzeczywisty stan danych jest ważniejszy niż pamięć agenta o tym, co "powinno" znajdować się w scenie.

### 5. Library rules
Niniejsze procedury.

### 6. External technical documentation
Oficjalne API i specyfikacje.

### 7. Heuristics
Doświadczenie i przypuszczenia.

## Konflikt źródeł

Jeżeli dwa źródła są sprzeczne:
- nie mieszaj ich,
- wskaż konflikt wewnętrznie,
- wybierz źródło o wyższym priorytecie,
- zachowaj informację o odrzuconej interpretacji.

## Zakaz "ulepszania referencji"

Agent nie ma prawa:
- dodawać ozdobników,
- zmieniać proporcji dla "lepszego designu",
- symetryzować świadomej asymetrii,
- upraszczać charakterystycznej cechy,
- zaokrąglać ostrych form tylko dlatego, że bevel wygląda bardziej realistycznie.

Wyjątek: wymaganie runtime lub jawna decyzja projektowa.
