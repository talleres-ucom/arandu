"""Reportes para la secretaria academica."""

from .inscripcion import Instituto
from .reglas import cupo_efectivo


def ocupacion(inst: Instituto, comision_id: str, periodo_id: str) -> dict[str, int]:
    """Ocupacion de una comision en un periodo: inscriptos activos, cupo, reservados y libres."""
    com = inst.comisiones[comision_id]
    inscriptos = len(inst.activas_en(comision_id, periodo_id))
    disponibles = cupo_efectivo(com)
    return {
        "inscriptos": inscriptos,
        "cupo": com.cupo,
        "reservados": com.cupo - disponibles,
        "libres": max(disponibles - inscriptos, 0),
    }


def imprimir_ocupacion(inst: Instituto, periodo_id: str) -> str:
    """Tabla de ocupacion de todas las comisiones, lista para imprimir."""
    from tabla_bonita import render

    filas = [(cid, *ocupacion(inst, cid, periodo_id).values()) for cid in sorted(inst.comisiones)]
    return render(filas, encabezado=("Comision", "Inscriptos", "Cupo", "Reservados", "Libres"))
