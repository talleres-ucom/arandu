# AGENTS.md · Arandu (inscripción a materias)

## Cómo se verifica un cambio
- Instalar una vez con `uv sync`; correr las pruebas con `uv run pytest`.
- Una tarea está terminada solo si la suite completa pasa, sin pruebas salteadas.

## Dónde está el contrato
- Reglas R1 a R8: `docs/reglas-del-dominio.md`. Si el código y el contrato no coinciden, manda el
  contrato.
- Cambio de comisión: `docs/criterios-cambio-de-comision.md` (K1 a K6).

## Qué no se toca
- Las pruebas existentes de `tests/`. Si una prueba parece contradecir un criterio, detenerse y
  explicar la contradicción; no modificarla ni saltearla.

## Al terminar cada tarea
- Agregar una entrada al final de `AI_USAGE.md` con: herramienta y modelo, qué se pidió, nivel
  declarado, cómo se verificó (comando y resultado) y el hash del commit.
