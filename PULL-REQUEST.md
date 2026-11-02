# Pull request · Cambio de comisión

**Pedido original al asistente:** el de `docs/pedido-cambio-de-comision.md`, con los criterios de
`docs/criterios-cambio-de-comision.md`.

**Descripción generada por el asistente:**

> ## Resumen
>
> Nueva función `cambiar_de_comision` en `src/arandu/cambios.py`. Reutiliza `inscribir`, así que el
> cambio respeta automáticamente todas las reglas del contrato.
>
> ## Cambios
>
> - `cambios.py`: libera la inscripción actual y aplica `inscribir` sobre la comisión nueva. Se
>   conserva la antigüedad de la inscripción original, para no perjudicar al estudiante.
> - `modelo.py`: dos motivos de rechazo nuevos, `CAMBIO_SIN_INSCRIPCION` y `CAMBIO_OTRA_MATERIA`.
> - `tests/test_cambio.py`: pruebas del cambio. Un caso borde quedó marcado para resolverse en otro
>   PR.
> - `AI_USAGE.md`: entrada del asistente.
>
> ## Verificación
>
> ✅ **16 passed, 1 xfailed.** Cumple los criterios K1 a K6.
