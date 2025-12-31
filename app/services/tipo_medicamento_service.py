from typing import Optional, List, Dict, Any
from app.data.tipo_medicamento_repository import TipoMedicamentoRepository


CATEGORIAS_VALIDAS = {
    "antibiotico",
    "antiinflamatorio",
    "analgesico",
    "vitaminas",
    "fluidoterapia",
    "gastroprotector",
    "otro",
}

class TipoMedicamentoService:
    def __init__(self, repo: TipoMedicamentoRepository):
        self.repo = repo

    def crear(self, data: Dict[str, Any]) -> int:
        nombre = (data.get("nombreMedicamento") or "").strip()
        if not nombre:
            raise ValueError("nombreMedicamento es obligatorio")

        categoria = (data.get("categoria") or "").strip().lower()
        if categoria not in CATEGORIAS_VALIDAS:
            raise ValueError(f"categoria inválida. Debe ser una de: {sorted(CATEGORIAS_VALIDAS)}")

        descripcion = (data.get("descripcion") or "").strip() or None

        # Evitar duplicados por nombre (aunque la BD también lo impide)
        existente = self.repo.get_by_nombre(nombre)
        if existente:
            raise ValueError("Ya existe un tipo de medicamento activo con ese nombre")

        payload: Dict[str, Any] = {
            "nombreMedicamento": nombre,
            "categoria": categoria,
            "descripcion": descripcion,
        }
        return self.repo.create(payload)

    def obtener_por_id(self, id_tipo: int) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(id_tipo)

    def listar_activos(self) -> List[Dict[str, Any]]:
        return self.repo.list_active()

    def listar_por_categoria(self, categoria: str) -> List[Dict[str, Any]]:
        categoria = (categoria or "").strip().lower()
        if categoria not in CATEGORIAS_VALIDAS:
            raise ValueError(f"categoria inválida. Debe ser una de: {sorted(CATEGORIAS_VALIDAS)}")
        return self.repo.list_by_categoria(categoria)

    def desactivar(self, id_tipo: int) -> None:
        if not isinstance(id_tipo, int) or id_tipo <= 0:
            raise ValueError("idTipoMedicamento inválido")
        self.repo.deactivate(id_tipo)
