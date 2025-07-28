from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

class Shape:
    def __init__(self, vertices, color, position=(0, 0), scale=1.0, mode=GL_TRIANGLES, gradient=False):
        self.vertices = vertices                
        self.color = color
        self.position = position 
        self.scale = scale
        self.mode = mode
        self.gradient = gradient

    def draw(self, angle=0):
        glPushMatrix()
        glTranslatef(*self.position, 0)
        glRotatef(angle, 0, 0, 1)
        glScalef(self.scale, self.scale, 1.0)

        glBegin(self.mode)
        if self.gradient:
            for i in range(len(self.vertices)):
                glColor3f(*self.color[i])
                x, y = self.vertices[i]
                glVertex2f(x, y)
        else:
            glColor3f(*self.color)
            for x, y in self.vertices:
                glVertex2f(x, y)
        glEnd()
        glPopMatrix()


house_shapes = []
tree_shapes = []
background_shapes = []
sky_shapes = []
sky_color=[0.0,0.0,0.0]

rain_lines = []
rain_angle = 0
rain_speed = 3
dx = 0
dy = 5

house_shapes.append(Shape(
    vertices=[(120, 330), (120, 170), (370, 170)],
    color=(255/255, 245/255, 220/255)
))
house_shapes.append(Shape(
    vertices=[(120, 330), (370, 170), (370, 330)],
    color=(255/255, 245/255, 220/255)
))
house_shapes.append(Shape(
    vertices=[(60, 310), (430, 310), (250, 400)],
    color=(0.402, 0.2, 0.502)

))

window_positions = [(150, 220), (290, 220)]

for x, y in window_positions:
    house_shapes.append(Shape(
        vertices=[(0, 0), (30, 0), (0, 30)],
        color=(0.0, 0.749, 1.0),
        position=(x, y),
        scale=1.7
    ))
    house_shapes.append(Shape(
        vertices=[(30, 0), (30, 30), (0, 30)],
        color=(0.549, 0.745, 0.839),
        position=(x, y),
        scale=1.7
    ))

door_position = (220, 170) 

house_shapes.append(Shape(
    vertices=[(0, 0), (30, 0), (0, 60)],
    color=(0.2, 0.8, 1.0), 
    position=door_position,
    scale=1.7
))
house_shapes.append(Shape(
    vertices=[(30, 0), (30, 60), (0, 60)],
    color=(0.2, 0.8, 1.0),
    position=door_position,
    scale=1.7
))

line_positions = [(167, 246), (307, 246)]
for x, y in line_positions:
    house_shapes.append(Shape(
        vertices=[(5, -15), (5, 15)],
        color=(0, 0, 0),
        position=(x, y),
        scale=1.7,
        mode= GL_LINES
    ))
    house_shapes.append(Shape(
        vertices=[(-8, 0), (17, 0)],
        color=(0, 0, 0),
        position=(x, y),
        scale=2,
        mode= GL_LINES
    ))

knob_position = (255, 215)
house_shapes.append(Shape(
        vertices=[(0, 0), (30, 0), (0, 30)],
        color=(0, 0, 0),
        position= knob_position,
        scale=0.3
))
house_shapes.append(Shape(
        vertices=[(30, 0), (30, 30), (0, 30)],
        color=(0, 0, 0),
        position= knob_position,
        scale=0.3
))

bg_position = (-330, -830)
background_shapes.append(Shape(
        vertices=[(0, 0), (30, 0), (0, 30)],
        color=(100/255, 60/255, 0/255),
        position= bg_position,
        scale=40
))
background_shapes.append(Shape(
        vertices=[(30, 0), (30, 30), (0, 30)],
        color=(100/255, 60/255, 0/255),
        position= bg_position,
        scale=40
))

sky_position = (-330, -500)
sky_shapes.append(Shape(
        vertices=[(0, 0), (30, 0), (0, 30)],
        color= sky_color,
        position= sky_position,
        scale=40
))
sky_shapes.append(Shape(
        vertices=[(30, 0), (30, 30), (0, 30)],
        color= sky_color,
        position= sky_position,
        scale=40
))

triangle_count = 25
screen_width = 1150

for i in range(triangle_count):
    spacing = screen_width / triangle_count
    x = -330+spacing*i
    y = 295
    triangle = Shape(
        vertices=[(0, 0), (50, 0), (25, 60)],
        color=[(0.1, 0.5, 0.1), (0.1, 0.5, 0.1), (0.5, 1.0, 0.5)],
        position=(x, y),
        scale=1.0,
        gradient=True
    )
    tree_shapes.append(triangle)

for i in range(1500):
    x = random.randint(-1150, 1150)
    y = random.randint(-1150, 1150)
    rain_lines.append(Shape(
        vertices=[(0, 0), (0, 15)],
        color=(0.6, 0.8, 1.0),
        position=[x, y],
        scale=2,
        mode=GL_LINES
    ))

window_width = 500
window_height = 500

def display(w, h):
    global window_width, window_height
    window_width = w
    window_height = h

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if w > h:
        aspect = w / h
        glOrtho(0, 500 * aspect, 0, 500, 0, 1)
        window_width = 500 * aspect
        window_height = 500
    else:
        aspect = h / w
        glOrtho(0, 500, 0, 500 * aspect, 0, 1)
        window_width = 500
        window_height = 500 * aspect

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def draw_scene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glTranslatef(400, 250, 0)
    glScalef(0.7, 0.7, 1.0)
    glTranslatef(-250, -250, 0)

    for shape in sky_shapes:
        shape.color = sky_color
    for shape in sky_shapes:
        shape.draw()
    for shape in background_shapes:
        shape.draw()
    for shape in tree_shapes:
        shape.draw()
    for shape in house_shapes:
        shape.draw()
    for line in rain_lines:
        line.draw()

    glPopMatrix()
    glutSwapBuffers()

def special_keys(key, x, y):
    global rain_angle
    if key == GLUT_KEY_UP:
        rain_angle += 5
    elif key == GLUT_KEY_DOWN:
        rain_angle -= 5
    rain_angle = max(-60, min(60, rain_angle))
    glutPostRedisplay()

def keyboard(key, x, y):
    global sky_color
    if key == b'w':
        new_color = []
        for c in sky_color:
            new_c = max(0, c - 0.05)
            new_color.append(new_c)
        sky_color = new_color
    elif key == b's':
        new_color = []
        for c in sky_color:
            new_c = min(1, c + 0.05)
            new_color.append(new_c)
        sky_color = new_color
    glutPostRedisplay()

def animate():
    angle_rad = math.radians(rain_angle)
    dx = math.sin(angle_rad) * rain_speed
    dy = math.cos(angle_rad) * rain_speed
    for drop in rain_lines:
        drop.position[0] += dx
        drop.position[1] -= dy
        x1, y1 = 0, 0
        x2, y2 = 0, 15
        x2r = x2 * math.cos(angle_rad) - y2 * math.sin(angle_rad)
        y2r = x2 * math.sin(angle_rad) + y2 * math.cos(angle_rad)
        drop.vertices = [(x1, y1), (x2r, y2r)]
        if drop.position[1] < 0 or drop.position[0] < 850 or drop.position[0] > 1000:
            drop.position[0] = random.uniform(-1150,1150)
            drop.position[1] = random.uniform(-1150,1150)
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(800, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Task 1")

glutDisplayFunc(draw_scene)
glutReshapeFunc(display)
glutSpecialFunc(special_keys)
glutIdleFunc(animate)
glutKeyboardFunc(keyboard)

glClearColor(0.0, 0.0, 0.0, 1.0)
glutMainLoop()