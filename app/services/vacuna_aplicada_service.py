from typing import Optional, List, Dict, Any
from app.data.vacuna_aplicada_repository import VacunaAplicadaRepository


class VacunaAplicadaService:
    def __init__(self, repo: VacunaAplicadaRepository):
        self.repo = repo

    def crear(
        self,
        id_atencion: int,
        id_tipo_vacuna: int,
        fecha_aplicacion: str,
        fecha_proxima_dosis: Optional[str] = None,
        dosis: Optional[str] = None,
        lote: Optional[str] = None,
        observaciones: Optional[str] = None,
    ) -> int:
        # Validaciones mínimas 
        if not isinstance(id_atencion, int) or id_atencion <= 0:
            raise ValueError("idAtencion inválido")
        if not isinstance(id_tipo_vacuna, int) or id_tipo_vacuna <= 0:
            raise ValueError("idTipoVacuna inválido")

        fecha_aplicacion = (fecha_aplicacion or "").strip()
        if not fecha_aplicacion:
            raise ValueError("fechaAplicacion es obligatoria (YYYY-MM-DD)")

        payload: Dict[str, Any] = {
            "idAtencion": id_atencion,
            "idTipoVacuna": id_tipo_vacuna,
            "fechaAplicacion": fecha_aplicacion,
            "fechaProximaDosis": (fecha_proxima_dosis or "").strip() or None,
            "dosis": (dosis or "").strip() or None,
            "lote": (lote or "").strip() or None,
            "observaciones": (observaciones or "").strip() or None,
        }

        return self.repo.create(payload)

    def obtener_por_id(self, id_vacuna_aplicada: int) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(id_vacuna_aplicada)

    def listar_por_atencion(self, id_atencion: int) -> List[Dict[str, Any]]:
        return self.repo.list_by_atencion(id_atencion)

    def listar_todas(self) -> List[Dict[str, Any]]:
        return self.repo.list_all_active()

    def desactivar(self, id_vacuna_aplicada: int) -> None:
        self.repo.deactivate(id_vacuna_aplicada)
