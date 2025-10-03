from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import os

score = 0
game_state = 'playing'

diamond = {
    'x': random.randint(100, 500),
    'y': 550,
    'size': 12,
    'speed': 120,
    'color': (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))
}

catcher = {
    'x': 300,
    'y': 50,
    'width': 50,
    'height': 10,
    'color': (1.0, 1.0, 1.0),
    'speed': 150
}

cross = {
    'x': 550,
    'y': 550,
    'size': 12,
    'color': (1.0,0.3,0.3)
}

arrow = {
    'x': 50,
    'y': 550,
    'size': 12,
    'color': (0.3,1.0,1.0)
}

pause_btn = {
    'x': 300,
    'y': 550,
    'size': 15,
    'color': (1.0,1.0,0.3)
}

keys_held = {'left': False, 'right': False}
last_time = time.time()


def draw_pixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    abs_dx = abs(dx)
    abs_dy = abs(dy)
    if abs_dx >= abs_dy:
        if dx >= 0 and dy >= 0: return 0
        if dx >= 0 and dy < 0: return 7
        if dx < 0 and dy < 0: return 4
        if dx < 0 and dy >= 0: return 3
    else:
        if dx >= 0 and dy >= 0: return 1
        if dx >= 0 and dy < 0: return 6
        if dx < 0 and dy < 0: return 5
        if dx < 0 and dy >= 0: return 2

def forward(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return y, -x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return -y, x
    if zone == 7: return x, -y

def backward(x, y, zone):
    if zone == 0: return x, y
    if zone == 1: return y, x
    if zone == 2: return -y, x
    if zone == 3: return -x, y
    if zone == 4: return -x, -y
    if zone == 5: return -y, -x
    if zone == 6: return y, -x
    if zone == 7: return x, -y

def draw_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1_, y1_ = forward(x1, y1, zone)
    x2_, y2_ = forward(x2, y2, zone)

    dx = x2_ - x1_
    dy = y2_ - y1_
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x, y = x1_, y1_

    while x <= x2_:
        rx, ry = backward(x, y, zone)
        draw_pixel(rx, ry)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1


def draw_diamond(cx, cy, size):
    t = (cx, cy + size)
    r = (cx + size, cy)
    b = (cx, cy - size)
    l = (cx - size, cy)
    draw_line(*t, *r)
    draw_line(*r, *b)
    draw_line(*b, *l)
    draw_line(*l, *t)

def draw_catcher(cx, cy, w, h):
    l = (cx-20 - w // 2, cy)
    r = (cx+20 + w // 2, cy)
    bl = (l[0]+5, cy - h-3)
    br = (r[0]-5, cy - h-3)
    draw_line(*l, *r)
    draw_line(*l, *bl)
    draw_line(*r, *br)
    draw_line(*bl, *br)

def draw_cross(cx, cy, size):
    t = (cx-12, cy + size)
    r = (cx + size, cy+12)
    b = (cx+12, cy - size)
    l = (cx - size, cy-12)
    draw_line(*t, *b)
    draw_line(*l, *r)

def draw_arrow(cx, cy, size):
    l = (cx + size, cy)
    r = (cx - size, cy)
    t = (cx - size + 12, cy + 12)
    b = (cx - size + 12, cy - 12)
    draw_line(*r, *l)
    draw_line(*r, *t)
    draw_line(*r, *b) 

def draw_pause_icon(cx, cy, size):
    gap = 6
    tl = (cx - gap, cy + size)
    bl = (cx - gap, cy - size)
    tr = (cx + gap, cy + size)
    br = (cx + gap, cy - size)

    draw_line(*bl, *tl)
    draw_line(*br, *tr)

def draw_play_icon(cx, cy, size):
    tl = (cx - size // 2, cy + size)
    bl = (cx - size // 2, cy - size)
    r = (cx + size, cy)

    draw_line(*bl, *r)
    draw_line(*r, *tl)
    draw_line(*tl, *bl)

def has_collided(d, c):
    return (
        d['x'] - d['size'] < c['x'] + c['width'] // 2 and
        d['x'] + d['size'] > c['x'] - c['width'] // 2 and
        d['y'] - d['size'] < c['y'] and
        d['y'] + d['size'] > c['y'] - c['height']
    )

def reset_diamond():
    diamond['x'] = random.randint(100, 500)
    diamond['y'] = 500
    diamond['speed'] += 10
    diamond['color'] = (
        random.uniform(0.5, 1.0),
        random.uniform(0.5, 1.0),
        random.uniform(0.5, 1.0))

def reset_game():
    global score, game_state
    score = 0
    game_state = 'playing'
    catcher['color'] = (1.0, 1.0, 1.0)
    catcher['x'] = 300
    diamond['speed'] = 120
    reset_diamond()
    print("Starting Over")

def mouse_click(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = 600 - y 

        ax, ay, asize = arrow['x'], arrow['y'], arrow['size']
        if (ax - asize <= x <= ax + asize) and (ay - asize <= y <= ay + asize):
            reset_game()
            return

        cx, cy, csize = cross['x'], cross['y'], cross['size']
        if (cx - csize <= x <= cx + csize) and (cy - csize <= y <= cy + csize):
            print("Goodbye. Final Score:", score)
            os._exit(0)
        
        px, py, psize = pause_btn['x'], pause_btn['y'], pause_btn['size']
        if (px - psize <= x <= px + psize) and (py - psize <= y <= py + psize):
            toggle_pause()

def toggle_pause():
    global game_state
    if game_state == 'playing':
        game_state = 'paused'
    elif game_state == 'paused':
        game_state = 'playing'

def update():
    global last_time, game_state, score
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    if game_state == 'playing':
        diamond['y'] -= diamond['speed'] * dt
        if keys_held['left']:
            catcher['x'] -= catcher['speed'] * dt
        if keys_held['right']:
            catcher['x'] += catcher['speed'] * dt

        total_half_width = 35 + (catcher['width'] // 2)
        catcher['x'] = max(total_half_width, min(600 - total_half_width, catcher['x']))
        
        if has_collided(diamond, catcher):
            score += 1
            print("Score:", score)
            reset_diamond()
        elif diamond['y'] < 0:
            game_state = 'over'
            catcher['color'] = (1.0, 0.0, 0.0)
            print("Game Over! Final Score:", score)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    
    glColor3f(*catcher['color'])
    draw_catcher(catcher['x'], catcher['y'], catcher['width'], catcher['height'])
    
    glColor3f(*cross['color'])
    draw_cross(cross['x'], cross['y'], cross['size'])
    
    glColor3f(*arrow['color'])
    draw_arrow(arrow['x'], arrow['y'], arrow['size'])

    if game_state != 'over':
        glColor3f(*diamond['color'])
        draw_diamond(diamond['x'], int(diamond['y']), diamond['size'])

    glColor3f(*pause_btn['color'])
    if game_state == 'playing':
        draw_pause_icon(pause_btn['x'], pause_btn['y'], pause_btn['size'])
    else:
        draw_play_icon(pause_btn['x'], pause_btn['y'], pause_btn['size'])

    glutSwapBuffers()

def idle():
    update()
    glutPostRedisplay()

def special_input(key, x, y):
    if key == GLUT_KEY_LEFT:
        keys_held['left'] = True
    elif key == GLUT_KEY_RIGHT:
        keys_held['right'] = True

def special_up(key, x, y):
    if key == GLUT_KEY_LEFT:
        keys_held['left'] = False
    elif key == GLUT_KEY_RIGHT:
        keys_held['right'] = False

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutCreateWindow(b"Diamonds")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, 600, 0, 600)

    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutSpecialFunc(special_input)
    glutSpecialUpFunc(special_up)
    glutMouseFunc(mouse_click)

    glutMainLoop()

main()