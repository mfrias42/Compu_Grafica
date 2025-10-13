from graphics import Graphics

class Scene:
    def __init__(self, ctx, camera):
        self.ctx = ctx
        self.camera = camera
        self.objects = []
        self.graphics_objects = []
        self.view_matrix = self.camera.get_view_matrix()
        self.projection_matrix = self.camera.get_projection_matrix()

    def add_object(self, obj, shader_program):
        self.objects.append(obj)
        graphics_obj = obj.create_graphics_object(self.ctx, shader_program)
        self.graphics_objects.append(graphics_obj)

    def render(self):
        for i, graphics_obj in enumerate(self.graphics_objects):
            obj = self.objects[i]
            
            model_matrix = obj.get_model_matrix()
            mvp_array = model_matrix * self.view_matrix * self.projection_matrix
            # Configurar uniforme en el shader
            graphics_obj.set_uniform('Mvp', mvp_array)
            graphics_obj.render()

    def on_mouse_click(self, u, v):
        print(f"Click detectado en coordenadas u={u:.3f}, v={v:.3f}")
        ray = self.camera.raycast(u, v)
        print(f"Rayo generado - Origen: {ray.origin}, Dirección: {ray.direction}")
        
        for obj in self.objects:
            print(f"Verificando colisión con objeto: {obj.name}")
            print(f"  Posición del objeto: {obj.position}")
            print(f"  Escala del objeto: {obj.scale}")
            if obj.check_hit(ray.origin, ray.direction):
                print(f"¡Golpeaste al objeto {obj.name}!")
            else:
                print(f"No hay colisión con {obj.name}")

    def on_resize(self, width, height):
        self.ctx.viewport = (0, 0, width, height)