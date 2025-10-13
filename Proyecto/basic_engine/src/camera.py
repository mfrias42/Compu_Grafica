import numpy as np
import math
import glm
from ray import Ray

class Camera:
    def __init__(self, position, target, up, fov, aspect_ratio, near, far):
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
        
        self.view_matrix = glm.lookAt(self.position, self.target, self.up)
        self.projection_matrix =  glm.perspective(glm.radians(self.fov), self.aspect_ratio, self.near, self.far)
    
    def get_view_matrix(self):
        return self.view_matrix
    
    def get_projection_matrix(self):
        return self.projection_matrix
    
    def raycast(self, u, v):
        fov_adjustment = glm.tan(glm.radians(self.fov) / 2)
        
        ndc_x = (2 * u - 1) * self.aspect_ratio * fov_adjustment
        ndc_y = (2 * v - 1) * fov_adjustment
        
        ray_dir_camera = glm.vec3(ndc_x, ndc_y, -1.0)
        ray_dir_camera = glm.normalize(ray_dir_camera)
        
        view = self.get_view_matrix()
        inv_view = glm.inverse(view)
        ray_dir_world = glm.vec3(inv_view * glm.vec4(ray_dir_camera, 0.0))
        
        return Ray(self.position, ray_dir_world)