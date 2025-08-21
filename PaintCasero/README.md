# Mini Paint Casero 🎨

Un pequeño editor gráfico que permite crear figuras geométricas básicas utilizando algoritmos de rasterización implementados desde cero.

## Características

### Funcionalidades Básicas
- **Líneas**: Algoritmo de Bresenham para líneas suaves
- **Rectángulos**: Dibujados usando 4 líneas
- **Círculos**: Algoritmo de punto medio para circunferencias perfectas
- **Triángulos**: Dibujados usando 3 líneas

### Funcionalidades Bonus ✨
- **Elipses**: Algoritmo de punto medio para elipses
- **Selector de colores**: Paleta de colores personalizable
- **Borrador**: Herramienta para borrar píxeles

## Instalación

1. Crear entorno virtual:
```bash
python -m venv .venv
```

2. Activar entorno virtual:
```bash
# En Windows:
.venv\Scripts\activate

# En macOS/Linux:
source .venv/bin/activate
```

3. Instalar dependencias:
```bash
pip install Pillow
```

## Uso

Ejecutar el programa:
```bash
python paint.py
```

### Instrucciones de uso:

#### Figuras Básicas:
1. **Línea**: 
   - Selecciona "Línea" en las herramientas
   - Haz click en dos puntos para dibujar una línea

2. **Rectángulo**:
   - Selecciona "Rectángulo" en las herramientas
   - Haz click en la esquina superior izquierda
   - Haz click en la esquina inferior derecha

3. **Círculo**:
   - Selecciona "Círculo" en las herramientas
   - Haz click en el centro del círculo
   - Haz click en un punto del borde para definir el radio

4. **Triángulo**:
   - Selecciona "Triángulo" en las herramientas
   - Haz click en los tres vértices del triángulo

#### Funcionalidades Bonus:
5. **Elipse**:
   - Selecciona "Elipse" en las herramientas
   - Haz click en el centro de la elipse
   - Haz click en un punto del borde para definir los radios

6. **Cambiar color**:
   - Haz click en "Color" para abrir el selector
   - Elige el color deseado

7. **Borrador**:
   - Selecciona "Borrador" en las herramientas
   - Haz click en los píxeles que quieres borrar

8. **Guardar**:
   - Haz click en "Guardar" para exportar tu dibujo

## Algoritmos Implementados

### Bresenham Line Algorithm
- Eficiente algoritmo para dibujar líneas usando solo aritmética de enteros
- Garantiza líneas suaves sin escalones

### Middle Point Circle Algorithm
- Algoritmo de punto medio para dibujar círculos perfectos
- Dibuja solo 1/8 del círculo y refleja en los 8 octantes

### Middle Point Ellipse Algorithm
- Algoritmo de punto medio para dibujar elipses
- Maneja dos regiones con diferentes pendientes

## Estructura del Proyecto

```
PaintCasero/
├── paint.py              # Programa principal con interfaz Tkinter
├── utils.py              # Funciones de utilidad
├── bresenhamLine.py      # Algoritmo de línea de Bresenham
├── middlePointCircle.py  # Algoritmo de punto medio para círculos
├── ellipse.py            # Algoritmo de punto medio para elipses
└── README.md             # Este archivo
```

## Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal
- **Tkinter**: Interfaz gráfica
- **Pillow (PIL)**: Procesamiento de imágenes
- **Algoritmos de rasterización**: Bresenham y Middle Point

## Funcionalidades Bonus Implementadas

### 🎨 Selector de Colores
- Botón "Color" que abre un selector de colores
- Permite elegir cualquier color RGB
- Color actual se aplica a todas las figuras

### 🔄 Elipse
- Nueva herramienta "Elipse"
- 2 clicks: centro + punto del borde
- Algoritmo de punto medio para elipses perfectas

### 🧽 Borrador
- Nueva herramienta "Borrador"
- Click único para borrar píxeles
- Pinta píxeles negros sobre el canvas

## Criterios de Evaluación

### ✅ Funcionalidad Básica
- Todas las figuras se dibujan correctamente
- Algoritmos de Bresenham y Middle Point implementados
- Interfaz Tkinter funcional y fácil de usar
- Guardado en PNG funcionando

### ✅ Funcionalidades Bonus
- Elipse implementada con algoritmo correcto
- Selector de colores personalizable
- Borrador funcional
- Código bien estructurado y comentado

## Autor

Desarrollado como trabajo práctico de Computación Gráfica.

## Licencia

Este proyecto es educativo y está disponible para uso académico.
