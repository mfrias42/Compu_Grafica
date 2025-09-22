# TP3 - Computación Gráfica

## Configuración del Entorno Virtual

### Activación del entorno virtual

```bash
# Activar el entorno virtual
source venv/bin/activate

# Verificar que está activado (deberías ver (venv) en el prompt)
```

### Instalación de dependencias

```bash
# Instalar dependencias desde requirements.txt
pip install -r requirements.txt

# O instalar paquetes individuales
pip install numpy matplotlib pygame
```

### Desactivación del entorno virtual

```bash
# Cuando termines de trabajar
deactivate
```

## Estructura del Proyecto

```
Tp3/
├── venv/           # Entorno virtual
├── requirements.txt # Dependencias del proyecto
├── README.md       # Este archivo
└── src/            # Código fuente (crear según necesites)
```

## Notas

- Siempre activa el entorno virtual antes de trabajar en el proyecto
- Agrega nuevas dependencias a `requirements.txt` cuando las instales
- El entorno virtual mantiene las dependencias aisladas del sistema

# Algoritmo de Recorte de Sutherland-Hodgman

Este proyecto implementa el algoritmo de recorte de Sutherland-Hodgman para recortar polígonos contra una ventana rectangular.

## Descripción del Algoritmo

El algoritmo de Sutherland-Hodgman es un método para recortar un polígono contra una ventana rectangular. Funciona de la siguiente manera:

1. **Definición de la ventana**: Se define una ventana rectangular con cuatro bordes.
2. **Recorte iterativo**: El polígono se recorta contra cada borde de la ventana de forma secuencial.
3. **Cálculo de intersecciones**: Cuando una línea del polígono cruza un borde, se calcula el punto de intersección.
4. **Construcción del resultado**: Se construye un nuevo polígono con los puntos que quedan dentro de la ventana.

## Características del Código

### Clase `SutherlandHodgmanClipper`
- **`__init__()`**: Inicializa el recortador con los límites de la ventana
- **`inside()`**: Determina si un punto está dentro de un borde específico
- **`intersection()`**: Calcula la intersección entre una línea y un borde
- **`clip_polygon()`**: Aplica el algoritmo de recorte a un polígono

### Clase `ClippingVisualizer`
- Interfaz gráfica interactiva usando Pyglet
- Visualización en tiempo real del proceso de recorte
- Generación de polígonos aleatorios para demostración

## Instalación

1. Asegúrate de tener Python 3.7+ instalado
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Visualización Gráfica (Recomendado)
```bash
python shape.py
```

### Demostración Simple (Sin interfaz gráfica)
```bash
python shape.py --demo
```

## Controles de la Interfaz Gráfica

- **ESC**: Salir de la aplicación
- **R**: Generar un nuevo polígono aleatorio

## Elementos Visuales

- **Rectángulo negro**: Ventana de recorte
- **Polígono azul**: Polígono original
- **Polígono rojo**: Polígono recortado

## Ejemplo de Uso Programático

```python
from shape import SutherlandHodgmanClipper

# Crear el recortador
clipper = SutherlandHodgmanClipper(0, 0, 10, 10)

# Definir un polígono
polygon = [(2, 2), (8, 2), (5, 8)]

# Aplicar el recorte
clipped_polygon = clipper.clip_polygon(polygon)
print(f"Polígono recortado: {clipped_polygon}")
```

## Casos de Prueba

El código incluye varios casos de prueba:
1. Polígono completamente dentro de la ventana
2. Polígono que se extiende fuera de la ventana
3. Polígono completamente fuera de la ventana
4. Polígono que toca los bordes de la ventana

## Algoritmo Detallado

### Paso 1: Definición de Bordes
Los bordes de la ventana se definen en sentido horario:
- Borde inferior: (left, bottom) → (right, bottom)
- Borde derecho: (right, bottom) → (right, top)
- Borde superior: (right, top) → (left, top)
- Borde izquierdo: (left, top) → (left, bottom)

### Paso 2: Procesamiento de Vértices
Para cada vértice del polígono:
1. Verificar si está dentro del borde actual
2. Si el vértice anterior estaba fuera y el actual está dentro: agregar intersección
3. Si el vértice actual está dentro: agregar el vértice
4. Si el vértice anterior estaba dentro y el actual está fuera: agregar intersección

### Paso 3: Cálculo de Intersecciones
Se usa la fórmula de intersección de líneas:
```
t = ((edge_x1 - x1) * edge_dy - (edge_y1 - y1) * edge_dx) / denom
intersection_x = x1 + t * dx
intersection_y = y1 + t * dy
```

## Ventajas del Algoritmo

- **Simplicidad**: Fácil de implementar y entender
- **Eficiencia**: Complejidad O(n*m) donde n es el número de vértices y m es el número de bordes
- **Robustez**: Maneja casos especiales como polígonos degenerados
- **Flexibilidad**: Se puede adaptar para diferentes tipos de ventanas de recorte

## Limitaciones

- Solo funciona con ventanas convexas (como rectángulos)
- Puede generar vértices adicionales en el polígono resultante
- No es óptimo para polígonos muy complejos con muchos vértices
