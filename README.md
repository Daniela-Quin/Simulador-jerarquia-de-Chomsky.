# Simulador-jerarquia-de-Chomsky.
Simulador interactivo de los niveles de la jerarquía de Chomsky.

Aplicación de escritorio con interfaz gráfica que simula, paso a paso, un modelo computacional de cada uno de los cuatro niveles de la Jerarquía de Chomsky.

| Nivel | Modelo                       | Lenguaje / función                    |
|-------|------------------------------|---------------------------------------|
| 3     | Autómata finito determinista | Cadenas binarias que terminan en `01` |
| 2     | Autómata con pila            | aⁿbⁿ, con n ≥ 1                       |
| 1     | Autómata linealmente acotado | aⁿbⁿcⁿ, con n ≥ 1                     |
| 0     | Máquina de Turing            | Incremento unario: 1ⁿ → 1ⁿ⁺¹          |

**Elaborado por:** Sharon Daniela Quintero Arias
**Politecnico Grancolombiano**

## Requisitos

- Python 3.8 o superior.
- `tkinter`, que viene incluido con Python en Windows y macOS. No hay que instalar ninguna dependencia con `pip`.
- En Linux (Debian/Ubuntu) puede que haga falta instalarlo:

  ```bash
  sudo apt install python3-tk
  ```

Para comprobar que tkinter funciona: `python -m tkinter` debe abrir una ventana de prueba.

## Instalación y ejecución

1. Clonar el repositorio (o descargarlo como ZIP desde el botón **Code** y descomprimirlo):

   ```bash
   git clone https://github.com/USUARIO/simulador-chomsky.git
   cd simulador-chomsky
   ```

2. Ejecutar la aplicación:

   ```bash
   python main_sim.py
   ```

   En Linux y macOS puede ser necesario usar `python3 main_sim.py`.

## Estructura del proyecto

```
simulador-chomsky/
├── docs/          # Simulador de la jerarquia de Chomsky (Doc de implementacion)
├── .gitignore
├── Nivel_0.py     # Máquina de Turing
├── Nivel_1.py     # Autómata linealmente acotado
├── Nivel_2.py     # Autómata con pila
├── Nivel_3.py     # Autómata finito
├── README.md
└── main_sim.py    # Ventana principal, estilo visual y pestañas
```

Los archivos deben conservar exactamente estos nombres, porque `main_sim.py` los importa.

## Cómo se usa

1. Elegir el nivel en las **pestañas** de la parte superior.
2. Escribir una cadena en el cuadro de texto, o pulsar uno de los botones de **Ejemplos** (que la carga y la inicia sola).
3. Pulsar **Iniciar** para preparar la simulación.
4. Pulsar **Siguiente paso** para ejecutar una transición a la vez y observar el modelo.
5. En los niveles 3, 2 y 1, cuando se termina de leer la cadena hay que pulsar **Siguiente paso** una vez más para ver el resultado (aceptada o rechazada).
6. **Reiniciar** devuelve el nivel a su estado inicial.

### Código de colores

| Color         | Significado                                                              |
|---------------|--------------------------------------------------------------------------|
| Amarillo      | Elemento activo: estado actual, celda bajo el cabezal o celda de la pila |
| Verde         | Cadena aceptada, símbolo apilado o ejecución terminada                   |
| Rojo          | Cadena rechazada o símbolo desapilado                                    |
| Lavanda claro | Símbolo ya marcado (nivel 1) o blanco virtual de la cinta (nivel 0)      |

Cada nivel incluye su propia guía de color en pantalla.

## Cadenas de prueba

Todas están disponibles como botones dentro de la interfaz.

### Nivel 3 — Autómata finito (termina en `01`)

| Cadena | Resultado |
|--------|-----------|
| `01`   | Acepta    |
| `1101` | Acepta    |
| `111`  | Rechaza   |
| `10`   | Rechaza   |

Se muestra el autómata dibujado y el estado actual resaltado en cada paso. Alfabeto: `{0, 1}`.

### Nivel 2 — Autómata con pila (aⁿbⁿ)

| Cadena   | Resultado |
|----------|-----------|
| `ab`     | Acepta    |
| `aabb`   | Acepta    |
| `aaabbb` | Acepta    |
| `abab`   | Rechaza   |

La pila se dibuja como una columna: las celdas apiladas aparecen en verde y las desapiladas en rojo. Alfabeto: `{a, b}`.

### Nivel 1 — Autómata linealmente acotado (aⁿbⁿcⁿ)

| Cadena      | Resultado |
|-------------|-----------|
| `abc`       | Acepta    |
| `aabbcc`    | Acepta    |
| `aaabbbccc` | Acepta    |
| `aabbbccc`  | Rechaza   |

La cinta se dibuja entre los delimitadores `⊢` y `⊣`. El cabezal se mueve en ambas direcciones y las celdas emparejadas se marcan como X, Y, Z. Alfabeto: `{a, b, c}`.

### Nivel 0 — Máquina de Turing (incremento unario)

| Cadena | Resultado |
|--------|-----------|
| `1`    | `11`      |
| `11`   | `111`     |
| `111`  | `1111`    |
| `1111` | `11111`   |

La cinta es extendible (`···` en ambos lados), el panel lateral muestra el alfabeto de la cinta Γ = {1, ⊔} y las transiciones, y debajo del cabezal se escribe el estado activo. Cualquier cadena con símbolos distintos de `1` se rechaza.

## Documentación

El documento de implementación, con los conceptos aplicados en cada nivel (definiciones formales, gramáticas, tablas de transiciones y explicación del código), está en la carpeta [`docs/`](docs/).

## Licencia

Proyecto académico/ MIT
