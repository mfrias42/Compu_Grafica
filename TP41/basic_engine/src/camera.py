import numpy as np
import math

class Camera:
    def __init__(self, position, target, up, fov, aspect_ratio, near, far):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
        
        self.view_matrix = self.calculate_view_matrix()
        self.projection_matrix = self.calculate_projection_matrix()
    
    def calculate_view_matrix(self):
        # Calcular la matriz de vista usando lookAt (convención OpenGL)
        forward = self.position - self.target  # Dirección desde target hacia position
        forward = forward / np.linalg.norm(forward)
        
        right = np.cross(self.up, forward)
        right = right / np.linalg.norm(right)
        
        up = np.cross(forward, right)
        
        # Matriz de vista en formato column-major para OpenGL
        view_matrix = np.array([
            [right[0], up[0], forward[0], 0],
            [right[1], up[1], forward[1], 0],
            [right[2], up[2], forward[2], 0],
            [-np.dot(right, self.position), -np.dot(up, self.position), -np.dot(forward, self.position), 1]
        ], dtype=np.float32)
        
        return view_matrix
    
    def calculate_projection_matrix(self):
        # Calcular la matriz de proyección perspectiva
        fov_rad = math.radians(self.fov)
        f = 1.0 / math.tan(fov_rad / 2.0)
        
        projection_matrix = np.array([
            [f / self.aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (self.far + self.near) / (self.near - self.far), (2 * self.far * self.near) / (self.near - self.far)],
            [0, 0, -1, 0]
        ], dtype=np.float32)
        
        return projection_matrix
    
    def get_view_matrix(self):
        return self.view_matrix
    
    def get_perspective_matrix(self):
        return self.projection_matrix
    
    def get_view_projection_matrix(self):
        return np.dot(self.projection_matrix, self.view_matrix)
    
    def update_aspect_ratio(self, width, height):
        self.aspect_ratio = width / height
        self.projection_matrix = self.calculate_projection_matrix()