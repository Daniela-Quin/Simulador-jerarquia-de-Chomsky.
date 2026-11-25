import tkinter as tk
from tkinter import ttk

from Nivel_0 import Nivel0
from Nivel_1 import Nivel1
from Nivel_2 import Nivel2
from Nivel_3 import Nivel3


COLORES = {
    "verde": "#15803d",
    "rojo": "#b91c1c",
    "azul": "#6b4fa0",
}

FONDO = "#f4f1f9"
MORADO = "#8f7fb5"
MORADO_HOVER = "#7d6ca3"
MORADO_CLARO = "#ddd5ec"
TEXTO = "#3b3350"

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Simulador de la Jerarquía de Chomsky")
        self.geometry("1160x600")
        self.minsize(1200, 600)

        self.configure(background=FONDO)

        estilo = ttk.Style(self)
        estilo.theme_use("clam")

        # Fondo y texto generales.
        estilo.configure("TFrame", background=FONDO)
        estilo.configure("TLabel", background=FONDO, foreground=TEXTO)

        # Botones.
        estilo.configure(
            "TButton",
            background=MORADO,
            foreground="white",
            padding=8,
            font=("Arial", 10, "bold"),
            borderwidth=0,
            bordercolor=MORADO,
            lightcolor=MORADO,
            darkcolor=MORADO,
            focuscolor=MORADO,
        )
        estilo.map(
            "TButton",
            background=[("active", MORADO_HOVER), ("pressed", MORADO_HOVER)],
        )

        # Pestañas.
        estilo.configure("TNotebook", background=FONDO, borderwidth=0)
        estilo.configure(
            "TNotebook.Tab",
            background=MORADO_CLARO,
            foreground=TEXTO,
            padding=(20, 8),
            font=("Arial", 11, "bold"),
            borderwidth=0,
        )
        estilo.map(
            "TNotebook.Tab",
            background=[("selected", MORADO)],
            foreground=[("selected", "white")],
        )

        # Cuadro de "Ejemplos".
        estilo.configure(
            "TLabelframe",
            background=FONDO,
            bordercolor=MORADO_CLARO,
        )
        estilo.configure(
            "TLabelframe.Label",
            background=FONDO,
            foreground=MORADO_HOVER,
            font=("Arial", 10, "bold"),
        )

        # Cuadro de texto.
        estilo.configure(
            "TEntry",
            fieldbackground="white",
            bordercolor=MORADO_CLARO,
            padding=5,
        )

        ttk.Label(
            self,
            text="Simulador de la Jerarquía de Chomsky",
            font=("Arial", 20, "bold"),
            foreground=MORADO_HOVER,
        ).pack(pady=(14, 8))

        pestanas = ttk.Notebook(self)
        pestanas.pack(
            fill="both",
            expand=True,
            padx=16,
            pady=(0, 16),
        )

        pestanas.add(Nivel3(pestanas, COLORES), text="Nivel 3")
        pestanas.add(Nivel2(pestanas, COLORES), text="Nivel 2")
        pestanas.add(Nivel1(pestanas, COLORES), text="Nivel 1")
        pestanas.add(Nivel0(pestanas, COLORES), text="Nivel 0")


if __name__ == "__main__":
    Aplicacion().mainloop()