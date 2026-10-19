# tank1990.v1.0
# File: tank1990.v1.py
# Date: 2026-06-10
# Python: Python 3.14.0
# Requirement with Python: pygame-ce
# Tested with: Python 3.14.0 & pygame-ce
# Environment: Local Python interpreter, no virtual environment
# Purpose: Create bot, play with bot, and two-player game

import pygame
import sys
import math
import random
from enum import Enum

# ─── Constants ───────────────────────────────────────────────────────────────
TILE      = 32
COLS      = 26
ROWS      = 24
HUD_W     = 160
WIN_W     = COLS * TILE + HUD_W
WIN_H     = ROWS * TILE
FPS       = 60

# Colors
C_BG       = (30,  30,  30)
C_BRICK    = (180, 80,  30)
C_BRICK_D  = (120, 50,  15)
C_STEEL    = (160, 160, 175)
C_STEEL_D  = (100, 100, 115)
C_FORT     = (200, 160, 40)
C_FORT_D   = (140, 110, 20)
C_GOLD     = (240, 200, 40)
C_SILVER   = (190, 190, 210)
C_RED      = (220, 60,  60)
C_GREEN    = (60,  200, 80)
C_WHITE    = (255, 255, 255)
C_BLACK    = (0,   0,   0)
C_DARK     = (20,  20,  20)
C_YELLOW   = (255, 230, 50)
C_ORANGE   = (255, 140, 0)
C_GRAY     = (100, 100, 110)
C_MENU_BG  = (15,  15,  20)
C_HUD_BG   = (18,  18,  24)

# Directions: 0=Up 1=Right 2=Down 3=Left
DIR_VEC = [(0,-1),(1,0),(0,1),(-1,0)]

# Tile types
T_EMPTY  = 0
T_BRICK  = 1
T_STEEL  = 2
T_FORT   = 3

class GameMode(Enum):
    MENU    = "menu"
    PLAY    = "play"
    GAMEOVER= "gameover"


# ─── Map builder ─────────────────────────────────────────────────────────────
BASE_MAP = [
    "                          ",
    " ##  ##  ##  ## ##  ##  ##",
    " ##  ##  ##     ##  ##  ##",
    " ##  ##  ##  ## ##  ##  ##",
    "                          ",
    " ## S##  ##  ## ##  ##S ##",
    " ##  ##  ##  ## ##  ##  ##",
    " ##  ##  ##  ## ##  ##  ##",
    "                          ",
    " ##  ##  ##  ## ##  ##  ##",
    " ##  ##  ##  ## ##  ##  ##",
    " ##  ##SS ##  ## ##S ##  ##",
    "            ##            ",
    " ##  ##  ## ## ##  ##  ## ",
    " ##  ##  ##    ##  ##  ## ",
    " ##  ##  ## ## ##  ##  ## ",
    "                          ",
    " ##  ##  ##  ## ##  ##  ##",
    " ##  ##  ##  ## ##  ##  ##",
    " ##  ##SS ##  ## ##S ##  ##",
    "                          ",
    " ##  ##  ##  ## ##  ##  ##",
    "          #FFF#           ",
    "          #FFF#           ",
]

def build_map():
    grid = []
    for row_str in BASE_MAP:
        row = []
        for ch in row_str.ljust(COLS)[:COLS]:
            if ch == '#':   row.append(T_BRICK)
            elif ch == 'S': row.append(T_STEEL)
            elif ch == 'F': row.append(T_FORT)
            else:           row.append(T_EMPTY)
        grid.append(row)
    while len(grid) < ROWS:
        grid.append([T_EMPTY]*COLS)
    return grid


# ─── Drawing helpers ─────────────────────────────────────────────────────────
def draw_brick(surf, rx, ry):
    pygame.draw.rect(surf, C_BRICK, (rx, ry, TILE, TILE))
    # Brick pattern
    for row in range(2):
        y0 = ry + row * 16
        for col in range(3):
            offset = 8 if row % 2 else 0
            x0 = rx + col * 11 - 3 + offset
            pygame.draw.rect(surf, C_BRICK_D, (x0+1, y0+1, 9, 6))

def draw_steel(surf, rx, ry):
    pygame.draw.rect(surf, C_STEEL, (rx, ry, TILE, TILE))
    pygame.draw.rect(surf, C_STEEL_D, (rx, ry, TILE//2, TILE//2))
    pygame.draw.rect(surf, C_STEEL_D, (rx+TILE//2, ry+TILE//2, TILE//2, TILE//2))
    pygame.draw.rect(surf, C_WHITE,   (rx+2, ry+2, 5, 5))

def draw_fort(surf, rx, ry):
    pygame.draw.rect(surf, C_FORT, (rx, ry, TILE, TILE))
    # Eagle silhouette
    pygame.draw.rect(surf, C_FORT_D, (rx+8, ry+6, 16, 14))
    pygame.draw.rect(surf, C_FORT_D, (rx+6, ry+10, 20, 8))
    pygame.draw.rect(surf, C_YELLOW, (rx+13, ry+8, 6, 5))

def draw_fort_dead(surf, rx, ry):
    pygame.draw.rect(surf, (60,30,10), (rx, ry, TILE, TILE))
    pygame.draw.line(surf, C_RED, (rx+4,ry+4), (rx+TILE-4,ry+TILE-4), 3)
    pygame.draw.line(surf, C_RED, (rx+TILE-4,ry+4), (rx+4,ry+TILE-4), 3)

def draw_tank(surf, x, y, direction, color, is_player=True):
    """Pixel-art style tank"""
    cx, cy = x + TILE//2, y + TILE//2

    body_color  = color
    tread_color = tuple(max(0,c-60) for c in color)
    barrel_col  = tuple(max(0,c-30) for c in color)

    # Treads (two rectangles on sides)
    if direction in (0, 2):  # vertical
        pygame.draw.rect(surf, tread_color, (x+2,  y+2,  7, TILE-4))
        pygame.draw.rect(surf, tread_color, (x+TILE-9, y+2, 7, TILE-4))
        # Tread lines
        for i in range(4):
            yy = y + 4 + i*7
            pygame.draw.line(surf, body_color, (x+2,yy), (x+8,yy), 1)
            pygame.draw.line(surf, body_color, (x+TILE-9,yy), (x+TILE-3,yy), 1)
        # Body
        pygame.draw.rect(surf, body_color, (x+9, y+6, TILE-18, TILE-12))
        # Turret
        pygame.draw.rect(surf, body_color, (x+11, y+9, TILE-22, TILE-18))
        # Barrel
        if direction == 0:
            pygame.draw.rect(surf, barrel_col, (cx-3, y, 6, 14))
        else:
            pygame.draw.rect(surf, barrel_col, (cx-3, y+TILE-14, 6, 14))
    else:  # horizontal
        pygame.draw.rect(surf, tread_color, (x+2, y+2,  TILE-4, 7))
        pygame.draw.rect(surf, tread_color, (x+2, y+TILE-9, TILE-4, 7))
        for i in range(4):
            xx = x + 4 + i*7
            pygame.draw.line(surf, body_color, (xx,y+2), (xx,y+8), 1)
            pygame.draw.line(surf, body_color, (xx,y+TILE-9), (xx,y+TILE-3), 1)
        pygame.draw.rect(surf, body_color, (x+6, y+9, TILE-12, TILE-18))
        pygame.draw.rect(surf, body_color, (x+9, y+11, TILE-18, TILE-22))
        if direction == 1:
            pygame.draw.rect(surf, barrel_col, (x+TILE-14, cy-3, 14, 6))
        else:
            pygame.draw.rect(surf, barrel_col, (x, cy-3, 14, 6))

    # Star on player tanks
    if is_player:
        pygame.draw.circle(surf, C_WHITE, (cx, cy), 3)

def draw_explosion(surf, particles):
    for p in particles:
        alpha = int(255 * (p['life'] / p['max_life']))
        color = (min(255, p['color'][0]), min(255, p['color'][1]), 0)
        r = max(1, int(p['r'] * p['life'] / p['max_life']))
        pygame.draw.circle(surf, color, (int(p['x']), int(p['y'])), r)


# ─── Entities ─────────────────────────────────────────────────────────────────
class Bullet:
    SPEED = 6
    def __init__(self, x, y, direction, owner):
        self.x, self.y = float(x), float(y)
        self.dir = direction
        self.owner = owner   # 'p1', 'p2', 'enemy'
        self.alive = True
        dx, dy = DIR_VEC[direction]
        self.vx, self.vy = dx * self.SPEED, dy * self.SPEED
        self.w = self.h = 6

    def update(self, grid):
        self.x += self.vx
        self.y += self.vy
        # Border
        if self.x < 0 or self.x > COLS*TILE or self.y < 0 or self.y > ROWS*TILE:
            self.alive = False
            return
        # Tile collision
        for corner in [(self.x, self.y),(self.x+self.w,self.y),
                       (self.x,self.y+self.h),(self.x+self.w,self.y+self.h)]:
            tx, ty = int(corner[0]//TILE), int(corner[1]//TILE)
            if 0 <= tx < COLS and 0 <= ty < ROWS:
                t = grid[ty][tx]
                if t == T_BRICK:
                    grid[ty][tx] = T_EMPTY
                    self.alive = False
                    return
                elif t == T_STEEL:
                    self.alive = False
                    return
                elif t == T_FORT:
                    grid[ty][tx] = T_EMPTY
                    self.alive = False
                    return

    def draw(self, surf):
        if not self.alive: return
        color = C_YELLOW if self.owner != 'enemy' else C_RED
        pygame.draw.rect(surf, color, (int(self.x), int(self.y), self.w, self.h))
        pygame.draw.rect(surf, C_WHITE, (int(self.x)+1, int(self.y)+1, 3, 3))


class Tank:
    SPEED = 2

    def __init__(self, x, y, color, player_id):
        self.start_x, self.start_y = float(x), float(y)
        self.x, self.y = float(x), float(y)
        self.dir = 0
        self.color = color
        self.player_id = player_id  # 'p1','p2','enemy'
        self.alive = True
        self.shoot_cooldown = 0
        self.move_cooldown  = 0
        self.w = self.h = TILE - 2
        self.lives = 3 if player_id in ('p1','p2') else 1

    def respawn(self):
        self.x, self.y = self.start_x, self.start_y
        self.alive = True
        self.shoot_cooldown = 90

    def can_shoot(self):
        return self.shoot_cooldown <= 0

    def shoot(self):
        if not self.can_shoot(): return None
        self.shoot_cooldown = 25
        dx, dy = DIR_VEC[self.dir]
        bx = self.x + self.w//2 - 3 + dx * (TILE//2)
        by = self.y + self.h//2 - 3 + dy * (TILE//2)
        return Bullet(bx, by, self.dir, self.player_id)

    def move(self, direction, grid):
        self.dir = direction
        dx, dy = DIR_VEC[direction]
        nx = self.x + dx * self.SPEED
        ny = self.y + dy * self.SPEED
        if self._can_move(nx, ny, grid):
            self.x, self.y = nx, ny
            # Snap to grid for clean movement
            if dx == 0:
                self.x = round(self.x / (TILE//2)) * (TILE//2)
            else:
                self.y = round(self.y / (TILE//2)) * (TILE//2)

    def _can_move(self, nx, ny, grid):
        margin = 2
        for cx, cy in [(nx+margin, ny+margin),
                       (nx+self.w-margin, ny+margin),
                       (nx+margin, ny+self.h-margin),
                       (nx+self.w-margin, ny+self.h-margin)]:
            tx, ty = int(cx // TILE), int(cy // TILE)
            if not (0 <= tx < COLS and 0 <= ty < ROWS):
                return False
            if grid[ty][tx] in (T_BRICK, T_STEEL, T_FORT):
                return False
        return True

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def draw(self, surf):
        if not self.alive: return
        is_p = self.player_id in ('p1', 'p2')
        draw_tank(surf, int(self.x), int(self.y), self.dir, self.color, is_p)


# ─── Bot AI ──────────────────────────────────────────────────────────────────
class BotAI:
    """Simple rule-based AI — no ML/API"""
    def __init__(self, tank):
        self.tank = tank
        self.think_timer  = 0
        self.move_dir     = 2   # start moving down
        self.stuck_timer  = 0
        self.last_pos     = (tank.x, tank.y)
        self.patrol_timer = 0
        self.target_dir   = None

    def _manhattan(self, ax, ay, bx, by):
        return abs(ax-bx) + abs(ay-by)

    def _dir_toward(self, tx, ty, ex, ey):
        """Best direction from enemy to target"""
        dx, dy = tx - ex, ty - ey
        if abs(dx) > abs(dy):
            return 1 if dx > 0 else 3
        else:
            return 2 if dy > 0 else 0

    def _line_of_sight(self, grid, targets):
        """Check if we can shoot at any target in current direction"""
        t = self.tank
        dx, dy = DIR_VEC[t.dir]
        cx, cy = t.x + TILE//2, t.y + TILE//2
        for step in range(1, COLS):
            cx2, cy2 = cx + dx*TILE*step//2, cy + dy*TILE*step//2
            tx2, ty2 = int(cx2//TILE), int(cy2//TILE)
            if not (0 <= tx2 < COLS and 0 <= ty2 < ROWS): break
            if grid[ty2][tx2] in (T_STEEL,): break
            if grid[ty2][tx2] == T_BRICK: break
            for target in targets:
                if target.alive:
                    tr = target.rect()
                    if tr.collidepoint(cx2, cy2):
                        return True
        return False

    def update(self, grid, player_tanks, bullets):
        t = self.tank
        if not t.alive: return None

        self.think_timer  -= 1
        self.patrol_timer -= 1

        # ── Stuck detection ──────────────────────────────
        if abs(t.x - self.last_pos[0]) < 1 and abs(t.y - self.last_pos[1]) < 1:
            self.stuck_timer += 1
        else:
            self.stuck_timer = 0
        self.last_pos = (t.x, t.y)

        if self.stuck_timer > 30:
            self.move_dir = random.randint(0, 3)
            self.stuck_timer = 0

        # ── Choose movement direction periodically ────────
        if self.think_timer <= 0:
            self.think_timer = random.randint(30, 80)

            # Find nearest living player
            living = [p for p in player_tanks if p.alive]
            if living:
                nearest = min(living, key=lambda p: self._manhattan(
                    p.x, p.y, t.x, t.y))
                dist = self._manhattan(nearest.x, nearest.y, t.x, t.y)
                if dist < 8 * TILE:
                    # Chase player
                    self.move_dir = self._dir_toward(nearest.x, nearest.y, t.x, t.y)
                else:
                    # Random patrol
                    if self.patrol_timer <= 0:
                        self.patrol_timer = random.randint(60, 120)
                        self.move_dir = random.choice([0,1,2,3])

        # ── Move ─────────────────────────────────────────
        t.move(self.move_dir, grid)
        if t.shoot_cooldown > 0:
            t.shoot_cooldown -= 1

        # ── Shoot ────────────────────────────────────────
        living = [p for p in player_tanks if p.alive]
        if living and t.can_shoot():
            # Aim at nearest player's row/column
            nearest = min(living, key=lambda p: self._manhattan(
                p.x, p.y, t.x, t.y))
            # Check alignment
            aligned_h = abs(t.y - nearest.y) < TILE
            aligned_v = abs(t.x - nearest.x) < TILE
            if aligned_h:
                t.dir = 1 if nearest.x > t.x else 3
            elif aligned_v:
                t.dir = 2 if nearest.y > t.y else 0

            if (aligned_h or aligned_v) and self._line_of_sight(grid, living):
                return t.shoot()
            # Random shoot toward fort
            elif random.random() < 0.005:
                return t.shoot()

        return None


# ─── Explosion particles ──────────────────────────────────────────────────────
def spawn_explosion(cx, cy, big=False):
    particles = []
    count = 20 if big else 12
    for _ in range(count):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1, 4 if big else 3)
        particles.append({
            'x': float(cx), 'y': float(cy),
            'vx': math.cos(angle)*speed,
            'vy': math.sin(angle)*speed,
            'r': random.randint(3, 8 if big else 5),
            'life': random.randint(15, 35),
            'max_life': 35,
            'color': random.choice([(255,200,0),(255,120,0),(255,60,0)]),
        })
    return particles


# ─── HUD ──────────────────────────────────────────────────────────────────────
def draw_hud(surf, font, small_font, game):
    ox = COLS * TILE
    pygame.draw.rect(surf, C_HUD_BG, (ox, 0, HUD_W, WIN_H))
    pygame.draw.line(surf, C_GRAY, (ox, 0), (ox, WIN_H), 2)

    y = 16
    # Title
    t = font.render("TANK", True, C_YELLOW)
    surf.blit(t, (ox + HUD_W//2 - t.get_width()//2, y))
    y += 28
    t2 = small_font.render("BATTLE", True, C_ORANGE)
    surf.blit(t2, (ox + HUD_W//2 - t2.get_width()//2, y))
    y += 24

    pygame.draw.line(surf, C_GRAY, (ox+10, y), (ox+HUD_W-10, y), 1)
    y += 10

    # Player lives
    for pid, color, label, keys in [
        ('p1', C_GOLD,   "P1",  "WASD+F"),
        ('p2', C_SILVER, "P2",  "Arrows+/"),
    ]:
        tank = game.players.get(pid)
        if tank is None: continue
        lbl = font.render(label, True, color)
        surf.blit(lbl, (ox+12, y))
        # Lives
        for i in range(tank.lives):
            draw_tank(surf, ox+70+i*22, y-4, 0, color, True)
        y += 28
        k = small_font.render(keys, True, C_GRAY)
        surf.blit(k, (ox+12, y))
        y += 20

    pygame.draw.line(surf, C_GRAY, (ox+10, y), (ox+HUD_W-10, y), 1)
    y += 10

    # Enemy count
    alive_e = sum(1 for e in game.enemies if e.alive)
    e_lbl = font.render("ENEMIES", True, C_RED)
    surf.blit(e_lbl, (ox + HUD_W//2 - e_lbl.get_width()//2, y))
    y += 24
    for i in range(len(game.enemies)):
        ex = ox + 14 + (i % 4) * 34
        ey = y + (i // 4) * 24
        color = C_RED if game.enemies[i].alive else C_GRAY
        draw_tank(surf, ex, ey, 2, color, False)
    y += ((len(game.enemies)-1)//4 + 1) * 24 + 6

    pygame.draw.line(surf, C_GRAY, (ox+10, y), (ox+HUD_W-10, y), 1)
    y += 10

    # Score
    s_lbl = font.render("SCORE", True, C_WHITE)
    surf.blit(s_lbl, (ox + HUD_W//2 - s_lbl.get_width()//2, y))
    y += 24
    s_val = font.render(str(game.score), True, C_YELLOW)
    surf.blit(s_val, (ox + HUD_W//2 - s_val.get_width()//2, y))
    y += 28

    # Stage
    st = small_font.render(f"Stage {game.stage}", True, C_GRAY)
    surf.blit(st, (ox + HUD_W//2 - st.get_width()//2, y))


# ─── Menu Screen ──────────────────────────────────────────────────────────────
def draw_menu(surf, font, big_font, small_font, selected, blink):
    surf.fill(C_MENU_BG)

    # Title
    title = big_font.render("TANK BATTLE", True, C_YELLOW)
    surf.blit(title, (WIN_W//2 - title.get_width()//2, 80))
    sub = font.render("1990 EDITION", True, C_ORANGE)
    surf.blit(sub, (WIN_W//2 - sub.get_width()//2, 128))

    # Decorative tanks
    draw_tank(surf, WIN_W//2 - 120, 170, 2, C_GOLD,   True)
    draw_tank(surf, WIN_W//2 + 90,  170, 2, C_SILVER, True)

    # Menu items
    options = ["1 PLAYER", "2 PLAYERS"]
    for i, opt in enumerate(options):
        color = C_WHITE if i == selected else C_GRAY
        lbl = font.render(opt, True, color)
        x = WIN_W//2 - lbl.get_width()//2
        y = 260 + i * 56
        surf.blit(lbl, (x, y))
        if i == selected and blink:
            arr = font.render(">", True, C_YELLOW)
            surf.blit(arr, (x - 30, y))
            arr2 = font.render("<", True, C_YELLOW)
            surf.blit(arr2, (x + lbl.get_width() + 12, y))

    # Controls
    ctrl_y = 420
    ctrls = [
        ("P1 Controls:", "W/A/S/D = Move,  F = Shoot", C_GOLD),
        ("P2 Controls:", "Arrows = Move,  / = Shoot",  C_SILVER),
        ("",             "Enter = Select,  Esc = Quit", C_GRAY),
    ]
    for label, val, col in ctrls:
        if label:
            l = small_font.render(label, True, col)
            surf.blit(l, (WIN_W//2 - 160, ctrl_y))
        v = small_font.render(val, True, C_GRAY)
        surf.blit(v, (WIN_W//2 - 40, ctrl_y))
        ctrl_y += 22


def draw_gameover(surf, font, big_font, small_font, won, score, blink):
    surf.fill(C_MENU_BG)
    msg = "YOU WIN!" if won else "GAME OVER"
    col = C_YELLOW if won else C_RED
    title = big_font.render(msg, True, col)
    surf.blit(title, (WIN_W//2 - title.get_width()//2, 160))

    sc = font.render(f"Score: {score}", True, C_WHITE)
    surf.blit(sc, (WIN_W//2 - sc.get_width()//2, 260))

    if blink:
        cont = small_font.render("Press ENTER to play again  /  ESC to quit", True, C_GRAY)
        surf.blit(cont, (WIN_W//2 - cont.get_width()//2, 360))


# ─── Game ─────────────────────────────────────────────────────────────────────
class Game:
    ENEMY_SPAWN_POSITIONS = [
        (1*TILE,  0),
        (12*TILE, 0),
        (23*TILE, 0),
    ]
    P1_SPAWN = (9*TILE, 22*TILE)
    P2_SPAWN = (15*TILE, 22*TILE)
    TOTAL_ENEMIES = 10

    def __init__(self, mode):
        self.mode      = mode   # 1 or 2
        self.grid      = build_map()
        self.score     = 0
        self.stage     = 1
        self.over      = False
        self.won       = False
        self.fort_dead = False
        self.particles = []

        # Players
        self.players = {}
        self.players['p1'] = Tank(*self.P1_SPAWN, C_GOLD,   'p1')
        if mode == 2:
            self.players['p2'] = Tank(*self.P2_SPAWN, C_SILVER, 'p2')

        # Enemies
        self.enemies      = []
        self.enemy_queue  = self.TOTAL_ENEMIES
        self.spawn_timer  = 120
        self.bots         = []
        self._spawn_enemies_initial()

        self.bullets = []

    def _spawn_enemies_initial(self):
        for pos in self.ENEMY_SPAWN_POSITIONS[:3]:
            if self.enemy_queue > 0:
                e = Tank(*pos, C_RED, 'enemy')
                e.dir = 2
                self.enemies.append(e)
                self.bots.append(BotAI(e))
                self.enemy_queue -= 1

    def _try_spawn_enemy(self):
        if self.enemy_queue <= 0: return
        alive = sum(1 for e in self.enemies if e.alive)
        if alive >= 4: return
        pos = random.choice(self.ENEMY_SPAWN_POSITIONS)
        e = Tank(*pos, C_RED, 'enemy')
        e.dir = 2
        # Check no collision with players
        er = e.rect()
        for p in self.players.values():
            if p.alive and er.colliderect(p.rect()): return
        self.enemies.append(e)
        self.bots.append(BotAI(e))
        self.enemy_queue -= 1

    def handle_input_shoot(self, player_id):
        tank = self.players.get(player_id)
        if tank and tank.alive:
            b = tank.shoot()
            if b: self.bullets.append(b)

    def update(self, keys):
        if self.over: return

        # Player 1 movement
        p1 = self.players.get('p1')
        if p1 and p1.alive:
            if keys[pygame.K_w]: p1.move(0, self.grid)
            if keys[pygame.K_d]: p1.move(1, self.grid)
            if keys[pygame.K_s]: p1.move(2, self.grid)
            if keys[pygame.K_a]: p1.move(3, self.grid)
            if p1.shoot_cooldown > 0: p1.shoot_cooldown -= 1

        # Player 2 movement
        p2 = self.players.get('p2')
        if p2 and p2.alive:
            if keys[pygame.K_UP]:    p2.move(0, self.grid)
            if keys[pygame.K_RIGHT]: p2.move(1, self.grid)
            if keys[pygame.K_DOWN]:  p2.move(2, self.grid)
            if keys[pygame.K_LEFT]:  p2.move(3, self.grid)
            if p2.shoot_cooldown > 0: p2.shoot_cooldown -= 1

        # Bot updates
        living_players = [p for p in self.players.values() if p.alive]
        for bot in self.bots:
            b = bot.update(self.grid, living_players, self.bullets)
            if b: self.bullets.append(b)

        # Bullet updates
        for b in self.bullets:
            b.update(self.grid)

        # Bullet vs tank collisions
        for b in list(self.bullets):
            if not b.alive: continue
            br = pygame.Rect(int(b.x), int(b.y), b.w, b.h)

            # vs enemies
            if b.owner in ('p1', 'p2'):
                for e in self.enemies:
                    if e.alive and br.colliderect(e.rect()):
                        e.alive = False
                        b.alive = False
                        self.score += 100
                        self.particles += spawn_explosion(
                            e.x+TILE//2, e.y+TILE//2, big=True)
                        break

            # vs players
            elif b.owner == 'enemy':
                for pid, p in self.players.items():
                    if p.alive and br.colliderect(p.rect()):
                        b.alive = False
                        p.lives -= 1
                        self.particles += spawn_explosion(
                            p.x+TILE//2, p.y+TILE//2, big=True)
                        if p.lives > 0:
                            p.respawn()
                        else:
                            p.alive = False
                        break

            # vs fort
            if b.alive:
                for ty_r in range(ROWS):
                    for tx_r in range(COLS):
                        if self.grid[ty_r][tx_r] == T_FORT:
                            fr = pygame.Rect(tx_r*TILE, ty_r*TILE, TILE, TILE)
                            if br.colliderect(fr):
                                self.grid[ty_r][tx_r] = T_EMPTY
                                self.fort_dead = True
                                b.alive = False
                                self.particles += spawn_explosion(
                                    tx_r*TILE+TILE//2, ty_r*TILE+TILE//2, big=True)

        self.bullets = [b for b in self.bullets if b.alive]

        # Update particles
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.15
            p['life'] -= 1
        self.particles = [p for p in self.particles if p['life'] > 0]

        # Spawn timer
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_timer = 180
            self._try_spawn_enemy()

        # Win/lose conditions
        if self.fort_dead:
            self.over = True; self.won = False
            return
        all_dead = all(not p.alive for p in self.players.values())
        if all_dead:
            self.over = True; self.won = False
            return
        enemies_remain = self.enemy_queue > 0 or any(e.alive for e in self.enemies)
        if not enemies_remain:
            self.over = True; self.won = True

    def draw(self, surf):
        surf.fill(C_BG)

        # Draw tiles
        for ty in range(ROWS):
            for tx in range(COLS):
                t = self.grid[ty][tx]
                rx, ry = tx*TILE, ty*TILE
                if t == T_BRICK:  draw_brick(surf, rx, ry)
                elif t == T_STEEL: draw_steel(surf, rx, ry)
                elif t == T_FORT:
                    if self.fort_dead: draw_fort_dead(surf, rx, ry)
                    else:              draw_fort(surf, rx, ry)

        # Enemies
        for e in self.enemies:
            e.draw(surf)

        # Players
        for p in self.players.values():
            p.draw(surf)

        # Bullets
        for b in self.bullets:
            b.draw(surf)

        # Particles
        draw_explosion(surf, self.particles)

        # Border
        pygame.draw.rect(surf, C_DARK, (0, 0, COLS*TILE, WIN_H), 3)


# ─── Main loop ────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    pygame.display.set_caption("Tank Battle 1990")
    surf = pygame.display.set_mode((WIN_W, WIN_H))
    clock = pygame.time.Clock()

    try:
        big_font   = pygame.font.SysFont("Consolas,Courier New,monospace", 48, bold=True)
        font       = pygame.font.SysFont("Consolas,Courier New,monospace", 22, bold=True)
        small_font = pygame.font.SysFont("Consolas,Courier New,monospace", 16)
    except:
        big_font   = pygame.font.Font(None, 54)
        font       = pygame.font.Font(None, 28)
        small_font = pygame.font.Font(None, 20)

    state    = GameMode.MENU
    selected = 0
    blink    = True
    blink_t  = 0
    game     = None

    while True:
        dt = clock.tick(FPS)
        blink_t += dt
        if blink_t > 500:
            blink = not blink
            blink_t = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == GameMode.PLAY:
                        state = GameMode.MENU
                    else:
                        pygame.quit(); sys.exit()

                # Menu
                if state == GameMode.MENU:
                    if event.key in (pygame.K_UP, pygame.K_w):
                        selected = (selected - 1) % 2
                    if event.key in (pygame.K_DOWN, pygame.K_s):
                        selected = (selected + 1) % 2
                    if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        game = Game(selected + 1)
                        state = GameMode.PLAY

                # Game over
                elif state == GameMode.GAMEOVER:
                    if event.key == pygame.K_RETURN:
                        game = Game(game.mode)
                        state = GameMode.PLAY

                # In-game shoot
                elif state == GameMode.PLAY and game:
                    if event.key == pygame.K_f:
                        game.handle_input_shoot('p1')
                    if event.key == pygame.K_SLASH or event.key == pygame.K_KP_DIVIDE:
                        game.handle_input_shoot('p2')

        # Update
        if state == GameMode.PLAY and game:
            keys = pygame.key.get_pressed()
            game.update(keys)
            if game.over:
                state = GameMode.GAMEOVER

        # Draw
        if state == GameMode.MENU:
            draw_menu(surf, font, big_font, small_font, selected, blink)
        elif state == GameMode.PLAY and game:
            game.draw(surf)
            draw_hud(surf, font, small_font, game)
        elif state == GameMode.GAMEOVER and game:
            game.draw(surf)
            draw_hud(surf, font, small_font, game)
            # Semi-transparent overlay
            overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            surf.blit(overlay, (0, 0))
            draw_gameover(surf, font, big_font, small_font, game.won, game.score, blink)

        pygame.display.flip()


if __name__ == "__main__":
    main()
