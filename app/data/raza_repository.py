from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class RazaRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        """
        Inserta una raza y retorna idRaza.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO raza (idEspecie, nombreRaza, estadoRegistro)
        VALUES (?, ?, 1)
        """
        cur = conn.cursor()
        cur.execute(sql, (
            data.get("idEspecie"),
            data.get("nombreRaza"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def get_by_id(self, id_raza: int) -> Optional[Dict[str, Any]]:
        """
        Retorna una raza activa por idRaza, o None.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM raza
        WHERE idRaza = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (id_raza,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def get_by_nombre_en_especie(self, id_especie: int, nombre_raza: str) -> Optional[Dict[str, Any]]:
        """
        Busca raza activa por (idEspecie, nombreRaza).
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM raza
        WHERE idEspecie = ? AND nombreRaza = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (id_especie, nombre_raza))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def list_active(self) -> List[Dict[str, Any]]:
        """
        Lista todas las razas activas.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM raza
        WHERE estadoRegistro = 1
        ORDER BY idEspecie, nombreRaza
        """
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def list_by_especie(self, id_especie: int) -> List[Dict[str, Any]]:
        """
        Lista razas activas por especie.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM raza
        WHERE idEspecie = ? AND estadoRegistro = 1
        ORDER BY nombreRaza
        """
        cur = conn.cursor()
        cur.execute(sql, (id_especie,))
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def deactivate(self, id_raza: int) -> None:
        """
        Eliminación lógica: estadoRegistro = 0
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE raza
        SET estadoRegistro = 0
        WHERE idRaza = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_raza,))
        conn.commit()
        self.db.close()
