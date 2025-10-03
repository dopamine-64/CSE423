from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

camera_pos = (0, 500, 500)
fovY = 120
tile_size = 100
offset = (11.7 * tile_size)

GRID_LENGTH = 600 

player_angle = 0
arrows = []

player_base = (-55.0, -650.0, 350.0)
player_tilt = -28.0 
player_scale = 1.2
player_angle = 0
player_pitch = 0

bow = (0.0, 22.0, 105.0)
kill_count = 0

god_mode = False
god_players = []

god_mode_cooldown = 0
god_shooter_index = 0

missed_arrows = 0
castle_health = 10
game_over = False

sky_time = 0.0
sky_speed = 0.002

first_person = False

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_gatehouse(center_x=0, front_y=250, wall_thickness=30, height=140):
    glPushMatrix()
    glTranslatef(center_x, front_y - wall_thickness / 2 - 1, 120)
    glColor3f(0.6, 0.5, 0.45)
    glScalef(160, 10, 20)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(center_x, front_y - wall_thickness / 2 - 1, 50)
    glColor3f(0.45, 0.35, 0.28)
    glScalef(50, 4, 100)
    glutSolidCube(1)
    glPopMatrix()

    draw_tower(center_x - 80, front_y, base_r=25, height=150)
    draw_tower(center_x + 80, front_y, base_r=25, height=150)

def draw_merlon(w=20, d=30, h=40, color=(0.6, 0.45, 0.35)):
    glPushMatrix()
    glColor3f(*color)
    glScalef(w, d, h)
    glutSolidCube(1)
    glPopMatrix()

def draw_tower(x, y, base_r=45, height=160):
    glPushMatrix()
    glTranslatef(x, y, 0)

    glColor3f(0.7, 0.6, 0.55)
    gluCylinder(gluNewQuadric(), base_r, base_r, height, 18, 4)

    glPushMatrix()
    glTranslatef(0, 0, height)
    glColor3f(0.6, 0.5, 0.45)
    glScalef(base_r * 2.2, base_r * 2.2, 8)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, height + 10)
    segments = 7
    ring_r = base_r * 1.4
    for i in range(segments):
        ang = (2 * math.pi / segments) * i
        px = ring_r * math.cos(ang)
        py = ring_r * math.sin(ang)
        glPushMatrix()
        glTranslatef(px, py, 0)
        draw_merlon(w=10, d=16, h=15, color=(0.55, 0.42, 0.32))
        glPopMatrix()
    glPopMatrix()

    glPopMatrix()

def draw_wall_front(x1, x2, y, thickness=30, height=120):
    length = abs(x2 - x1)
    cx = (x1 + x2) / 2.0
    glPushMatrix()
    glTranslatef(cx, y, height / 2)
    glColor3f(0.854, 0.706, 0.549)
    glScalef(length, thickness, height)
    glutSolidCube(1)
    glPopMatrix()

    step = 60
    count = max(1, int(length / step))
    for i in range(count + 1):
        t = i / count
        x = x1 + t * (x2 - x1)
        glPushMatrix()
        glTranslatef(x, y, height + 10)
        draw_merlon(w=18, d=thickness * 0.8, h=17)
        glPopMatrix()

def draw_wall_back(x1, x2, y, thickness=30, height=120):
    length = abs(x2 - x1)
    cx = (x1 + x2) / 2.0
    glPushMatrix()
    glTranslatef(cx, y, height / 2)
    glColor3f(0.9, 0.8, 0.7)
    glScalef(length, thickness, height)
    glutSolidCube(1)
    glPopMatrix()

    step = 60
    count = max(1, int(length / step))
    for i in range(count + 1):
        t = i / count
        x = x1 + t * (x2 - x1)
        glPushMatrix()
        glTranslatef(x, y, height + 10)
        draw_merlon(w=18, d=thickness * 0.8, h=17)
        glPopMatrix()

def draw_wall_sides(y1, y2, x, thickness=30, height=120):
    length = abs(y2 - y1)
    cy = (y1 + y2) / 2.0
    glPushMatrix()
    glTranslatef(x, cy, height / 2)
    glColor3f(0.9, 0.8, 0.7)
    glScalef(thickness, length, height)
    glutSolidCube(1)
    glPopMatrix()

    step = 60
    count = max(1, int(length / step))
    for i in range(count + 1):
        t = i / count
        y = y1 + t * (y2 - y1)
        glPushMatrix()
        glTranslatef(x, y, height + 10)
        draw_merlon(w=18, d=thickness * 0.8, h=17)
        glPopMatrix()

def draw_keep(x=0, y=0, w=140, d=140, h=180):
    glPushMatrix()
    glTranslatef(x, y, h / 2)
    glColor3f(0.68, 0.62, 0.56)
    glScalef(w, d, h)
    glutSolidCube(1)
    glPopMatrix()

    for sx in (-1, 1):
        for sy in (-1, 1):
            glPushMatrix()
            glTranslatef(x + sx * (w / 2 - 15), y + sy * (d / 2 - 15), h + 15)
            draw_merlon(w=26, d=26, h=32, color=(0.55, 0.44, 0.34))
            glPopMatrix()

def draw_castle():
    half = 250
    t = 30
    h = 120

    glPushMatrix()
    glTranslatef(0, -20, 40)
    glColor3f(0.82, 0.50, 0.40)
    glScalef(2 * half + 60, 2 * half + 60, 2)
    glutSolidCube(1)
    glPopMatrix()
    
    draw_wall_back(-half, half, -half, thickness=t, height=h)
    draw_tower(-half, -half, base_r=45, height=200)
    draw_tower(half, -half, base_r=45, height=200)
    draw_keep(-5, 0, w=140, d=140, h=180)
    draw_wall_sides(-half, half, half, thickness=t, height=h)
    draw_wall_sides(-half, half, -half, thickness=t, height=h)
    draw_wall_front(-half, half, half, thickness=t, height=h)
    draw_gatehouse(center_x=0, front_y=half + 40, wall_thickness=t, height=h + 20)
    draw_tower(-half, half+15, base_r=45, height=190)
    draw_tower(half, half+15, base_r=45, height=190)

cloud_positions = []

def init_clouds(num_clouds):
    global cloud_positions
    cloud_positions = []
    for _ in range(num_clouds):
        x = random.randint(-740, 740)
        y = random.randint(-1500, -100)
        z = random.randint(520, 680)
        cloud_positions.append((x, y, z))

def draw_cloud(x, y, z):
    glColor3f(1, 1, 1)
    for dx, dy, dz in [(0,0,0), (20,0,0), (-20,0,0), (10,10,0), (-10,10,0), (0,5,10)]:
        glPushMatrix()
        glTranslatef(x+dx, y+dy, z+dz)
        glScalef(20, 20, 20)
        glutSolidCube(1)
        glPopMatrix()

def draw_clouds():
    for (x, y, z) in cloud_positions:
        draw_cloud(x, y, z)

def draw_grid_and_walls():
    for i in range(23):
        for j in range(23):
            if (i + j) % 2 == 0:
                glColor3f(0.3, 0.6, 0.0)
            else:
                glColor3f(0.13, 0.5, 0.13)
            x = j * tile_size - offset
            y = i * tile_size - offset
            glBegin(GL_QUADS)
            glVertex3f(x, y, 0.0)
            glVertex3f(x + tile_size, y, 0.0)
            glVertex3f(x + tile_size, y + tile_size, 0.0)
            glVertex3f(x, y + tile_size, 0.0)
            glEnd()

    glPushMatrix()
    glTranslatef(-50, -700, 0)
    glScalef(2.0, 2.0, 2.0)
    draw_castle()
    glPopMatrix()

def draw_player_on_keep():
    glPushMatrix()

    glTranslatef(*player_base)
    glRotatef(player_tilt, 1, 0, 0)
    glRotatef(player_angle, 0, 0, 1)
    glRotatef(player_pitch, 1, 0, 0)
    glScalef(player_scale, player_scale, player_scale)

    glPushMatrix()
    glColor3f(0.5, 0.0, 0.0)
    glTranslatef(0, 0, 60)
    glScalef(0.8, 0.4, 2.0)
    glutSolidCube(35)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.2, 0.2, 0.9)
    glTranslatef(-10, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.2, 0.2, 0.9)
    glTranslatef(10, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(0, 0, 90)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 3, 20, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(1.0, 0.8, 0.6)
    glTranslatef(-20, 15, 100)
    glRotatef(-70, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 3, 40, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(1.0, 0.8, 0.6)
    glTranslatef(20, 15, 100)
    glRotatef(-70, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 3, 40, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(0, 0, 118)
    glutSolidSphere(18, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.4, 0.25, 0.1)
    glTranslatef(0, 66, 100)
    glRotatef(180, 0, 0, 1)
    
    glPushMatrix()
    glTranslatef(0, 22, 16)
    glRotatef(70, 1, 0, 0)
    glScalef(2, 22, 2)
    glutSolidCube(2)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 22, -16)
    glRotatef(-70, 1, 0, 0)
    glScalef(2, 22, 2)
    glutSolidCube(2)
    glPopMatrix()
    glPopMatrix()

    glPopMatrix()

def get_bow_world_pos_and_yaw():

    bx, by, bz = bow

    bx *= player_scale
    by *= player_scale
    bz *= player_scale

    tilt = math.radians(player_tilt)
    c = math.cos(tilt)
    s = math.sin(tilt)

    y1 = by * c - bz * s
    z1 = by * s + bz * c
    x1 = bx

    yaw = math.radians(player_angle)
    cy = math.cos(yaw)
    sy = math.sin(yaw)
    x2 = x1 * cy - y1 * sy
    y2 = x1 * sy + y1 * cy

    wx = player_base[0] + x2
    wy = player_base[1] + y2
    wz = player_base[2] + z1

    return wx, wy, wz, player_angle, player_pitch

def draw_arrows():
    global arrows, missed_arrows, game_over
    updated = []
    for (x, y, z, angle_deg, pitch_deg, vz) in arrows:
        speed = 18.0
        rad = math.radians(angle_deg)
        pitch_rad = math.radians(pitch_deg)

        x += speed * math.cos(rad) * math.cos(pitch_rad)
        y += speed * math.sin(rad) * math.cos(pitch_rad)
        z += speed * math.sin(pitch_rad)

        vz -= 0.35
        z += vz - 0.5

        if abs(x) < 4000 and abs(y) < 4000 and z > 0:
            updated.append((x, y, z, angle_deg, pitch_deg, vz))

            glPushMatrix()
            glTranslatef(x, y, z)
            glRotatef(angle_deg - 90, 0, 0, 1)
            glScalef(2.0, 2.0, 2.0)

            glColor3f(0.5, 0.3, 0.1)
            glPushMatrix()
            glScalef(2.0, 30.0, 2.0)
            glutSolidCube(1)
            glPopMatrix()

            glColor3f(0.8, 0.0, 0.0)
            glPushMatrix()
            glTranslatef(0, 16, 0)
            glRotatef(-90, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 2.5, 0.0, 7.0, 10, 1)
            glPopMatrix()

            glColor3f(0.9, 0.9, 0.9)
            glPushMatrix()
            glTranslatef(0, -15, 0)
            glScalef(3.0, 3.0, 1.0)
            glutSolidCube(1)
            glPopMatrix()

            glPopMatrix()
        else:
            missed_arrows += 1
            if missed_arrows >= 40:
                game_over = True

    arrows = updated

enemies = []
def init_enemies(num=5):
    global enemies
    enemies = []
    for _ in range(num):
        spawn_enemy()

def spawn_enemy():
    x = random.randint(-700, 700) 
    y = random.randint(600, 900) 
    z = 0 
    enemies.append([x, y, z])

def draw_enemy(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)

    glColor3f(0.5, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 40)
    glutSolidSphere(35, 25, 25)
    glPopMatrix()

    glColor3f(0.0, 0.3, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 90)
    glutSolidSphere(22, 20, 20)
    glPopMatrix()

    glColor3f(1, 0, 0)
    glPushMatrix()
    glTranslatef(-7, 20, 95)
    glutSolidSphere(4, 12, 12)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(7, 20, 95)
    glutSolidSphere(4, 12, 12)
    glPopMatrix()

    glColor3f(1, 1, 1)
    glPushMatrix()
    glTranslatef(-10, -5, 105)
    glRotatef(-40, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 0.5, 20, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(10, -5, 105)
    glRotatef(-40, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 0.5, 20, 10, 10)
    glPopMatrix()

    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 15, 90)
    glScalef(10, 5, 5)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(1, 1, 1)
    for dx in (-4, 0, 4):
        glPushMatrix()
        glTranslatef(dx, 23, 87)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 1.2, 0.2, 6, 6, 6)
        glPopMatrix()

    glColor3f(0.2, 0.2, 0.2)
    for i in range(5):
        glPushMatrix()
        glTranslatef(0, -25, 60 + i * 15)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 2.5, 0.0, 12, 10, 10)
        glPopMatrix()

    glPopMatrix()

def update_enemies():
    global enemies, castle_health, game_over
    updated = []
    for (x, y, z) in enemies:

        y -= 0.3  
        if y <= -20:
            castle_health -= 1
            if castle_health <= 0:
                game_over = True
            else:
                spawn_enemy()
        else:
            updated.append([x, y, z])

    while len(updated) < 5:
        updated.append(spawn_enemy())

    enemies = updated

def draw_enemies():
    for (x, y, z) in enemies:
        draw_enemy(x, y, z)

fire_particles = []

def init_fire_line(length=400, spacing=20):
    global fire_particles
    fire_particles = []
    for i in range(-length//2, length//2 + 1, spacing):
        fire_particles.append([i, -420, 0, random.uniform(10, 20)])  

def draw_fire_line():
    global fire_particles
    for p in fire_particles:
        x, y, base_z, h = p

        flicker = random.uniform(-3, 3)
        flame_height = h + flicker

        r = 1.0
        g = random.uniform(0.3, 0.7)
        b = 0.0

        glPushMatrix()
        glTranslatef(x, y+400, base_z)

        glColor3f(r, g, b)
        glutSolidSphere(6, 10, 10)

        glTranslatef(0, 0, flame_height * 0.5)
        glColor3f(1.0, g + 0.2, 0.0)
        glutSolidSphere(5, 10, 10)

        glTranslatef(0, 0, flame_height * 0.5)
        glColor3f(1.0, 1.0, 0.2)
        glutSolidSphere(3, 10, 10)

        glPopMatrix()

def check_arrow_enemy_collision():
    global arrows, enemies, kill_count
    updated_arrows = []

    for i in range(len(arrows)):
        ax, ay, az, angle_deg, pitch_deg, vz = arrows[i]

        speed = 18.0
        rad = math.radians(angle_deg)
        pitch_rad = math.radians(pitch_deg)
        prev_x = ax - speed * math.cos(rad) * math.cos(pitch_rad)
        prev_y = ay - speed * math.sin(rad) * math.cos(pitch_rad)
        prev_z = az - speed * math.sin(pitch_rad)

        hit = False
        for enemy in enemies:
            ex, ey, ez = enemy
            cx, cy, cz = ex, ey, ez + 30
            r = 60
            vx, vy, vz_arrow = ax - prev_x, ay - prev_y, az - prev_z
            steps = 5
            for step in range(steps + 1):
                t = step / steps
                px = prev_x + t * vx
                py = prev_y + t * vy
                pz = prev_z + t * vz_arrow

                dx = cx - px
                dy = cy - py
                dz = cz - pz
                if dx*dx + dy*dy + dz*dz < r*r:
                    kill_count += 1
                    enemies.remove(enemy)
                    spawn_enemy()
                    hit = True
                    break

            if hit:
                break

        if not hit:
            updated_arrows.append((ax, ay, az, angle_deg, pitch_deg, vz))

    arrows = updated_arrows

def draw_player_model():

    glPushMatrix()
    glColor3f(0.5, 0.2, 0.8)
    glTranslatef(0, 0, 60)
    glScalef(0.8, 0.4, 2.0)
    glutSolidCube(35)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.2, 0.2, 0.9)
    glTranslatef(-10, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.2, 0.2, 0.9)
    glTranslatef(10, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(0, 0, 90)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 3, 20, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(1.0, 0.8, 0.6)
    glTranslatef(-20, 15, 100)
    glRotatef(-70, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 3, 40, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(1.0, 0.8, 0.6)
    glTranslatef(20, 15, 100)
    glRotatef(-70, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 3, 40, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(0, 0, 118)
    glutSolidSphere(18, 20, 20)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.4, 0.25, 0.1)
    glTranslatef(0, 66, 100)
    glRotatef(180, 0, 0, 1)
    glPushMatrix()
    glTranslatef(0, 22, 16); glRotatef(70, 1, 0, 0); glScalef(2, 22, 2); glutSolidCube(2); glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 22, -16); glRotatef(-70, 1, 0, 0); glScalef(2, 22, 2); glutSolidCube(2); glPopMatrix()
    glPopMatrix()

def draw_god_players():
    if not god_mode: return
    for gp in god_players:
        glPushMatrix()
        glTranslatef(*gp["base"])
        glRotatef(player_tilt, 1, 0, 0)
        glRotatef(gp["angle"], 0, 0, 1)
        glRotatef(gp["pitch"], 1, 0, 0)
        glScalef(0.9, 0.9, 0.9)
        draw_player_model()
        glPopMatrix()

def get_bow_world_pos(base, yaw_deg, pitch_deg, scale=1.0):
    bx, by, bz = bow
    bx *= scale; by *= scale; bz *= scale

    tilt = math.radians(player_tilt)
    c, s = math.cos(tilt), math.sin(tilt)
    y1 = by*c - bz*s
    z1 = by*s + bz*c
    x1 = bx

    yaw = math.radians(yaw_deg)
    cy, sy = math.cos(yaw), math.sin(yaw)
    x2 = x1*cy - y1*sy
    y2 = x1*sy + y1*cy

    wx = base[0] + x2
    wy = base[1] + y2
    wz = base[2] + z1

    return wx, wy, wz, yaw_deg, pitch_deg

def get_bow_world_pos_and_forward():
    bx, by, bz = bow
    bx *= player_scale
    by *= player_scale
    bz *= player_scale

    tilt = math.radians(player_tilt)
    c, s = math.cos(tilt), math.sin(tilt)
    y1 = by * c - bz * s
    z1 = by * s + bz * c
    x1 = bx

    yaw = math.radians(player_angle)
    cy, sy = math.cos(yaw), math.sin(yaw)
    x2 = x1 * cy - y1 * sy
    y2 = x1 * sy + y1 * cy

    wx = player_base[0] + x2
    wy = player_base[1] + y2
    wz = player_base[2] + z1

    fx, fy, fz = 0, 1, 0
    fy_tilt = fy * c - fz * s
    fz_tilt = fy * s + fz * c
    fx_tilt = fx
    fx_world = fx_tilt * cy - fy_tilt * sy
    fy_world = fx_tilt * sy + fy_tilt * cy
    fz_world = fz_tilt

    length = math.sqrt(fx_world**2 + fy_world**2 + fz_world**2)
    fx_world /= length
    fy_world /= length
    fz_world /= length

    return wx, wy, wz, fx_world, fy_world, fz_world

def god_mode_behavior():
    global god_mode_cooldown, god_shooter_index

    if not god_mode or not enemies:
        return

    for gp in god_players:
        gp["angle"] = (gp["angle"] + 1) % 360 

    if god_mode_cooldown > 0:
        god_mode_cooldown -= 1
        return

    shooter = god_players[god_shooter_index]
    sx, sy, sz = shooter["base"]

    target_enemy = None
    min_dist = float("inf")
    for e in enemies:
        dx, dy = e[0] - sx, e[1] - sy
        dist = math.hypot(dx, dy)
        angle_to_enemy = math.degrees(math.atan2(dy, dx)) % 360
        diff = abs((shooter["angle"] % 360) - angle_to_enemy)
        if diff < 5 and dist < min_dist:
            min_dist = dist
            target_enemy = e

    if target_enemy:
        bx, by, bz, yaw, pitch = get_bow_world_pos(
            base=shooter["base"], yaw_deg=shooter["angle"], pitch_deg=shooter["pitch"], scale=0.9
        )
        arrows.append((bx, by, bz, yaw, pitch, 0.8))
        god_mode_cooldown = 30
        god_shooter_index = (god_shooter_index + 1) % len(god_players)

def reset_game():
    global arrows, enemies, kill_count, missed_arrows, castle_health, game_over
    global god_mode, god_players, god_mode_cooldown, god_shooter_index
    global player_angle, player_pitch, player_base
    global first_person, camera_pos

    arrows = []
    enemies = []
    init_enemies(5)

    kill_count = 0
    missed_arrows = 0
    castle_health = 10
    game_over = False

    player_angle = 0
    player_pitch = 0
    player_base = (-55.0, -650.0, 350.0)

    god_mode = False
    god_players = []
    god_mode_cooldown = 0
    god_shooter_index = 0      

    first_person = False
    camera_pos = (0, 500, 500) 

def keyboardListener(key, x, y):
    global player_angle, player_pitch, god_mode, god_players
    if key == b'd':
        player_angle += 5
    elif key == b'a':
        player_angle -= 5
    elif key == b'w':
        player_pitch = min(player_pitch + 5, 45)
    elif key == b's':
        player_pitch = max(player_pitch - 5, -45)
    elif key == b'g':
        god_mode = not god_mode
        if god_mode:
            god_players = [
                {"base": (-550.0, -200.0, 380.0),
                "angle": 0, "pitch": 0},
                {"base": (450.0, -200.0, 380.0),
                "angle": 0, "pitch": 0}
            ]
        else:
            god_players = []
    elif key == b'r':
        reset_game()

def specialKeyListener(key, x, y):
    global camera_pos
    x0, y0, z0 = camera_pos
    if key == GLUT_KEY_LEFT: x0 += 10
    if key == GLUT_KEY_RIGHT: x0 -= 10
    if key == GLUT_KEY_UP: y0 -= 10
    if key == GLUT_KEY_DOWN: y0 += 10
    camera_pos = (x0, y0, z0)

def mouseListener(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        bx, by, bz, yaw_deg, pitch_deg = get_bow_world_pos_and_yaw()
        arrows.append((bx, by, bz, yaw_deg+90, pitch_deg, 0.8))
    global first_person
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person
        glutPostRedisplay()

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1000/800, 0.1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if first_person:
        bx, by, bz, fx, fy, fz = get_bow_world_pos_and_forward()
        cam_back = 50
        cam_up   = 200
        eye_x = bx - cam_back * fx
        eye_y = by - cam_back * fy
        eye_z = bz + cam_up

        center_x = bx + 1000 * fx
        center_y = by + 1000 * fy
        center_z = bz + 1000 * fz

        gluLookAt(eye_x, eye_y, eye_z,
                  center_x, center_y, center_z,
                  0, 0, 1)
    else:
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

def idle():
    global sky_time
    sky_time += sky_speed
    if sky_time > 1.0:
        sky_time -= 1.0
    glutPostRedisplay()

def showScreen():
    r = 0.5 + 0.3 * math.sin(2 * math.pi * sky_time)
    g = 0.8 + 0.1 * math.sin(2 * math.pi * sky_time)
    b = 0.9 + 0.1 * math.sin(2 * math.pi * sky_time)
    glClearColor(r, g, b, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    
    if game_over:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_text(400+30, 400+60, "GAME OVER", GLUT_BITMAP_HELVETICA_18)
        draw_text(400+30, 360+60, f"Kills: {kill_count}")
        draw_text(400+30, 330+60, f"Missed Arrows: {missed_arrows}")
        draw_text(400+30, 300+60, f"Castle Health: {castle_health}")
        draw_text(400+30, 270+60, f"PRESS 'R' TO RESTART")
        glutSwapBuffers()
        return
    
    draw_grid_and_walls()
    draw_player_on_keep()
    draw_god_players()
    god_mode_behavior()
    check_arrow_enemy_collision()
    draw_arrows()
    update_enemies()
    draw_fire_line()
    draw_enemies()
    draw_clouds()
    draw_text(15, 760, f"Kills: {kill_count}")
    draw_text(15, 740, f"Castle Health: {castle_health}")
    draw_text(15, 720, f"Missed: {missed_arrows}/40")

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Castle Defense 3D")
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glClearColor(0.5, 0.81, 0.9, 1.0)
    init_clouds(15)
    init_enemies(5)
    init_fire_line(2280, 10)
    glutMainLoop()

if __name__ == "__main__":
    main()