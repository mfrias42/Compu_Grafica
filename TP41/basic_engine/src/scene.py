from graphics import Graphics
import numpy as np

class Scene:
    def __init__(self, ctx, camera):
        self.ctx = ctx
        self.camera = camera
        self.objects = []
        self.graphics_objects = []

    def add_object(self, obj, shader_program):
        self.objects.append(obj)
        graphics_obj = obj.create_graphics_object(self.ctx, shader_program)
        self.graphics_objects.append(graphics_obj)

    def render(self):
        for i, graphics_obj in enumerate(self.graphics_objects):
            obj = self.objects[i]
            
            # Obtener matrices de la cámara y del objeto
            model_matrix = obj.get_model_matrix()
            view_matrix = self.camera.get_view_matrix()
            projection_matrix = self.camera.get_perspective_matrix()
            
            # Multiplicar matrices: MVP = Projection * View * Model
            mv_matrix = np.dot(view_matrix, model_matrix)
            mvp_matrix = np.dot(projection_matrix, mv_matrix)
            
            # Transponer para OpenGL (column-major)
            mvp_array = mvp_matrix.T.astype(np.float32)
            
            # Configurar uniforme en el shader
            graphics_obj.set_uniform('Mvp', mvp_array)
            graphics_obj.render()

    def on_resize(self, width, height):
        self.ctx.viewport = (0, 0, width, height)
        self.camera.update_aspect_ratio(width, height)