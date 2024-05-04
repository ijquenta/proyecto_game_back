from core.database import select, execute, execute_function, execute_response
from flask import Flask, request, jsonify, make_response
from utils.date_formatting import *


def listarCursoMateriaContabilidad(data):
    fecini = darFormatoFechaSinHorav2(data['fecini'])
    fecfin = darFormatoFechaSinHorav2(data['fecfin'])
    lista_cm = select(f'''
        SELECT cm.curmatid, cm.curid, c.curnombre, cm.matid, m.matnombre, cm.periddocente, p.pernomcompleto, p.perfoto, cm.curmatfecini, cm.curmatfecfin, cm.curmatcosto, t1.numest as numero_estudiantes
        FROM academico.curso_materia cm
        JOIN ( SELECT curmatid, count(peridestudiante) as numest FROM academico.inscripcion WHERE insestado = 1 GROUP BY curmatid) as t1 ON t1.curmatid = cm.curmatid
        LEFT JOIN academico.curso c ON c.curid = cm.curid
        LEFT JOIN academico.materia m ON m.matid = cm.matid
        LEFT JOIN academico.persona p on p.perid = cm.periddocente
        WHERE cm.curmatfecini > '{fecini}' AND cm.curmatfecfin < '{fecfin}'
        and cm.curmatestado = 1
    ''')
    for lcm in lista_cm:
        lcm['curmatfecini'] = darFormatoFechaSinHora(lcm['curmatfecini'])
        lcm['curmatfecfin'] = darFormatoFechaSinHora(lcm['curmatfecfin'])
    return lista_cm