import tkinter as tk
from tkinter import ttk

COLOR_CELDA = "#fde68a"    # amarillo suave: celda en la pila
COLOR_PUSH = "#86efac"     # verde claro: celda recién apilada
COLOR_POP = "#fca5a5"      # rojo claro: celda que se desapila

class Nivel2(ttk.Frame):
    def __init__(self, padre, colores):
        super().__init__(padre, padding=18)

        self.colores = colores
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self._temporizador = None

        self.cadena = tk.StringVar(self, value="")
        self.indice = tk.IntVar(self, value=0)
        self.pila = []
        self.espera_b = tk.BooleanVar(self, value=False)
        self.finalizada = tk.BooleanVar(self, value=False)

        self.cadena_visual = tk.StringVar(self, value="")
        self.pila_visual = tk.StringVar(self, value="Pila: vacía")
        self.detalle = tk.StringVar(
            self,
            value="Pulse Iniciar simulación",
        )

        self.crear_interfaz()

    def crear_interfaz(self):
        ttk.Label(
            self,
            text="Nivel 2 — Autómata con pila",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, pady=6)

        ttk.Label(
            self,
            text="Lenguaje: aⁿbⁿ, con n mayor o igual que 1",
        ).grid(row=1, column=0)

        self.entrada = ttk.Entry(self, width=35)
        self.entrada.grid(row=2, column=0, pady=(16, 4))
        self.entrada.insert(0, "aabb")

        ttk.Label(
            self,
            textvariable=self.cadena_visual,
            font=("Courier", 17),
        ).grid(row=3, column=0, pady=10)

        ttk.Label(
            self,
            textvariable=self.pila_visual,
            font=("Courier", 15),
        ).grid(row=4, column=0)

        ttk.Label(
            self,
            textvariable=self.detalle,
            wraplength=700,
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

        lista_ejemplos = ("ab", "aabb", "aaabbb", "abab")

        for columna, ejemplo in enumerate(lista_ejemplos):
            acepta = ejemplo in ("ab", "aabb", "aaabbb")
            texto = (
                ejemplo + (" — acepta" if acepta else " — rechaza")
            )

            ttk.Button(
                ejemplos,
                text=texto,
                command=lambda valor=ejemplo: self.usar_ejemplo(valor),
            ).grid(row=0, column=columna, padx=4)

        self.crear_pila()
        self.crear_info()

    def crear_pila(self):
        """Crea el lienzo donde se dibuja la pila."""
        self.lienzo = tk.Canvas(
            self,
            width=320,
            height=380,
            background="white",
            highlightthickness=1,
            highlightbackground="#ddd5ec",
        )
        self.lienzo.grid(row=0, column=1, rowspan=9, padx=(0, 20))
        self.dibujar_pila()

    def dibujar_pila(self, color_cima=False, fantasma=False):
        """Dibuja la pila como una columna de celdas (cima arriba).

        color_cima: pinta de verde la última celda apilada.
        fantasma: muestra en rojo la celda que se acaba de desapilar.
        """
        # Si había un redibujado pendiente, se cancela.
        if self._temporizador is not None:
            self.after_cancel(self._temporizador)
            self._temporizador = None

        lienzo = self.lienzo
        lienzo.delete("all")

        izq, der, base, tope = 100, 220, 340, 50
        centro = (izq + der) // 2
        alto = min(36, (base - tope) // (len(self.pila) + 1))

        # Contenedor abierto por arriba.
        lienzo.create_line(
            izq, tope, izq, base, der, base, der, tope,
            width=3,
        )
        lienzo.create_text(
            centro, 25, text="CIMA",
            font=("Arial", 11, "bold"), fill="#3b3350",
        )
        lienzo.create_text(
            centro, base + 22, text="FONDO",
            font=("Arial", 11, "bold"), fill="#3b3350",
        )

        # Celdas: la posición 0 es el fondo.
        for i, simbolo in enumerate(self.pila):
            y2 = base - i * alto
            y1 = y2 - alto
            es_cima = i == len(self.pila) - 1
            lienzo.create_rectangle(
                izq + 3, y1, der - 3, y2,
                fill=COLOR_PUSH if (color_cima and es_cima) else COLOR_CELDA,
                outline="#3b3350",
                width=2,
            )
            lienzo.create_text(
                centro, (y1 + y2) // 2, text=simbolo,
                font=("Arial", 13, "bold"), fill="#3b3350",
            )

        # Celda que acaba de salir de la pila.
        if fantasma:
            i = len(self.pila)
            y2 = base - i * alto
            y1 = y2 - alto
            lienzo.create_rectangle(
                izq + 3, y1, der - 3, y2,
                fill=COLOR_POP,
                outline="#3b3350",
                width=2,
                dash=(4, 3),
            )
            lienzo.create_text(
                centro, (y1 + y2) // 2, text="a",
                font=("Arial", 13, "bold"), fill="#3b3350",
            )

        if not self.pila and not fantasma:
            lienzo.create_text(
                centro, base - 20, text="(vacía)",
                font=("Arial", 11, "italic"), fill="#8f7fb5",
            )

    def crear_info(self):
        """Leyenda de colores de la pila."""
        leyenda = ttk.Frame(self)
        leyenda.grid(row=9, column=1, padx=(0, 20), pady=(0, 6))

        for color, texto in (
            (COLOR_PUSH, "Apilada"),
            (COLOR_POP, "Desapilada"),
            (COLOR_CELDA, "En la pila"),
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

    def actualizar(self):
        cadena = self.cadena.get()
        indice = self.indice.get()

        elementos = []
        for posicion, simbolo in enumerate(cadena):
            elemento = (
                f"[{simbolo}]"
                if posicion == indice
                else simbolo
            )
            elementos.append(elemento)

        if cadena:
            self.cadena_visual.set(" ".join(elementos))
        else:
            self.cadena_visual.set("Cadena sin iniciar")

        if self.pila:
            contenido = " ".join(self.pila)
            self.pila_visual.set(
                f"Pila: fondo → {contenido} → cima"
            )
        else:
            self.pila_visual.set("Pila: vacía")

    def iniciar(self):
        cadena = self.entrada.get().strip()

        if not cadena:
            self.resultado.config(
                text="Ingrese una cadena",
                foreground=self.colores["rojo"],
            )
            return

        if any(simbolo not in ("a", "b") for simbolo in cadena):
            self.resultado.config(
                text="Solo se permiten los símbolos a y b",
                foreground=self.colores["rojo"],
            )
            return

        self.cadena.set(cadena)
        self.indice.set(0)
        self.pila.clear()
        self.espera_b.set(False)
        self.finalizada.set(False)

        self.detalle.set("Estado inicial; pila vacía")
        self.resultado.config(
            text="Simulación iniciada",
            foreground=self.colores["azul"],
        )

        self.actualizar()
        self.dibujar_pila()

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
            aceptada = not self.pila and self.espera_b.get()

            self.resultado.config(
                text=f'CADENA "{cadena}" '
                + ("ACEPTADA" if aceptada else "RECHAZADA"),
                foreground=(
                    self.colores["verde"]
                    if aceptada
                    else self.colores["rojo"]
                ),
            )
            self.detalle.set("Procesamiento terminado")
            self.finalizada.set(True)
            self.cadena_visual.set(" ".join(cadena))
            self.actualizar()
            return

        simbolo = cadena[indice]

        if simbolo == "a":
            if self.espera_b.get():
                self.detalle.set(
                    "No puede aparecer a después de haber comenzado b"
                )
                self.resultado.config(
                    text="Cadena rechazada",
                    foreground=self.colores["rojo"],
                )
                self.finalizada.set(True)
                self.actualizar()
                return

            self.pila.append("a")
            self.dibujar_pila(color_cima=True)
            self.detalle.set("Se apiló una a")

        else:
            self.espera_b.set(True)

            if not self.pila:
                self.detalle.set(
                    "Se encontró b sin una a correspondiente"
                )
                self.resultado.config(
                    text="Cadena rechazada",
                    foreground=self.colores["rojo"],
                )
                self.finalizada.set(True)
                self.actualizar()
                return

            self.pila.pop()
            self.dibujar_pila(fantasma=True)
            self._temporizador = self.after(450, self.dibujar_pila)
            self.detalle.set("Se desapiló una a al leer b")

        self.indice.set(indice + 1)
        self.resultado.config(text="")
        self.actualizar()

        if self.indice.get() == len(cadena):
            self.resultado.config(
                text="Pulse Siguiente una vez más para ver el resultado",
                foreground=self.colores["azul"],
            )

    def reiniciar(self):
        self.entrada.delete(0, tk.END)
        self.entrada.insert(0, "aabb")

        self.cadena.set("")
        self.indice.set(0)
        self.pila.clear()
        self.espera_b.set(False)
        self.finalizada.set(False)

        self.cadena_visual.set("")
        self.pila_visual.set("Pila: vacía")
        self.detalle.set("Pulse Iniciar simulación")
        self.resultado.config(text="")
        self.dibujar_pila()