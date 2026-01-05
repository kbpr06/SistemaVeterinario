# app/ui/theme.py
from dataclasses import dataclass
import ttkbootstrap as tb

VERDE_VETERINARIA = "#177E67"

@dataclass(frozen=True)
class UITheme:
    bootstyle_theme: str = "flatly"

    primary: str = VERDE_VETERINARIA
    secondary: str = "#2C3E50"
    bg: str = "#F5F7FA"
    card: str = "#FFFFFF"
    text: str = "#1F2937"
    muted: str = "#6B7280"

    font_family: str = "Segoe UI"
    font_size: int = 10


def setup_theme(theme: UITheme) -> tb.Style:
    """
    Crea el Style de ttkbootstrap, aplica el verde real al 'success'
    y define estilos base que usas en tu UI.
    """
    style = tb.Style(theme=theme.bootstyle_theme)

    # ✅ Esto hace que "success" use tu verde exacto en toda la app
    style.colors.success = theme.primary

    # Base fonts
    style.configure(".", font=(theme.font_family, theme.font_size))

    # Frames
    style.configure("App.TFrame", background=theme.bg)
    style.configure("Card.TFrame", background=theme.card)
    style.configure("Header.TFrame", background=theme.primary)

    # Labels
    style.configure(
        "Title.TLabel",
        font=(theme.font_family, 22, "bold"),
        foreground=theme.secondary,
        background=theme.bg
    )
    style.configure(
        "Subtitle.TLabel",
        font=(theme.font_family, 11),
        foreground=theme.muted,
        background=theme.bg
    )

    style.configure(
        "CardTitle.TLabel",
        font=(theme.font_family, 16, "bold"),
        foreground=theme.secondary,
        background=theme.card
    )
    style.configure(
        "CardSub.TLabel",
        font=(theme.font_family, 10),
        foreground=theme.muted,
        background=theme.card
    )

     # --- Dashboard / bienvenida
    style.configure(
        "DashTitle.TLabel",
        font=(theme.font_family, 18, "bold"),
        foreground=theme.secondary,
        background=theme.bg
    )

    style.configure(
        "DashWelcome.TLabel",
        font=(theme.font_family, 11),
        foreground=theme.muted,
        background=theme.bg)

    # Header verde fijo
    style.configure("Header.TFrame", background="#177E67")

# Texto dentro del header (blanco)
    style.configure("HeaderTitle.TLabel",
                font=(theme.font_family, 18, "bold"),
                foreground="#FFFFFF",
                background="#177E67")

    style.configure("HeaderSub.TLabel",
                font=(theme.font_family, 10),
                foreground="#EAF5F2",
                background="#177E67")

# Barra superior de card (verde)
    style.configure("ModuleTop.TFrame", background="#177E67")

# Card base (más elegante)
    style.configure("ModuleCard.TFrame",
                background=theme.card,
                relief="solid",
                borderwidth=1)

    style.configure("ModuleCardHover.TFrame",
                background="#F3FBF9",   # tinte suave
                relief="solid",
                borderwidth=1)

# Título/desc dentro de card (que se vea pro)
    style.configure("ModuleTitle.TLabel",
                font=(theme.font_family, 13, "bold"),
                foreground=theme.secondary,
                background=theme.card)

    style.configure("ModuleDesc.TLabel",
                font=(theme.font_family, 10),
                foreground=theme.muted,
                background=theme.card)


    return style
