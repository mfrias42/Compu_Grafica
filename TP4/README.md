# Motor Gráfico Básico - TP4 Computación Gráfica

Este proyecto implementa un motor gráfico básico usando OpenGL con Python.

## Configuración del Entorno Virtual

### 1. Activar el entorno virtual
```bash
source venv/bin/activate
```

### 2. Verificar que las dependencias están instaladas
```bash
pip list
```

### 3. Ejecutar la aplicación
```bash
cd src
python main.py
```

### 4. Desactivar el entorno virtual (cuando termines)
```bash
deactivate
```

## Dependencias Instaladas

- **ModernGL**: Motor OpenGL moderno para Python
- **Pyglet**: Biblioteca para crear ventanas y manejar eventos
- **NumPy**: Operaciones matemáticas y arrays
- **PyGLM**: Matemáticas para gráficos 3D (matrices, vectores, etc.)

## Estructura del Proyecto

```
TP4/
├── src/
│   ├── main.py          # Punto de entrada principal
│   ├── window.py        # Gestión de ventana y eventos
│   ├── camera.py        # Sistema de cámara
│   ├── cube.py          # Objeto cubo 3D
│   ├── scene.py         # Gestión de escena
│   ├── graphics.py      # Renderizado gráfico
│   └── shader_program.py # Gestión de shaders
├── shaders/
│   ├── basic.vert       # Vertex shader
│   └── basic.frag       # Fragment shader
├── venv/                # Entorno virtual
└── requirements.txt     # Dependencias del proyecto
```

## Notas

- El entorno virtual ya está configurado y listo para usar
- Todas las dependencias están instaladas
- La aplicación debería ejecutarse sin problemas
- Si encuentras algún error, asegúrate de que el entorno virtual esté activado