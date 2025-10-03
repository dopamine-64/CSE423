from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

camera_pos = (0, 500, 500)
fovY = 120
tile_size = 100
offset = (12.7 * tile_size) / 2

player_x = 0
player_y = 0
player_speed = 35
player_angle = 0 

player_vel_x = 0
player_vel_y = 0
acceleration = 5
friction = 0.9

player_life = 5
score = 0
bullets_missed = 0
game_over = False
game_over_reason = ""  

enemy_count = 5
enemy_positions = []
enemy_min_distance = 100  
enemy_speed = 0.4

enemy_scale = 1.0
scale_growing = True

def spawn_initial_enemies():
    global enemy_positions
    enemy_positions = []
    for _ in range(enemy_count):
        ex = random.randint(-int(offset) + 50, int(offset) - 50)
        ey = random.randint(-int(offset) + 50, int(offset) - 50)
        enemy_positions.append([ex, ey])

def random_spawn_point(min_dist_from_player=150):
    grid_min = -offset + 50
    grid_max = -offset + 13 * tile_size - 50
    for _ in range(100):
        rx = random.randint(int(grid_min), int(grid_max))
        ry = random.randint(int(grid_min), int(grid_max))
        if math.hypot(rx - player_x, ry - player_y) >= min_dist_from_player:
            return [rx, ry]
    return [grid_min, grid_min]

spawn_initial_enemies()

bullets = []
bullet_speed = 25.0
bullet_size = 10.0
bullet_max_dist = 100000.0

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
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

def within_grid(x, y, pad=0.0):
    grid_min = -offset + pad
    grid_max = -offset + 13 * tile_size - pad
    return (grid_min <= x <= grid_max) and (grid_min <= y <= grid_max)

def draw_player():
    glPushMatrix()
    glTranslatef(player_x, player_y, 0)

    if game_over:
        glRotatef(90, 0, -1, 0) 
    else:
        glRotatef(player_angle, 0, 0, 1)

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
    glColor3f(0.0, 0.5, 0.0)
    glTranslatef(0, 0, 75)
    glScalef(0.8, 0.4, 2.0)
    glutSolidCube(30)
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(0, 0, 90)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 3, 80, 20, 20)
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(1.0, 0.8, 0.6)
    glTranslatef(-20, 10, 100)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 8, 3, 40, 20, 20)
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(1.0, 0.8, 0.6)
    glTranslatef(20, 10, 100)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 8, 3, 40, 20, 20)
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(0, 0, 120)
    glutSolidSphere(22, 20, 20)
    glPopMatrix()

    glPopMatrix()

def draw_enemies():
    global enemy_scale
    for (ex, ey) in enemy_positions:
        
        glPushMatrix()
        glTranslatef(ex, ey, 0)
        glScalef(enemy_scale, enemy_scale, 1.0)
        glColor3f(1.0, 0.0, 0.0)
        glutSolidSphere(40, 20, 20)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(ex, ey, 40)
        glScalef(enemy_scale, enemy_scale, 1.0)
        glColor3f(0.0, 0.0, 0.0)
        glutSolidSphere(24, 20, 20)
        glPopMatrix()

def draw_bullets():
    for b in bullets:
        glPushMatrix()
        glTranslatef(b["x"], b["y"], 95)
        glColor3f(1.0, 0.0, 0.0)
        glutSolidCube(bullet_size)
        glPopMatrix()

def draw_grid_and_walls():
    total_size = 13 * tile_size
    wall_height = 100

    for i in range(13):
        for j in range(13):
            if (i + j) % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)
            else:
                glColor3f(0.6, 0.4, 0.8)
            x = j * tile_size - offset
            y = i * tile_size - offset
            glBegin(GL_QUADS)
            glVertex3f(x, y, 0.0)
            glVertex3f(x + tile_size, y, 0.0)
            glVertex3f(x + tile_size, y + tile_size, 0.0)
            glVertex3f(x, y + tile_size, 0.0)
            glEnd()

    left = -offset
    right = -offset + total_size
    bottom = -offset
    top = -offset + total_size

    glColor3f(0.3, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(left, bottom, 0.0)
    glVertex3f(right, bottom, 0.0)
    glVertex3f(right, bottom, wall_height)
    glVertex3f(left, bottom, wall_height)
    glEnd()

    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(right, bottom, 0.0)
    glVertex3f(right, top, 0.0)
    glVertex3f(right, top, wall_height)
    glVertex3f(right, bottom, wall_height)
    glEnd()
    
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(right, top, 0.0)
    glVertex3f(left, top, 0.0)
    glVertex3f(left, top, wall_height)
    glVertex3f(right, top, wall_height)
    glEnd()
    
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(left, top, 0.0)
    glVertex3f(left, bottom, 0.0)
    glVertex3f(left, bottom, wall_height)
    glVertex3f(left, top, wall_height)
    glEnd()

def move_enemies():
    global enemy_positions, player_life, game_over, game_over_reason
    if game_over:
        return

    grid_min = -offset
    grid_max = -offset + 13 * tile_size

    for i in range(len(enemy_positions)):
        ex, ey = enemy_positions[i]

        dx = player_x - ex
        dy = player_y - ey
        dist_to_player = math.hypot(dx, dy)
        if dist_to_player > enemy_min_distance:
            ex += (dx / dist_to_player) * enemy_speed
            ey += (dy / dist_to_player) * enemy_speed

        for j in range(len(enemy_positions)):
            if i == j:
                continue
            ox, oy = enemy_positions[j]
            dx2 = ex - ox
            dy2 = ey - oy
            dist = math.hypot(dx2, dy2)
            if dist < enemy_min_distance and dist != 0:
                push = (enemy_min_distance - dist) / 2.0
                ex += (dx2 / dist) * push
                ey += (dy2 / dist) * push

        ex = max(grid_min + 30, min(ex, grid_max))
        ey = max(grid_min + 30, min(ey, grid_max))

        if not game_over and math.hypot(ex - player_x, ey - player_y) < 100:
            player_life = max(0, player_life - 1)
            enemy_positions[i] = random_spawn_point(min_dist_from_player=150)
            if player_life <= 0:
                set_game_over("life")
            continue

        enemy_positions[i] = [ex, ey]

def set_game_over(reason):
    global game_over, game_over_reason
    game_over = True
    game_over_reason = reason

def update_enemy_scale():
    global enemy_scale, scale_growing
    if game_over:
        return
    if scale_growing:
        enemy_scale += 0.01
        if enemy_scale >= 1.5:
            scale_growing = False
    else:
        enemy_scale -= 0.01
        if enemy_scale <= 1.0:
            scale_growing = True

def fire_bullet():
    if game_over:
        return
    rad = math.radians(player_angle)
    dir_x = math.sin(-rad)
    dir_y = math.cos(rad)

    muzzle_offset = 60
    bx = player_x + dir_x * muzzle_offset
    by = player_y + dir_y * muzzle_offset
    if not within_grid(bx, by, pad=20):
        bx, by = player_x, player_y

    bullets.append({
        "x": bx,
        "y": by,
        "dx": dir_x * bullet_speed,
        "dy": dir_y * bullet_speed,
        "dist": 0.0
    })

def update_bullets_and_collisions():
    global bullets, enemy_positions, score, bullets_missed, cheat_bullet_ready
    if game_over:
        return

    new_bullets = []
    for b in bullets:
        b["x"] += b["dx"]
        b["y"] += b["dy"]
        step_dist = math.hypot(b["dx"], b["dy"])
        b["dist"] += step_dist

        if not within_grid(b["x"], b["y"], pad=0) or b["dist"] > bullet_max_dist:
            bullets_missed += 1
            cheat_bullet_ready = True 
            if bullets_missed >= 10:
                set_game_over("miss")
            continue

        hit_index = -1
        for i, (ex, ey) in enumerate(enemy_positions):
            if math.hypot(b["x"] - ex, b["y"] - ey) <= 45:
                hit_index = i
                break

        if hit_index != -1:
            score += 1
            enemy_positions[hit_index] = random_spawn_point(min_dist_from_player=150)
            cheat_bullet_ready = True  
            continue 

        new_bullets.append(b)

    bullets = new_bullets

cheat_mode = False 
auto_cam_follow = False
cheat_rotation_speed = 5
cheat_bullet_ready = True 
aim_tolerance_deg = 2.0 

def keyboardListener(key, x, y):
    global player_vel_x, player_vel_y, player_angle
    global cheat_mode, auto_cam_follow

    if game_over:
        if key in (b'R', b'r'):
            reset_game()
        return

    rad = math.radians(player_angle)

    if key == b'w':
        player_vel_x += math.sin(-rad) * acceleration
        player_vel_y += math.cos(rad) * acceleration
    elif key == b's':
        player_vel_x -= math.sin(-rad) * acceleration
        player_vel_y -= math.cos(rad) * acceleration
    elif key == b'd':
        player_angle -= 15
    elif key == b'a':
        player_angle += 15
    elif key in (b'R', b'r'):
        reset_game()
    elif key in (b'C', b'c'):
        cheat_mode = not cheat_mode
    elif key in (b'V', b'v'): 
        auto_cam_follow = not auto_cam_follow

def cheat_mode_behavior():
    global player_angle, cheat_bullet_ready

    if not enemy_positions:
        return

    player_angle += 5 
    player_angle %= 360

    if not cheat_bullet_ready:
        return  

    target_enemy = None
    min_dist = float('inf')
    for i in range(len(enemy_positions)):
        e = enemy_positions[i]
        dx = e[0] - player_x
        dy = e[1] - player_y
        dist = math.hypot(dx, dy)

        angle_to_enemy = math.degrees(math.atan2(-dx, dy)) % 360
        diff = abs(player_angle - angle_to_enemy)
        if diff > 180:
            diff = 360 - diff

        if diff < 5 and dist < min_dist:
            min_dist = dist
            target_enemy = e

    if target_enemy:
        fire_bullet()
        cheat_bullet_ready = False

def specialKeyListener(key, x, y):
    global camera_pos
    cx, cy, cz = camera_pos
    if key == GLUT_KEY_UP:
        cz += 10
    if key == GLUT_KEY_DOWN:
        cz -= 10
    if key == GLUT_KEY_LEFT:
        cx -= 10
    if key == GLUT_KEY_RIGHT:
        cx += 10
    camera_pos = (cx, cy, cz)

def mouseListener(button, state, x, y):
    global first_person
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_bullet()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person = not first_person

def reset_game():
    global player_x, player_y, player_vel_x, player_vel_y, player_angle
    global player_life, score, bullets_missed, bullets
    global game_over, game_over_reason, cheat_bullet_ready
    global enemy_scale, scale_growing
    global first_person, camera_pos
    global cheat_mode, auto_cam_follow

    player_x = 0
    player_y = 0
    player_vel_x = 0
    player_vel_y = 0
    player_angle = 0

    player_life = 5
    score = 0
    bullets_missed = 0
    bullets = []

    game_over = False
    game_over_reason = ""

    enemy_scale = 1.0
    scale_growing = True
    spawn_initial_enemies()

    first_person = False
    camera_pos = (0, 500, 500)

    cheat_mode = False
    auto_cam_follow = False
    cheat_bullet_ready = True


first_person = False
def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    x, y, z = camera_pos

    if first_person:
        rad = math.radians(player_angle)
        cam_x = player_x
        cam_y = player_y
        cam_z = 175 
        look_x = player_x + math.sin(-rad) * 100
        look_y = player_y + math.cos(rad) * 100
        look_z = cam_z
        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 0, 1)

    elif cheat_mode and auto_cam_follow:
        cam_x, cam_y, cam_z = 40, 20, 160
        look_x, look_y, look_z = -20, -20, 150
        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 0, 1)

    else: 
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

def idle():
    global player_x, player_y, player_vel_x, player_vel_y

    if not game_over:
        player_x += player_vel_x
        player_y += player_vel_y
        player_vel_x *= friction
        player_vel_y *= friction

        if cheat_mode:
            cheat_mode_behavior()
    else:
        player_vel_x = 0
        player_vel_y = 0


    grid_min = -offset
    grid_max = -offset + 13 * tile_size

    if player_x < grid_min + 20:
        player_x = grid_min + 20
        player_vel_x = 0
    elif player_x > grid_max - 10:
        player_x = grid_max - 10
        player_vel_x = 0

    if player_y < grid_min + 20:
        player_y = grid_min + 20
        player_vel_y = 0
    elif player_y > grid_max - 10:
        player_y = grid_max - 10
        player_vel_y = 0

    move_enemies()
    update_enemy_scale()
    update_bullets_and_collisions()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    draw_grid_and_walls()

    if not game_over:
        draw_text(15, 770, f"Player Life Remaining: {player_life}")
        draw_text(15, 740, f"Game Score: {score}")
        draw_text(15, 710, f"Bullets Missed: {bullets_missed} / 10")
    else:
        draw_text(15, 770, "GAME OVER")
        reason = "You ran out of lives!" if game_over_reason == "life" else "You missed 10 bullets!"
        draw_text(15, 740, reason)
        draw_text(15, 710, "Press 'R' to Restart")

    draw_enemies()
    draw_player()
    draw_bullets()

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy 3D")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()