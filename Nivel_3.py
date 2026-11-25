import tkinter as tk
from tkinter import ttk


TRANSICIONES = {
    ("q0", "0"): "q1",
    ("q0", "1"): "q0",
    ("q1", "0"): "q1",
    ("q1", "1"): "q2",
    ("q2", "0"): "q1",
    ("q2", "1"): "q0",
}

COLOR_NORMAL = "white"
COLOR_ACTIVO = "#fde68a"    # amarillo suave: estado actual
COLOR_ACEPTA = "#86efac"    # verde claro: cadena aceptada
COLOR_RECHAZA = "#fca5a5"   # rojo claro: cadena rechazada

class Nivel3(ttk.Frame):
    def __init__(self, padre, colores):
        super().__init__(padre, padding=18)

        self.colores = colores
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.cadena = tk.StringVar(self, value="")
        self.indice = tk.IntVar(self, value=0)
        self.estado = tk.StringVar(self, value="q0")
        self.finalizada = tk.BooleanVar(self, value=False)

        self.cadena_visual = tk.StringVar(self, value="")
        self.estado_visual = tk.StringVar(
            self,
            value="Estado inicial: q0",
        )
        self.detalle = tk.StringVar(
            self,
            value="Pulse Iniciar simulación",
        )

        self.crear_interfaz()

    def crear_interfaz(self):
        ttk.Label(
            self,
            text="Nivel 3 — Autómata finito",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, pady=6)

        ttk.Label(
            self,
            text="Lenguaje: cadenas binarias cuyo último par de símbolos es 01",
        ).grid(row=1, column=0)

        self.entrada = ttk.Entry(self, width=35)
        self.entrada.grid(row=2, column=0, pady=(16, 4))
        self.entrada.insert(0, "1101")

        ttk.Label(
            self,
            textvariable=self.cadena_visual,
            font=("Courier", 17),
        ).grid(row=3, column=0, pady=10)

        ttk.Label(
            self,
            textvariable=self.estado_visual,
            font=("Arial", 13, "bold"),
        ).grid(row=4, column=0)

        ttk.Label(
            self,
            textvariable=self.detalle,
            wraplength=700,
        ).grid(row=5, column=0, pady=5)

        self.resultado = ttk.Label(
            self,
            text="",
            font=("Arial", 13, "bold"),
        )
        self.resultado.grid(row=6, column=0, pady=7)

        controles = ttk.Frame(self)
        controles.grid(row=7, column=0, pady=8)

        ttk.Button(
            controles,
            text="Iniciar",
            command=self.iniciar,
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            controles,
            text="Siguiente paso",
            command=self.siguiente,
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            controles,
            text="Reiniciar",
            command=self.reiniciar,
        ).grid(row=0, column=2, padx=5)

        ejemplos = ttk.LabelFrame(self, text="Ejemplos", padding=8)
        ejemplos.grid(row=8, column=0, pady=8)

        lista_ejemplos = ("01", "1101", "111", "10")

        for columna, ejemplo in enumerate(lista_ejemplos):
            acepta = ejemplo.endswith("01")
            texto = ejemplo + (" — acepta" if acepta else " — rechaza")

            ttk.Button(
                ejemplos,
                text=texto,
                command=lambda valor=ejemplo: self.usar_ejemplo(valor),
            ).grid(row=0, column=columna, padx=4)

        self.crear_automata()
        self.crear_info()

    def crear_info(self):
        """Leyenda de colores y definición formal del AFD."""
        marco = ttk.Frame(self)
        marco.grid(row=9, column=1, padx=(0, 20), pady=(0, 6))

        leyenda = ttk.Frame(marco)
        leyenda.pack(pady=(0, 6))

        for color, texto in (
            (COLOR_ACTIVO, "Estado actual"),
            (COLOR_ACEPTA, "Aceptada"),
            (COLOR_RECHAZA, "Rechazada"),
        ):
            tk.Label(
                leyenda,
                bg=color,
                width=2,
                relief="solid",
                borderwidth=1,
            ).pack(side="left", padx=(8, 3))
            ttk.Label(leyenda, text=texto).pack(side="left")

        ttk.Label(
            marco,
            text=(
                "M = (Q, Σ, δ, q0, F)\n"
                "Q = {q0, q1, q2}    Σ = {0, 1}\n"
                "q0 = estado inicial    F = {q2}"
            ),
            font=("Courier", 10),
            justify="left",
        ).pack()

    def crear_automata(self):
        """Dibuja el autómata en la pestaña y guarda los círculos
        para poder cambiarles el color después."""
        self.lienzo = tk.Canvas(
            self,
            width=500,
            height=320,
            background="white",
            highlightthickness=1,
            highlightbackground="#ddd5ec",
        )
        self.lienzo.grid(row=0, column=1, rowspan=9, padx=(0, 20))
        lienzo = self.lienzo

        posiciones = {
            "q0": (100, 150),
            "q1": (300, 220),
            "q2": (300, 80),
        }

        # Flecha de inicio hacia q0.
        lienzo.create_line(25, 150, 68, 150, arrow=tk.LAST, width=2)

        # q0 -> q1 con 0.
        lienzo.create_line(
            120, 165, 185, 210, 270, 218,
            smooth=True, arrow=tk.LAST, width=2,
        )
        lienzo.create_text(190, 185, text="0", font=("Arial", 12))

        # q1 -> q2 con 1.
        lienzo.create_line(
            280, 193, 250, 150, 280, 107,
            smooth=True, arrow=tk.LAST, width=2,
        )
        lienzo.create_text(248, 150, text="1", font=("Arial", 12))

        # q2 -> q1 con 0.
        lienzo.create_line(
            320, 107, 350, 150, 320, 193,
            smooth=True, arrow=tk.LAST, width=2,
        )
        lienzo.create_text(355, 150, text="0", font=("Arial", 12))

        # q2 -> q0 con 1.
        lienzo.create_line(
            275, 60, 170, 25, 75, 120,
            smooth=True, arrow=tk.LAST, width=2,
        )
        lienzo.create_text(175, 40, text="1", font=("Arial", 12))

        # Bucle de q0 con 1.
        lienzo.create_line(
            80, 125, 65, 90, 110, 85, 120, 125,
            smooth=True, arrow=tk.LAST, width=2,
        )
        lienzo.create_text(92, 78, text="1", font=("Arial", 12))

        # Bucle de q1 con 0.
        lienzo.create_line(
            280, 240, 265, 275, 315, 280, 320, 240,
            smooth=True, arrow=tk.LAST, width=2,
        )
        lienzo.create_text(293, 292, text="0", font=("Arial", 12))

        # Círculos de los estados (se guardan para recolorearlos).
        self.circulos = {}
        for nombre, (x, y) in posiciones.items():
            self.circulos[nombre] = lienzo.create_oval(
                x - 25, y - 25, x + 25, y + 25,
                fill=COLOR_NORMAL,
                width=2,
            )
            lienzo.create_text(x, y, text=nombre, font=("Arial", 12))

        # q2 es de aceptación: segundo círculo interior (sin relleno).
        x, y = posiciones["q2"]
        lienzo.create_oval(x - 20, y - 20, x + 20, y + 20, width=1)

    def resaltar_estado(self, estado=None, color=COLOR_ACTIVO):
        """Pinta de `color` el círculo de `estado` y deja los demás
        en blanco. Si estado es None, limpia todos."""
        for circulo in self.circulos.values():
            self.lienzo.itemconfig(circulo, fill=COLOR_NORMAL)

        if estado in self.circulos:
            self.lienzo.itemconfig(self.circulos[estado], fill=color)

    def usar_ejemplo(self, valor):
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, valor)
        self.iniciar()

    def actualizar_cadena(self):
        cadena = self.cadena.get()
        indice = self.indice.get()

        if not cadena:
            self.cadena_visual.set("Cadena sin iniciar")
            return

        elementos = []
        for posicion, simbolo in enumerate(cadena):
            elementos.append(
                f"[{simbolo}]" if posicion == indice else simbolo
            )

        self.cadena_visual.set(" ".join(elementos))

    def iniciar(self):
        cadena = self.entrada.get().strip()

        if not cadena:
            self.resultado.config(
                text="Ingrese una cadena",
                foreground=self.colores["rojo"],
            )
            self.resaltar_estado(None)
            return

        if any(simbolo not in ("0", "1") for simbolo in cadena):
            self.resultado.config(
                text="Solo se permiten los símbolos 0 y 1",
                foreground=self.colores["rojo"],
            )
            self.resaltar_estado(None)
            return

        self.cadena.set(cadena)
        self.indice.set(0)
        self.estado.set("q0")
        self.finalizada.set(False)

        self.estado_visual.set("Estado actual: q0")
        self.detalle.set("No se ha leído ningún símbolo")
        self.resultado.config(
            text="Simulación iniciada",
            foreground=self.colores["azul"],
        )

        self.actualizar_cadena()
        self.resaltar_estado("q0")

    def siguiente(self):
        if not self.cadena.get():
            self.resultado.config(
                text="Primero pulse Iniciar",
                foreground=self.colores["rojo"],
            )
            return

        if self.finalizada.get():
            self.resultado.config(
                text="La simulación terminó. Pulse Reiniciar",
                foreground=self.colores["rojo"],
            )
            return

        cadena = self.cadena.get()
        indice = self.indice.get()

        if indice >= len(cadena):
            aceptada = self.estado.get() == "q2"

            self.resultado.config(
                text=f'CADENA "{cadena}" '
                + ("ACEPTADA" if aceptada else "RECHAZADA"),
                foreground=(
                    self.colores["verde"]
                    if aceptada
                    else self.colores["rojo"]
                ),
            )
            self.detalle.set("No quedan símbolos por leer")
            self.finalizada.set(True)
            self.cadena_visual.set(" ".join(cadena))
            self.resaltar_estado(
                self.estado.get(),
                COLOR_ACEPTA if aceptada else COLOR_RECHAZA,
            )
            return
        simbolo = cadena[indice]
        estado_anterior = self.estado.get()
        estado_nuevo = TRANSICIONES[(estado_anterior, simbolo)]

        self.estado.set(estado_nuevo)
        self.indice.set(indice + 1)
        self.estado_visual.set(f"Estado actual: {estado_nuevo}")
        self.resaltar_estado(estado_nuevo)
        self.detalle.set(
            f"Símbolo leído: {simbolo}\n"
            f"Transición: {estado_anterior} → {estado_nuevo}"
        )

        self.actualizar_cadena()

        if self.indice.get() == len(cadena):
            self.resultado.config(
                text="Pulse Siguiente una vez más para ver el resultado",
                foreground=self.colores["azul"],
            )
        else:
            self.resultado.config(text="")

    def reiniciar(self):
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, "1101")

        self.cadena.set("")
        self.indice.set(0)
        self.estado.set("q0")
        self.finalizada.set(False)

        self.cadena_visual.set("")
        self.estado_visual.set("Estado inicial: q0")
        self.detalle.set("Pulse Iniciar simulación")
        self.resultado.config(text="")
        self.resaltar_estado(None)