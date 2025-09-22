import numpy as np
import math
from graphics import Graphics

class Sphere:
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), name="sphere", segments=20):
        self.name = name
        self.position = np.array(position, dtype=np.float32)
        self.rotation = np.array(rotation, dtype=np.float32)
        self.scale = np.array(scale, dtype=np.float32)
        self.segments = segments
        
        # Generar vértices e índices de la esfera
        self.vertices, self.indices = self._generate_sphere_geometry()

    def _generate_sphere_geometry(self):
        vertices = []
        indices = []
        
        # Generar vértices
        for i in range(self.segments + 1):
            lat = math.pi * (-0.5 + float(i) / self.segments)
            sin_lat = math.sin(lat)
            cos_lat = math.cos(lat)
            
            for j in range(self.segments + 1):
                lon = 2 * math.pi * float(j) / self.segments
                sin_lon = math.sin(lon)
                cos_lon = math.cos(lon)
                
                # Posición del vértice
                x = cos_lat * cos_lon
                y = sin_lat
                z = cos_lat * sin_lon
                
                # Color basado en la posición (normalizado a [0,1])
                r = (x + 1) * 0.5
                g = (y + 1) * 0.5
                b = (z + 1) * 0.5
                
                vertices.extend([x, y, z, r, g, b])
        
        # Generar índices
        for i in range(self.segments):
            for j in range(self.segments):
                first = i * (self.segments + 1) + j
                second = first + self.segments + 1
                
                # Primer triángulo
                indices.extend([first, second, first + 1])
                # Segundo triángulo
                indices.extend([second, second + 1, first + 1])
        
        return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

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