from core.database import select
from utils.date_formatting import *

def listarEstudiantesNivel():
    return select(f'''
                   SELECT
                        c.curnivel,
                        COUNT(i.insid) AS cantidad_estudiantes
                    FROM academico.curso c
                    LEFT JOIN academico.curso_materia cm ON c.curid = cm.curid
                    LEFT JOIN academico.inscripcion i ON cm.curmatid = i.curmatid
                    GROUP BY c.curnivel
                    order by
                    c.curnivel
                  ''')

def listarEstudiantesMateria():
    return select(f'''
                  SELECT m.matnombre, COUNT(i.insid) AS cantidad_estudiantes
                    FROM academico.curso_materia cm
                    LEFT JOIN academico.inscripcion i ON cm.curmatid = i.curmatid
                    LEFT JOIN academico.materia m ON cm.matid = m.matid
                    GROUP BY m.matnombre
                    ORDER BY m.matnombre;
                  ''')

def listarCantidades():
    return select(f'''      
    SELECT
        cm.curmatnum,
        cm.curmatnum_inactivos,
        m.matnum,
        m.matnum_inactivos,
        c.nivnum,
        c.nivnum_inactivos,
        u.usunum,
        u.usunum_inactivos,
        u2.estnum,
        u2.estnum_inactivos,
        u3.docnum,
        u3.docnum_inactivos,
        u4.secnum,
        u4.secnum_inactivos,
        t.texnum,
        t.texnum_inactivos
    FROM
        (SELECT 
            COUNT(curmatid) AS curmatnum,
            SUM(1 - curmatestado) AS curmatnum_inactivos
        FROM academico.curso_materia) cm,
        (SELECT 
            COUNT(matid) AS matnum,
            SUM(1 - matestado) AS matnum_inactivos
        FROM academico.materia) m,
        (SELECT 
            COUNT(curid) AS nivnum,
            SUM(1 - curestado) AS nivnum_inactivos
        FROM academico.curso) c,
        (SELECT 
            COUNT(usuid) AS usunum,
            SUM(1 - usuestado) AS usunum_inactivos
        FROM academico.usuario) u,
        (SELECT 
            COUNT(usuid) AS estnum,
            SUM(1 - usuestado) AS estnum_inactivos
        FROM academico.usuario WHERE rolid = 4) u2,
        (SELECT 
            COUNT(usuid) AS docnum,
            SUM(1 - usuestado) AS docnum_inactivos
        FROM academico.usuario WHERE rolid = 3) u3,
        (SELECT 
            COUNT(usuid) AS secnum,
            SUM(1 - usuestado) AS secnum_inactivos
        FROM academico.usuario WHERE rolid = 2) u4,
        (SELECT 
            COUNT(texid) AS texnum,
            SUM(1 - texestado) AS texnum_inactivos
        FROM academico.texto) t;
    ''')  

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
