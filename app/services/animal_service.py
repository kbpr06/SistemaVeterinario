from typing import Dict, Any, Optional, List
from datetime import datetime, date
from app.data.animal_repository import AnimalRepository


class AnimalService:
    """
    Capa de lógica de negocio del módulo Animal.
    Aquí validamos reglas y formateamos datos (payload) antes de enviarlos al Repository.
    """

    def __init__(self, repo: AnimalRepository):
        self.repo = repo

    # ------------------------
    # Helpers de validación
    # ------------------------
    def _require_int(self, value: Any, field_name: str) -> int:
        if value is None or str(value).strip() == "":
            raise ValueError(f"El campo '{field_name}' es obligatorio.")
        try:
            n = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"El campo '{field_name}' debe ser un número entero.")
        if n <= 0:
            raise ValueError(f"El campo '{field_name}' debe ser mayor que 0.")
        return n

    def _require_text(self, value: Any, field_name: str) -> str:
        if value is None:
            raise ValueError(f"El campo '{field_name}' es obligatorio.")
        text = str(value).strip()
        if not text:
            raise ValueError(f"El campo '{field_name}' es obligatorio.")
        return text

    def _optional_text(self, value: Any) -> Optional[str]:
        if value is None:
            return None
        text = str(value).strip()
        return text if text else None

    def _optional_text_maxlen(self, value: Any, field_name: str, max_len: int) -> Optional[str]:
        if value is None:
            return None
        text = str(value).strip()
        if not text:
            return None
        if len(text) > max_len:
            raise ValueError(f"El campo '{field_name}' no puede superar {max_len} caracteres.")
        return text

    def _optional_int01(self, value: Any, field_name: str) -> Optional[int]:
        """
        Para campos 1/0/NULL (ej: viveDentroCasa).
        """
        if value is None or str(value).strip() == "":
            return None
        try:
            n = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"El campo '{field_name}' debe ser 1, 0 o vacío.")
        if n not in (0, 1):
            raise ValueError(f"El campo '{field_name}' debe ser 1, 0 o vacío.")
        return n

    def _optional_int_range(self, value: Any, field_name: str, min_v: int, max_v: int) -> Optional[int]:
        """
        Entero opcional con rango.
        """
        if value is None or str(value).strip() == "":
            return None
        try:
            n = int(value)
        except (TypeError, ValueError):
            raise ValueError(f"El campo '{field_name}' debe ser un número entero.")
        if n < min_v or n > max_v:
            raise ValueError(f"El campo '{field_name}' debe estar entre {min_v} y {max_v}.")
        return n

    def _validate_sexo(self, sexo: str) -> str:
        sexo = sexo.strip()
        if sexo not in ("M", "H", "Desconocido"):
            raise ValueError("El campo 'sexo' debe ser 'M', 'H' o 'Desconocido'.")
        return sexo

    def _optional_date_yyyy_mm_dd(self, value: Any, field_name: str) -> Optional[str]:
        """
        Valida fecha en formato YYYY-MM-DD.
        Retorna el string normalizado o None si viene vacío.
        """
        if value is None or str(value).strip() == "":
            return None

        text = str(value).strip()
        try:
            dt = datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError(f"El campo '{field_name}' debe tener formato YYYY-MM-DD (ej: 2020-03-15).")

        hoy = date.today()
        if dt > hoy:
            raise ValueError(f"El campo '{field_name}' no puede ser una fecha futura.")
        if dt.year < 1990:
            # Ajustable: es una barrera razonable para evitar errores (ej: 1900)
            raise ValueError(f"El campo '{field_name}' parece demasiado antiguo. Revisa el año.")

        return dt.isoformat()

    # ------------------------
    # Convive con otros (lista controlada)
    # ------------------------
    _CONVIVE_OPCIONES_VALIDAS = {
        "Perros",
        "Gatos",
        "Aves",
        "Equinos",
        "Bovinos",
        "Porcinos",
        "Caprinos",
        "Ovinos",
        "Otros",
        "No sabe",
        "Solo",
    }

    def _validate_convive_checklist(self, value: Any) -> Optional[str]:
        """
        Recibe:
        - None / "" => None
        - "Perros,Gatos" => valida y normaliza
        - ["Perros","Gatos"] => valida y normaliza

        Devuelve string guardable en BD: "Gatos,Perros" (ordenado)
        """
        if value is None:
            return None

        # Si viene como texto
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return None
            parts = [p.strip() for p in text.split(",") if p.strip()]

        # Si viene como lista
        elif isinstance(value, list):
            parts = []
            for item in value:
                if item is None:
                    continue
                s = str(item).strip()
                if s:
                    parts.append(s)
            if not parts:
                return None
        else:
            raise ValueError("El campo 'conviveConOtros' debe ser texto o lista.")

        # Normalizar (eliminar duplicados)
        clean = []
        seen = set()
        for p in parts:
            if p not in self._CONVIVE_OPCIONES_VALIDAS:
                raise ValueError(f"Valor no permitido en 'conviveConOtros': '{p}'.")
            if p not in seen:
                seen.add(p)
                clean.append(p)

        # Ordenado para consistencia en BD
        clean_sorted = sorted(clean)
        return ",".join(clean_sorted) if clean_sorted else None

    # ------------------------
    # Casos de uso del módulo
    # ------------------------
    def crear_animal(self, data: Dict[str, Any]) -> int:
        """
        Crea un animal con reglas de negocio:
        - obligatorios: idTenedor, idEspecie, nombre
        - sexo: M/H/Desconocido (default Desconocido)
        - fechaNacimientoEst (opcional) y edadEstimadaMeses (opcional)
          * NO se permiten ambas al mismo tiempo
        - microchip: si viene, no puede repetirse en animales activos
        - viveDentroCasa: 1/0/NULL
        - conviveConOtros: lista controlada guardada como texto "Perros,Gatos"
        """
        id_tenedor = self._require_int(data.get("idTenedor"), "idTenedor")
        id_especie = self._require_int(data.get("idEspecie"), "idEspecie")

        # idRaza opcional
        id_raza_raw = data.get("idRaza")
        if id_raza_raw is not None and str(id_raza_raw).strip() != "":
            id_raza = self._require_int(id_raza_raw, "idRaza")
        else:
            id_raza = None

        nombre = self._require_text(data.get("nombre"), "nombre")

        sexo_raw = self._optional_text(data.get("sexo")) or "Desconocido"
        sexo = self._validate_sexo(sexo_raw)

        # Fecha y Edad (no ambas)
        fecha_nac = self._optional_date_yyyy_mm_dd(data.get("fechaNacimientoEst"), "fechaNacimientoEst")
        edad_meses = self._optional_int_range(data.get("edadEstimadaMeses"), "edadEstimadaMeses", 0, 300)

        if fecha_nac is not None and edad_meses is not None:
            raise ValueError("Ingresa solo 'fechaNacimientoEst' o 'edadEstimadaMeses', no ambas.")

        color = self._optional_text_maxlen(data.get("color"), "color", 60)
        estado_repr = self._optional_text_maxlen(data.get("estadoReproductivo"), "estadoReproductivo", 60)

        microchip = self._optional_text_maxlen(data.get("numeroMicrochip"), "numeroMicrochip", 60)
        if microchip is not None:
            existe = self.repo.get_by_microchip(microchip)
            if existe is not None:
                raise ValueError("Ya existe un animal activo con ese número de microchip.")

        vive_dentro = self._optional_int01(data.get("viveDentroCasa"), "viveDentroCasa")
        convive = self._validate_convive_checklist(data.get("conviveConOtros"))
        obs = self._optional_text_maxlen(data.get("observaciones"), "observaciones", 500)

        payload = {
            "idTenedor": id_tenedor,
            "idEspecie": id_especie,
            "idRaza": id_raza,
            "nombre": nombre,
            "sexo": sexo,
            "fechaNacimientoEst": fecha_nac,
            "edadEstimadaMeses": edad_meses,
            "color": color,
            "estadoReproductivo": estado_repr,
            "numeroMicrochip": microchip,
            "viveDentroCasa": vive_dentro,
            "conviveConOtros": convive,
            "observaciones": obs,
        }
                
        return self.repo.create(payload)

    def obtener_por_id(self, id_animal: int) -> Optional[Dict[str, Any]]:
        id_animal = self._require_int(id_animal, "idAnimal")
        return self.repo.get_by_id(id_animal)

    def listar_activos(self) -> List[Dict[str, Any]]:
        return self.repo.list_active()

    def listar_por_tenedor(self, id_tenedor: int) -> List[Dict[str, Any]]:
        id_tenedor = self._require_int(id_tenedor, "idTenedor")
        return self.repo.list_by_tenedor(id_tenedor)

    def desactivar_animal(self, id_animal: int) -> None:
        id_animal = self._require_int(id_animal, "idAnimal")
        self.repo.deactivate(id_animal)
 