from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class DesparasitacionAplicadaRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO desparasitacion_aplicada
        (idAtencion, idTipoDesparasitacion, fechaAplicacion, fechaProximaDosis, dosis, lote, observaciones, estadoRegistro)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """
        cur = conn.cursor()
        cur.execute(sql, (
            data["idAtencion"],
            data["idTipoDesparasitacion"],
            data["fechaAplicacion"],
            data.get("fechaProximaDosis"),
            data.get("dosis"),
            data.get("lote"),
            data.get("observaciones"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def list_by_atencion(self, id_atencion: int) -> List[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM desparasitacion_aplicada
        WHERE idAtencion = ? AND estadoRegistro = 1
        ORDER BY fechaAplicacion DESC
        """
        cur = conn.cursor()
        cur.execute(sql, (id_atencion,))
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def deactivate(self, id_desparasitacion: int) -> None:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE desparasitacion_aplicada
        SET estadoRegistro = 0
        WHERE idDesparasitacion = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_desparasitacion,))
        conn.commit()
        self.db.close()
