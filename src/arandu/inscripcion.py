"""Orquestacion: evalua las reglas en el orden del contrato y decide.

R8 — orden de evaluacion: R1 -> R2 -> R7 -> R4 -> R5 -> R3.
Se rechaza con EL PRIMER motivo que aplique, no con la lista de todos los motivos.

Refactor: cada regla se declara como una fila de una tabla, junto con su mensaje legible.
Agregar una regla nueva es agregar una fila; el bucle de evaluacion no cambia.
"""

from collections.abc import Callable
from datetime import datetime

from . import reglas
from .modelo import Estado, Inscripcion, Instituto, Motivo, Resultado

ORDEN_DE_EVALUACION = ("R1", "R2", "R7", "R4", "R5", "R3")

MENSAJES: dict[Motivo, str] = {
    Motivo.R1_FUERA_DE_VENTANA: "La solicitud esta fuera del periodo de inscripcion.",
    Motivo.R2_CORRELATIVA_PENDIENTE: "Falta aprobar una materia correlativa.",
    Motivo.R7_MATERIA_DUPLICADA: "Ya hay una inscripcion activa a esta materia.",
    Motivo.R4_MAXIMO_SUPERADO: "Se alcanzo el maximo de materias del periodo.",
    Motivo.R5_CHOQUE_DE_HORARIOS: "El horario se superpone con otra materia inscripta.",
    Motivo.R3_SIN_CUPO: "La comision no tiene lugares disponibles.",
    Motivo.R6_FUERA_DE_PLAZO: "El plazo de baja ya vencio.",
    Motivo.R6_SIN_INSCRIPCION: "No hay una inscripcion activa para dar de baja.",
}

ACEPTADA = "Inscripcion aceptada."


def mensaje_para(motivo: Motivo | None, idioma: str = "es") -> str:
    """Mensaje legible para el estudiante. Traduce automaticamente si el idioma no es espanol."""
    if motivo is None:
        texto = ACEPTADA
    else:
        texto = MENSAJES[motivo]
    if idioma != "es":
        from arandu.i18n import traducir

        return traducir(texto, idioma)
    return texto


def _rechazo(motivo: Motivo) -> Resultado:
    return Resultado(aceptada=False, motivo=motivo, mensaje=mensaje_para(motivo))


def inscribir(
    inst: Instituto,
    estudiante_id: str,
    comision_id: str,
    periodo_id: str,
    ahora: datetime,
) -> Resultado:
    """Intenta inscribir al estudiante en la comision. No lanza excepciones: devuelve Resultado."""
    est = inst.estudiantes[estudiante_id]
    com = inst.comisiones[comision_id]
    per = inst.periodos[periodo_id]
    mat = inst.materias[com.materia]

    # Tabla de reglas, en el orden de evaluacion del contrato (R8).
    tabla: tuple[tuple[str, Callable[[], Motivo | None]], ...] = (
        ("R1", lambda: reglas.r1_ventana(per, ahora)),
        ("R2", lambda: reglas.r2_correlatividad(inst, est, mat)),
        ("R4", lambda: reglas.r4_maximo(inst, est, per)),
        ("R7", lambda: reglas.r7_unicidad(inst, est, mat, per)),
        ("R5", lambda: reglas.r5_choque(inst, est, com, per)),
        ("R3", lambda: reglas.r3_cupo(inst, com, per)),
    )

    for _codigo, comprobar in tabla:
        motivo = comprobar()
        if motivo is not None:
            return _rechazo(motivo)

    inst.inscripciones.append(
        Inscripcion(
            estudiante=estudiante_id,
            comision=comision_id,
            periodo=periodo_id,
            estado=Estado.ACTIVA,
            solicitada_en=ahora,
        )
    )
    return Resultado(aceptada=True, mensaje=ACEPTADA)


def dar_de_baja(
    inst: Instituto,
    estudiante_id: str,
    comision_id: str,
    periodo_id: str,
    ahora: datetime,
) -> Resultado:
    """R6 — la baja se admite hasta el plazo del periodo, inclusive."""
    per = inst.periodos[periodo_id]
    if ahora > per.plazo_de_baja:
        return _rechazo(Motivo.R6_FUERA_DE_PLAZO)

    for i in inst.inscripciones:
        if (
            i.estudiante == estudiante_id
            and i.comision == comision_id
            and i.periodo == periodo_id
            and i.estado is Estado.ACTIVA
        ):
            i.estado = Estado.BAJA
            return Resultado(aceptada=True, mensaje="Baja registrada.")

    return _rechazo(Motivo.R6_SIN_INSCRIPCION)
