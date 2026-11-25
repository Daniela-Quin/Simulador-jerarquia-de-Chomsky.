import tkinter as tk
from tkinter import ttk

ANCHO_CINTA = 720

COLOR_CABEZAL = "#fde68a"   # amarillo suave: celda bajo el cabezal
COLOR_MARCADA = "#ddd5ec"   # lavanda claro: símbolo ya marcado (X, Y, Z)
COLOR_DELIM = "#8f7fb5"     # malva: delimitadores ⊢ y ⊣
COLOR_ACEPTA = "#86efac"    # verde claro: cadena aceptada
COLOR_RECHAZA = "#fca5a5"   # rojo claro: cadena rechazada

class Nivel1(ttk.Frame):
    def __init__(self, padre, colores):
        super().__init__(padre, padding=8)

        self.colores = colores
        self.columnconfigure(0, weight=1)

        self.cinta_original = tk.StringVar(self, value="")
        self.cinta_visual = tk.StringVar(self, value="")
        self.cabezal = tk.IntVar(self, value=0)
        self.estado = tk.StringVar(self, value="q0")
        self.finalizada = tk.BooleanVar(self, value=False)
        self.detalle = tk.StringVar(
            self,
            value="Pulse Iniciar simulación",
        )

        self.marcas = []
        self.fase = tk.StringVar(self, value="buscar_a")

        self.crear_interfaz()

    def crear_interfaz(self):
        ttk.Label(
            self,
            text="Nivel 1 — Autómata linealmente acotado",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, pady=6)

        ttk.Label(
            self,
            text="Lenguaje: aⁿbⁿcⁿ, con n mayor o igual que 1",
        ).grid(row=1, column=0)

        self.entrada = ttk.Entry(self, width=35)
        self.entrada.grid(row=2, column=0, pady=(16, 4))
        self.entrada.insert(0, "aabbcc")

        self.lienzo = tk.Canvas(
            self,
            width=ANCHO_CINTA,
            height=110,
            background="white",
            highlightthickness=1,
            highlightbackground="#ddd5ec",
        )
        self.lienzo.grid(row=3, column=0, pady=4)

        estado_frame = ttk.Frame(self)
        estado_frame.grid(row=4, column=0, pady=4)

        ttk.Label(
            estado_frame,
            text="Estado actual: ",
            font=("Arial", 13, "bold"),
        ).pack(side="left")

        ttk.Label(
            estado_frame,
            textvariable=self.estado,
            font=("Arial", 13, "bold"),
        ).pack(side="left")

        ttk.Label(
            self,
            textvariable=self.detalle,
            wraplength=700,
        ).grid(row=5, column=0, pady=2)

        self.resultado = ttk.Label(
            self,
            text="",
            font=("Arial", 13, "bold"),
        )
        self.resultado.grid(row=6, column=0, pady=2)

        controles = ttk.Frame(self)
        controles.grid(row=7, column=0, pady=4)

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
        ejemplos.grid(row=8, column=0, pady=4)

        lista_ejemplos = (
            "abc",
            "aabbcc",
            "aaabbbccc",
            "aabbbccc",
        )

        for columna, ejemplo in enumerate(lista_ejemplos):
            acepta = ejemplo in (
                "abc",
                "aabbcc",
                "aaabbbccc",
            )
            texto = (
                ejemplo + (" — acepta" if acepta else " — rechaza")
            )

            ttk.Button(
                ejemplos,
                text=texto,
                command=lambda valor=ejemplo: self.usar_ejemplo(valor),
            ).grid(row=0, column=columna, padx=4)

        self.actualizar_cinta()
        self.crear_info()

    def crear_info(self):
        """Leyenda de colores de la cinta."""
        leyenda = ttk.Frame(self)
        leyenda.grid(row=9, column=0, pady=(0, 6))

        for color, texto in (
            (COLOR_CABEZAL, "Cabezal"),
            (COLOR_MARCADA, "Marcado (X, Y, Z)"),
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

    def usar_ejemplo(self, valor):
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, valor)
        self.iniciar()

    def actualizar_cinta(self):
        """Dibuja la cinta acotada: ⊢ celdas ⊣, con el cabezal.

        Se redibuja completa en cada paso a partir de self.marcas
        (contenido de la cinta) y self.cabezal (posición actual).
        """
        lienzo = self.lienzo
        lienzo.delete("all")

        simbolos = list(self.marcas)
        total = len(simbolos) + 2    # + los dos delimitadores
        lado = min(48, (ANCHO_CINTA - 40) // total)
        x0 = (ANCHO_CINTA - lado * total) // 2
        y1, y2 = 15, 15 + lado
        fuente = ("Arial", max(10, lado // 3), "bold")
        posicion = self.cabezal.get()

        # Color de la celda del cabezal según el resultado.
        color_cabezal = COLOR_CABEZAL
        if self.finalizada.get():
            color_cabezal = (
                COLOR_ACEPTA
                if self.estado.get() == "qA"
                else COLOR_RECHAZA
            )

        for i in range(total):
            x1 = x0 + i * lado
            x2 = x1 + lado

            if i == 0 or i == total - 1:
                # Delimitadores de frontera.
                relleno = COLOR_DELIM
                texto = "⊢" if i == 0 else "⊣"
                color_texto = "white"
            else:
                simbolo = simbolos[i - 1]
                relleno = (
                    COLOR_MARCADA
                    if simbolo in ("X", "Y", "Z")
                    else "white"
                )
                if i - 1 == posicion:
                    relleno = color_cabezal
                texto = simbolo
                color_texto = "#3b3350"

            lienzo.create_rectangle(
                x1, y1, x2, y2,
                fill=relleno,
                outline="#3b3350",
                width=2,
            )
            lienzo.create_text(
                (x1 + x2) // 2, (y1 + y2) // 2,
                text=texto, font=fuente, fill=color_texto,
            )

        if not simbolos:
            lienzo.create_text(
                ANCHO_CINTA // 2, y2 + 25,
                text="Cinta vacía: pulse Iniciar",
                font=("Arial", 11, "italic"), fill="#8f7fb5",
            )
            return

        # Cabezal: triángulo bajo la celda actual y estado escrito.
        if 0 <= posicion < len(simbolos):
            cx = x0 + (posicion + 1) * lado + lado // 2
            lienzo.create_polygon(
                cx, y2 + 6, cx - 8, y2 + 20, cx + 8, y2 + 20,
                fill="#3b3350",
            )
            lienzo.create_text(
                cx, y2 + 34,
                text=self.estado.get(),
                font=("Arial", 11, "bold"), fill="#3b3350",
            )

    def iniciar(self):
        cadena = self.entrada.get().strip()

        if not cadena:
            self.resultado.config(
                text="Ingrese una cadena",
                foreground=self.colores["rojo"],
            )
            return

        if any(simbolo not in ("a", "b", "c") for simbolo in cadena):
            self.resultado.config(
                text="Solo se permiten los símbolos a, b y c",
                foreground=self.colores["rojo"],
            )
            return

        self.cinta_original.set(cadena)
        self.cabezal.set(0)
        self.estado.set("q0")
        self.fase.set("buscar_a")

        self.marcas.clear()
        self.marcas.extend(list(cadena))
        self.finalizada.set(False)

        self.actualizar_cinta()

        self.detalle.set(
            "Estado q0\n"
            "Fase: buscar una a al comienzo\n"
            "El cabezal está en la posición 0"
        )
        self.resultado.config(
            text="Simulación iniciada",
            foreground=self.colores["azul"],
        )

    def siguiente(self):
        if not self.cinta_original.get():
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

        posicion = self.cabezal.get()
        fase = self.fase.get()
        longitud = len(self.marcas)

        if not 0 <= posicion < longitud:
            self.resultado.config(
                text="Error: el cabezal salió de los límites de la cinta",
                foreground=self.colores["rojo"],
            )
            self.finalizada.set(True)
            return

        simbolo = self.marcas[posicion]

        def rechazar(mensaje):
            cadena = self.cinta_original.get()

            self.resultado.config(
                text=f'CADENA "{cadena}" RECHAZADA',
                foreground=self.colores["rojo"],
            )
            self.detalle.set(mensaje)
            self.finalizada.set(True)
            self.actualizar_cinta()

        def avanzar():
            if posicion + 1 >= longitud:
                return False

            self.cabezal.set(posicion + 1)
            return True

        # Busca una a sin marcar.
        if fase == "buscar_a":
            if simbolo == "a":
                self.marcas[posicion] = "X"
                self.fase.set("buscar_b")
                self.estado.set("q1")

                if not avanzar():
                    rechazar(
                        "No se encontró una b para emparejar con esta a."
                    )
                    return

                self.detalle.set(
                    "Se marcó una a como X; "
                    "el cabezal busca una b."
                )

            elif simbolo == "X":
                if avanzar():
                    self.detalle.set(
                        "Se recorrió una a ya marcada hacia la derecha."
                    )
                else:
                    self.fase.set("volver_verificar")
                    self.estado.set("q4")
                    self.detalle.set(
                        "Se marcaron todas las a; "
                        "el cabezal vuelve al inicio."
                    )

            else:
                self.fase.set("volver_verificar")
                self.estado.set("q4")

                if posicion > 0:
                    self.cabezal.set(posicion - 1)
                    self.detalle.set(
                        "No quedan a sin marcar; el cabezal vuelve "
                        "al inicio para verificar la cinta."
                    )
                else:
                    self.fase.set("verificar")
                    self.detalle.set(
                        "Se inicia la verificación de los símbolos "
                        "marcados."
                    )

        # Busca una b sin marcar.
        elif fase == "buscar_b":
            if simbolo == "b":
                self.marcas[posicion] = "Y"
                self.fase.set("buscar_c")
                self.estado.set("q2")

                if not avanzar():
                    rechazar(
                        "No se encontró una c para emparejar con esta b."
                    )
                    return

                self.detalle.set(
                    "Se marcó una b como Y; "
                    "el cabezal busca una c."
                )

            elif simbolo in ("a", "X", "Y"):
                if not avanzar():
                    rechazar("No se encontró una b sin marcar.")
                    return

                self.detalle.set(
                    "El cabezal avanza buscando una b sin marcar."
                )

            else:
                rechazar(
                    "Se encontró una c antes de la b correspondiente."
                )
                return

        # Busca una c sin marcar.
        elif fase == "buscar_c":
            if simbolo == "c":
                self.marcas[posicion] = "Z"
                self.fase.set("volver")
                self.estado.set("q3")

                if posicion > 0:
                    self.cabezal.set(posicion - 1)

                self.detalle.set(
                    "Se marcó una c como Z; "
                    "el cabezal vuelve a la izquierda."
                )

            elif simbolo in ("b", "Y", "Z"):
                if not avanzar():
                    rechazar("No se encontró una c sin marcar.")
                    return

                self.detalle.set(
                    "El cabezal avanza buscando una c sin marcar."
                )

            else:
                rechazar("No se encontró una c correspondiente.")
                return

        # Regresa al comienzo para otra ronda.
        elif fase == "volver":
            if posicion > 0:
                self.cabezal.set(posicion - 1)
                self.estado.set("q4")
                self.detalle.set(
                    "El cabezal se mueve una celda a la izquierda."
                )
            else:
                self.fase.set("buscar_a")
                self.estado.set("q0")
                self.detalle.set(
                    "El cabezal llegó al inicio; "
                    "comienza otra ronda."
                )

        # Regresa al inicio antes de verificar.
        elif fase == "volver_verificar":
            if posicion > 0:
                self.cabezal.set(posicion - 1)
                self.estado.set("q4")
                self.detalle.set(
                    "El cabezal vuelve a la izquierda "
                    "para verificar la cinta."
                )
            else:
                self.fase.set("verificar")
                self.estado.set("q4")
                self.detalle.set(
                    "El cabezal llegó al inicio; "
                    "comienza la verificación."
                )

        # Verifica que todos los símbolos estén marcados.
        elif fase == "verificar":
            if simbolo not in ("X", "Y", "Z"):
                rechazar("Quedaron símbolos sin emparejar.")
                return

            if posicion == longitud - 1:
                self.estado.set("qA")
                self.detalle.set(
                    "Todos los símbolos quedaron emparejados."
                )
                cadena = self.cinta_original.get()

                self.resultado.config(
                    text=f'CADENA "{cadena}" ACEPTADA',
                    foreground=self.colores["verde"],
                )
                self.finalizada.set(True)
            else:
                self.cabezal.set(posicion + 1)
                self.estado.set("q4")
                self.detalle.set(
                    "Símbolo verificado; "
                    "el cabezal avanza a la derecha."
                )

        self.actualizar_cinta()

        if not self.finalizada.get():
            self.resultado.config(text="")

    def reiniciar(self):
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, "aabbcc")

        self.cinta_original.set("")
        self.cinta_visual.set("")
        self.marcas.clear()
        self.cabezal.set(0)
        self.estado.set("q0")
        self.fase.set("buscar_a")
        self.finalizada.set(False)

        self.detalle.set("Pulse Iniciar simulación")
        self.resultado.config(text="")
        self.actualizar_cinta()