# app/ui/components/forms.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class LabeledEntry(ttk.Frame):
    def __init__(self, master, label: str, show: str = None, width: int = 38, **kwargs):
        super().__init__(master, **kwargs)

        self.lbl = ttk.Label(self, text=label, bootstyle="secondary")
        self.lbl.pack(anchor="w", pady=(0, 4))

        self.var = ttk.StringVar()
        self.entry = ttk.Entry(self, textvariable=self.var, width=width, show=show, bootstyle="default")
        self.entry.pack(fill="x")

    def get(self) -> str:
        return self.var.get()

    def set(self, value: str):
        self.var.set(value)

    def focus(self):
        self.entry.focus_set()
