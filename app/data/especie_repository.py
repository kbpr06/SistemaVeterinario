from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class EspecieRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO especie (nombreEspecie, estadoRegistro)
        VALUES (?, 1)
        """
        cur = conn.cursor()
        cur.execute(sql, (data.get("nombreEspecie"),))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def get_by_id(self, id_especie: int) -> Optional[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM especie
        WHERE idEspecie = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (id_especie,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def get_by_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM especie
        WHERE nombreEspecie = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (nombre,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def list_active(self) -> List[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM especie
        WHERE estadoRegistro = 1
        ORDER BY nombreEspecie
        """
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def deactivate(self, id_especie: int) -> None:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE especie
        SET estadoRegistro = 0
        WHERE idEspecie = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_especie,))
        conn.commit()
        self.db.close()
