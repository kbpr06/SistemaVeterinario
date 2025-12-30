from typing import Optional, Dict, Any
import bcrypt

from app.data.usuario_repository import UsuarioRepository


class UsuarioService:
    ROLES_VALIDOS = {"admin_sistema", "veterinario", "tecnico", "administrativo"}

    def __init__(self, repo: UsuarioRepository):
        self.repo = repo

    def _normalize_username(self, username: str) -> str:
        if username is None:
            raise ValueError("El nombre de usuario es obligatorio")

        username = str(username).strip().lower()
        if not username:
            raise ValueError("El nombre de usuario es obligatorio")

        # Evitar espacios internos
        if " " in username:
            raise ValueError("El nombre de usuario no debe contener espacios")

        return username

    def _validate_password(self, password: str) -> None:
        if password is None:
            raise ValueError("La contraseña es obligatoria")
        password = str(password)
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")

    def _hash_password(self, password: str) -> str:
        """
        Devuelve el hash bcrypt como string (UTF-8) para guardarlo en SQLite.
        """
        self._validate_password(password)
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def _check_password(self, password: str, hashed_str: str) -> bool:
        if not password or not hashed_str:
            return False
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed_str.encode("utf-8"))
        except Exception:
            return False

    def crear_usuario(self, data: Dict[str, Any]) -> int:
        """
        Crea usuario con hash bcrypt. nombreUsuario se guarda en minúscula.
        """
        username = self._normalize_username(data.get("nombreUsuario"))
        rol = data.get("rol")

        if rol not in self.ROLES_VALIDOS:
            raise ValueError("Rol inválido")

        password = data.get("password")
        hashed = self._hash_password(password)

        # Validar duplicado (activo)
        existente = self.repo.get_by_username(username)
        if existente:
            raise ValueError("Ya existe un usuario activo con ese nombre de usuario")

        payload = {
            "idPersonal": data.get("idPersonal"),  # puede ser None
            "nombreUsuario": username,
            "claveEncriptada": hashed,
            "rol": rol,
        }
        return self.repo.create(payload)

    def login(self, nombre_usuario: str, password: str) -> Dict[str, Any]:
        """
        Retorna datos del usuario si credenciales son válidas.
        """
        username = self._normalize_username(nombre_usuario)
        user = self.repo.get_by_username(username)
        if not user:
            raise ValueError("Usuario o contraseña incorrectos")

        if not self._check_password(password, user.get("claveEncriptada", "")):
            raise ValueError("Usuario o contraseña incorrectos")

        # Nunca devolvemos el hash hacia afuera
        user_safe = dict(user)
        user_safe.pop("claveEncriptada", None)
        return user_safe

    def crear_admin_sistema_si_no_existe(self, username: str, password: str) -> Optional[int]:
        """
        Crea un admin_sistema inicial solo si no existe uno activo.
        Retorna el idUsuario creado o None si ya existía.
        """
        if self.repo.exists_active_admin_sistema():
            return None

        data = {
            "idPersonal": None,
            "nombreUsuario": username,
            "password": password,
            "rol": "admin_sistema",
        }
        return self.crear_usuario(data)

    # --- Helpers de permisos (para UI después) ---
    def es_clinico(self, rol: str) -> bool:
        return rol in {"veterinario", "tecnico"}

    def es_admin_normal(self, rol: str) -> bool:
        # tu “admin” es el administrativo
        return rol == "administrativo"

    def es_admin_sistema(self, rol: str) -> bool:
        return rol == "admin_sistema"
