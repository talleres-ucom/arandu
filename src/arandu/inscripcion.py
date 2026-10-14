"""Orquestador del caso de inscripcion.

Este modulo es el punto de entrada del proceso de negocio: recibe una solicitud de
inscripcion o baja y decide si se acepta o se rechaza segun el contrato del dominio.
No implementa la logica de cada regla; esa vive en `reglas.py` y este archivo solo
coordina la evaluacion en el orden definido por R8.

Orden de evaluacion (contrato):
R1 -> R2 -> R7 -> R4 -> R5 -> R3

La primera regla que devuelve un motivo es la que gana. Eso hace que el rechazo sea
determinista y verificable, y que un caso con varios motivos posibles quede resuelto
por el primero que aplique.
"""

from datetime import datetime

from . import reglas
from .modelo import Estado, Inscripcion, Instituto, Motivo, Resultado

ORDEN_DE_EVALUACION = ("R1", "R2", "R7", "R4", "R5", "R3")


def inscribir(
    inst: Instituto,
    estudiante_id: str,
    comision_id: str,
    periodo_id: str,
    ahora: datetime,
) -> Resultado:
    """Intenta aceptar una inscripcion para un estudiante en una comision.

    La operacion aplica el contrato de la v1 en orden estricto:
    1) verifica la ventana de inscripcion (R1),
    2) correlatividad (R2),
    3) unicidad por materia (R7),
    4) maximo de materias activas (R4),
    5) choque de horarios (R5),
    6) cupo disponible (R3).

    Si alguna regla rechaza, la funcion devuelve `Resultado(aceptada=False, motivo=...)` y
    no registra la inscripcion. Si todas pasan, agrega una inscripcion activa para ese
    estudiante, comision y periodo con el instante de solicitud recibido.
    """
    est = inst.estudiantes[estudiante_id]
    com = inst.comisiones[comision_id]
    per = inst.periodos[periodo_id]
    mat = inst.materias[com.materia]

    comprobaciones = (
        lambda: reglas.r1_ventana(per, ahora),
        lambda: reglas.r2_correlatividad(inst, est, mat),
        lambda: reglas.r7_unicidad(inst, est, mat, per),
        lambda: reglas.r4_maximo(inst, est, per),
        lambda: reglas.r5_choque(inst, est, com, per),
        lambda: reglas.r3_cupo(inst, com, per),
    )

    for comprobar in comprobaciones:
        motivo = comprobar()
        if motivo is not None:
            return Resultado(aceptada=False, motivo=motivo)

    inst.inscripciones.append(
        Inscripcion(
            estudiante=estudiante_id,
            comision=comision_id,
            periodo=periodo_id,
            estado=Estado.ACTIVA,
            solicitada_en=ahora,
        )
    )
    return Resultado(aceptada=True)


def dar_de_baja(
    inst: Instituto,
    estudiante_id: str,
    comision_id: str,
    periodo_id: str,
    ahora: datetime,
) -> Resultado:
    """Procesa una baja de una inscripcion activa dentro del plazo vigente.

    R6 define dos reglas simples: la baja solo puede hacerse hasta el plazo de baja del
    periodo, inclusive; y si la inscripcion existe y esta activa, se marca como BAJA y deja
    de contar para R3, R4 y R5.

    Si el momento supera el plazo, la operacion rechaza con `R6_FUERA_DE_PLAZO`. Si no existe
    una inscripcion activa para esa combinacion estudiante-comision-periodo, devuelve
    `R6_SIN_INSCRIPCION`.
    """
    per = inst.periodos[periodo_id]
    if ahora > per.plazo_de_baja:
        return Resultado(aceptada=False, motivo=Motivo.R6_FUERA_DE_PLAZO)

    for i in inst.inscripciones:
        if (
            i.estudiante == estudiante_id
            and i.comision == comision_id
            and i.periodo == periodo_id
            and i.estado is Estado.ACTIVA
        ):
            i.estado = Estado.BAJA
            return Resultado(aceptada=True)

    return Resultado(aceptada=False, motivo=Motivo.R6_SIN_INSCRIPCION)
