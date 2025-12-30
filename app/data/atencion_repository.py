from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class AtencionRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        """
        Inserta una atención clínica y retorna el idAtencion.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO atencion_clinica
        (idAnimal, idPersonal, idMotivoConsulta, fechaAtencion, sintomas, pesoKg,
         diagnostico, tratamiento, observaciones, fechaControlSugerida, lugarAtencion, estadoRegistro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """
        cur = conn.cursor()
        cur.execute(sql, (
            data.get("idAnimal"),
            data.get("idPersonal"),
            data.get("idMotivoConsulta"),
            data.get("fechaAtencion"),
            data.get("sintomas"),
            data.get("pesoKg"),
            data.get("diagnostico"),
            data.get("tratamiento"),
            data.get("observaciones"),
            data.get("fechaControlSugerida"),
            data.get("lugarAtencion"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def get_by_id(self, id_atencion: int) -> Optional[Dict[str, Any]]:
        """
        Retorna una atención ACTIVA por idAtencion, o None.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM atencion_clinica
        WHERE idAtencion = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (id_atencion,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def list_by_animal(self, id_animal: int) -> List[Dict[str, Any]]:
        """
        Lista atenciones ACTIVAS de un animal, ordenadas por fecha (más reciente primero).
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM atencion_clinica
        WHERE idAnimal = ? AND estadoRegistro = 1
        ORDER BY fechaAtencion DESC, idAtencion DESC
        """
        cur = conn.cursor()
        cur.execute(sql, (id_animal,))
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def list_by_fecha(self, fecha: str) -> List[Dict[str, Any]]:
        """
        Lista atenciones ACTIVAS de una fecha exacta YYYY-MM-DD.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM atencion_clinica
        WHERE fechaAtencion = ? AND estadoRegistro = 1
        ORDER BY idAtencion DESC
        """
        cur = conn.cursor()
        cur.execute(sql, (fecha,))
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def deactivate(self, id_atencion: int) -> None:
        """
        Eliminación lógica.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE atencion_clinica
        SET estadoRegistro = 0
        WHERE idAtencion = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_atencion,))
        conn.commit()
        self.db.close()
