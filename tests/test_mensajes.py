"""Pruebas de los mensajes legibles y del motor de reglas en tabla."""

from datetime import datetime, time, timedelta

import pytest

from arandu.fixtures import PERIODO_ACTUAL, instituto_arandu
from arandu.inscripcion import ACEPTADA, MENSAJES, inscribir, mensaje_para
from arandu.modelo import Comision, Franja, Materia, Motivo

DENTRO = datetime(2026, 9, 10, 20, 0)


@pytest.fixture
def inst():
    return instituto_arandu()


def test_cada_motivo_tiene_su_mensaje():
    for motivo in Motivo:
        assert mensaje_para(motivo) == MENSAJES[motivo]


def test_inscripcion_aceptada_incluye_mensaje(inst):
    r = inscribir(inst, "e2", "PROG1-A", PERIODO_ACTUAL, DENTRO)
    assert r.aceptada
    assert r.mensaje == ACEPTADA


def test_rechazo_incluye_el_mensaje_del_motivo(inst):
    tarde = inst.periodos[PERIODO_ACTUAL].cierre + timedelta(minutes=1)
    r = inscribir(inst, "e2", "PROG1-A", PERIODO_ACTUAL, tarde)
    assert not r.aceptada
    assert r.mensaje == MENSAJES[r.motivo]


def test_ingresante_no_puede_superar_cuatro_materias(inst):
    # e2 no tiene historial: es ingresante.
    inst.materias["ING1"] = Materia("ING1", "Ingles I", "AS-2026")
    inst.comisiones["ING1-A"] = Comision("ING1-A", "ING1", 30, (Franja(5, time(9, 0), time(11, 0)),))
    for comision in ("ALG1-A", "MAT1-A", "PROG1-A", "RED1-A"):
        assert inscribir(inst, "e2", comision, PERIODO_ACTUAL, DENTRO).aceptada
    r = inscribir(inst, "e2", "ING1-A", PERIODO_ACTUAL, DENTRO)
    assert r.motivo is Motivo.R4_MAXIMO_SUPERADO
    assert r.mensaje == MENSAJES[Motivo.R4_MAXIMO_SUPERADO]
