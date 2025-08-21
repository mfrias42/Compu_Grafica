def bresenham_line(canvas, x1, y1, x2, y2):
    points = []
    delta_x = abs(x2 - x1)
    delta_y = abs(y2 - y1)
    step_x = 1 if x1 < x2 else -1
    step_y = 1 if y1 < y2 else -1
    error = delta_x - delta_y
    while True:
        if x1 == x2 and y1 == y2:
            points.append((x1, y1))
            break
        points.append((x1, y1))
        e2 = 2 * error
        if e2 > -delta_y:
            error -= delta_y
            x1 += step_x
        if e2 < delta_x:
            error += delta_x
            y1 += step_y
    return points


def draw_line(canvas, x1, y1, x2, y2):
    points = []
    delta_x = x2 - x1
    delta_y = y2 - y1
    step = max(abs(delta_x), abs(delta_y)) 
    
    # Inicializar step_x y step_y
    step_x = 0
    step_y = 0
    
    if delta_x != 0:
        step_x = delta_x / step
        step_y = delta_y / step
    for i in range(step + 1):
        points.append((round(x1 + i * step_x), round(y1 + i * step_y)))
    return points

def new_canvas(width, height, background = (0, 0, 0)):
    return [[background for _ in range(width)]for _ in range(height)]

def set_pixel(canvas, x, y, color = (255, 255, 255)):
    height = len(canvas)
    width = len(canvas[0])
    if 0 <= x < width and 0 <= y < height:
        canvas[y][x] = color


def print_canvas(canvas):
    for row in canvas:
        print("|".join(str(pixel) for pixel in row))

def save_ppm_p3(filename, canvas):
    height = len(canvas)
    width = len(canvas[0])
    with open(filename, "w") as file:
        file.write("P3\n")
        file.write(f"{width} {height}\n")
        file.write("255\n")
        for row in canvas:
            line = []
            for (r, g, b) in row:
                line.append(f"{r} {g} {b}")
            file.write(" ".join(line))
            file.write("\n")

canvas = new_canvas(32, 24)

# Dibujar cuadrado blanco
def draw_square(canvas, x1, y1, x2, y2, color):
    # Línea superior
    points = bresenham_line(canvas, x1, y1, x2, y1)
    for x, y in points:
        set_pixel(canvas, x, y, color)
    
    # Línea inferior
    points = bresenham_line(canvas, x1, y2, x2, y2)
    for x, y in points:
        set_pixel(canvas, x, y, color)
    
    # Línea izquierda
    points = bresenham_line(canvas, x1, y1, x1, y2)
    for x, y in points:
        set_pixel(canvas, x, y, color)
    
    # Línea derecha
    points = bresenham_line(canvas, x2, y1, x2, y2)
    for x, y in points:
        set_pixel(canvas, x, y, color)

# Dibujar línea diagonal con color específico
def draw_colored_line(canvas, x1, y1, x2, y2, color):
    points = bresenham_line(canvas, x1, y1, x2, y2)
    for x, y in points:
        set_pixel(canvas, x, y, color)

# Dibujar cuadrado blanco
draw_square(canvas, 8, 6, 24, 18, (255, 255, 255))

# Dibujar primera línea diagonal (esquina superior izquierda a inferior derecha) - Amarilla
draw_colored_line(canvas, 0, 0, 31, 23, (255, 255, 0))

# Dibujar segunda línea diagonal (esquina inferior izquierda a superior derecha) - Celeste
draw_colored_line(canvas, 0, 23, 31, 0, (0, 255, 255))

# Dibujar tercera línea diagonal (con ángulo ajustado) - Violeta
draw_colored_line(canvas, 3, 20, 28, 3, (255, 0, 255))

print_canvas(canvas)
save_ppm_p3("line.ppm", canvas)