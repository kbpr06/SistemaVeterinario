from typing import Optional, Dict, Any, List
from app.data.desparasitacion_aplicada_repository import DesparasitacionAplicadaRepository


class DesparasitacionAplicadaService:
    def __init__(self, repo: DesparasitacionAplicadaRepository):
        self.repo = repo

    def crear(
        self,
        id_atencion: int,
        id_tipo_desparasitacion: int,
        fecha_aplicacion: str,
        fecha_proxima_dosis: Optional[str] = None,
        dosis: Optional[str] = None,
        lote: Optional[str] = None,
        observaciones: Optional[str] = None,
    ) -> int:
        # Validaciones mínimas
        if not isinstance(id_atencion, int) or id_atencion <= 0:
            raise ValueError("idAtencion inválido")
        if not isinstance(id_tipo_desparasitacion, int) or id_tipo_desparasitacion <= 0:
            raise ValueError("idTipoDesparasitacion inválido")

        fecha_aplicacion = (fecha_aplicacion or "").strip()
        if not fecha_aplicacion:
            raise ValueError("fechaAplicacion es obligatoria (YYYY-MM-DD)")

        payload: Dict[str, Any] = {
            "idAtencion": id_atencion,
            "idTipoDesparasitacion": id_tipo_desparasitacion,
            "fechaAplicacion": fecha_aplicacion,
            "fechaProximaDosis": (fecha_proxima_dosis or "").strip() or None,
            "dosis": (dosis or "").strip() or None,
            "lote": (lote or "").strip() or None,
            "observaciones": (observaciones or "").strip() or None,
        }

        return self.repo.create(payload)

    def listar_por_atencion(self, id_atencion: int) -> List[Dict[str, Any]]:
        if not isinstance(id_atencion, int) or id_atencion <= 0:
            raise ValueError("idAtencion inválido")
        return self.repo.list_by_atencion(id_atencion)

    def desactivar(self, id_desparasitacion: int) -> None:
        if not isinstance(id_desparasitacion, int) or id_desparasitacion <= 0:
            raise ValueError("idDesparasitacion inválido")
        self.repo.deactivate(id_desparasitacion)
