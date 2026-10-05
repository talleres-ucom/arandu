from datetime import time

import pytest

from arandu.horarios import chocan, se_solapan
from arandu.modelo import Franja


@pytest.mark.parametrize(
    ("primera", "segunda", "esperado"),
    [
        (Franja(0, time(9), time(11)), Franja(0, time(10), time(12)), True),
        (Franja(0, time(10), time(12)), Franja(0, time(9), time(11)), True),
        (Franja(0, time(9), time(12)), Franja(0, time(10), time(11)), True),
        (Franja(0, time(9), time(10)), Franja(0, time(10), time(11)), False),
        (Franja(0, time(10), time(11)), Franja(0, time(9), time(10)), False),
        (Franja(0, time(9), time(10)), Franja(0, time(11), time(12)), False),
        (Franja(0, time(9), time(11)), Franja(1, time(10), time(12)), False),
    ],
)
def test_se_solapan_respeta_dia_y_cruce_estricto(primera, segunda, esperado):
    assert se_solapan(primera, segunda) is esperado


def test_chocan_detecta_solapamiento_entre_iterables():
    unas = (franja for franja in [Franja(2, time(8), time(10))])
    otras = (franja for franja in [Franja(2, time(9), time(11))])

    assert chocan(unas, otras)


@pytest.mark.parametrize(
    ("unas", "otras"),
    [
        ([], [Franja(0, time(9), time(11))]),
        ([Franja(0, time(9), time(11))], []),
        ([Franja(0, time(9), time(10))], [Franja(0, time(10), time(11))]),
    ],
)
def test_chocan_es_falso_sin_parejas_solapadas(unas, otras):
    assert not chocan(unas, otras)
