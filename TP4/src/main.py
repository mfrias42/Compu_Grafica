from window import Window
from texture import Texture
from material import Material
from shader_program import ShaderProgram
from cube import Cube
from quad import Quad
from camera import Camera
from scene import Scene
import numpy as np
from scene import Scene, RayScene


# Ventana
window = Window(800, 600, "Basic Graphic Engine") #una ventana de 800x600
# Shader
shader_program = ShaderProgram(window.ctx, '../shaders/basic.vert', '../shaders/basic.frag') #carga los shaders very y frag
shader_program_skybox = ShaderProgram(window.ctx, '../shaders/sprite.vert', '../shaders/sprite.frag')

skybox_texture = Texture(width = window.width, height = window.height, channels_amount = 3, color = (0, 0, 0)) 

material = Material(shader_program)
material_sprite = Material(shader_program_skybox, textures_data = [skybox_texture])


# Objetos

cube1 = Cube((-2, -0.5, 0), (0, 0, 0), (1, 1, 1), name="Cube1")
cube2 = Cube((0, 0, 0),    (0, 0, 0), (1, 1, 1), name="Cube2") 
cube3 = Cube((2, 0.5, 0),    (0, 0, 0), (1, 1, 1), name="Cube3")
quad = Quad((0, 0, 0), (0, 0, 0), (6, 5, 1), name="Sprite", hittable = False)

# Cámara
camera = Camera((0, 0, 6), (0, 0, 0), (0, 1, 0), 45, window.width / window.height, 0.1, 100.0) 

#creo dos cubos  en posiciones diferentes
# Escena
scene = RayScene(window.ctx, camera, window.width, window.height)

scene.add_object(quad, material_sprite)
scene.add_object(cube1, shader_program)
scene.add_object(cube2, shader_program) 
scene.add_object(cube3, shader_program)
window.set_scene(scene)


window.run()
