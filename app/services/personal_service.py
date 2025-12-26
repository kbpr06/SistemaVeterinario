from typing import Optional, List, Dict, Any
from datetime import date
from app.data.personal_repository import PersonalRepository


class PersonalService:
    def __init__(self, repo: PersonalRepository):
        self.repo = repo

    # ---------- Helpers ----------
    def _normalize_text(self, s: Optional[str]) -> Optional[str]:
        if s is None:
            return None
        s = str(s).strip()
        return s if s else None

    def _normalize_rut(self, rut: str) -> str:
        """
        Normaliza a formato: 12345678-9 (sin puntos, con guion).
        Acepta entradas con puntos/espacios; fuerza K mayúscula.
        """
        rut = self._normalize_text(rut)
        if not rut:
            raise ValueError("El RUT es obligatorio")

        r = rut.replace(".", "").replace(" ", "").upper()
        if "-" not in r:
            raise ValueError("El RUT debe incluir guion (ej: 12345678-9)")

        cuerpo, dv = r.split("-", 1)
        cuerpo = cuerpo.strip()
        dv = dv.strip()

        if not cuerpo.isdigit():
            raise ValueError("El cuerpo del RUT debe ser numérico (sin puntos)")
        if dv not in "0123456789K":
            raise ValueError("El dígito verificador del RUT es inválido")

        return f"{cuerpo}-{dv}"

    def _validate_date_yyyy_mm_dd(self, value: Optional[str], field_name: str) -> Optional[str]:
        value = self._normalize_text(value)
        if not value:
            return None
        # Validación simple: intenta parsear
        try:
            y, m, d = value.split("-")
            _ = date(int(y), int(m), int(d))
        except Exception:
            raise ValueError(f"{field_name} debe tener formato YYYY-MM-DD")
        return value

    # ---------- Operaciones ----------
    def crear_personal(self, data: Dict[str, Any]) -> int:
        rut = self._normalize_rut(data.get("rut", ""))
        nombres = self._normalize_text(data.get("nombres"))
        apellidos = self._normalize_text(data.get("apellidos"))
        cargo = self._normalize_text(data.get("cargo"))

        if not nombres:
            raise ValueError("Los nombres son obligatorios")
        if not apellidos:
            raise ValueError("Los apellidos son obligatorios")
        if not cargo:
            raise ValueError("El cargo es obligatorio")

        # (Recomendados / opcionales)
        area_trabajo = self._normalize_text(data.get("areaTrabajo"))
        telefono = self._normalize_text(data.get("telefono"))
        correo = self._normalize_text(data.get("correo"))
        observaciones = self._normalize_text(data.get("observaciones"))

        fecha_ingreso = self._validate_date_yyyy_mm_dd(data.get("fechaIngreso"), "Fecha de ingreso")
        fecha_nac = self._validate_date_yyyy_mm_dd(data.get("fechaNacimiento"), "Fecha de nacimiento")

        # Unicidad RUT (activo)
        existente = self.repo.get_by_rut(rut)
        if existente:
            raise ValueError("Ya existe un personal activo con ese RUT")

        payload = {
            "rut": rut,
            "nombres": nombres,
            "apellidos": apellidos,
            "cargo": cargo,
            "areaTrabajo": area_trabajo,
            "telefono": telefono,
            "correo": correo,
            "fechaIngreso": fecha_ingreso,
            "fechaNacimiento": fecha_nac,
            "observaciones": observaciones,
        }
        return self.repo.create(payload)

    def obtener_por_rut(self, rut: str) -> Optional[Dict[str, Any]]:
        rut_norm = self._normalize_rut(rut)
        return self.repo.get_by_rut(rut_norm)

    def obtener_por_id(self, id_personal: int) -> Optional[Dict[str, Any]]:
        if not isinstance(id_personal, int) or id_personal <= 0:
            raise ValueError("idPersonal inválido")
        return self.repo.get_by_id(id_personal)

    def listar_activos(self) -> List[Dict[str, Any]]:
        return self.repo.list_active()

    def desactivar(self, id_personal: int) -> None:
        if not isinstance(id_personal, int) or id_personal <= 0:
            raise ValueError("idPersonal inválido")
        self.repo.deactivate(id_personal)
