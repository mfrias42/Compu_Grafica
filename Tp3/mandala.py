import pyglet
import moderngl
import numpy as np
import math
from time import time
from pathlib import Path

# Vertex shader simple para quad completo
vertex_shader = """
#version 330 core

in vec2 in_pos;
out vec2 v_uv;

void main() {
    gl_Position = vec4(in_pos, 0.0, 1.0);
    v_uv = in_pos * 0.5 + 0.5;
}
"""

# Fragment shader del mandala adaptado
fragment_shader = """
#version 330 core

in vec2 v_uv;
out vec4 fragColor;

uniform vec2 iResolution;
uniform float iTime;
uniform float iDirection;

#define PI 3.14159265
#define aspect (iResolution.x/iResolution.y)

float circle(vec2 p, float r, float width) {
    float d = 0.;
    d += smoothstep(1., 0., width*abs(p.x - r));
    return d;
}

float arc(vec2 p, float r, float a, float width) {
    float d = 0.;
    if (abs(p.y) < a) {
        d += smoothstep(1., 0., width*abs(p.x - r));
    }
    return d;
}

float rose(vec2 p, float t, float width) {
    const float a0 = 6.;
    float d = 0.;
    p.x *= 7. + 8. * t;
    d += smoothstep(1., 0., width*abs(p.x - sin(a0*p.y)));
    d += smoothstep(1., 0., width*abs(p.x - abs(sin(a0*p.y))));
    d += smoothstep(1., 0., width*abs(abs(p.x) - sin(a0*p.y)));
    d += smoothstep(1., 0., width*abs(abs(p.x) - abs(sin(a0*p.y))));
    return d;
}

float rose2(vec2 p, float t, float width) {
    const float a0 = 6.;
    float d = 0.;
    p.x *= 7. + 8. * t;
    d += smoothstep(1., 0., width*abs(p.x - cos(a0*p.y)));
    d += smoothstep(1., 0., width*abs(p.x - abs(cos(a0*p.y))));
    d += smoothstep(1., 0., width*abs(abs(p.x) - cos(a0*p.y)));
    d += smoothstep(1., 0., width*abs(abs(p.x) - abs(cos(a0*p.y))));
    return d;
}

float spiral(vec2 p, float width) {
    float d = 0.;
    d += smoothstep(1., 0., width*abs(p.x - 0.5 * p.y / PI));
    d += smoothstep(1., 0., width*abs(p.x - 0.5 * abs(p.y) / PI));
    d += smoothstep(1., 0., width*abs(abs(p.x) - 0.5 * p.y / PI));
    d += smoothstep(1., 0., width*abs(abs(p.x) - 0.5 * abs(p.y) / PI));
    return d;
}

float star(vec2 p, float r, float n, float width) {
    float a = atan(p.y, p.x);
    float d = length(p);
    float star_r = r * (0.5 + 0.5 * cos(n * a));
    return smoothstep(1., 0., width * abs(d - star_r));
}

float hexagon(vec2 p, float r, float width) {
    vec2 q = abs(p);
    float d = max(q.x * 0.866025 + q.y * 0.5, q.y) - r;
    return smoothstep(1., 0., width * abs(d));
}

float wave(vec2 p, float freq, float amp, float width) {
    float d = 0.;
    d += smoothstep(1., 0., width * abs(p.y - amp * sin(freq * p.x)));
    d += smoothstep(1., 0., width * abs(p.y - amp * cos(freq * p.x)));
    return d;
}

void main() {
    vec2 uv = v_uv;
    vec2 p = uv - 0.5;
    p.x *= aspect;

    vec2 f = vec2(sqrt(p.x*p.x + p.y*p.y), atan(p.y, p.x));

    float T0 = cos(0.3*iTime);
    float T1 = 0.5 + 0.5 * cos(0.3*iTime);
    float T2 = sin(0.15*iTime);
    
    float m0 = 0.;
    float m1 = 0.;
    float m2 = 0.;
    float m3 = 0.;
    float m4 = 0.;
    
    if (f.x < 0.7325) {
        f.y += 0.1 * iTime * iDirection;
        vec2 c;
        vec2 f2;
        
        c = vec2(0.225 - 0.1*T0, PI / 4.);
        if (f.x < 0.25) {
            for (float i=0.; i < 2.; ++i) {
                f2 = mod(f, c) - 0.5 * c;
                m0 += spiral(vec2(f2.x, f2.y), 192.);
                m0 += star(f2, 0.1 + 0.05*T1, 6., 128.);
            }
        }
        
        c = vec2(0.225 + 0.1*T0, PI / 4.);
        if (f.x > 0.43) {
            for (float i=0.; i < 2.; ++i) {
                f.y += PI / 8.;
                f2 = mod(f, c) - 0.5 * c;
                m1 += rose((0.75-0.5*T0)*f2, 0.4*T1, 24.);
                m1 += rose2((0.5+0.5*T1)*f2, 0.2 + 0.2*T0, 36.);
                m1 += hexagon(f2 * (2.0 + T0), 0.08, 96.);
            }
        }
        
        c = vec2(0.6 - 0.2*T0, PI / 4.);
        if (f.x > 0.265) {
            for (float i=0.; i < 2.; ++i) {
                f.y += PI / 8.;
                f2 = mod(f, c) - 0.5 * c;
                m2 += spiral(vec2((0.25 + 0.5*T1)*f2.x, f2.y), 392.);
                m2 += rose2((1.+0.25*T0)*f2, 0.5, 24.);
                m2 += wave(f2 * 3.0, 8.0 + 4.0*T0, 0.02, 256.);
            }
        }
        
        c = vec2(0.4 + 0.23*T0, PI / 4.);
        if (f.x < 0.265) {
            for (float i=0.; i < 2.; ++i) {
                f.y += PI / 8.;
                f2 = mod(f, c) - 0.5 * c;
                m3 += spiral(vec2(f2.x, f2.y), 256.);
                m3 += rose(f2, 1.5 * T1, 16.);
                m3 += star(f2 * (1.5 + 0.5*T2), 0.06, 8., 192.);
            }
        }
        
        m4 += circle(f, 0.040, 192.);
        m4 += circle(f, 0.265, 192.);
        m4 += circle(f, 0.430, 192.);
    }
    m4 += circle(f, 0.7325, 192.);

    // Color
    float z = m0 + m1 + m2 + m3 + m4;
    z *= z;
    z = clamp(z, 0., 1.);
    
    // Colores más vibrantes y variados
    vec3 color1 = vec3(0.8, 0.2, 0.6) * (0.5 + 0.5*sin(T2));
    vec3 color2 = vec3(0.2, 0.8, 0.9) * (0.5 + 0.5*cos(T2 * 1.3));
    vec3 color3 = vec3(0.9, 0.7, 0.1) * (0.5 + 0.5*sin(T2 * 0.7));
    
    vec3 col = z * (color1 + color2 + color3) * 0.4;
    
    // Background
    vec3 bkg = vec3(0.32,0.36,0.4) + p.y*0.1;
    col += bkg;
    
    // Vignetting
    vec2 r = -1.0 + 2.0*(uv);
    float vb = max(abs(r.x), abs(r.y));
    col *= (0.15 + 0.85*(1.0-exp(-(1.0-vb)*30.0)));

    fragColor = vec4(col, 1.0);
}
"""

class MandalaWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=800, height=800, caption="Mandala 2D Animado")
        
        # Crear contexto OpenGL
        self.ctx = moderngl.create_context()
        
        # Compilar shaders
        self.program = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )
        
        # Crear quad que cubre toda la pantalla
        vertices = np.array([
            -1.0, -1.0,  # bottom-left
             1.0, -1.0,  # bottom-right
             1.0,  1.0,  # top-right
            -1.0,  1.0,  # top-left
        ], dtype=np.float32)
        
        indices = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)
        
        # Crear buffers
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.ibo = self.ctx.buffer(indices.tobytes())
        
        # Crear VAO
        self.vao = self.ctx.vertex_array(
            self.program,
            [(self.vbo, '2f', 'in_pos')],
            self.ibo
        )
        
        # Configurar uniforms
        self.program['iResolution'] = (self.width, self.height)
        
        # Tiempo inicial, dirección de rotación y pausa
        self.start_time = time()
        self.rotation_direction = 1.0  # 1.0 para horario, -1.0 para antihorario
        self.is_paused = False
        self.pause_time = 0.0
        self.total_pause_duration = 0.0
        
        # Variables para controlar la velocidad con el cursor
        self.mouse_x = self.width // 2
        self.mouse_y = self.height // 2
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.max_distance = ((self.width // 2) ** 2 + (self.height // 2) ** 2) ** 0.5
        self.current_speed_multiplier = 1.0
        
        # Configurar OpenGL
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        
    def on_draw(self):
        # Limpiar pantalla
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        
        # Actualizar tiempo y dirección
        if self.is_paused:
            # Si está pausado, mantener el tiempo actual
            current_time = self.pause_time
        else:
            # Si no está pausado, calcular tiempo normal menos el tiempo total pausado
            current_time = (time() - self.start_time - self.total_pause_duration) * self.current_speed_multiplier
        
        self.program['iTime'] = current_time
        self.program['iDirection'] = self.rotation_direction
        
        # Renderizar
        self.vao.render()
        
    def on_resize(self, width, height):
        self.ctx.viewport = (0, 0, width, height)
        self.program['iResolution'] = (width, height)
    
    def on_mouse_press(self, x, y, button, modifiers):
        # Cambiar dirección de rotación al hacer click
        self.rotation_direction *= -1.0
    
    def on_key_press(self, symbol, modifiers):
        # Pausar/reanudar con la tecla espacio
        if symbol == pyglet.window.key.SPACE:
            if self.is_paused:
                # Reanudar: calcular cuánto tiempo estuvo pausado
                pause_duration = time() - self.pause_start_time
                self.total_pause_duration += pause_duration
                self.is_paused = False
            else:
                # Pausar: guardar el tiempo actual y cuándo se pausó
                # Pausar: guardar el tiempo actual con la velocidad actual
                self.pause_time = (time() - self.start_time - self.total_pause_duration) * self.current_speed_multiplier
                self.pause_start_time = time()
                self.is_paused = True
    
    def on_mouse_motion(self, x, y, dx, dy):
        # Actualizar posición del cursor
        self.mouse_x = x
        self.mouse_y = y
        
        # Calcular nueva velocidad basada en la distancia al centro
        distance = ((self.mouse_x - self.center_x) ** 2 + (self.mouse_y - self.center_y) ** 2) ** 0.5
        # Normalizar distancia (0.0 a 1.0) y convertir a multiplicador de velocidad (0.1 a 3.0)
        normalized_distance = min(distance / self.max_distance, 1.0)
        self.current_speed_multiplier = 0.1 + normalized_distance * 2.9

if __name__ == "__main__":
    window = MandalaWindow()
    pyglet.app.run()