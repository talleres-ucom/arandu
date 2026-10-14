# Registro de uso de IA

Una entrada por tarea delegada. Se completa **antes** de empezar, no al final:
declarar el nivel despues es narrar lo que paso, no decidirlo.

## Entrada modelo

**Tarea:** que le pedi exactamente
**Nivel declarado:** N0 / N1 / N2 / N3 / N4
**Por que ese nivel:** la dimension que lo limito — reversibilidad, alcance del dano,
verificabilidad o sensibilidad del contexto
**Como lo verifique:** que corri o que compare, no "lo lei"
**Que cambie de lo que me devolvio:** y por que
**Sorpresas:** algo que hizo y no estaba en lo pedido

---

## Entradas

**Tarea:** La regla R4 no tiene ninguna prueba en la suite. Hay que escribir pruebas que cubran R4 tal
como la define el contrato, en docs/reglas-del-dominio.md, sección 3.
Los datos de fixtures.py no alcanzan para inscribir a un estudiante en siete materias sin
choques. Las pruebas pueden armar sus propios datos, como hace
test_correlativa_cursada_y_reprobada_no_habilita.
**Nivel declarado:** N3
**Por que ese nivel:** la dimension que lo limito — reversibilidad, alcance del dano,
verificabilidad o sensibilidad del contexto. La tarea toca una regla contractual del dominio y modifica la evidencia de regresion; no es solo refactor, pero tampoco es un cambio riesgoso a
produccion.
**Como lo verifique:** corrí la suite relevante con `python -m pytest tests/test_casos_limitrofes.py -q` y confirmé que las pruebas de R4 pasan aplicando el contrato de la especificacion.
**Que cambie de lo que me devolvio:** pedí una solucion basada en datos propios del test, no en fixtures fijos, y ajusté la prueba para que construya 7 comisiones distintas sin choques y verifique el limite exacto de 6 inscripciones activas. Esto fue necesario porque el contrato dice que el estudiante no puede superar 6 materias activas en el mismo periodo y la estructura original del fixture no alcanza para ese caso.
**Sorpresas:** el punto mas importante fue que el contrato exige un limite exacto de 6, no solo un rechazo a partir de 7; eso me obligó a completar dos casos frontera: 6 aceptadas y la 7ma rechazada, ademas de verificar que una baja libera el lugar.

**Tarea:** Reporte de la mesa de ayuda: «Me di de baja y el lugar no se liberó». Debe encontrarse el defecto que hace que una baja no libere cupo y dejar una prueba que falle antes del arreglo y pase despues.
**Nivel declarado:** N3
**Por que ese nivel:** el daño tiene impacto directo sobre disponibilidad real del cupo, y la validacion recae sobre un comportamiento observable del contrato de R3 y R6.
**Como lo verifique:** agregué la prueba de regresion y la ejecuté en estado defectuoso para confirmar la falla; luego corrijo la implementacion y vuelvo a correr la suite relevante.
**Que cambie de lo que me devolvio:** lo que pedí fue una prueba de regresion centrada en el caso de baja y un arreglo minimo que marca la inscripcion como BAJA para que el cupo se libere de inmediato y no siga contandose como activa.
**Sorpresas:** la falla no estaba aislada en una regla: el mismo problema impacta R3, R4 y R7, porque las bajas no se consideran "inactivas" para la evaluacion.

