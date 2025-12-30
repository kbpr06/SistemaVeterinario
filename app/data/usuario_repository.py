from typing import Optional, Dict, Any, List
from app.data.db_connection import DBConnection


class UsuarioRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        """
        Crea un usuario y retorna idUsuario.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO usuario_sistema
        (idPersonal, nombreUsuario, claveEncriptada, rol, estadoRegistro)
        VALUES (?, ?, ?, ?, 1)
        """
        cur = conn.cursor()
        cur.execute(sql, (
            data.get("idPersonal"),
            data.get("nombreUsuario"),
            data.get("claveEncriptada"),
            data.get("rol"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def get_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retorna un usuario ACTIVO por nombreUsuario, o None.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM usuario_sistema
        WHERE nombreUsuario = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (username,))
        row = cur.fetchone()
        self.db.close()
        return dict(row) if row else None

    def exists_active_admin_sistema(self) -> bool:
        """
        Retorna True si existe al menos 1 usuario activo con rol admin_sistema.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT 1
        FROM usuario_sistema
        WHERE rol = 'admin_sistema' AND estadoRegistro = 1
        LIMIT 1
        """
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        self.db.close()
        return row is not None

    def list_active(self) -> List[Dict[str, Any]]:
        """
        Lista usuarios activos.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM usuario_sistema
        WHERE estadoRegistro = 1
        ORDER BY nombreUsuario
        """
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        self.db.close()
        return [dict(r) for r in rows]

    def deactivate(self, id_usuario: int) -> None:
        """
        Eliminación lógica.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE usuario_sistema
        SET estadoRegistro = 0
        WHERE idUsuario = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_usuario,))
        conn.commit()
        self.db.close()
