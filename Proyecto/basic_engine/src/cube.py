from hit import HitBox
import numpy as np
import glm
from graphics import Graphics

class Cube:
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), name="cube"):
        self.name = name
        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)
        self.scale = glm.vec3(*scale)
        self.__collision = HitBox(position, scale)

        # Array para crear el VBO: Vertex Buffer Object: almacena los vértices y colores de un cubo
        self.vertices = np.array([ 
            # posiciones        # colores 
            -1, -1, -1,  1, 0, 0, 
            1, -1, -1,  0, 1, 0, 
            1,  1, -1,  0, 0, 1, 
            -1,  1, -1,  1, 1, 0, 
            -1, -1,  1,  1, 0, 1, 
            1, -1,  1,  0, 1, 1, 
            1,  1,  1,  1, 1, 1, 
            -1,  1,  1,  0, 0, 0 
        ], dtype='f4') 


        # Array para crear el IBO: Index Buffer Object: define las caras del cubo
        self.indices = np.array([ 
            0, 1, 2, 2, 3, 0,  # atrás 
            4, 5, 6, 6, 7, 4,  # frente 
            0, 4, 7, 7, 3, 0,  # izquierda 
            1, 5, 6, 6, 2, 1,  # derecha 
            3, 2, 6, 6, 7, 3,  # arriba 
            0, 1, 5, 5, 4, 0   # abajo 
        ], dtype='i4') 


    def get_model_matrix(self):
        model = glm.mat4(1)
        model = glm.translate(model, self.position)
        model = glm.rotate(model, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        model = glm.rotate(model, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        model = glm.rotate(model, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        model = glm.scale(model, self.scale)
        return model
    
    def check_hit(self, origin, direction):
        # Actualizar la posición y escala del hitbox
        self.__collision = HitBox(self.position, self.scale)
        return self.__collision.check_hit(origin, direction)
    
    def create_graphics_object(self, ctx, shader_program):
        return Graphics(ctx, shader_program, self.vertices, self.indices)