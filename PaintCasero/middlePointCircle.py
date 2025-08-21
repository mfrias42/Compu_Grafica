def middle_point_circle(cx, cy, r):
    points = []
    x = 0
    y = -r 
    p = -r 
    while x < -y:
        if p > 0:
            y+=1 
            p +=  2 * (x + y) + 1
        else:
            p +=  2 * x  + 1
        points.append((cx + x, cy + y))
        points.append((cx - x, cy + y))
        points.append((cx + x, cy - y))
        points.append((cx - x, cy - y)) 
        points.append((cx + y, cy + x)) 
        points.append((cx - y, cy + x))
        points.append((cx + y, cy - x))
        points.append((cx - y, cy - x)) 
        x += 1 
    return points