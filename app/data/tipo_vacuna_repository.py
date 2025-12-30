from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class TipoVacunaRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO tipo_vacuna
        (nombreVacuna, descripcion, idEspecie, intervaloRecMeses, estadoRegistro)
        VALUES (?, ?, ?, ?, 1)
        """
        cur = conn.cursor()
        cur.execute(sql, (
            data.get("nombreVacuna"),
            data.get("descripcion"),
            data.get("idEspecie"),
            data.get("intervaloRecMeses"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def get_by_id(self, id_tipo: int) -> Optional[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM tipo_vacuna
        WHERE idTipoVacuna = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (id_tipo,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def get_by_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM tipo_vacuna
        WHERE lower(trim(nombreVacuna)) = lower(trim(?))
          AND estadoRegistro = 1
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
        FROM tipo_vacuna
        WHERE estadoRegistro = 1
        ORDER BY nombreVacuna
        """
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def list_by_especie(self, id_especie: int) -> List[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM tipo_vacuna
        WHERE estadoRegistro = 1
          AND (idEspecie IS NULL OR idEspecie = ?)
        ORDER BY nombreVacuna
        """
        cur = conn.cursor()
        cur.execute(sql, (id_especie,))
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def deactivate(self, id_tipo: int) -> None:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE tipo_vacuna
        SET estadoRegistro = 0
        WHERE idTipoVacuna = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_tipo,))
        conn.commit()
        self.db.close()
