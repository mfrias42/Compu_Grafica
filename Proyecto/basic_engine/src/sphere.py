import math
import numpy as np
from graphics import Graphics
from src.hit import HitBox
import glm

class Sphere:
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), name="sphere", segments=20):
        self.name = name
        self.position = glm.vec3(position[0], position[1], position[2])
        self.rotation = glm.vec3(rotation[0], rotation[1], rotation[2])
        self.scale = glm.vec3(scale[0], scale[1], scale[2])
        self.segments = segments
        
        # Crear hitbox para detección de colisiones
        self.__collision = HitBox(self.position, self.scale)
        
        # Generar vértices e índices de la esfera
        self.vertices, self.indices = self._generate_sphere_geometry()

    def _generate_sphere_geometry(self):
        vertices = []
        indices = []
        
        # Generar vértices usando glm
        for i in range(self.segments + 1):
            lat = glm.pi() * (-0.5 + float(i) / self.segments)
            sin_lat = glm.sin(lat)
            cos_lat = glm.cos(lat)
            
            for j in range(self.segments + 1):
                lon = 2 * glm.pi() * float(j) / self.segments
                sin_lon = glm.sin(lon)
                cos_lon = glm.cos(lon)
                
                # Posición del vértice usando glm
                position = glm.vec3(cos_lat * cos_lon, sin_lat, cos_lat * sin_lon)
                
                # Color basado en la posición (normalizado a [0,1])
                color = glm.vec3(
                    (position.x + 1) * 0.5,
                    (position.y + 1) * 0.5,
                    (position.z + 1) * 0.5
                )
                
                vertices.extend([position.x, position.y, position.z, color.r, color.g, color.b])
        
        # Generar índices
        for i in range(self.segments):
            for j in range(self.segments):
                first = i * (self.segments + 1) + j
                second = first + self.segments + 1
                
                # Primer triángulo
                indices.extend([first, second, first + 1])
                # Segundo triángulo
                indices.extend([second, second + 1, first + 1])
        
        # Convertir a numpy arrays para compatibilidad con OpenGL
        return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)

    def get_model_matrix(self):
        # Crear matriz de transformación usando glm
        translation = glm.translate(glm.mat4(1.0), self.position)
        rotation_x = glm.rotate(glm.mat4(1.0), glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        rotation_y = glm.rotate(glm.mat4(1.0), glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        rotation_z = glm.rotate(glm.mat4(1.0), glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        scaling = glm.scale(glm.mat4(1.0), self.scale)
        
        # Combinar transformaciones: T * R * S
        rotation = rotation_z * rotation_y * rotation_x
        model = translation * rotation * scaling
        
        # Convertir a numpy array para compatibilidad con OpenGL
        return glm.array(model, dtype=glm.float32)
    
    def check_hit(self, ray_origin, ray_direction):
        # Actualizar la posición y escala del hitbox
        self.__collision = HitBox(self.position, self.scale)
        return self.__collision.check_hit(ray_origin, ray_direction)
    
    def create_graphics_object(self, ctx, shader_program):
        return Graphics(ctx, shader_program, self.vertices, self.indices)