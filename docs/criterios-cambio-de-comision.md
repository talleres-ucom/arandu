# Criterios de aceptación · Cambio de comisión

Escritos por la cátedra a partir del pedido. Si el código y estos criterios no coinciden, mandan los
criterios. Todos usan los datos de `src/arandu/fixtures.py`, más la comisión **PROG1-C** (Programación
I, **cupo 1**, sábados de 8:00 a 10:00) y la comisión **RED1-J** (Redes I, cupo 30, jueves de 19:00 a
20:00), que agrega cada prueba. **T0** es el 10-09-2026 a las 20:00, dentro de la ventana de
inscripción; «20:05» quiere decir T0 más 5 minutos.

Recordatorio de horarios: PROG1-A es los miércoles de 19:00 a 21:30 y PROG1-B, los jueves de 19:00 a
21:30.

## K1 · El cambio se acepta

- **Dado** que e2 está inscripto en PROG1-A (20:00),
- **cuando** a las 20:05 pide cambiar de PROG1-A a PROG1-B,
- **entonces** se acepta, e2 queda inscripto en PROG1-B y su inscripción en PROG1-A queda dada de
  baja.

## K2 · Si el cambio se rechaza, conserva su lugar

- **Dado** que PROG1-C está llena (e3 inscripto) y que e2 está inscripto en PROG1-A,
- **cuando** e2 pide cambiar de PROG1-A a PROG1-C a las 20:05,
- **entonces** se rechaza con `R3_SIN_CUPO` y e2 **sigue inscripto en PROG1-A**.

## K3 · Solo dentro de la misma materia

- **Dado** que e2 está inscripto en PROG1-A,
- **cuando** pide cambiar de PROG1-A a MAT1-A (otra materia) a las 20:05,
- **entonces** se rechaza con `CAMBIO_OTRA_MATERIA` y e2 sigue inscripto en PROG1-A y no en MAT1-A.

## K4 · El cambio respeta las demás reglas

- **Dado** que e2 está inscripto en PROG1-A y en RED1-J (jueves de 19:00 a 20:00),
- **cuando** pide cambiar de PROG1-A a PROG1-B (jueves de 19:00 a 21:30) a las 20:05,
- **entonces** se rechaza con `R5_CHOQUE_DE_HORARIOS` y e2 sigue inscripto en PROG1-A.

## K5 · Sin inscripción no hay cambio

- **Dado** que e3 no está inscripto en PROG1-A,
- **cuando** pide cambiar de PROG1-A a PROG1-B a las 20:05,
- **entonces** se rechaza con `CAMBIO_SIN_INSCRIPCION` y e3 no queda inscripto en PROG1-B.

## K6 · La nueva inscripción lleva el instante del cambio

- **Dado** que e2 se inscribió en PROG1-A a las 20:00,
- **cuando** a las 20:05 cambia a PROG1-B,
- **entonces** su inscripción activa en PROG1-B tiene como instante las 20:05.
