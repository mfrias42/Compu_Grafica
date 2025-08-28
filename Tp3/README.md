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
