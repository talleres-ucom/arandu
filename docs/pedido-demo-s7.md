# Demo de S7 · Un pedido para especificar

> «Para cuidar a los estudiantes, nadie puede tener más de dos materias el mismo día.»
>
> — Secretaría Académica

El motivo de rechazo nuevo ya está en `src/arandu/modelo.py`: `LIMITE_DIARIO`.

## Ronda A · El pedido tal cual

Prompt para el asistente:

> Implementar en Arandu el pedido de `docs/pedido-demo-s7.md`. El motivo de rechazo es
> `Motivo.LIMITE_DIARIO`. Correr las pruebas al terminar.

## Ronda B · Con criterios y pruebas

Prompt para el asistente:

> Implementar en Arandu el pedido de `docs/pedido-demo-s7.md` según los criterios de
> `docs/criterios-demo-s7.md`. Las pruebas de `tests/test_limite_diario.py` definen cuándo está
> terminado: tienen que pasar todas, junto con el resto de la suite. **No modificar ningún archivo de
> `tests/`.** Si una prueba parece contradecir los criterios, detenerse y explicar por qué.
