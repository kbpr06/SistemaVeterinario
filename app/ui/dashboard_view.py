# app/ui/dashboard_view.py
import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

try:
    from PIL import Image, ImageTk
    PIL_OK = True
except Exception:
    PIL_OK = False


VERDE_VETERINARIA = "#177E67"


class DashboardView(ttk.Frame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.configure(style="App.TFrame")

        self._img_refs = {}

        # ========= HEADER (igual al login) =========
        header = ttk.Frame(self, padding=(20, 12), style="Header.TFrame")
        header.pack(fill="x")

        header_inner = ttk.Frame(header, style="Header.TFrame")
        header_inner.pack(fill="x")

        header_inner.columnconfigure(0, weight=1)
        header_inner.columnconfigure(1, weight=2)
        header_inner.columnconfigure(2, weight=1)

        # Logo veterinaria izquierda (opcional)
        self.logo_vet = self._load_logo("logo_veterinaria.png", (80, 80))
        if self.logo_vet:
            ttk.Label(header_inner, image=self.logo_vet, background=VERDE_VETERINARIA)\
                .grid(row=0, column=0, sticky="w")
        else:
            ttk.Label(header_inner, text="", background=VERDE_VETERINARIA).grid(row=0, column=0, sticky="w")

        # Título centrado
        title_box = ttk.Frame(header_inner, style="Header.TFrame")
        title_box.grid(row=0, column=1)

        ttk.Label(title_box, text="Hare Hapa’o Manu", style="HeaderTitle.TLabel").pack()
        ttk.Label(title_box, text="Veterinaria Municipal", style="HeaderSub.TLabel").pack()

            # ========= TOP (bienvenida + logout) =========
        top = ttk.Frame(self, style="App.TFrame")
        top.pack(fill="x", pady=(12, 10), padx=20)

        left = ttk.Frame(top, style="App.TFrame")
        left.pack(side="left", fill="x", expand=True)

        self.lbl_title = ttk.Label(left, text="Inicio", style="DashTitle.TLabel")
        self.lbl_title.pack(anchor="w")

        self.lbl_welcome = ttk.Label(left, text="", style="DashWelcome.TLabel")
        self.lbl_welcome.pack(anchor="w", pady=(2, 0))

        btn_logout = ttk.Button(top, text="Cerrar sesión", bootstyle="secondary", command=self.app.logout)
        btn_logout.pack(side="right")

        # ========= GRID =========
        grid = ttk.Frame(self, style="App.TFrame")
        grid.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        for c in range(3):
            grid.columnconfigure(c, weight=1, uniform="cols")
        for r in range(2):
            grid.rowconfigure(r, weight=1, uniform="rows")

        self.modules = [
            ("tenedores", "Tenedores", "Gestión de responsables", "mod_tenedores.png"),
            ("animales", "Animales", "Registro y ficha del paciente", "mod_animales.png"),
            ("atencion", "Atención Clínica", "Registrar atenciones y tratamientos", "mod_atencion.png"),
            ("reportes", "Reportes", "Informes por fechas y filtros", "mod_reportes.png"),
            ("catalogos", "Catálogos", "Especies, motivos, vacunas, etc.", "mod_catalogos.png"),
            ("admin", "Administración", "Usuarios, roles y respaldos", "mod_admin.png"),
        ]

        positions = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]
        for (key, title, desc, icon), (r, c) in zip(self.modules, positions):
            self._make_module_card(grid, key, title, desc, icon, r, c)

    # ================= UI =================
    def _make_module_card(self, parent, key, title, desc, icon_filename, r, c):
        card = ttk.Frame(parent, style="ModuleCard.TFrame")
        card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

        # banda superior verde (le da identidad al tiro)
        top_bar = ttk.Frame(card, height=8, style="ModuleTop.TFrame")
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        body = ttk.Frame(card, padding=18, style="ModuleCard.TFrame")
        body.pack(fill="both", expand=True)

        body.columnconfigure(0, weight=0)
        body.columnconfigure(1, weight=1)

        icon_label = ttk.Label(body, style="ModuleDesc.TLabel")
        icon_label.grid(row=0, column=0, rowspan=2, sticky="nw", padx=(0, 12))

        icon = self._load_icon(icon_filename, size=(46, 46))
        if icon:
            icon_label.configure(image=icon)
            self._img_refs[f"{key}_icon"] = icon
        else:
            icon_label.configure(text="■")

        lbl_title = ttk.Label(body, text=title, style="ModuleTitle.TLabel")
        lbl_title.grid(row=0, column=1, sticky="nw")

        lbl_desc = ttk.Label(body, text=desc, style="ModuleDesc.TLabel", wraplength=280, justify="left")
        lbl_desc.grid(row=1, column=1, sticky="nw", pady=(6, 0))

        # click en toda la card
        self._bind_click_recursive(card, lambda e: self.open_module(key, title))
        self._bind_hover(card, body)

    def _bind_click_recursive(self, widget, callback):
        widget.bind("<Button-1>", callback)
        for child in widget.winfo_children():
            self._bind_click_recursive(child, callback)

    def _bind_hover(self, card, body):
        def on_enter(_):
            card.configure(style="ModuleCardHover.TFrame")
            body.configure(style="ModuleCardHover.TFrame")

        def on_leave(_):
            card.configure(style="ModuleCard.TFrame")
            body.configure(style="ModuleCard.TFrame")

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        for child in card.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

    def _load_logo(self, filename, size):
        if not PIL_OK:
            return None
        path = os.path.join("app", "ui", "assets", filename)
        if not os.path.exists(path):
            return None
        try:
            img = Image.open(path)
            img = img.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def _load_icon(self, filename, size=(48, 48)):
        return self._load_logo(filename, size)

    # ================= Actions =================
    def open_module(self, key, title):
        Messagebox.show_info(f"Módulo '{title}' (key={key})\n\nEn construcción ✅", "Navegación")

    def refresh(self):
        if self.app.current_user:
            username = self.app.current_user.get("nombreUsuario", "")
            rol = self.app.current_user.get("rol", "")
            self.lbl_welcome.config(text=f"Bienvenido/a, {username}  ·  Rol: {rol}")
        else:
            self.lbl_welcome.config(text="")
