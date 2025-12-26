from typing import Optional, List, Dict, Any
from app.data.raza_repository import RazaRepository
from app.services.especie_service import EspecieService


class RazaService:
    def __init__(self, repo: RazaRepository, especie_service: EspecieService):
        self.repo = repo
        self.especie_service = especie_service

    def _normalize_text(self, s: Optional[str]) -> Optional[str]:
        if s is None:
            return None
        s = str(s).strip()
        return s if s else None

    def _normalize_nombre(self, nombre: str) -> str:
        nombre = self._normalize_text(nombre)
        if not nombre:
            raise ValueError("El nombre de la raza es obligatorio")

        nombre = " ".join(nombre.split())
        return nombre[0].upper() + nombre[1:]

    def crear_raza(self, data: Dict[str, Any]) -> int:
        id_especie = data.get("idEspecie")
        if not isinstance(id_especie, int) or id_especie <= 0:
            raise ValueError("idEspecie inválido")

        # Validar especie activa
        especie = self.especie_service.obtener_por_id(id_especie)
        if not especie:
            raise ValueError("La especie indicada no existe o está desactivada")

        nombre = self._normalize_nombre(data.get("nombreRaza", ""))

        # Evitar duplicados en la misma especie
        existente = self.repo.get_by_nombre_en_especie(id_especie, nombre)
        if existente:
            raise ValueError("Ya existe una raza activa con ese nombre para esa especie")

        payload = {
            "idEspecie": id_especie,
            "nombreRaza": nombre
        }
        return self.repo.create(payload)

    def obtener_por_id(self, id_raza: int) -> Optional[Dict[str, Any]]:
        if not isinstance(id_raza, int) or id_raza <= 0:
            raise ValueError("idRaza inválido")
        return self.repo.get_by_id(id_raza)

    def listar_activos(self) -> List[Dict[str, Any]]:
        return self.repo.list_active()

    def listar_por_especie(self, id_especie: int) -> List[Dict[str, Any]]:
        if not isinstance(id_especie, int) or id_especie <= 0:
            raise ValueError("idEspecie inválido")
        return self.repo.list_by_especie(id_especie)

    def desactivar(self, id_raza: int) -> None:
        if not isinstance(id_raza, int) or id_raza <= 0:
            raise ValueError("idRaza inválido")
        self.repo.deactivate(id_raza)
