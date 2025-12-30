from typing import Optional, Dict, Any, List
import re
from app.data.atencion_repository import AtencionRepository
from app.data.animal_repository import AnimalRepository
from app.data.personal_repository import PersonalRepository
from app.data.motivo_repository import MotivoRepository


class AtencionService:
    LUGARES_VALIDOS = {"Consulta", "Operativo", "Domicilio"}
    _RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")

    def __init__(
        self,
        repo: AtencionRepository,
        animal_repo: AnimalRepository,
        personal_repo: PersonalRepository,
        motivo_repo: MotivoRepository
    ):
        self.repo = repo
        self.animal_repo = animal_repo
        self.personal_repo = personal_repo
        self.motivo_repo = motivo_repo

    def _validar_fecha(self, value: Optional[str], campo: str, obligatorio: bool) -> Optional[str]:
        if value is None or str(value).strip() == "":
            if obligatorio:
                raise ValueError(f"{campo} es obligatorio")
            return None

        value = str(value).strip()
        if not self._RE_FECHA.match(value):
            raise ValueError(f"{campo} debe tener formato YYYY-MM-DD")
        return value

    def _validar_peso(self, peso) -> Optional[float]:
        if peso is None or str(peso).strip() == "":
            return None
        try:
            peso_f = float(peso)
        except Exception:
            raise ValueError("pesoKg debe ser un número")
        if peso_f < 0:
            raise ValueError("pesoKg no puede ser negativo")
        return peso_f

    def crear_atencion(self, data: Dict[str, Any]) -> int:
        # Obligatorios
        id_animal = data.get("idAnimal")
        id_personal = data.get("idPersonal")
        id_motivo = data.get("idMotivoConsulta")

        if not id_animal:
            raise ValueError("idAnimal es obligatorio")
        if not id_personal:
            raise ValueError("idPersonal es obligatorio")
        if not id_motivo:
            raise ValueError("idMotivoConsulta es obligatorio")

        fecha_atencion = self._validar_fecha(data.get("fechaAtencion"), "fechaAtencion", True)

        lugar = data.get("lugarAtencion") or "Consulta"
        lugar = str(lugar).strip()
        if lugar not in self.LUGARES_VALIDOS:
            raise ValueError("lugarAtencion inválido (Consulta/Operativo/Domicilio)")

        # Validaciones de FK (para dar error bonito antes que SQLite)
        animal = self.animal_repo.get_by_id(int(id_animal))
        if not animal:
            raise ValueError("El animal indicado no existe o está inactivo")

        personal = self.personal_repo.get_by_id(int(id_personal))
        if not personal:
            raise ValueError("El personal indicado no existe o está inactivo")

        motivo = self.motivo_repo.get_by_id(int(id_motivo))
        if not motivo:
            raise ValueError("El motivo de consulta indicado no existe o está inactivo")

        payload = {
            "idAnimal": int(id_animal),
            "idPersonal": int(id_personal),
            "idMotivoConsulta": int(id_motivo),
            "fechaAtencion": fecha_atencion,
            "sintomas": (data.get("sintomas") or "").strip() or None,
            "pesoKg": self._validar_peso(data.get("pesoKg")),
            "diagnostico": (data.get("diagnostico") or "").strip() or None,
            "tratamiento": (data.get("tratamiento") or "").strip() or None,
            "observaciones": (data.get("observaciones") or "").strip() or None,
            "fechaControlSugerida": self._validar_fecha(data.get("fechaControlSugerida"), "fechaControlSugerida", False),
            "lugarAtencion": lugar,
        }
        return self.repo.create(payload)

    def obtener_por_id(self, id_atencion: int) -> Optional[Dict[str, Any]]:
        return self.repo.get_by_id(id_atencion)

    def listar_por_animal(self, id_animal: int) -> List[Dict[str, Any]]:
        return self.repo.list_by_animal(int(id_animal))

    def listar_por_fecha(self, fecha: str) -> List[Dict[str, Any]]:
        fecha_ok = self._validar_fecha(fecha, "fecha", True)
        return self.repo.list_by_fecha(fecha_ok)

    def desactivar(self, id_atencion: int) -> None:
        self.repo.deactivate(int(id_atencion))
