from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class TipoDesparasitacionRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO tipo_desparasitacion
        (nombreDesparasitacion, tipo, idEspecie, intervaloRecMeses, estadoRegistro)
        VALUES (?, ?, ?, ?, 1)
        """
        cur = conn.cursor()
        cur.execute(sql, (
            data["nombreDesparasitacion"],
            data["tipo"],
            data.get("idEspecie"),
            data.get("intervaloRecMeses"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def list_active(self) -> List[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM tipo_desparasitacion
        WHERE estadoRegistro = 1
        ORDER BY nombreDesparasitacion
        """
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def get_by_name(self, nombre: str) -> Optional[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM tipo_desparasitacion
        WHERE nombreDesparasitacion = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (nombre,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def deactivate(self, id_tipo: int) -> None:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE tipo_desparasitacion
        SET estadoRegistro = 0
        WHERE idTipoDesparasitacion = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_tipo,))
        conn.commit()
        self.db.close()
