from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class AnimalRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        """
        Inserta un animal y retorna el idAnimal generado.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO animal
        (idTenedor, idEspecie, idRaza, nombre, sexo, fechaNacimientoEst, edadEstimadaMeses, color, estadoReproductivo,
         numeroMicrochip, viveDentroCasa, conviveConOtros, observaciones, estadoRegistro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        """
        cur = conn.cursor()
        
        cur.execute(sql, (
            data.get("idTenedor"),
            data.get("idEspecie"),
            data.get("idRaza"),
            data.get("nombre"),
            data.get("sexo"),
            data.get("fechaNacimientoEst"),
            data.get("edadEstimadaMeses"),
            data.get("color"),
            data.get("estadoReproductivo"),
            data.get("numeroMicrochip"),
            data.get("viveDentroCasa"),
            data.get("conviveConOtros"),
            data.get("observaciones"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def get_by_id(self, id_animal: int) -> Optional[Dict[str, Any]]:
        """
        Retorna un animal activo por idAnimal, o None.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM animal
        WHERE idAnimal = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (id_animal,))
        row = cur.fetchone()
        self.db.close()

        return dict(row) if row else None

    def get_by_microchip(self, microchip: str) -> Optional[Dict[str, Any]]:
        """
        Retorna un animal activo por numeroMicrochip (si existe), o None.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM animal
        WHERE numeroMicrochip = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (microchip,))
        row = cur.fetchone()
        self.db.close()

        return dict(row) if row else None

    def list_active(self) -> List[Dict[str, Any]]:
        """
        Lista animales activos.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM animal
        WHERE estadoRegistro = 1
        ORDER BY nombre
        """
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.db.close()

        return [dict(r) for r in rows]

    def list_by_tenedor(self, id_tenedor: int) -> List[Dict[str, Any]]:
        """
        Lista animales activos de un tenedor.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM animal
        WHERE idTenedor = ? AND estadoRegistro = 1
        ORDER BY nombre
        """
        cur = conn.cursor()
        cur.execute(sql, (id_tenedor,))
        rows = cur.fetchall()
        self.db.close()

        return [dict(r) for r in rows]

    def deactivate(self, id_animal: int) -> None:
        """
        Eliminación lógica: estadoRegistro = 0
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE animal
        SET estadoRegistro = 0
        WHERE idAnimal = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_animal,))
        conn.commit()
        self.db.close()
