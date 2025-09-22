import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk
from utils import new_canvas, set_pixel, save_png
from bresenhamLine import bresenham_line
from middlePointCircle import middle_point_circle
from math import cos, sin, pi

WIDTH, HEIGHT = 400, 400
DEFAULT_COLOR = (255,255,255)
DEFAULT_BG_COLOR = (0,0,0)

canvas_data = new_canvas(WIDTH, HEIGHT, DEFAULT_BG_COLOR)
draw_color = DEFAULT_COLOR
bg_color = DEFAULT_BG_COLOR
points = []

root = tk.Tk()
root.title("Mini Paint Casero Visible")

mode = tk.StringVar(value="linea")

# Usar Canvas de Tkinter para mostrar la imagen
canvas_widget = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg='#%02x%02x%02x' % DEFAULT_BG_COLOR, highlightthickness=0)
canvas_widget.pack()

# Imagen Pillow y PhotoImage para mostrar en Tkinter
img = Image.new("RGB", (WIDTH, HEIGHT), bg_color)
photo = ImageTk.PhotoImage(img)
canvas_img = canvas_widget.create_image(0, 0, anchor=tk.NW, image=photo)
canvas_widget.image = photo  # Mantener referencia

def redraw_canvas():
    global photo, img
    pixels = [pix for row in canvas_data for pix in row]
    img = Image.new("RGB", (WIDTH, HEIGHT), bg_color)
    img.putdata(pixels)
    photo = ImageTk.PhotoImage(img)
    canvas_widget.itemconfig(canvas_img, image=photo)
    canvas_widget.image = photo  # Mantener referencia (esto es CRUCIAL)

def clear_canvas():
    global canvas_data, points
    canvas_data = new_canvas(WIDTH, HEIGHT, bg_color)
    points = []
    redraw_canvas()

def update_draw_color():
    global draw_color
    color_code = colorchooser.askcolor(title="Color de dibujo")
    if color_code and color_code[0]:
        draw_color = tuple(int(c) for c in color_code[0])

def update_bg_color():
    global bg_color, canvas_data
    color_code = colorchooser.askcolor(title="Color de fondo")
    if color_code and color_code[0]:
        bg_color = tuple(int(c) for c in color_code[0])
        clear_canvas()
        canvas_widget.config(bg='#%02x%02x%02x' % bg_color)

def on_click(event):
    global points
    points.append((event.x, event.y))

    if mode.get() == "linea" and len(points) == 2:
        x0, y0 = points[0]
        x1, y1 = points[1]
        for px, py in bresenham_line(x0, y0, x1, y1):
            set_pixel(canvas_data, px, py, draw_color)
        redraw_canvas()
        points = []

    elif mode.get() == "rect" and len(points) == 2:
        x0, y0 = points[0]
        x1, y1 = points[1]
        for px, py in bresenham_line(x0, y0, x1, y0):
            set_pixel(canvas_data, px, py, draw_color)
        for px, py in bresenham_line(x1, y0, x1, y1):
            set_pixel(canvas_data, px, py, draw_color)
        for px, py in bresenham_line(x1, y1, x0, y1):
            set_pixel(canvas_data, px, py, draw_color)
        for px, py in bresenham_line(x0, y1, x0, y0):
            set_pixel(canvas_data, px, py, draw_color)
        redraw_canvas()
        points = []

    elif mode.get() == "circle" and len(points) == 2:
        (cx, cy), (px, py) = points
        r = int(((px - cx) ** 2 + (py - cy) ** 2) ** 0.5)
        circulo = middle_point_circle(cx, cy, r)
        for px, py in circulo:
            set_pixel(canvas_data, px, py, draw_color)
        redraw_canvas()
        points = []

    elif mode.get() == "tri" and len(points) == 3:
        for i in range(3):
            x0, y0 = points[i]
            x1, y1 = points[(i+1)%3]
            for px, py in bresenham_line(x0, y0, x1, y1):
                set_pixel(canvas_data, px, py, draw_color)
        redraw_canvas()
        points = []

    elif mode.get() == "ellipse" and len(points) == 3:
        cx, cy = points[0]
        ex, ey = points[1]
        rx = int(((ex-cx)**2 + (ey-cy)**2)**0.5)
        px3, py3 = points[2]
        ry = int(((px3-cx)**2 + (py3-cy)**2)**0.5)
        for theta in range(0, 360, 1):
            rad = theta * pi / 180
            x = int(cx + rx * cos(rad))
            y = int(cy + ry * sin(rad))
            set_pixel(canvas_data, x, y, draw_color)
        redraw_canvas()
        points = []

    elif mode.get() == "erase" and len(points) == 1:
        x, y = points[0]
        size = 10
        for dx in range(-size//2, size//2):
            for dy in range(-size//2, size//2):
                set_pixel(canvas_data, x+dx, y+dy, bg_color)
        redraw_canvas()
        points = []

def save_image():
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if filename:
        save_png(filename, canvas_data)

frame_top = tk.Frame(root)
frame_top.pack()
tk.Button(frame_top, text="Línea", command=lambda: set_mode("linea")).pack(side=tk.LEFT)
tk.Button(frame_top, text="Rectángulo", command=lambda: set_mode("rect")).pack(side=tk.LEFT)
tk.Button(frame_top, text="Círculo", command=lambda: set_mode("circle")).pack(side=tk.LEFT)
tk.Button(frame_top, text="Triángulo", command=lambda: set_mode("tri")).pack(side=tk.LEFT)
tk.Button(frame_top, text="Elipse", command=lambda: set_mode("ellipse")).pack(side=tk.LEFT)
tk.Button(frame_top, text="Borrador", command=lambda: set_mode("erase")).pack(side=tk.LEFT)

frame_color = tk.Frame(root)
frame_color.pack()
tk.Button(frame_color, text="Color de dibujo", command=update_draw_color).pack(side=tk.LEFT)
tk.Button(frame_color, text="Color de fondo", command=update_bg_color).pack(side=tk.LEFT)
tk.Button(frame_color, text="Limpiar", command=clear_canvas).pack(side=tk.LEFT)
tk.Button(frame_color, text="Guardar", command=save_image).pack(side=tk.LEFT)

def set_mode(m):
    mode.set(m)
    points.clear()

canvas_widget.bind("<Button-1>", on_click)
redraw_canvas()

root.mainloop()