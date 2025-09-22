import pyglet
import numpy as np
from typing import List, Tuple

class SutherlandHodgmanClipper:
    """
    Implementación del algoritmo de recorte de Sutherland-Hodgman
    para recortar un polígono contra una ventana rectangular.
    """
    
    def __init__(self, window_left: float, window_bottom: float, 
                 window_right: float, window_top: float):
        """
        Inicializa el recortador con los límites de la ventana.
        
        Args:
            window_left: Coordenada x izquierda de la ventana
            window_bottom: Coordenada y inferior de la ventana
            window_right: Coordenada x derecha de la ventana
            window_top: Coordenada y superior de la ventana
        """
        self.window_left = window_left
        self.window_bottom = window_bottom
        self.window_right = window_right
        self.window_top = window_top
        
        # Definir los bordes de la ventana en sentido horario
        # Cada borde se define como (x1, y1, x2, y2) donde (x1, y1) es el punto de inicio
        # y (x2, y2) es el punto final del borde
        self.edges = [
            (window_left, window_bottom, window_right, window_bottom),  # Borde inferior
            (window_right, window_bottom, window_right, window_top),    # Borde derecho
            (window_right, window_top, window_left, window_top),        # Borde superior
            (window_left, window_top, window_left, window_bottom)       # Borde izquierdo
        ]
    
    def inside(self, point: Tuple[float, float], edge: Tuple[float, float, float, float]) -> bool:
        """
        Determina si un punto está dentro del borde especificado.
        
        Args:
            point: Punto (x, y) a evaluar
            edge: Borde (x1, y1, x2, y2) donde (x1, y1) es el punto de inicio
                  y (x2, y2) es el punto final del borde
        
        Returns:
            True si el punto está dentro del borde, False en caso contrario
        """
        x, y = point
        x1, y1, x2, y2 = edge
        
        # Para cada borde, definimos qué lado es "dentro":
        # - Borde inferior: "dentro" está arriba (y >= y1)
        # - Borde derecho: "dentro" está a la izquierda (x <= x1)
        # - Borde superior: "dentro" está abajo (y <= y1)
        # - Borde izquierdo: "dentro" está a la derecha (x >= x1)
        
        if abs(x2 - x1) < 1e-10:  # Borde vertical (izquierdo o derecho)
            if x1 == self.window_left:  # Borde izquierdo
                return x >= x1
            else:  # Borde derecho
                return x <= x1
        else:  # Borde horizontal (inferior o superior)
            if y1 == self.window_bottom:  # Borde inferior
                return y >= y1
            else:  # Borde superior
                return y <= y1
    
    def intersection(self, point1: Tuple[float, float], point2: Tuple[float, float], 
                    edge: Tuple[float, float, float, float]) -> Tuple[float, float]:
        """
        Calcula la intersección entre una línea y un borde de la ventana.
        
        Args:
            point1: Primer punto de la línea (x1, y1)
            point2: Segundo punto de la línea (x2, y2)
            edge: Borde de la ventana (x1, y1, x2, y2)
        
        Returns:
            Punto de intersección (x, y)
        """
        x1, y1 = point1
        x2, y2 = point2
        edge_x1, edge_y1, edge_x2, edge_y2 = edge
        
        # Parámetros de la línea del polígono
        dx = x2 - x1
        dy = y2 - y1
        
        # Parámetros del borde
        edge_dx = edge_x2 - edge_x1
        edge_dy = edge_y2 - edge_y1
        
        # Denominador para el cálculo de la intersección
        denom = dx * edge_dy - dy * edge_dx
        
        if abs(denom) < 1e-10:  # Líneas paralelas
            return point1
        
        # Calcular parámetro t para la intersección
        t = ((edge_x1 - x1) * edge_dy - (edge_y1 - y1) * edge_dx) / denom
        
        # Calcular punto de intersección
        intersection_x = x1 + t * dx
        intersection_y = y1 + t * dy
        
        return (intersection_x, intersection_y)
    
    def clip_polygon(self, polygon: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Recorta un polígono contra la ventana usando el algoritmo de Sutherland-Hodgman.
        
        Args:
            polygon: Lista de puntos del polígono [(x1, y1), (x2, y2), ...]
        
        Returns:
            Lista de puntos del polígono recortado
        """
        if len(polygon) < 3:
            return polygon
        
        # Inicializar el polígono resultante
        result = polygon.copy()
        
        # Recortar contra cada borde de la ventana
        for edge in self.edges:
            input_polygon = result
            result = []
            
            if len(input_polygon) == 0:
                break
            
            # Procesar cada vértice del polígono
            for i in range(len(input_polygon)):
                current_point = input_polygon[i]
                previous_point = input_polygon[i - 1] if i > 0 else input_polygon[-1]
                
                # Verificar si el punto actual está dentro del borde
                current_inside = self.inside(current_point, edge)
                previous_inside = self.inside(previous_point, edge)
                
                if current_inside:
                    if not previous_inside:
                        # El punto anterior está fuera, calcular intersección
                        intersection = self.intersection(previous_point, current_point, edge)
                        result.append(intersection)
                    result.append(current_point)
                else:
                    if previous_inside:
                        # El punto anterior está dentro, calcular intersección
                        intersection = self.intersection(previous_point, current_point, edge)
                        result.append(intersection)
        
        return result


class ClippingVisualizer:
    """
    Visualizador gráfico para el algoritmo de recorte de Sutherland-Hodgman.
    """
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.window = pyglet.window.Window(width, height, caption="Sutherland-Hodgman Clipping")
        
        # Configurar la ventana de recorte (viewport)
        self.clip_left = 200
        self.clip_bottom = 150
        self.clip_right = 600
        self.clip_top = 450
        
        # Crear el recortador
        self.clipper = SutherlandHodgmanClipper(
            self.clip_left, self.clip_bottom, 
            self.clip_right, self.clip_top
        )
        
        # Polígono de ejemplo (triángulo que cruza la ventana de recorte)
        self.original_polygon = [
            (150, 100),  # Dentro de la ventana
            (650, 200),  # Fuera de la ventana (derecha)
            (300, 500)   # Fuera de la ventana (arriba)
        ]
        
        # Polígono recortado
        self.clipped_polygon = self.clipper.clip_polygon(self.original_polygon)
        
        # Configurar eventos
        self.window.event(self.on_draw)
        self.window.event(self.on_key_press)
        
        # Colores
        self.window_color = (0.9, 0.9, 0.9, 1.0)  # Gris claro
        self.original_color = (0.2, 0.6, 1.0, 1.0)  # Azul
        self.clipped_color = (1.0, 0.3, 0.3, 1.0)  # Rojo
        self.clip_window_color = (0.0, 0.0, 0.0, 1.0)  # Negro
    
    def draw_polygon(self, vertices, color):
        """Dibuja un polígono con el color especificado."""
        if len(vertices) < 3:
            return
        
        # Convertir vértices a formato de Pyglet
        vertex_list = []
        for vertex in vertices:
            vertex_list.extend([vertex[0], vertex[1]])
        
        # Crear arrays de colores
        color_array = []
        for _ in range(len(vertices)):
            color_array.extend(color)
        
        # Dibujar el polígono relleno
        pyglet.graphics.draw(len(vertices), pyglet.gl.GL_POLYGON,
                           ('v2f', vertex_list),
                           ('c4f', color_array))
        
        # Dibujar el contorno negro
        black_color = [0.0, 0.0, 0.0, 1.0] * len(vertices)
        pyglet.graphics.draw(len(vertices), pyglet.gl.GL_LINE_LOOP,
                           ('v2f', vertex_list),
                           ('c4f', black_color))
    
    def draw_clip_window(self):
        """Dibuja la ventana de recorte."""
        vertices = [
            (self.clip_left, self.clip_bottom),
            (self.clip_right, self.clip_bottom),
            (self.clip_right, self.clip_top),
            (self.clip_left, self.clip_top)
        ]
        
        # Convertir vértices a formato de Pyglet
        vertex_list = []
        for vertex in vertices:
            vertex_list.extend([vertex[0], vertex[1]])
        
        # Crear array de colores para la ventana
        window_color_array = []
        for _ in range(len(vertices)):
            window_color_array.extend(self.clip_window_color)
        
        # Dibujar el contorno de la ventana
        pyglet.graphics.draw(len(vertices), pyglet.gl.GL_LINE_LOOP,
                           ('v2f', vertex_list),
                           ('c4f', window_color_array))
    
    def on_draw(self):
        """Función de dibujo principal."""
        # Limpiar con color de fondo claro
        pyglet.gl.glClearColor(0.9, 0.9, 0.9, 1.0)
        self.window.clear()
        
        # Dibujar la ventana de recorte
        self.draw_clip_window()
        
        # Dibujar el polígono original
        self.draw_polygon(self.original_polygon, self.original_color)
        
        # Dibujar el polígono recortado
        if len(self.clipped_polygon) >= 3:
            self.draw_polygon(self.clipped_polygon, self.clipped_color)
    
    def on_key_press(self, symbol, modifiers):
        """Maneja las pulsaciones de teclas."""
        if symbol == pyglet.window.key.ESCAPE:
            self.window.close()
        elif symbol == pyglet.window.key.R:
            # Regenerar polígono aleatorio
            self.generate_random_polygon()
            self.clipped_polygon = self.clipper.clip_polygon(self.original_polygon)
    
    def generate_random_polygon(self):
        """Genera un polígono aleatorio para demostración."""
        import random
        
        # Generar un polígono simple (triángulo)
        center_x = random.randint(100, 700)
        center_y = random.randint(100, 500)
        radius = random.randint(50, 150)
        
        self.original_polygon = []
        num_vertices = random.randint(3, 6)
        
        for i in range(num_vertices):
            angle = 2 * np.pi * i / num_vertices
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
            self.original_polygon.append((x, y))
    
    def run(self):
        """Ejecuta la aplicación."""
        print("Controles:")
        print("  ESC: Salir")
        print("  R: Generar nuevo polígono aleatorio")
        print("\nVentana de recorte: rectángulo negro")
        print("Polígono original: azul")
        print("Polígono recortado: rojo")
        
        pyglet.app.run()


def demo_simple():
    """Demostración simple del algoritmo sin interfaz gráfica."""
    print("=== Demostración del Algoritmo de Sutherland-Hodgman ===\n")
    
    # Definir la ventana de recorte
    clip_left, clip_bottom = 0, 0
    clip_right, clip_top = 10, 10
    
    # Crear el recortador
    clipper = SutherlandHodgmanClipper(clip_left, clip_bottom, clip_right, clip_top)
    
    # Caso 1: Polígono completamente dentro de la ventana
    polygon1 = [(2, 2), (8, 2), (5, 8)]
    
    print(f"Ventana de recorte: ({clip_left}, {clip_bottom}) a ({clip_right}, {clip_top})")
    print(f"Caso 1 - Polígono completamente dentro: {polygon1}")
    
    # Aplicar el recorte
    clipped_polygon1 = clipper.clip_polygon(polygon1)
    
    print(f"Polígono recortado: {clipped_polygon1}")
    
    # Caso 2: Polígono que se extiende fuera de la ventana
    polygon2 = [(-2, 5), (12, 5), (5, 12)]
    
    print(f"\nCaso 2 - Polígono que se extiende fuera: {polygon2}")
    clipped_polygon2 = clipper.clip_polygon(polygon2)
    print(f"Polígono recortado: {clipped_polygon2}")
    
    # Caso 3: Polígono que cruza múltiples bordes
    polygon3 = [(-3, 3), (13, 3), (5, 13), (5, -3)]
    
    print(f"\nCaso 3 - Polígono que cruza múltiples bordes: {polygon3}")
    clipped_polygon3 = clipper.clip_polygon(polygon3)
    print(f"Polígono recortado: {clipped_polygon3}")
    
    # Caso 4: Polígono completamente fuera de la ventana
    polygon4 = [(-5, -5), (-2, -5), (-3, -2)]
    
    print(f"\nCaso 4 - Polígono completamente fuera: {polygon4}")
    clipped_polygon4 = clipper.clip_polygon(polygon4)
    print(f"Polígono recortado: {clipped_polygon4}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_simple()
    else:
        # Ejecutar la visualización gráfica
        visualizer = ClippingVisualizer()
        visualizer.run()
