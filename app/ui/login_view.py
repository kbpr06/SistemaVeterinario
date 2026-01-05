# app/ui/login_view.py
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk

from app.ui.components.forms import LabeledEntry


class LoginView(ttk.Frame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, **kwargs)
        self.app = app

        # Fondo general de la vista
        self.configure(style="App.TFrame")

        # ================= HEADER (franja verde sólida) =================
        header = ttk.Frame(self, padding=(20, 12), style="Header.TFrame")
        header.pack(fill="x")

        header_inner = ttk.Frame(header, padding=(20, 15), style="Header.TFrame")
        header_inner.pack(fill="x")

        header_inner.columnconfigure(0, weight=1)
        header_inner.columnconfigure(1, weight=2)
        header_inner.columnconfigure(2, weight=1)

        # --- Logo veterinaria (izquierda)
        self.logo_vet = self._load_logo("app/ui/assets/logo_veterinaria.png", (140, 140))
        ttk.Label(header_inner, image=self.logo_vet, bootstyle="inverse-success").grid(row=0, column=0, sticky="w")

        # --- Título centrado
        title_box = ttk.Frame(header_inner, style="Header.TFrame")
        title_box.grid(row=0, column=1)

        ttk.Label(
            title_box,
            text="Hare Hapa’o Manu",
            font=("Segoe UI", 25, "bold"),
            bootstyle="inverse-success"
        ).pack()

        ttk.Label(
            title_box,
            text="Veterinaria Municipal",
            font=("Segoe UI", 15),
            bootstyle="inverse-success"
        ).pack()

        # --- Logo medio ambiente (derecha)
        self.logo_muni = self._load_logo("app/ui/assets/logo_medioambiente.png", (140, 140))
        ttk.Label(header_inner, image=self.logo_muni, bootstyle="inverse-success").grid(row=0, column=2, sticky="e")

        # ================= CUERPO =================
        wrapper = ttk.Frame(self, style="App.TFrame")
        wrapper.pack(expand=True, pady=(20, 0))

        # ✅ Card (aquí estaba el error: era bootstyle, debe ser style)
        card = ttk.Frame(wrapper, padding=40, style="Card.TFrame")
        card.pack()

        card_title = ttk.Label(card, text="Inicio de sesión", style="CardTitle.TLabel")
        card_title.pack(pady=(0, 5))

        card_sub = ttk.Label(card, text="Ingresa tus credenciales para continuar", style="CardSub.TLabel")
        card_sub.pack(pady=(0, 20))

        self.in_user = LabeledEntry(card, "Usuario")
        self.in_user.pack(fill="x", pady=(0, 12))

        self.in_pass = LabeledEntry(card, "Contraseña", show="•")
        self.in_pass.pack(fill="x", pady=(0, 18))

        btns = ttk.Frame(card, style="Card.TFrame")
        btns.pack(fill="x")

        self.btn_login = ttk.Button(btns, text="Ingresar", bootstyle="success", command=self.on_login)
        self.btn_login.pack(side="left", fill="x", expand=True)

        self.in_user.focus()

    # ================= HELPERS =================
    def _load_logo(self, path: str, size: tuple[int, int]):
        img = Image.open(path)
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def on_login(self):
        usuario = self.in_user.get().strip()
        clave = self.in_pass.get().strip()

        if not usuario or not clave:
            Messagebox.show_warning("Debes ingresar usuario y contraseña.", "Faltan datos")
            return

        try:
            user = self.app.usuario_service.login(usuario, clave)
            self.app.login_success(user)
        except Exception as e:
            Messagebox.show_error(str(e), "No se pudo iniciar sesión")
