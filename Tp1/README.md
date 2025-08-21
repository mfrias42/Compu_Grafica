# Mini Paint Casero 🎨

Un pequeño editor gráfico que permite crear figuras geométricas básicas utilizando algoritmos de rasterización implementados desde cero.

## Características

- **Líneas**: Algoritmo de Bresenham para líneas suaves
- **Rectángulos**: Dibujados usando 4 líneas
- **Círculos**: Algoritmo de punto medio para circunferencias perfectas
- **Triángulos**: Dibujados usando 3 líneas
- **Colores**: Selector de colores personalizable
- **Guardado**: Exporta dibujos como archivos PNG

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
pip install -r requirements.txt
```

## Uso

Ejecutar el programa:
```bash
python paint.py
```

### Instrucciones de uso:

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

5. **Cambiar color**:
   - Haz click en "Cambiar Color" para abrir el selector

6. **Guardar**:
   - Haz click en "Guardar PNG" para exportar tu dibujo

7. **Limpiar**:
   - Haz click en "Limpiar Canvas" para empezar de nuevo

## Algoritmos Implementados

### Bresenham Line Algorithm
- Eficiente algoritmo para dibujar líneas usando solo aritmética de enteros
- Garantiza líneas suaves sin escalones

### Middle Point Circle Algorithm
- Algoritmo de punto medio para dibujar círculos perfectos
- Dibuja solo 1/8 del círculo y refleja en los 8 octantes

## Estructura del Proyecto

```
Tp1/
├── paint.py          # Programa principal con interfaz Tkinter
├── utils.py          # Funciones de utilidad y algoritmos
├── line.py           # Implementación original de líneas
├── circle.py         # Implementación original de círculos
├── requirements.txt  # Dependencias
└── README.md         # Este archivo
```

## Archivos Generados

- `mi_dibujo.png`: Imagen guardada por el usuario
- `circle_smooth.png`: Ejemplo de círculo generado por circle.py
- `line.ppm`: Ejemplo de líneas generado por line.py

## Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal
- **Tkinter**: Interfaz gráfica
- **Pillow (PIL)**: Procesamiento de imágenes
- **Algoritmos de rasterización**: Bresenham y Middle Point

## Bonus Features (Opcionales)

Para agregar funcionalidades adicionales:

1. **Elipse**: Implementar algoritmo de elipse
2. **Borrador**: Herramienta para borrar píxeles
3. **Grosor de línea**: Permitir cambiar el grosor
4. **Relleno**: Rellenar figuras cerradas
5. **Deshacer/Rehacer**: Historial de acciones

## Autor

Desarrollado como trabajo práctico de Computación Gráfica.

## Licencia

Este proyecto es educativo y está disponible para uso académico.