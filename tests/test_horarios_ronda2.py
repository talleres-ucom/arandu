from datetime import time

from arandu.horarios import chocan
from arandu.modelo import Franja


def test_mismo_dia_con_intervalos_que_se_cruzan_chocan():
    primera = Franja(0, time(20), time(22))
    segunda = Franja(0, time(21), time(23))

    assert chocan([primera], [segunda]) is True


def test_clase_que_empieza_a_las_21_no_choca_con_la_que_termina_a_las_21():
    primera = Franja(0, time(20), time(21))
    segunda = Franja(0, time(21), time(22))

    assert chocan([primera], [segunda]) is False


def test_mismo_horario_en_distinto_dia_no_choca():
    primera = Franja(0, time(20), time(22))
    segunda = Franja(1, time(20), time(22))

    assert chocan([primera], [segunda]) is False


def test_franja_contenida_en_otra_choca():
    primera = Franja(0, time(20), time(22))
    segunda = Franja(0, time(20, 30), time(21, 30))

    assert chocan([primera], [segunda]) is True