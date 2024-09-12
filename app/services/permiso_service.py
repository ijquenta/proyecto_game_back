from core.database import db, as_string, select, sql
from utils.date_formatting import *

def listarPermiso():
    data = select(f'''
        SELECT distinct  r.rolnombre,   
                             o.opeid,
                             o.openombre,   
                             p.permactivo 
        FROM academico.permiso p
        left join academico.operacion o on o.opeid = p.opeid
        left join academico.rol r ON p.rolid = r.rolid
    ''')
    return data

def getPermisos():
    return select(f''' SELECT permid, rolid, opeid, permactivo, permusureg, permfecreg, permusumod, permfecmod, permdescripcion, permestado FROM academico.permiso; ''')

def getRoles():
    return select(f''' SELECT rolid, rolnombre, roldescripcion, rolusureg, rolfecreg, rolusumod, rolfecmod, rolestado FROM academico.rol order by rolnombre; ''')

def getOperaciones():
    return select(f''' SELECT opeid, openombre, opeusureg, opefecreg, opeusumod, opefecmod, opedescripcion, opeestado FROM academico.operacion order by openombre;''')

def updatePermiso(data):
    try:
        # Construir la consulta SQL
        query = sql.SQL('''
            UPDATE academico.permiso
            SET permactivo = {permactivo},
                permusumod = {permusumod},
                permfecmod = {permfecmod}
            WHERE permid = {permid}
            RETURNING *
        ''').format(
            permactivo=sql.Literal(data['permactivo']),
            permusumod=sql.Literal(data['permusumod']),
            permfecmod=sql.Literal(datetime.utcnow()),
            permid=sql.Literal(data['permid'])
        )
        
        # Ejecutar la consulta y obtener el resultado
        result = select(as_string(query))
        
        if not result:
            return {"code": 0, "message": "Permiso not found"}, 404
        
        return {"code": 1, "message": "Permiso updated successfully", "permiso": result}, 200
    except Exception as e:
        print("Error updating permiso:", str(e))
        return {"code": 0, "message": "Error updating permiso", "error": str(e)}, 500

def addPermiso(data):
    try:
        # Construir la consulta SQL para insertar un nuevo permiso
        query = sql.SQL('''
            INSERT INTO academico.permiso (
                rolid, opeid, permactivo, permusureg, permfecreg, permdescripcion, permestado
            ) VALUES (
                {rolid}, {opeid}, {permactivo}, {permusureg}, {permfecreg}, {permdescripcion}, {permestado}
            ) RETURNING *
        ''').format(
            rolid=sql.Literal(data['rolid']),
            opeid=sql.Literal(data['opeid']),
            permactivo=sql.Literal(data['permactivo']),
            permusureg=sql.Literal(data['permusureg']),
            permfecreg=sql.Literal(datetime.now()),
            permdescripcion=sql.Literal(data['permdescripcion']),
            permestado=sql.Literal(data['permestado'])
        )

        # Ejecutar la consulta y obtener el resultado
        result = select(as_string(query))
        
        if not result:
            return {"code": 0, "message": "Failed to add permiso"}, 404
        
        return result, 200
    except Exception as e:
        print("Error adding permiso:", str(e))
        return {"code": 0, "message": "Error adding permiso", "error": str(e)}, 500

def deletePermiso(data):
    try:
        # Construir la consulta SQL para eliminar un permiso
        query = sql.SQL('''
            DELETE FROM academico.permiso
            WHERE permid = {permid}
        ''').format(
            permid=sql.Literal(data['permid'])
        )

        # Ejecutar la consulta y obtener el resultado
        result = select(as_string(query))

        if not result:
            return {"code": 0, "message": "Permiso not found"}, 404

        return {"code": 1, "message": "Permiso deleted successfully"}, 200
    except Exception as e:
        print("Error deleting permiso:", str(e))
        return {"code": 0, "message": "Error deleting permiso", "error": str(e)}, 500
