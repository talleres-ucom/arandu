"""Pruebas del reporte de ocupacion."""

from datetime import datetime

import pytest

from arandu.fixtures import PERIODO_ACTUAL, instituto_arandu
from arandu.inscripcion import inscribir
from arandu.reportes import ocupacion

DENTRO = datetime(2026, 9, 10, 20, 0)


@pytest.fixture
def inst():
    return instituto_arandu()


def test_comision_vacia(inst):
    r = ocupacion(inst, "PROG1-A", PERIODO_ACTUAL)
    assert r == {"inscriptos": 0, "cupo": 30, "reservados": 3, "libres": 27}


def test_ocupacion_cuenta_inscriptos(inst):
    assert inscribir(inst, "e1", "PROG1-A", PERIODO_ACTUAL, DENTRO).aceptada
    assert inscribir(inst, "e2", "PROG1-A", PERIODO_ACTUAL, DENTRO).aceptada
    r = ocupacion(inst, "PROG1-A", PERIODO_ACTUAL)
    assert r["inscriptos"] == 2
    assert r["libres"] == 25


def test_comision_sin_cupo(inst):
    r = ocupacion(inst, "BD1-B", PERIODO_ACTUAL)
    assert r["libres"] == 0
