def middle_point_ellipse(cx, cy, rx, ry):
    """
    Algoritmo de punto medio para dibujar elipses.
    cx, cy: centro de la elipse
    rx, ry: radios en X e Y
    """
    points = []
    x = 0
    y = ry
    
    # Región 1: pendiente < -1
    p1 = ry * ry - rx * rx * ry + rx * rx // 4
    px = 0
    py = 2 * rx * rx * y
    
    while px < py:
        # Dibujar los 4 cuadrantes
        points.append((cx + x, cy + y))
        points.append((cx - x, cy + y))
        points.append((cx + x, cy - y))
        points.append((cx - x, cy - y))
        
        x += 1
        px += 2 * ry * ry
        
        if p1 < 0:
            p1 += ry * ry + px
        else:
            y -= 1
            py -= 2 * rx * rx
            p1 += ry * ry + px - py
    
    # Región 2: pendiente >= -1
    p2 = ry * ry * (x + 0.5) * (x + 0.5) + rx * rx * (y - 1) * (y - 1) - rx * rx * ry * ry
    
    while y >= 0:
        # Dibujar los 4 cuadrantes
        points.append((cx + x, cy + y))
        points.append((cx - x, cy + y))
        points.append((cx + x, cy - y))
        points.append((cx - x, cy - y))
        
        y -= 1
        py -= 2 * rx * rx
        
        if p2 > 0:
            p2 += rx * rx - py
        else:
            x += 1
            px += 2 * ry * ry
            p2 += rx * rx - py + px
    
    return points
