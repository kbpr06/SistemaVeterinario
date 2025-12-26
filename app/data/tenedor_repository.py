from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class TenedorRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        """Inserta un tenedor responsable y retorna el id generado.
        data: diccionario con los campos del tenedor."""
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """INSERT INTO tenedor_responsable
        (rut, nombres, apellidos, telefono, correo, direccion, sector, observaciones, estadoRegistro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)"""
        cur = conn.cursor()
        cur.execute(sql, (
            data.get("rut"),
            data.get("nombres"),
            data.get("apellidos"),
            data.get("telefono"),
            data.get("correo"),
            data.get("direccion"),
            data.get("sector"),
            data.get("observaciones"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def get_by_rut(self, rut: str) -> Optional[Dict[str, Any]]:
        """ Busca un tenedor por RUT (solo activos).
        Retorna dict con columnas, o None si no existe."""
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """SELECT *
        FROM tenedor_responsable
        WHERE rut = ? AND estadoRegistro = 1 """
        cur = conn.cursor()
        cur.execute(sql, (rut,))
        row = cur.fetchone()
        self.db.close()

        if row is None:
            return None
        return dict(row)

    def list_active(self) -> List[Dict[str, Any]]:
        """Lista todos los tenedores activos."""
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """SELECT *
        FROM tenedor_responsable
        WHERE estadoRegistro = 1
        ORDER BY apellidos, nombres
        """
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def update(self, id_tenedor: int, data: Dict[str, Any]) -> None:
        """Actualiza datos de un tenedor por id."""
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """UPDATE tenedor_responsable
        SET nombres = ?,
            apellidos = ?,
            telefono = ?,
            correo = ?,
            direccion = ?,
            sector = ?,
            observaciones = ?
        WHERE idTenedor = ? AND estadoRegistro = 1"""
        cur = conn.cursor()
        cur.execute(sql, (
            data.get("nombres"),
            data.get("apellidos"),
            data.get("telefono"),
            data.get("correo"),
            data.get("direccion"),
            data.get("sector"),
            data.get("observaciones"),
            id_tenedor,
        ))
        conn.commit()
        self.db.close()

    def deactivate(self, id_tenedor: int) -> None:
        """ Eliminación lógica: marca estadoRegistro = 0"""
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """ UPDATE tenedor_responsable
        SET estadoRegistro = 0
        WHERE idTenedor = ?"""
        cur = conn.cursor()
        cur.execute(sql, (id_tenedor,))
        conn.commit()
        self.db.close()
