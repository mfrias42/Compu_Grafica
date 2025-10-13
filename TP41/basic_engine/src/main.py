from window import Window
from shader_program import ShaderProgram
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cube import Cube
from sphere import Sphere
from camera import Camera
from scene import Scene

# Ventana
window = Window(800, 600, "Basic Graphic Engine")
# Shader
shader_program = ShaderProgram(window.ctx, '../shaders/basic.vert', '../basic.frag')

# Cámara
camera = Camera((0, 0, 5), (0, 0, 0), (0, 1, 0), 45, window.width / window.height, 0.1, 100.0)

# Objetos - Cubo y esfera posicionados lado a lado
cube1 = Cube((-1.2, 0, -3), (45, 45, 0), (0.3, 0.3, 0.3), name="Cube1")
sphere1 = Sphere((1.2, 0, -3), (0, 0, 0), (0.4, 0.4, 0.4), name="Sphere1")

# Escena
scene = Scene(window.ctx, camera)
scene.add_object(cube1, shader_program)
scene.add_object(sphere1, shader_program)

# Carga de la escena y ejecución del loop principal
window.set_scene(scene)
window.run()