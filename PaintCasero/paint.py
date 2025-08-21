import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk
# Importar las funciones de utils y los algoritmos desarrollados en clase
from utils import new_canvas, set_pixel, save_png
from bresenhamLine import bresenham_line
from middlePointCircle import middle_point_circle
from ellipse import middle_point_ellipse

WIDTH, HEIGHT = 400, 400 # Tamaño de canvas/ventana

# 1) Crear el canvas lógico (array de píxeles) con WIDTH y HEIGHT, inicializado con fondo negro
canvas_data = new_canvas(WIDTH, HEIGHT, (0, 0, 0)) # Usar la función de utils que crea un lienzo vacío

# Tkinter setup
root = tk.Tk()
root.title("Mini Paint Casero")

# Imagen con Pillow para usar en Tkinter 
img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0)) # Asigno un color de fondo de la ventana de dibujo, modo oscuro
photo = ImageTk.PhotoImage(img)
label = tk.Label(root, image=photo)
label.pack()

# Estado
mode = tk.StringVar(value="linea")
points = [] # Variable global de puntos
current_color = (255, 255, 255)  # Color actual (blanco por defecto)

# Copia el canvas lógico a la imagen Pillow y la refresca en Tkinter, para poder mantener la lógica de nuestros algoritmos.
def redraw_canvas():
    global photo, img
    # Flatten de los píxeles
    pixels = [pix for row in canvas_data for pix in row]
    img.putdata(pixels)
    photo = ImageTk.PhotoImage(img)
    label.config(image=photo)
    label.image = photo

# Maneja los clicks de los botones según el modo de dibujo (línea, círculo, etc.)
def on_click(event):
    global points # points es una matriz de puntos donde se hace click points[0] es el primer click points[1] es el segundo y así...
    
    # --- Borrador (manejo especial) ---
    if mode.get() == "borrador":
        # Borrar área de 5x5 píxeles alrededor del click
        x, y = event.x, event.y
        for dx in range(-2, 3):  # -2, -1, 0, 1, 2
            for dy in range(-2, 3):  # -2, -1, 0, 1, 2
                nx, ny = x + dx, y + dy
                # Verificar que esté dentro de los límites del canvas
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    set_pixel(canvas_data, nx, ny, (0, 0, 0))  # Color negro para borrar
        redraw_canvas()
        return  # Salir sin agregar punto a la lista
    
    points.append((event.x, event.y)) # Guarda las posiciones x, y que vienen en el event de click.

    # --- Dibujar Línea ---
    if mode.get() == "linea" and len(points) == 2: # Se necesitan 2 puntos.
        # 2) Generar la lista de puntos de la línea entre points[0] y points[1] con el algoritmo visto en clase
        # El primer click es el inicio de la linea y el segundo es el final.
        x0, y0 = points[0]
        x1, y1 = points[1]
        linea = bresenham_line(x0, y0, x1, y1)  # Usar algoritmo de Bresenham
        # 3) Dibujar esos puntos en el canvas usando la función adecuada
        # Pista: hay que recorrer la lista de puntos y pintar píxel por píxel
        for x, y in linea:
            set_pixel(canvas_data, x, y, current_color)
        redraw_canvas() # Siempre redibujo el canvas luego de agregar una figura.
        points = [] # Vacío points para poder dibujar la siguiente figura.

    # --- Dibujar Rectángulo ---
    elif mode.get() == "rect" and len(points) == 2: # Se necesitan 2 puntos.
        x0, y0 = points[0] # El primer click es un punto arriba a la izquierda.
        x1, y1 = points[1] # El segundo click es un punto abajo a la derecha.
        # 4) Dibujar los cuatro lados usando el algoritmo de línea
        # Pista: arriba, derecha, abajo, izquierda
        # Línea superior
        linea_arriba = bresenham_line(x0, y0, x1, y0)
        for x, y in linea_arriba:
            set_pixel(canvas_data, x, y, current_color)
        # Línea derecha
        linea_derecha = bresenham_line(x1, y0, x1, y1)
        for x, y in linea_derecha:
            set_pixel(canvas_data, x, y, current_color)
        # Línea abajo
        linea_abajo = bresenham_line(x1, y1, x0, y1)
        for x, y in linea_abajo:
            set_pixel(canvas_data, x, y, current_color)
        # Línea izquierda
        linea_izquierda = bresenham_line(x0, y1, x0, y0)
        for x, y in linea_izquierda:
            set_pixel(canvas_data, x, y, current_color)
        redraw_canvas() # Siempre redibujo el canvas luego de agregar una figura.
        points = [] # Vacío points para poder dibujar la siguiente figura.

    # --- Dibujar Círculo ---
    elif mode.get() == "circle" and len(points) == 2: # Se necesitan 2 puntos.
        (cx, cy), (px, py) = points # El primer click es el centro del círculo.
        r = int(((px - cx) ** 2 + (py - cy) ** 2) ** 0.5) # Con el segundo click, se calcula el radio.
        # 5) Generar los puntos del círculo con el algoritmo visto en clase
        circulo = middle_point_circle(cx, cy, r)  # Usar algoritmo de punto medio
        # 6) Pintar los píxeles en el canvas
        for x, y in circulo:
            set_pixel(canvas_data, x, y, current_color)
        redraw_canvas() # Siempre redibujo el canvas luego de agregar una figura.
        points = [] # Vacío points para poder dibujar la siguiente figura.

    # --- Dibujar Triángulo ---
    elif mode.get() == "tri" and len(points) == 3: # 7) Se necesitan 3 puntos para dibujar un triángulo
        # 7) Dibujar las 3 líneas necesarias que conectan los puntos usando el algoritmo correspondiente
        x0, y0 = points[0]
        x1, y1 = points[1]
        x2, y2 = points[2]
        
        # Línea del punto 0 al punto 1
        linea1 = bresenham_line(x0, y0, x1, y1)
        for x, y in linea1:
            set_pixel(canvas_data, x, y, current_color)
        
        # Línea del punto 1 al punto 2
        linea2 = bresenham_line(x1, y1, x2, y2)
        for x, y in linea2:
            set_pixel(canvas_data, x, y, current_color)
        
        # Línea del punto 2 al punto 0
        linea3 = bresenham_line(x2, y2, x0, y0)
        for x, y in linea3:
            set_pixel(canvas_data, x, y, current_color)
        
        # 8) Redibujamos el canvas y vaciamos la lista de puntos
        redraw_canvas()
        points = []

    # --- Dibujar Elipse ---
    elif mode.get() == "elipse" and len(points) == 2: # Se necesitan 2 puntos.
        (cx, cy), (px, py) = points # El primer click es el centro de la elipse.
        # Calcular radios usando la distancia desde el centro
        rx = abs(px - cx)
        ry = abs(py - cy)
        # Generar puntos de la elipse
        elipse = middle_point_ellipse(cx, cy, rx, ry)
        # Pintar los píxeles en el canvas
        for x, y in elipse:
            set_pixel(canvas_data, x, y, current_color)
        redraw_canvas()
        points = []


def on_drag(event):
    """Maneja el arrastre del mouse para el borrador."""
    if mode.get() == "borrador":
        # Borrar área de 5x5 píxeles alrededor del arrastre
        x, y = event.x, event.y
        for dx in range(-2, 3):  # -2, -1, 0, 1, 2
            for dy in range(-2, 3):  # -2, -1, 0, 1, 2
                nx, ny = x + dx, y + dy
                # Verificar que esté dentro de los límites del canvas
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    set_pixel(canvas_data, nx, ny, (0, 0, 0))  # Color negro para borrar
        redraw_canvas()


def change_color():
    """Permite al usuario cambiar el color de dibujo."""
    global current_color
    color = colorchooser.askcolor(title="Elegir color de dibujo")
    if color[0]:  # Si se seleccionó un color
        # Asegurar que los valores estén en el rango 0-255
        r, g, b = color[0]
        current_color = (max(0, min(255, int(r))), 
                        max(0, min(255, int(g))), 
                        max(0, min(255, int(b))))

def save_image():
    # 9) Guardar la imagen como .png usando la función vista en clase
    filename = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG files", "*.png")])
    if filename:
        save_png(filename, canvas_data)  # Usar la función que guarda el canvas en un archivo


# Creamos los botones con Tkinter en un recuadro distinto al canvas
frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Línea", command=lambda: mode.set("linea")).pack(side=tk.LEFT)
tk.Button(frame, text="Rectángulo", command=lambda: mode.set("rect")).pack(side=tk.LEFT)
tk.Button(frame, text="Círculo", command=lambda: mode.set("circle")).pack(side=tk.LEFT)
tk.Button(frame, text="Triángulo", command=lambda: mode.set("tri")).pack(side=tk.LEFT)
tk.Button(frame, text="Elipse", command=lambda: mode.set("elipse")).pack(side=tk.LEFT)
tk.Button(frame, text="Borrador", command=lambda: mode.set("borrador")).pack(side=tk.LEFT)
tk.Button(frame, text="Color", command=change_color).pack(side=tk.LEFT)
tk.Button(frame, text="Guardar", command=save_image).pack(side=tk.LEFT)

# Me suscribo al evento click izquierdo en el canvas creado con Tkinter
label.bind("<Button-1>", on_click)
label.bind("<B1-Motion>", on_drag)  # Evento para arrastrar con click presionado

# Mostrar fondo con el color de fondo inicial
redraw_canvas()

# Ejecutamos Tkinter para iniciar el bucle de eventos de la ventana.
root.mainloop()
