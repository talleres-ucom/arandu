# Criterios · Demo de S7 · Límite diario

Preguntas que el pedido no respondía, y lo que se decidió:

| # | Pregunta | Decisión |
|---|---|---|
| 1 | ¿«Día» es una fecha o un día de la semana? | Día de la semana: las comisiones tienen franjas semanales. |
| 2 | ¿«Más de dos» deja tener dos? | Sí: dos se aceptan, la tercera se rechaza. |
| 3 | ¿Cuentan las bajas? | No: solo inscripciones activas, como en R4 y R5. |
| 4 | Una comisión con dos franjas el mismo día, ¿cuenta como dos? | No: se cuentan **materias**, no franjas. |
| 5 | ¿En qué lugar del orden de R8 se evalúa? | Después de R5 y antes de R3: R1 → R2 → R7 → R4 → R5 → límite diario → R3. |

## C1 · La tercera materia del mismo día se rechaza

- **Dado** que e2 tiene ALG1-A y MAT1-A (las dos los lunes),
- **cuando** pide una tercera comisión con clase los lunes, sin choque (RED1-M, lunes de 7:00 a 9:00),
- **entonces** se rechaza con `LIMITE_DIARIO`.

## C2 · Dos materias el mismo día se aceptan

- **Dado** que e2 tiene ALG1-A (lunes),
- **cuando** pide MAT1-A (lunes),
- **entonces** se acepta.

## C3 · Las bajas no cuentan

- **Dado** que e2 tuvo ALG1-A y MAT1-A y se dio de baja de MAT1-A,
- **cuando** pide RED1-M (lunes),
- **entonces** se acepta.

## C4 · Se cuentan materias, no franjas

- **Dado** que e2 tiene ALG1-A (lunes),
- **cuando** pide una comisión de otra materia con dos franjas el lunes (TAL-A: 7:00–8:00 y 9:00–10:00),
- **entonces** se acepta: son dos materias el lunes, aunque haya tres franjas.

## C5 · El límite se informa después de R5 y antes de R3

- **Dado** que e2 tiene ALG1-A y MAT1-A (lunes),
- **cuando** pide una tercera comisión de los lunes que además está llena (cupo 0),
- **entonces** se rechaza con `LIMITE_DIARIO`, no con `R3_SIN_CUPO`.
