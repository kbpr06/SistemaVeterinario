from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class TipoMedicamentoRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO tipo_medicamento
        (nombreMedicamento, categoria, descripcion, estadoRegistro)
        VALUES (?, ?, ?, 1)
        """
        try:
            cur = conn.cursor()
            cur.execute(sql, (
                data.get("nombreMedicamento"),
                data.get("categoria"),
                data.get("descripcion"),
            ))
            conn.commit()
            return cur.lastrowid
        finally:
            self.db.close()

    def get_by_id(self, id_tipo: int) -> Optional[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM tipo_medicamento
        WHERE idTipoMedicamento = ? AND estadoRegistro = 1
        """
        try:
            cur = conn.cursor()
            cur.execute(sql, (id_tipo,))
            row = cur.fetchone()
            return dict(row) if row else None
        finally:
            self.db.close()

    def get_by_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM tipo_medicamento
        WHERE lower(nombreMedicamento) = lower(?) AND estadoRegistro = 1
        """
        try:
            cur = conn.cursor()
            cur.execute(sql, (nombre,))
            row = cur.fetchone()
            return dict(row) if row else None
        finally:
            self.db.close()

    def list_active(self) -> List[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM tipo_medicamento
        WHERE estadoRegistro = 1
        ORDER BY categoria, nombreMedicamento
        """
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        finally:
            self.db.close()

    def list_by_categoria(self, categoria: str) -> List[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM tipo_medicamento
        WHERE categoria = ? AND estadoRegistro = 1
        ORDER BY nombreMedicamento
        """
        try:
            cur = conn.cursor()
            cur.execute(sql, (categoria,))
            rows = cur.fetchall()
            return [dict(r) for r in rows]
        finally:
            self.db.close()

    def deactivate(self, id_tipo: int) -> None:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE tipo_medicamento
        SET estadoRegistro = 0
        WHERE idTipoMedicamento = ?
        """
        try:
            cur = conn.cursor()
            cur.execute(sql, (id_tipo,))
            conn.commit()
        finally:
            self.db.close()
