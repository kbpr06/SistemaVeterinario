from typing import Optional, List, Dict, Any
from app.data.especie_repository import EspecieRepository


class EspecieService:
    def __init__(self, repo: EspecieRepository):
        self.repo = repo

    def _normalize_text(self, s: Optional[str]) -> Optional[str]:
        if s is None:
            return None
        s = str(s).strip()
        return s if s else None

    def _normalize_nombre(self, nombre: str) -> str:
        nombre = self._normalize_text(nombre)
        if not nombre:
            raise ValueError("El nombre de la especie es obligatorio")

        nombre = " ".join(nombre.split())
        return nombre[0].upper() + nombre[1:]

    def crear_especie(self, data: Dict[str, Any]) -> int:
        nombre = self._normalize_nombre(data.get("nombreEspecie", ""))

        existente = self.repo.get_by_nombre(nombre)
        if existente:
            raise ValueError("Ya existe una especie activa con ese nombre")

        payload = {"nombreEspecie": nombre}
        return self.repo.create(payload)

    def obtener_por_id(self, id_especie: int) -> Optional[Dict[str, Any]]:
        if not isinstance(id_especie, int) or id_especie <= 0:
            raise ValueError("idEspecie inválido")
        return self.repo.get_by_id(id_especie)

    def obtener_por_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        nombre_norm = self._normalize_nombre(nombre)
        return self.repo.get_by_nombre(nombre_norm)

    def listar_activos(self) -> List[Dict[str, Any]]:
        return self.repo.list_active()

    def desactivar(self, id_especie: int) -> None:
        if not isinstance(id_especie, int) or id_especie <= 0:
            raise ValueError("idEspecie inválido")
        self.repo.deactivate(id_especie)
