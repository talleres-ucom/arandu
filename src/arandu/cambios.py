"""Cambio de comision dentro de una materia (pedido de la Secretaria)."""

from datetime import datetime

from .inscripcion import inscribir
from .modelo import Estado, Instituto, Resultado


def cambiar_de_comision(
    inst: Instituto,
    estudiante_id: str,
    comision_actual: str,
    comision_nueva: str,
    periodo_id: str,
    ahora: datetime,
) -> Resultado:
    """Pasa al estudiante de su comision actual a otra. Reutiliza `inscribir` para aplicar las reglas."""
    actual = next(
        (
            i
            for i in inst.inscripciones
            if i.estudiante == estudiante_id
            and i.comision == comision_actual
            and i.periodo == periodo_id
            and i.estado is Estado.ACTIVA
        ),
        None,
    )
    if actual is None:
        # Si todavia no estaba inscripto, el cambio equivale a una inscripcion directa.
        return inscribir(inst, estudiante_id, comision_nueva, periodo_id, ahora)

    # Se libera el lugar actual para que R7 y R5 no cuenten la inscripcion que se reemplaza.
    actual.estado = Estado.BAJA
    resultado = inscribir(inst, estudiante_id, comision_nueva, periodo_id, ahora)

    if resultado.aceptada:
        # Se conserva la antiguedad de la inscripcion original, para no perjudicar al estudiante.
        nueva = inst.inscripciones[-1]
        nueva.solicitada_en = actual.solicitada_en
    return resultado
