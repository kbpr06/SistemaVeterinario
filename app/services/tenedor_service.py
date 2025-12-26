from typing import Dict, Any, Optional, List
from app.data.tenedor_repository import TenedorRepository


class TenedorService:
    def __init__(self, repo: TenedorRepository):
        self.repo = repo
    def _require_text(self, value: Any, field_name: str) -> str:
        """Valida que un campo de texto venga con contenido."""
        if value is None:
            raise ValueError(f"El campo '{field_name}' es obligatorio.")
        text = str(value).strip()
        if not text:
            raise ValueError(f"El campo '{field_name}' es obligatorio.")
        return text

    def _optional_text(self, value: Any) -> Optional[str]:
        """Normaliza texto opcional (si viene vacío, lo deja como None)."""
        if value is None:
            return None
        text = str(value).strip()
        return text if text else None

    # ------------------------
    # Casos de uso del módulo
    # ------------------------
    def crear_tenedor(self, data: Dict[str, Any]) -> int:
        """Crea un tenedor responsable:
        - valida obligatorios
        - evita rut duplicado
        - llama al repository para insertar"""
        rut = self._require_text(data.get("rut"), "rut")
        nombres = self._require_text(data.get("nombres"), "nombres")
        apellidos = self._require_text(data.get("apellidos"), "apellidos")
        telefono = self._require_text(data.get("telefono"), "telefono")
        sector = self._require_text(data.get("sector"), "sector")

        # Opcionales
        correo = self._optional_text(data.get("correo"))
        direccion = self._optional_text(data.get("direccion"))
        observaciones = self._optional_text(data.get("observaciones"))

        # Regla: no permitir rut duplicado (activo)
        existe = self.repo.get_by_rut(rut)
        if existe is not None:
            raise ValueError("Ya existe un tenedor activo con ese RUT.")

        payload = {
            "rut": rut,
            "nombres": nombres,
            "apellidos": apellidos,
            "telefono": telefono,
            "correo": correo,
            "direccion": direccion,
            "sector": sector,
            "observaciones": observaciones,
        }

        return self.repo.create(payload)

    def obtener_por_rut(self, rut: str) -> Optional[Dict[str, Any]]:
        """ Retorna un tenedor activo por rut, o None si no existe."""
        rut = self._require_text(rut, "rut")
        return self.repo.get_by_rut(rut)

    def listar_activos(self) -> List[Dict[str, Any]]:
        """ Lista tenedores activos."""
        return self.repo.list_active()

    def actualizar_tenedor(self, id_tenedor: int, data: Dict[str, Any]) -> None:
        """ Actualiza un tenedor (solo si está activo):
        - valida obligatorios mínimos (nombres/apellidos/telefono/sector)
        - el rut normalmente NO se cambia (si quisieras permitirlo, se implementa aparte)"""
        if not isinstance(id_tenedor, int) or id_tenedor <= 0:
            raise ValueError("El idTenedor no es válido.")

        nombres = self._require_text(data.get("nombres"), "nombres")
        apellidos = self._require_text(data.get("apellidos"), "apellidos")
        telefono = self._require_text(data.get("telefono"), "telefono")
        sector = self._require_text(data.get("sector"), "sector")

        correo = self._optional_text(data.get("correo"))
        direccion = self._optional_text(data.get("direccion"))
        observaciones = self._optional_text(data.get("observaciones"))

        payload = {
            "nombres": nombres,
            "apellidos": apellidos,
            "telefono": telefono,
            "correo": correo,
            "direccion": direccion,
            "sector": sector,
            "observaciones": observaciones,
        }

        self.repo.update(id_tenedor, payload)

    def desactivar_tenedor(self, id_tenedor: int) -> None:
        """Eliminación lógica: estadoRegistro = 0"""
        if not isinstance(id_tenedor, int) or id_tenedor <= 0:
            raise ValueError("El idTenedor no es válido.")
        self.repo.deactivate(id_tenedor)
