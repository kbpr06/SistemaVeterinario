from typing import Optional, List, Dict, Any
from app.data.db_connection import DBConnection


class MedicamentoAplicadoRepository:
    def __init__(self, db: DBConnection):
        self.db = db

    def create(self, data: Dict[str, Any]) -> int:
        """
        Inserta un medicamento aplicado y retorna el idMedicamentoAplicado generado.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        INSERT INTO medicamento_aplicado
        (idAtencion, idTipoMedicamento, fechaAplicacion, dosis, via, observaciones, estadoRegistro)
        VALUES (?, ?, ?, ?, ?, ?, 1)
        """

        cur = conn.cursor()
        cur.execute(sql, (
            data.get("idAtencion"),
            data.get("idTipoMedicamento"),
            data.get("fechaAplicacion"),
            data.get("dosis"),
            data.get("via"),
            data.get("observaciones"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        self.db.close()
        return new_id

    def list_by_atencion(self, id_atencion: int) -> List[Dict[str, Any]]:
        """
        Lista medicamentos aplicados (activos) de una atención.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM medicamento_aplicado
        WHERE idAtencion = ? AND estadoRegistro = 1
        ORDER BY fechaAplicacion DESC, idMedicamentoAplicado DESC
        """

        cur = conn.cursor()
        cur.execute(sql, (id_atencion,))
        rows = cur.fetchall()
        self.db.close()

        return [dict(r) for r in rows]

    def get_by_id(self, id_medicamento_aplicado: int) -> Optional[Dict[str, Any]]:
        """
        Retorna un medicamento aplicado activo por id, o None.
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        SELECT *
        FROM medicamento_aplicado
        WHERE idMedicamentoAplicado = ? AND estadoRegistro = 1
        """
        cur = conn.cursor()
        cur.execute(sql, (id_medicamento_aplicado,))
        row = cur.fetchone()
        self.db.close()

        return dict(row) if row else None

    def deactivate(self, id_medicamento_aplicado: int) -> None:
        """
        Eliminación lógica: estadoRegistro = 0
        """
        conn = self.db.connect()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos")

        sql = """
        UPDATE medicamento_aplicado
        SET estadoRegistro = 0
        WHERE idMedicamentoAplicado = ?
        """
        cur = conn.cursor()
        cur.execute(sql, (id_medicamento_aplicado,))
        conn.commit()
        self.db.close()
