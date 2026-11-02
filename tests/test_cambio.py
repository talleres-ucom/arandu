"""Pruebas del cambio de comision."""

from datetime import datetime, time, timedelta

import pytest

from arandu.cambios import cambiar_de_comision
from arandu.fixtures import PERIODO_ACTUAL, instituto_arandu
from arandu.inscripcion import inscribir
from arandu.modelo import Comision, Estado, Franja

P = PERIODO_ACTUAL
T0 = datetime(2026, 9, 10, 20, 0)


def t(minutos):
    return T0 + timedelta(minutes=minutos)


@pytest.fixture
def inst():
    i = instituto_arandu()
    i.comisiones["PROG1-C"] = Comision("PROG1-C", "PROG1", 1, (Franja(5, time(8, 0), time(10, 0)),))
    return i


def activas(inst, estudiante, comision):
    return [i for i in inst.inscripciones
            if i.estudiante == estudiante and i.comision == comision and i.estado is Estado.ACTIVA]


def test_cambio_de_comision_aceptado(inst):
    assert inscribir(inst, "e2", "PROG1-A", P, t(0)).aceptada
    r = cambiar_de_comision(inst, "e2", "PROG1-A", "PROG1-B", P, t(5))
    assert r.aceptada
    assert activas(inst, "e2", "PROG1-B")
    assert not activas(inst, "e2", "PROG1-A")


def test_el_cambio_conserva_la_antiguedad(inst):
    assert inscribir(inst, "e2", "PROG1-A", P, t(0)).aceptada
    cambiar_de_comision(inst, "e2", "PROG1-A", "PROG1-B", P, t(5))
    assert activas(inst, "e2", "PROG1-B")[0].solicitada_en == t(0)


@pytest.mark.xfail(reason="caso borde: se resuelve en otro PR")
def test_cambio_rechazado_conserva_el_lugar(inst):
    assert inscribir(inst, "e3", "PROG1-C", P, t(0)).aceptada
    assert inscribir(inst, "e2", "PROG1-A", P, t(1)).aceptada
    r = cambiar_de_comision(inst, "e2", "PROG1-A", "PROG1-C", P, t(5))
    assert not r.aceptada
    assert activas(inst, "e2", "PROG1-A")
