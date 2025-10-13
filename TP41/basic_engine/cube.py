import numpy as np
import math
from graphics import Graphics

class Cube:
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), name="cube"):
        self.name = name
        self.position = np.array(position, dtype=np.float32)
        self.rotation = np.array(rotation, dtype=np.float32)
        self.scale = np.array(scale, dtype=np.float32)

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
        # Matriz identidad
        model = np.eye(4, dtype=np.float32)
        
        # Aplicar escala
        scale_matrix = np.eye(4, dtype=np.float32)
        scale_matrix[0, 0] = self.scale[0]
        scale_matrix[1, 1] = self.scale[1]
        scale_matrix[2, 2] = self.scale[2]
        
        # Aplicar rotaciones
        rx = math.radians(self.rotation[0])
        ry = math.radians(self.rotation[1])
        rz = math.radians(self.rotation[2])
        
        # Rotación X
        rot_x = np.eye(4, dtype=np.float32)
        rot_x[1, 1] = math.cos(rx)
        rot_x[1, 2] = -math.sin(rx)
        rot_x[2, 1] = math.sin(rx)
        rot_x[2, 2] = math.cos(rx)
        
        # Rotación Y
        rot_y = np.eye(4, dtype=np.float32)
        rot_y[0, 0] = math.cos(ry)
        rot_y[0, 2] = math.sin(ry)
        rot_y[2, 0] = -math.sin(ry)
        rot_y[2, 2] = math.cos(ry)
        
        # Rotación Z
        rot_z = np.eye(4, dtype=np.float32)
        rot_z[0, 0] = math.cos(rz)
        rot_z[0, 1] = -math.sin(rz)
        rot_z[1, 0] = math.sin(rz)
        rot_z[1, 1] = math.cos(rz)
        
        # Aplicar traslación
        trans_matrix = np.eye(4, dtype=np.float32)
        trans_matrix[0, 3] = self.position[0]
        trans_matrix[1, 3] = self.position[1]
        trans_matrix[2, 3] = self.position[2]
        
        # Combinar transformaciones: T * R * S
        model = np.dot(trans_matrix, np.dot(np.dot(rot_z, np.dot(rot_y, rot_x)), scale_matrix))
        return model
    
    def create_graphics_object(self, ctx, shader_program):
        return Graphics(ctx, shader_program, self.vertices, self.indices)