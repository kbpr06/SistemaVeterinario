# app/ui/app_window.py
import ttkbootstrap as ttk

from app.ui.theme import UITheme, setup_theme
from app.ui.login_view import LoginView
from app.ui.dashboard_view import DashboardView

from app.data.db_connection import DBConnection
from app.data.usuario_repository import UsuarioRepository
from app.services.usuario_service import UsuarioService


class AppWindow(ttk.Window):
    def __init__(self):
        self.theme_cfg = UITheme()
        super().__init__(themename=self.theme_cfg.bootstyle_theme)

        # ✅ aplica tema (y deja el verde real en "success")
        setup_theme(self.theme_cfg)

        self.title("Sistema Veterinario - UMBA")
        self.geometry("1000x650")
        self.minsize(900, 600)

        # --- Servicios backend (reutilizamos tu backend real)
        self.db = DBConnection("db/veterinaria.db")
        self.usuario_repo = UsuarioRepository(self.db)
        self.usuario_service = UsuarioService(self.usuario_repo)

        self.current_user = None  # guardaremos aquí el usuario logueado

        # --- Contenedor principal
        self.container = ttk.Frame(self, padding=20, style="App.TFrame")
        self.container.pack(fill="both", expand=True)

        # --- Registro de pantallas (Frames)
        self.frames = {}
        self._register_frames()

        self.show_frame("login")

    def _register_frames(self):
        self.frames["login"] = LoginView(self.container, app=self)
        self.frames["dashboard"] = DashboardView(self.container, app=self)

        for f in self.frames.values():
            f.grid(row=0, column=0, sticky="nsew")

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

    def show_frame(self, name: str):
        frame = self.frames.get(name)
        if frame:
            frame.tkraise()

    def login_success(self, user_dict: dict):
        self.current_user = user_dict
        self.frames["dashboard"].refresh()
        self.show_frame("dashboard")

    def logout(self):
        self.current_user = None
        self.show_frame("login")
