from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class MotivoRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        """
        Inserta un motivo (catálogo) y retorna el idMotivoConsulta generado.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO motivo_consulta
        (nombreMotivo, descripcion, estadoRegistro)
        VALUES (?, ?, 1)
        """
        cur = conn.cursor()
        cur.execute(sql, (
            data.get("nombreMotivo"),
            data.get("descripcion"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def get_by_id(self, id_motivo: int) -> Optional[Dict[str, Any]]:
        """
        Retorna un motivo activo por idMotivoConsulta, o None.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM motivo_consulta
        WHERE idMotivoConsulta = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (id_motivo,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def get_by_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        """
        Retorna un motivo activo por nombreMotivo, o None.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM motivo_consulta
        WHERE nombreMotivo = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (nombre,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def list_active(self) -> List[Dict[str, Any]]:
        """
        Lista motivos activos.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM motivo_consulta
        WHERE estadoRegistro = 1
        ORDER BY nombreMotivo
        """
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def deactivate(self, id_motivo: int) -> None:
        """
        Eliminación lógica: estadoRegistro = 0
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE motivo_consulta
        SET estadoRegistro = 0
        WHERE idMotivoConsulta = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_motivo,))
        conn.commit()
        self.db.close()
