def bresenham_line(x0, y0, x1, y1):
    puntos = []

    dx = abs(x1 - x0)      # Diferencia en X
    dy = abs(y1 - y0)      # Diferencia en Y
    sx = 1 if x0 < x1 else -1   # Sentido en X
    sy = 1 if y0 < y1 else -1   # Sentido en Y
    err = dx - dy               # Error inicial
    
    while True:
        puntos.append((x0, y0))  # Guardar punto actual
        if x0 == x1 and y0 == y1:
            break  # Llegamos al final

        e2 = 2 * err
        if e2 > -dy:     # Corregir en X
            err -= dy
            x0 += sx
        if e2 < dx:      # Corregir en Y
            err += dx
            y0 += sy
        
    return puntos