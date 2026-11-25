import tkinter as tk
from tkinter import ttk

ANCHO_CINTA = 720

COLOR_CABEZAL = "#fde68a"   # amarillo suave: celda bajo el cabezal
COLOR_ACEPTA = "#86efac"    # verde claro: la máquina terminó
COLOR_EXTRA = "#ddd5ec"     # lavanda claro: celdas vacías de reserva

class Nivel0(ttk.Frame):
    def __init__(self, padre, colores):
        super().__init__(padre, padding=8)

        self.colores = colores
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.cinta = tk.StringVar(self, value="⊔ ⊔ ⊔")
        self.estado = tk.StringVar(
            self,
            value="Estado inicial: q0",
        )
        self.cabezal = tk.IntVar(self, value=0)
        self.cadena = tk.StringVar(self, value="")
        self.lista_cinta = []
        self.finalizada = tk.BooleanVar(self, value=False)
        self.detalle = tk.StringVar(
            self,
            value="Pulse Iniciar simulación",
        )

        self.crear_interfaz()

    def crear_interfaz(self):
        ttk.Label(
            self,
            text="Nivel 0 — Máquina de Turing",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, pady=6)

        ttk.Label(
            self,
            text=(
                "Función: incrementa una cadena unaria. "
                "Ejemplo: 111 → 1111\n"
                "Alfabeto de cinta: {1, ⊔}. "
                "Estados principales: q0 y qA."
            ),
        ).grid(row=1, column=0)

        self.entrada = ttk.Entry(self, width=35)
        self.entrada.grid(row=2, column=0, pady=(16, 4))
        self.entrada.insert(0, "111")

        self.lienzo = tk.Canvas(
            self,
            width=ANCHO_CINTA,
            height=115,
            background="white",
            highlightthickness=1,
            highlightbackground="#ddd5ec",
        )
        self.lienzo.grid(row=3, column=0, pady=4)

        ttk.Label(
            self,
            textvariable=self.estado,
            font=("Arial", 13, "bold"),
        ).grid(row=4, column=0)

        ttk.Label(
            self,
            textvariable=self.detalle,
        ).grid(row=5, column=0, pady=8)

        self.resultado = ttk.Label(
            self,
            text="",
            font=("Arial", 13, "bold"),
        )
        self.resultado.grid(row=6, column=0, pady=6)

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

        for columna, ejemplo in enumerate(
            ("1", "11", "111", "1111")
        ):
            ttk.Button(
                ejemplos,
                text=f"{ejemplo} → {ejemplo}1",
                command=lambda valor=ejemplo: self.usar_ejemplo(valor),
            ).grid(row=0, column=columna, padx=4)

        self.actualizar_cinta()
        self.crear_info()

    def crear_info(self):
        """Definición formal de la máquina y leyenda de colores."""
        marco = ttk.LabelFrame(
            self, text="Definición de la máquina", padding=10,
        )
        marco.grid(row=0, column=1, rowspan=9, padx=(10, 10))

        ttk.Label(
            marco,
            text=(
                "Q = {q0, qA}\n"
                "Σ = {1}\n"
                "Γ = {1, ⊔}  (alfabeto de cinta)\n"
                "Estado inicial: q0\n"
                "F = {qA}\n\n"
                "Transiciones δ:\n"
                "δ(q0, 1) = (q0, 1, →)\n"
                "δ(q0, ⊔) = (qA, 1, —)\n\n"
                "→ mover a la derecha\n"
                "— no mover (se detiene)"
            ),
            font=("Courier", 10),
            justify="left",
        ).pack(anchor="w")

        leyenda = ttk.Frame(marco)
        leyenda.pack(anchor="w", pady=(10, 0))

        for color, texto in (
            (COLOR_CABEZAL, "Cabezal"),
            (COLOR_ACEPTA, "Terminó"),
            (COLOR_EXTRA, "Blanco virtual"),
        ):
            fila = ttk.Frame(leyenda)
            fila.pack(anchor="w", pady=1)
            tk.Label(
                fila,
                bg=color,
                width=2,
                relief="solid",
                borderwidth=1,
            ).pack(side="left", padx=(0, 4))
            ttk.Label(fila, text=texto).pack(side="left")

    def usar_ejemplo(self, valor):
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, valor)
        self.iniciar()

    def actualizar_cinta(self):
        """Dibuja la cinta extendible con el cabezal.

        Las celdas lavanda son blancos virtuales: la cinta de una
        Máquina de Turing no tiene fin en ninguna dirección, por eso
        se marcan los extremos con puntos suspensivos.
        """
        lienzo = self.lienzo
        lienzo.delete("all")

        extra = 2    # blancos virtuales a cada lado
        celdas = ["⊔"] * extra + list(self.lista_cinta) + ["⊔"] * extra
        total = len(celdas)
        lado = min(46, (ANCHO_CINTA - 80) // total)
        x0 = (ANCHO_CINTA - lado * total) // 2
        y1, y2 = 15, 15 + lado
        fuente = ("Arial", max(10, lado // 3), "bold")

        hay_cinta = bool(self.lista_cinta)
        posicion = self.cabezal.get() + extra
        color_cabezal = (
            COLOR_ACEPTA if self.finalizada.get() else COLOR_CABEZAL
        )

        for i, simbolo in enumerate(celdas):
            x1 = x0 + i * lado
            x2 = x1 + lado

            relleno = "white"
            if i < extra or i >= total - extra:
                relleno = COLOR_EXTRA
            if hay_cinta and i == posicion:
                relleno = color_cabezal

            lienzo.create_rectangle(
                x1, y1, x2, y2,
                fill=relleno,
                outline="#3b3350",
                width=2,
            )
            lienzo.create_text(
                (x1 + x2) // 2, (y1 + y2) // 2,
                text=simbolo, font=fuente, fill="#3b3350",
            )

        # Puntos suspensivos: la cinta continúa a ambos lados.
        centro_y = (y1 + y2) // 2
        lienzo.create_text(
            x0 - 22, centro_y, text="···",
            font=("Arial", 16, "bold"), fill="#8f7fb5",
        )
        lienzo.create_text(
            x0 + lado * total + 22, centro_y, text="···",
            font=("Arial", 16, "bold"), fill="#8f7fb5",
        )

        # Cabezal: triángulo bajo la celda actual y estado activo.
        if hay_cinta:
            cx = x0 + posicion * lado + lado // 2
            lienzo.create_polygon(
                cx, y2 + 6, cx - 8, y2 + 20, cx + 8, y2 + 20,
                fill="#3b3350",
            )
            lienzo.create_text(
                cx, y2 + 34,
                text=self.estado.get().split(":")[-1].strip(),
                font=("Arial", 11, "bold"), fill="#3b3350",
            )

    def iniciar(self):
        cadena = self.entrada.get().strip()

        self.cadena.set("")
        self.lista_cinta.clear()
        self.finalizada.set(False)

        if not cadena:
            self.actualizar_cinta()
            self.resultado.config(
                text="Ingrese una cadena formada por uno o más 1",
                foreground=self.colores["rojo"],
            )
            return

        if any(simbolo != "1" for simbolo in cadena):
            self.actualizar_cinta()
            self.estado.set("Entrada inválida")
            self.detalle.set(
                "La máquina unaria solo acepta el símbolo 1"
            )
            self.resultado.config(
                text=(
                    f'CADENA "{cadena}" RECHAZADA: '
                    "contiene símbolos distintos de 1"
                ),
                foreground=self.colores["rojo"],
            )
            return

        self.cadena.set(cadena)
        self.lista_cinta.extend(list(cadena))

        # Celda vacía donde se escribirá el nuevo 1.
        self.lista_cinta.append("⊔")

        self.cabezal.set(0)
        self.estado.set("Estado activo: q0")
        self.detalle.set(
            "Simulación iniciada; "
            "el cabezal comienza al principio"
        )
        self.resultado.config(
            text="Simulación iniciada",
            foreground=self.colores["azul"],
        )

        self.actualizar_cinta()

    def siguiente(self):
        if not self.cadena.get():
            self.resultado.config(
                text="Primero inicie una entrada válida formada solo por 1",
                foreground=self.colores["rojo"],
            )
            return

        if self.finalizada.get():
            self.resultado.config(
                text="La simulación terminó. Pulse Reiniciar",
                foreground=self.colores["rojo"],
            )
            return

        posicion = self.cabezal.get()
        posicion_celda_vacia = len(self.lista_cinta) - 1

        # Recorre hacia la derecha los símbolos 1.
        if posicion < posicion_celda_vacia:
            simbolo = self.lista_cinta[posicion]

            self.cabezal.set(posicion + 1)
            self.estado.set("Estado activo: q0")
            self.detalle.set(
                f"Se leyó {simbolo}; "
                "el cabezal avanza a la derecha"
            )
            self.resultado.config(text="")
            self.actualizar_cinta()
            return

        # Escribe el nuevo 1 en la celda vacía.
        self.lista_cinta[posicion] = "1"
        self.lista_cinta.append("⊔")

        self.estado.set("Estado activo: qA")
        self.detalle.set(
            "Se escribió 1 en la celda vacía; "
            "la máquina acepta"
        )

        cadena = self.cadena.get()
        self.resultado.config(
            text=f"FUNCIÓN EJECUTADA: {cadena} → {cadena}1",
            foreground=self.colores["verde"],
        )

        self.finalizada.set(True)
        self.actualizar_cinta()

    def reiniciar(self):
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, "111")

        self.lista_cinta.clear()
        self.cadena.set("")
        self.cabezal.set(0)
        self.finalizada.set(False)

        self.actualizar_cinta()
        self.estado.set("Estado inicial: q0")
        self.detalle.set("Pulse Iniciar simulación")
        self.resultado.config(text="")