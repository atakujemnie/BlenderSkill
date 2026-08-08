# Context, Mode and Selection

## Ukryty stan

Najczęstsze źródła błędów automatyzacji:
- niewłaściwy mode,
- inny active object,
- inny view layer,
- obiekt wyłączony z widoku,
- błędna selection,
- brak odpowiedniego area/region dla operatora.

## Stabilny baseline

Przed operacją wymagającą Object Mode:
1. ustal aktywny view layer,
2. znajdź obiekt jawnie,
3. jeżeli potrzeba — przejdź do Object Mode,
4. ustaw active object,
5. ustaw selection tylko dla wymaganych obiektów,
6. wykonaj operator,
7. nie zakładaj, że selection pozostało bez zmian.

## `temp_override`

Jeżeli operator wymaga konkretnego kontekstu, używaj jawnego override zamiast przypadkowej zależności od aktualnego UI.

Schemat:
```python
with bpy.context.temp_override(
    active_object=obj,
    object=obj,
    selected_objects=[obj],
    selected_editable_objects=[obj],
):
    if bpy.ops.object.some_operator.poll():
        bpy.ops.object.some_operator()
```

Dokładne pola override zależą od operatora.

## Mode rule

Nie przełączaj wielokrotnie:
`OBJECT -> EDIT -> OBJECT -> EDIT`
dla serii prostych zmian topologii.

Jeżeli pipeline jest proceduralny, rozważ jedną sesję BMesh.

## Selection rule

Selection jest interfejsem użytkownika, nie identyfikatorem logiki biznesowej skryptu.
Logika powinna trzymać referencje do obiektów.
