"""Pruebas de la demo de S7. Una por criterio de docs/criterios-demo-s7.md."""

from datetime import datetime, time

import pytest

from arandu.fixtures import PERIODO_ACTUAL, instituto_arandu
from arandu.inscripcion import dar_de_baja, inscribir
from arandu.modelo import Comision, Franja, Motivo

P = PERIODO_ACTUAL
T = datetime(2026, 9, 10, 20, 0)
LUN = 0


@pytest.fixture
def inst():
    i = instituto_arandu()
    i.comisiones["RED1-M"] = Comision("RED1-M", "RED1", 30, (Franja(LUN, time(7, 0), time(9, 0)),))
    i.comisiones["RED1-Z"] = Comision("RED1-Z", "RED1", 0, (Franja(LUN, time(7, 0), time(9, 0)),))
    i.comisiones["TAL-A"] = Comision(
        "TAL-A", "PROG1", 30, (Franja(LUN, time(7, 0), time(8, 0)), Franja(LUN, time(9, 0), time(10, 0))))
    return i


def test_c1_la_tercera_materia_del_mismo_dia_se_rechaza(inst):
    assert inscribir(inst, "e2", "ALG1-A", P, T).aceptada
    assert inscribir(inst, "e2", "MAT1-A", P, T).aceptada
    r = inscribir(inst, "e2", "RED1-M", P, T)
    assert not r.aceptada and r.motivo is Motivo.LIMITE_DIARIO


def test_c2_dos_materias_el_mismo_dia_se_aceptan(inst):
    assert inscribir(inst, "e2", "ALG1-A", P, T).aceptada
    assert inscribir(inst, "e2", "MAT1-A", P, T).aceptada


def test_c3_las_bajas_no_cuentan(inst):
    assert inscribir(inst, "e2", "ALG1-A", P, T).aceptada
    assert inscribir(inst, "e2", "MAT1-A", P, T).aceptada
    assert dar_de_baja(inst, "e2", "MAT1-A", P, T).aceptada
    assert inscribir(inst, "e2", "RED1-M", P, T).aceptada


def test_c4_se_cuentan_materias_no_franjas(inst):
    assert inscribir(inst, "e2", "ALG1-A", P, T).aceptada
    assert inscribir(inst, "e2", "TAL-A", P, T).aceptada


def test_c5_el_limite_se_informa_antes_que_el_cupo(inst):
    assert inscribir(inst, "e2", "ALG1-A", P, T).aceptada
    assert inscribir(inst, "e2", "MAT1-A", P, T).aceptada
    r = inscribir(inst, "e2", "RED1-Z", P, T)
    assert r.motivo is Motivo.LIMITE_DIARIO
