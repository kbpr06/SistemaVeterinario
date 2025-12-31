from typing import Optional, List, Dict, Any

from app.data.medicamento_aplicado_repository import MedicamentoAplicadoRepository
from app.data.atencion_repository import AtencionRepository
from app.data.tipo_medicamento_repository import TipoMedicamentoRepository


class MedicamentoAplicadoService:
    VIAS_VALIDAS = {"IM", "IV", "VO", "SC", "Topica", "Otra"}

    def __init__(
        self,
        repo: MedicamentoAplicadoRepository,
        atencion_repo: AtencionRepository,
        tipo_medicamento_repo: TipoMedicamentoRepository,
    ):
        self.repo = repo
        self.atencion_repo = atencion_repo
        self.tipo_medicamento_repo = tipo_medicamento_repo

    def crear(
        self,
        id_atencion: int,
        id_tipo_medicamento: int,
        fecha_aplicacion: str,
        dosis: Optional[str] = None,
        via: Optional[str] = None,
        observaciones: Optional[str] = None,
    ) -> int:
        # 1) Validaciones básicas de IDs
        if not isinstance(id_atencion, int) or id_atencion <= 0:
            raise ValueError("idAtencion inválido")
        if not isinstance(id_tipo_medicamento, int) or id_tipo_medicamento <= 0:
            raise ValueError("idTipoMedicamento inválido")

        # 2) Validar existencia (para no depender solo del error SQL)
        at = self.atencion_repo.get_by_id(id_atencion)
        if not at:
            raise ValueError("No existe una atención clínica activa con ese idAtencion")

        tm = self.tipo_medicamento_repo.get_by_id(id_tipo_medicamento)
        if not tm:
            raise ValueError("No existe un tipo de medicamento activo con ese idTipoMedicamento")

        # 3) Validar fecha
        fecha_aplicacion = (fecha_aplicacion or "").strip()
        if not fecha_aplicacion:
            raise ValueError("fechaAplicacion es obligatoria (YYYY-MM-DD)")

        # 4) Validar vía (si viene)
        via_clean = (via or "").strip()
        if via_clean:
            # Respetamos mayúsculas como en CHECK, pero aceptamos que el usuario escriba "im", "Iv", etc.
            via_clean = via_clean.upper()
            # "Topica" tiene mayúscula inicial en tu CHECK, así que la normalizamos:
            if via_clean == "TOPICA":
                via_clean = "Topica"

            if via_clean not in self.VIAS_VALIDAS:
                raise ValueError(f"Vía inválida. Debe ser una de: {', '.join(sorted(self.VIAS_VALIDAS))}")
        else:
            via_clean = None  # en BD se permite NULL

        payload: Dict[str, Any] = {
            "idAtencion": id_atencion,
            "idTipoMedicamento": id_tipo_medicamento,
            "fechaAplicacion": fecha_aplicacion,
            "dosis": (dosis or "").strip() or None,
            "via": via_clean,
            "observaciones": (observaciones or "").strip() or None,
        }

        return self.repo.create(payload)

    def listar_por_atencion(self, id_atencion: int) -> List[Dict[str, Any]]:
        if not isinstance(id_atencion, int) or id_atencion <= 0:
            raise ValueError("idAtencion inválido")
        return self.repo.list_by_atencion(id_atencion)

    def obtener_por_id(self, id_medicamento_aplicado: int) -> Optional[Dict[str, Any]]:
        if not isinstance(id_medicamento_aplicado, int) or id_medicamento_aplicado <= 0:
            raise ValueError("idMedicamentoAplicado inválido")
        return self.repo.get_by_id(id_medicamento_aplicado)

    def desactivar(self, id_medicamento_aplicado: int) -> None:
        if not isinstance(id_medicamento_aplicado, int) or id_medicamento_aplicado <= 0:
            raise ValueError("idMedicamentoAplicado inválido")
        self.repo.deactivate(id_medicamento_aplicado)
