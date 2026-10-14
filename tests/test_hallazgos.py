from datetime import datetime, time

from arandu.fixtures import PERIODO_ACTUAL, instituto_arandu
from arandu.inscripcion import inscribir
from arandu.modelo import Comision, Estudiante, Franja, Materia, Motivo

DENTRO = datetime(2026, 9, 10, 20, 0)


def test_r7_rechaza_misma_materia_en_otra_comision():
    inst = instituto_arandu()

    assert inscribir(inst, "e2", "PROG1-A", PERIODO_ACTUAL, DENTRO).aceptada
    r = inscribir(inst, "e2", "PROG1-B", PERIODO_ACTUAL, DENTRO)

    assert not r.aceptada and r.motivo is Motivo.R7_MATERIA_DUPLICADA


def test_r2_exige_todas_las_correlativas_aprobadas():
    inst = instituto_arandu()
    inst.materias["WEB2"] = Materia("WEB2", "Desarrollo Web II", "AS-2026", correlativas=("ALG1", "PROG1"))
    inst.comisiones["WEB2-A"] = Comision(
        "WEB2-A",
        "WEB2",
        30,
        (Franja(3, time(8, 0), time(10, 0)),),
    )

    r = inscribir(inst, "e1", "WEB2-A", PERIODO_ACTUAL, DENTRO)

    assert not r.aceptada and r.motivo is Motivo.R2_CORRELATIVA_PENDIENTE


def test_r3_no_descuenta_reserva_inventada():
    inst = instituto_arandu()
    inst.materias["MAT2"] = Materia("MAT2", "Matematica II", "AS-2026")
    inst.comisiones["MAT2-A"] = Comision(
        "MAT2-A",
        "MAT2",
        10,
        (Franja(4, time(9, 0), time(11, 0)),),
    )

    for i in range(10):
        estudiante_id = f"e{i + 10}"
        inst.estudiantes[estudiante_id] = Estudiante(estudiante_id, f"Estudiante {i}", "AS-2026")
        r = inscribir(inst, estudiante_id, "MAT2-A", PERIODO_ACTUAL, DENTRO)
        assert r.aceptada, f"el estudiante {estudiante_id} debio poder inscribirse al cupo real"
