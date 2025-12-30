from typing import Optional, Dict, Any, List
from app.data.tipo_vacuna_repository import TipoVacunaRepository
from app.data.especie_repository import EspecieRepository


class TipoVacunaService:
    def __init__(self, repo: TipoVacunaRepository, especie_repo: EspecieRepository):
        self.repo = repo
        self.especie_repo = especie_repo

    def crear(self, data: Dict[str, Any]) -> int:
        nombre = (data.get("nombreVacuna") or "").strip()
        if not nombre:
            raise ValueError("nombreVacuna es obligatorio")

        # Duplicado por nombre (case-insensitive)
        existente = self.repo.get_by_nombre(nombre)
        if existente:
            raise ValueError("Ya existe un tipo de vacuna activo con ese nombre")

        descripcion = (data.get("descripcion") or "").strip() or None

        id_especie = data.get("idEspecie")
        if id_especie is not None and str(id_especie).strip() != "":
            try:
                id_especie = int(id_especie)
            except Exception:
                raise ValueError("idEspecie debe ser un número entero")

            esp = self.especie_repo.get_by_id(id_especie)
            if not esp:
                raise ValueError("La especie indicada no existe o está inactiva")
        else:
            id_especie = None

        intervalo = data.get("intervaloRecMeses")
        if intervalo is None or str(intervalo).strip() == "":
            intervalo = None
        else:
            try:
                intervalo = int(intervalo)
            except Exception:
                raise ValueError("intervaloRecMeses debe ser un entero")
            if intervalo < 0:
                raise ValueError("intervaloRecMeses no puede ser negativo")

        payload = {
            "nombreVacuna": nombre,
            "descripcion": descripcion,
            "idEspecie": id_especie,
            "intervaloRecMeses": intervalo,
        }
        return self.repo.create(payload)

    def obtener_por_id(self, id_tipo: int) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(int(id_tipo))

    def listar_activos(self) -> List[Dict[str, Any]]:
        return self.repo.list_active()

    def listar_para_especie(self, id_especie: int) -> List[Dict[str, Any]]:
        return self.repo.list_by_especie(int(id_especie))

    def desactivar(self, id_tipo: int) -> None:
        self.repo.deactivate(int(id_tipo))
