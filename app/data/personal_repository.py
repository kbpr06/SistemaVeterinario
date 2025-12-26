from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class PersonalRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO personal_veterinario
        (rut, nombres, apellidos, cargo, areaTrabajo, telefono, correo,
         fechaIngreso, fechaNacimiento, observaciones, estadoRegistro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """
        cur = conn.cursor()
        cur.execute(sql, (
            data.get("rut"),
            data.get("nombres"),
            data.get("apellidos"),
            data.get("cargo"),
            data.get("areaTrabajo"),
            data.get("telefono"),
            data.get("correo"),
            data.get("fechaIngreso"),
            data.get("fechaNacimiento"),
            data.get("observaciones"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def get_by_id(self, id_personal: int) -> Optional[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM personal_veterinario
        WHERE idPersonal = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (id_personal,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def get_by_rut(self, rut: str) -> Optional[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM personal_veterinario
        WHERE rut = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (rut,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def list_active(self) -> List[Dict[str, Any]]:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM personal_veterinario
        WHERE estadoRegistro = 1
        ORDER BY apellidos, nombres
        """
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def deactivate(self, id_personal: int) -> None:
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE personal_veterinario
        SET estadoRegistro = 0
        WHERE idPersonal = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_personal,))
        conn.commit()
        self.db.close()
