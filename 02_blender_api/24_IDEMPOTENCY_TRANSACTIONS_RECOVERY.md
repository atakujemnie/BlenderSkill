# Idempotency, Transactions and Recovery

## Idempotency

Uruchomienie tego samego kroku drugi raz nie powinno:
- tworzyć kolejnego `.001`,
- podwajać modifiera,
- dodawać drugiego materiału,
- ponownie przesuwać obiektu,
- mnożyć helper objects.

## Pattern: get-or-create

```python
obj = bpy.data.objects.get(name)
if obj is None:
    obj = create_object(name)
```

## Tagowanie

Dodawaj custom properties:
```python
obj["ai_asset_id"] = "bench_A"
obj["ai_stage"] = "blockout"
obj["ai_feature_ids"] = "F001,F002"
```

Umożliwia to znalezienie obiektu bez polegania na nazwie.

## Transaction boundary

Przed ryzykownym etapem:
- zapisz plik,
- lub utwórz backup kolekcji/obiektu,
- lub duplikuj źródłową siatkę jako hidden recovery copy.

## Małe transakcje

Lepsze:
1. wykonaj rowek,
2. sprawdź,
3. wykonaj bevel,
4. sprawdź.

Gorsze:
1. boolean,
2. bevel,
3. join,
4. apply,
5. triangulate,
6. delete helpers,
7. dopiero render.

## Recovery

Naprawa powinna cofać się do ostatniego poprawnego checkpointu, a nie wykonywać kolejne nakładki maskujące problem.
