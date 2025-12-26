from typing import Optional, List, Dict, Any
from app.data.motivo_repository import MotivoRepository


class MotivoService:
    def __init__(self, repo: MotivoRepository):
        self.repo = repo

    # ---------- Helpers ----------
    def _normalize_text(self, s: Optional[str]) -> Optional[str]:
        if s is None:
            return None
        s = str(s).strip()
        return s if s else None

    def _normalize_nombre(self, nombre: str) -> str:
        """
        Normaliza el nombre del motivo:
        - Trim
        - Evita dobles espacios
        - Capitaliza de forma suave (puedes cambiarlo si prefieres todo en mayúscula)
        """
        nombre = self._normalize_text(nombre)
        if not nombre:
            raise ValueError("El nombre del motivo es obligatorio")

        # Quitar dobles espacios internos
        nombre = " ".join(nombre.split())

        # Capitalización suave: primera letra mayúscula (sin forzar todo)
        # Ej: "control sano" -> "Control sano"
        return nombre[0].upper() + nombre[1:]

    # ---------- Operaciones ----------
    def crear_motivo(self, data: Dict[str, Any]) -> int:
        nombre = self._normalize_nombre(data.get("nombreMotivo", ""))
        descripcion = self._normalize_text(data.get("descripcion"))

        # Unicidad (activo)
        existente = self.repo.get_by_nombre(nombre)
        if existente:
            raise ValueError("Ya existe un motivo activo con ese nombre")

        payload = {
            "nombreMotivo": nombre,
            "descripcion": descripcion
        }
        return self.repo.create(payload)

    def obtener_por_id(self, id_motivo: int) -> Optional[Dict[str, Any]]:
        if not isinstance(id_motivo, int) or id_motivo <= 0:
            raise ValueError("idMotivoConsulta inválido")
        return self.repo.get_by_id(id_motivo)

    def obtener_por_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        nombre_norm = self._normalize_nombre(nombre)
        return self.repo.get_by_nombre(nombre_norm)

    def listar_activos(self) -> List[Dict[str, Any]]:
        return self.repo.list_active()

    def desactivar(self, id_motivo: int) -> None:
        if not isinstance(id_motivo, int) or id_motivo <= 0:
            raise ValueError("idMotivoConsulta inválido")
        self.repo.deactivate(id_motivo)
