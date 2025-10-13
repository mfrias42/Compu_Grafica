import moderngl
import pyglet

class Window(pyglet.window.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable = True)
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)
        self.ctx.viewport = (0, 0, width, height)
        self.scene = None

    def set_scene(self, scene):
        self.scene = scene

    def on_draw(self): # se ejecuta por cada frame
        self.clear()
        self.ctx.clear(0.2, 0.3, 0.8, 1.0)  # Color de fondo azul claro
        if self.scene:
            self.scene.render()

    def on_resize(self, width, height):
        if self.scene:
            self.scene.on_resize(width, height)

    def run(self): # activar el loop de la ventana
        pyglet.app.run()