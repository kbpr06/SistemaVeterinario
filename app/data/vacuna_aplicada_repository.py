from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class VacunaAplicadaRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        """
        Inserta una vacuna aplicada y retorna el idVacunaAplicada generado.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO vacuna_aplicada
        (idAtencion, idTipoVacuna, fechaAplicacion, fechaProximaDosis, dosis, lote, observaciones, estadoRegistro)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """
        cur = conn.cursor()
        cur.execute(sql, (
            data.get("idAtencion"),
            data.get("idTipoVacuna"),
            data.get("fechaAplicacion"),
            data.get("fechaProximaDosis"),
            data.get("dosis"),
            data.get("lote"),
            data.get("observaciones"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def get_by_id(self, id_vacuna_aplicada: int) -> Optional[Dict[str, Any]]:
        """
        Retorna una vacuna aplicada activa por idVacunaAplicada, o None.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM vacuna_aplicada
        WHERE idVacunaAplicada = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (id_vacuna_aplicada,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def list_by_atencion(self, id_atencion: int) -> List[Dict[str, Any]]:
        """
        Lista vacunas activas asociadas a una atención.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM vacuna_aplicada
        WHERE idAtencion = ? AND estadoRegistro = 1
        ORDER BY fechaAplicacion DESC, idVacunaAplicada DESC
        """
        cur = conn.cursor()
        cur.execute(sql, (id_atencion,))
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def list_all_active(self) -> List[Dict[str, Any]]:
        """
        Lista todas las vacunas aplicadas activas.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM vacuna_aplicada
        WHERE estadoRegistro = 1
        ORDER BY fechaAplicacion DESC, idVacunaAplicada DESC
        """
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def deactivate(self, id_vacuna_aplicada: int) -> None:
        """
        Eliminación lógica: estadoRegistro = 0
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE vacuna_aplicada
        SET estadoRegistro = 0
        WHERE idVacunaAplicada = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_vacuna_aplicada,))
        conn.commit()
        self.db.close()
