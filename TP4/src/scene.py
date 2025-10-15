import glm
import moderngl
import numpy as np
from graphics import Graphics, ComputeGraphics
from raytracer import RayTracer, RayTracerGPU
import math

class Scene:
    def __init__(self, ctx, camera):
        self.ctx = ctx
        self.objects = []
        self.time = 0.0
        self.graphics = {}
        self.camera = camera
        self.model = glm.mat4(1)
        self.view = camera.get_view_matrix()
        self.projection = camera.get_perspective_matrix()

    def add_object(self, model, material):
        self.objects.append(model)
        self.graphics[model.name] = Graphics(self.ctx, model, material)

    def render(self):
        self.time += 0.01
        for obj in self.objects:
            if(obj.animated):
                obj.rotation += glm.vec3(0.8,0.6,0.4)
                obj.position.x += math.sin(self.time)* 0.01

            model = obj.get_model_matrix()
            mvp = self.projection * self.view * model
            self.graphics[obj.name].render({"Mvp": mvp})


    def on_mouse_click(self, u, v):
        # Generar un rayo desde la cámara con la posición normalizada del mouse
        ray = self.camera.raycast(u, v)

        # Chequear colisiones contra todos los objetos de la escena
        for obj in self.objects:
            if obj.check_hit(ray.origin, ray.direction):
                print(f"¡Golpeaste al objeto {obj.name}!")

    def on_resize(self, width, height):
        # Actualizar aspecto de la cámara cuando cambia el tamaño de ventana
        self.camera.aspect = width / height

    def start(self):
        print("!start")


class RayScene(Scene):
    def __init__(self,ctx, camara, width, height):
        super().__init__(ctx, camara)
        self.raytracer = RayTracer(camara, width, height)

    def start(self):
        self.raytracer.render_frame(self.objects)
        if "Sprite" in self.graphics:
            self.graphics["Sprite"].update_texture("u_texture", self.raytracer.get_texture())

    def render(self):
        super().render()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.raytracer = RayTracer(self.camera, width, height)
        self.start()

class RaySceneGPU(Scene):
    def __init__(self, ctx, camera, width, height, output_model, output_material):
        self.ctx = ctx
        self.camera = camera
        self.width = width
        self.height = height
        self.raytracer = None

        self.output_graphics = Graphics(ctx, output_model, output_material)
        self.raytracer = RayTracerGPU(self.ctx, self.camera, self.width, self.height, self.output_graphics)

        super().__init__(self.ctx, self.camera)

    def add_object(self, model, material):
        self.objects.append(model)
        self.graphics[model.name] = ComputeGraphics(self.ctx, model, material)

    def start(self):
        print("start raytracing GPU!")
        self.primitives = []
        n = len(self.objects)
        self.models_f = np.zeros((n,16), dtype = 'f4')
        self.inv_f = np.zeros((n,16), dtype = 'f4')
        self.mats_f = np.zeros((n,4), dtype = 'f4')

        self._update_matrix()
        self._matrix_to_ssbo()
    
    def redner(self):
        self.time += 0.01
        for obj in self.objects:
            if obj.animated:
                obj.rotation += glm.vec3(0.8,0.6,0.4)
                obj.position.x += math.sin(self.time)* 0.01
            
            if(self.raytracer is not None):
                self._update_matrix()
                self._matrix_to_ssbo()
                self.raytracer.run()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.width, self.height = width, height
        self.camera.aspect = width / height

    def _update_matrix(self):
        self.primitives = []

        for i, (name, graphics) in enumerate(self.graphics.items()):
            graphics.create_primitive(self.primitives)
            graphics.create_transformation_matrix(self.models_f, i)
            graphics.create_inverse_transformation_matrix(self.inv_f, i)
            graphics.create_material_matrix(self.mats_f, i)

    def _matrix_to_ssbo(self):
        self.raytracer.matrix_to_ssbo(self.models_f, 0)
        self.raytracer.matrix_to_ssbo(self.inv_f, 1)
        self.raytracer.matrix_to_ssbo(self.mats_f, 2)
        self.raytracer.primitives_to_ssbo(self.primitives, 3)
