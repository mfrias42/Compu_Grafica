from raytracer import RayTracer
import math
from graphics import Graphics
import glm


class Scene:
    def __init__(self, ctx, camera):
        self.ctx = ctx
        self.objects = []
        self.graphics = {}
        self.camera = camera
        self.model = glm.mat4(1)
        self.view = camera.get_view_matrix()
        self.projection = camera.get_perspective_matrix()

    def add_object(self, model, material):
        self.objects.append(model)
        self.graphics[model.name] = Graphics(self.ctx, model, material)

class RayScene(Scene):
    
    def __init__(self, ctx, camera, width, height):
            super().__init__(ctx, camera)
            self.raytracer = RayTracer(camera, width, height)

    def start(self):
        print("start!")
    
    def render(self):
        self.time += 0.01
        for obj in self.objects:
            if(obj.name != "Sprite"):
                obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                obj.position.x += math.sin(self.time) * 0.01
                
            model = obj.get_model_matrix()
            mvp = self.projection * self.view * model
            self.graphics[obj.name].set_uniform("Mvp", mvp)


    def on_mouse_click(self, u, v):
        ray = self.camera.raycast(u, v)

        for obj in self.objects:
            if obj.check_hit(ray.origin, ray.direction):
                print(f"¡Golpeaste el objeto {obj.name}!")

    def on_resize(self, width, height):
        self.ctx.viewport = (0, 0, width, height)
        self.camera.projection = glm.perspective(glm.radians(45), width / height, 0.1, 100.0)

    def update(self, dt):
        for obj in self.objects:
             obj.rotation.y += 20 * dt  # Rotar 20 grados x segundo
