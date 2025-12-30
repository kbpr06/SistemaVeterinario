from typing import Optional, Dict, Any, List
from app.data.tipo_desparasitacion_repository import TipoDesparasitacionRepository


class TipoDesparasitacionService:
    TIPOS_VALIDOS = {"Interna", "Externa", "Mixta"}

    def __init__(self, repo: TipoDesparasitacionRepository):
        self.repo = repo

    def crear(
        self,
        nombre_desparasitacion: str,
        tipo: str = "Mixta",
        id_especie: Optional[int] = None,
        intervalo_rec_meses: Optional[int] = None,
    ) -> int:

        nombre_desparasitacion = (nombre_desparasitacion or "").strip()
        if not nombre_desparasitacion:
            raise ValueError("El nombre de la desparasitación es obligatorio")

        tipo = (tipo or "Mixta").strip().capitalize()
        # Capitalize deja "Interna", "Externa", "Mixta" si viene bien escrito
        if tipo not in self.TIPOS_VALIDOS:
            raise ValueError("Tipo inválido. Use: Interna, Externa o Mixta")

        if id_especie is not None:
            if not isinstance(id_especie, int) or id_especie <= 0:
                raise ValueError("idEspecie inválido")

        if intervalo_rec_meses is not None:
            if not isinstance(intervalo_rec_meses, int) or intervalo_rec_meses < 0:
                raise ValueError("intervaloRecMeses inválido (>= 0)")

        payload: Dict[str, Any] = {
            "nombreDesparasitacion": nombre_desparasitacion,
            "tipo": tipo,
            "idEspecie": id_especie,
            "intervaloRecMeses": intervalo_rec_meses,
        }
        return self.repo.create(payload)

    def listar_activos(self) -> List[Dict[str, Any]]:
        return self.repo.list_active()

    def obtener_por_nombre(self, nombre: str) -> Optional[Dict[str, Any]]:
        nombre = (nombre or "").strip()
        if not nombre:
            return None
        return self.repo.get_by_name(nombre)

    def desactivar(self, id_tipo: int) -> None:
        if not isinstance(id_tipo, int) or id_tipo <= 0:
            raise ValueError("idTipoDesparasitacion inválido")
        self.repo.deactivate(id_tipo)
