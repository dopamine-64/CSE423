from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

points = []
speed = 2.5 
window_width = 500
window_height = 500
frozen = False

background_shapes = []
bg_position = (0, 0)
square_color = (0,0,0)
scale = 3000
triangle_visible = False

def add_triangle(position, square_color, scale):
    x, y = position
    size = scale
    square_color= square_color

    background_shapes.append([
        (x, y),
        (x + size, y),
        (x, y + size)
    ])

    background_shapes.append([
        (x + size, y),
        (x + size, y + size),
        (x, y + size)
    ])

add_triangle(bg_position, square_color, scale)

class Point:
    def __init__(self, x, y, speed):
        angle_deg = random.choice([45, 135, 225, 315])
        angle_rad = math.radians(angle_deg)
        self.direction = [math.cos(angle_rad), math.sin(angle_rad)]
        self.position = [x, y]
        self.speed= speed
        self.color = (random.random(), random.random(), random.random())
        self.size = 5

    def update(self):
        if self.position[0] <= 0 or self.position[0] >= window_width:
            self.direction[0] *= -1
            self.position[0] = max(0, min(self.position[0], window_width))
        if self.position[1] <= 0 or self.position[1] >= window_height:
            self.direction[1] *= -1
            self.position[1] = max(0, min(self.position[1], window_height))

        self.position[0] += self.direction[0] * speed
        self.position[1] += self.direction[1] * speed

    def draw(self):
        glColor3f(*self.color)
        glPointSize(self.size)
        glBegin(GL_POINTS)
        glVertex2f(*self.position)
        glEnd()

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


def mouse(button, state, x, y):
    global triangle_visible
    if frozen:
        return

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        gl_x = x
        gl_y = window_height - y
        points.append(Point(gl_x, gl_y, speed))

    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        triangle_visible = not triangle_visible
        glutPostRedisplay()

def special_keys(key, x, y):
    global speed
    if frozen:
        return
    if key == GLUT_KEY_UP:
        speed += 0.5
    elif key == GLUT_KEY_DOWN:
        speed = max(0.5, speed - 0.5)

def keyboard(key, x, y):
    global frozen
    if key == b' ':
        frozen = not frozen
        glutPostRedisplay()

def draw_background():
    glColor3f(*square_color)
    for triangle in background_shapes:
        glBegin(GL_TRIANGLES)
        for vertex in triangle:
            glVertex2f(*vertex)
        glEnd()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    for p in points:
        if not frozen:
            p.update()
        p.draw()

    if triangle_visible:
        draw_background()

    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Task 2")

glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutMouseFunc(mouse)
glutReshapeFunc(display)
glutSpecialFunc(special_keys)
glutKeyboardFunc(keyboard)

glClearColor(0.0, 0.0, 0.0, 1.0)
glutMainLoop()