# File: tank1990.v1.1.py
# Date: 2026-06-15
# Python: 3.14
# Requirement: pygame-ce
# Tested with: Python 3.14.0 with pygame-ce
# Environment: Local Python interpreter, no virtual environment
# Purpose: Create bot, play with bot, and two-player game
# Game_version: 1.2.0
# Developers: Bayar-Erdene, Altanbayar, AmgalanBaatar, Gansukh

#-----New features--------------------------------------------------------------
# In this version we fixed bug in controller
# Now players can adjust the size of the tab
# Added bot cooldown
# Added developers names on the bottom right corner

import pygame
import sys
import math
import random
import struct
import wave
import io
from enum import Enum

# ─── Base resolution (logical) ───────────────────────────────────────────────
TILE   = 32
COLS   = 26
ROWS   = 24
HUD_W  = 160
BASE_W = COLS * TILE + HUD_W   # 992
BASE_H = ROWS * TILE            # 768
FPS    = 60

# Scale factor (Tab / Shift+Tab to resize)
SCALES     = [0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2.0]
SCALE_IDX  = 6   # default 1.0

C_BG      = (30,  30,  30)
C_BRICK   = (180, 80,  30)
C_BRICK_D = (120, 50,  15)
C_STEEL   = (160, 160, 175)
C_STEEL_D = (100, 100, 115)
C_FORT    = (200, 160, 40)
C_FORT_D  = (140, 110, 20)
C_GOLD    = (240, 200, 40)
C_SILVER  = (190, 190, 210)
C_RED     = (220, 60,  60)
C_WHITE   = (255, 255, 255)
C_DARK    = (20,  20,  20)
C_YELLOW  = (255, 230, 50)
C_ORANGE  = (255, 140, 0)
C_GRAY    = (100, 100, 110)
C_LGRAY   = (160, 160, 170)
C_MENU_BG = (15,  15,  20)
C_HUD_BG  = (18,  18,  24)
C_GREEN   = (60,  200, 80)
C_BLUE    = (80,  140, 220)

DIR_VEC = [(0,-1),(1,0),(0,1),(-1,0)]
T_EMPTY = 0; T_BRICK = 1; T_STEEL = 2; T_FORT = 3

# Credits shown bottom-right of menu
CREDITS = ["Bayar-Erdene", "Altanbayar", "Amgalanbaatar", "Gantugs"]

# ─── Difficulty ───────────────────────────────────────────────────────────────
DIFFICULTY = {
    'easy':   {'bot_think': (70,130), 'bot_shoot_chance': 0.0015, 'bot_speed_mul': 0.65,
               'shoot_cd': 55, 'chase_dist': 5,  'label': 'EASY',   'color': C_GREEN},
    'normal': {'bot_think': (35, 85), 'bot_shoot_chance': 0.004,  'bot_speed_mul': 1.0,
               'shoot_cd': 38, 'chase_dist': 8,  'label': 'NORMAL', 'color': C_YELLOW},
    'hard':   {'bot_think': (12, 40), 'bot_shoot_chance': 0.009,  'bot_speed_mul': 1.35,
               'shoot_cd': 22, 'chase_dist': 14, 'label': 'HARD',   'color': C_RED},
}

class GameMode(Enum):
    MENU     = "menu"
    SETTINGS = "settings"
    PLAY     = "play"
    GAMEOVER = "gameover"

# ─── Sound ────────────────────────────────────────────────────────────────────
def _make_wav(samples, rate=22050):
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(b''.join(
            struct.pack('<h', max(-32768, min(32767, int(s)))) for s in samples))
    buf.seek(0)
    return pygame.mixer.Sound(buf)

def make_shoot_sound():
    rate=22050; n=int(rate*0.08); samples=[]
    for i in range(n):
        t=i/rate; env=math.exp(-t*40)
        s=math.sin(2*math.pi*180*t)*0.4+random.uniform(-0.6,0.6)
        samples.append(s*env*28000)
    return _make_wav(samples, rate)

def make_explode_sound():
    rate=22050; n=int(rate*0.25); samples=[]
    for i in range(n):
        t=i/rate; env=math.exp(-t*14)
        s=random.uniform(-1,1)*0.8+math.sin(2*math.pi*60*t)*0.2
        samples.append(s*env*30000)
    return _make_wav(samples, rate)

def make_hit_sound():
    rate=22050; n=int(rate*0.06); samples=[]
    for i in range(n):
        t=i/rate; env=math.exp(-t*60)
        s=math.sin(2*math.pi*300*t)*0.5+random.uniform(-0.5,0.5)
        samples.append(s*env*25000)
    return _make_wav(samples, rate)

# ─── Map ──────────────────────────────────────────────────────────────────────
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
    grid=[]
    for row_str in BASE_MAP:
        row=[]
        for ch in row_str.ljust(COLS)[:COLS]:
            if ch=='#': row.append(T_BRICK)
            elif ch=='S': row.append(T_STEEL)
            elif ch=='F': row.append(T_FORT)
            else: row.append(T_EMPTY)
        grid.append(row)
    while len(grid)<ROWS: grid.append([T_EMPTY]*COLS)
    return grid

# ─── Draw helpers ─────────────────────────────────────────────────────────────
def draw_brick(surf, rx, ry):
    pygame.draw.rect(surf, C_BRICK, (rx,ry,TILE,TILE))
    for row in range(2):
        y0=ry+row*16
        for col in range(3):
            offset=8 if row%2 else 0
            x0=rx+col*11-3+offset
            pygame.draw.rect(surf, C_BRICK_D, (x0+1,y0+1,9,6))

def draw_steel(surf, rx, ry):
    pygame.draw.rect(surf, C_STEEL, (rx,ry,TILE,TILE))
    pygame.draw.rect(surf, C_STEEL_D, (rx,ry,TILE//2,TILE//2))
    pygame.draw.rect(surf, C_STEEL_D, (rx+TILE//2,ry+TILE//2,TILE//2,TILE//2))
    pygame.draw.rect(surf, C_WHITE, (rx+2,ry+2,5,5))

def draw_fort(surf, rx, ry):
    pygame.draw.rect(surf, C_FORT, (rx,ry,TILE,TILE))
    pygame.draw.rect(surf, C_FORT_D, (rx+8,ry+6,16,14))
    pygame.draw.rect(surf, C_FORT_D, (rx+6,ry+10,20,8))
    pygame.draw.rect(surf, C_YELLOW, (rx+13,ry+8,6,5))

def draw_fort_dead(surf, rx, ry):
    pygame.draw.rect(surf, (60,30,10), (rx,ry,TILE,TILE))
    pygame.draw.line(surf, C_RED, (rx+4,ry+4),(rx+TILE-4,ry+TILE-4),3)
    pygame.draw.line(surf, C_RED, (rx+TILE-4,ry+4),(rx+4,ry+TILE-4),3)

def draw_tank(surf, x, y, direction, color, is_player=True):
    cx,cy=x+TILE//2, y+TILE//2
    tread=tuple(max(0,c-60) for c in color)
    barrel=tuple(max(0,c-30) for c in color)
    if direction in (0,2):
        pygame.draw.rect(surf,tread,(x+2,y+2,7,TILE-4))
        pygame.draw.rect(surf,tread,(x+TILE-9,y+2,7,TILE-4))
        for i in range(4):
            yy=y+4+i*7
            pygame.draw.line(surf,color,(x+2,yy),(x+8,yy),1)
            pygame.draw.line(surf,color,(x+TILE-9,yy),(x+TILE-3,yy),1)
        pygame.draw.rect(surf,color,(x+9,y+6,TILE-18,TILE-12))
        pygame.draw.rect(surf,color,(x+11,y+9,TILE-22,TILE-18))
        if direction==0: pygame.draw.rect(surf,barrel,(cx-3,y,6,14))
        else:            pygame.draw.rect(surf,barrel,(cx-3,y+TILE-14,6,14))
    else:
        pygame.draw.rect(surf,tread,(x+2,y+2,TILE-4,7))
        pygame.draw.rect(surf,tread,(x+2,y+TILE-9,TILE-4,7))
        for i in range(4):
            xx=x+4+i*7
            pygame.draw.line(surf,color,(xx,y+2),(xx,y+8),1)
            pygame.draw.line(surf,color,(xx,y+TILE-9),(xx,y+TILE-3),1)
        pygame.draw.rect(surf,color,(x+6,y+9,TILE-12,TILE-18))
        pygame.draw.rect(surf,color,(x+9,y+11,TILE-18,TILE-22))
        if direction==1: pygame.draw.rect(surf,barrel,(x+TILE-14,cy-3,14,6))
        else:            pygame.draw.rect(surf,barrel,(x,cy-3,14,6))
    if is_player:
        pygame.draw.circle(surf, C_WHITE, (cx,cy), 3)

def draw_explosion(surf, particles):
    for p in particles:
        color=(min(255,p['color'][0]),min(255,p['color'][1]),0)
        r=max(1,int(p['r']*p['life']/p['max_life']))
        pygame.draw.circle(surf,color,(int(p['x']),int(p['y'])),r)

# ─── Entities ─────────────────────────────────────────────────────────────────
class Bullet:
    SPEED=6
    def __init__(self,x,y,direction,owner):
        self.x,self.y=float(x),float(y)
        self.dir=direction; self.owner=owner; self.alive=True
        dx,dy=DIR_VEC[direction]
        self.vx,self.vy=dx*self.SPEED,dy*self.SPEED
        self.w=self.h=6

    def update(self,grid):
        self.x+=self.vx; self.y+=self.vy
        if self.x<0 or self.x>COLS*TILE or self.y<0 or self.y>ROWS*TILE:
            self.alive=False; return False
        for corner in [(self.x,self.y),(self.x+self.w,self.y),
                       (self.x,self.y+self.h),(self.x+self.w,self.y+self.h)]:
            tx,ty=int(corner[0]//TILE),int(corner[1]//TILE)
            if 0<=tx<COLS and 0<=ty<ROWS:
                t=grid[ty][tx]
                if t==T_BRICK: grid[ty][tx]=T_EMPTY; self.alive=False; return 'brick'
                elif t==T_STEEL: self.alive=False; return 'steel'
                elif t==T_FORT: grid[ty][tx]=T_EMPTY; self.alive=False; return 'fort'
        return False

    def draw(self,surf):
        if not self.alive: return
        col=C_YELLOW if self.owner!='enemy' else C_RED
        pygame.draw.rect(surf,col,(int(self.x),int(self.y),self.w,self.h))
        pygame.draw.rect(surf,C_WHITE,(int(self.x)+1,int(self.y)+1,3,3))


class Tank:
    BASE_SPEED=2
    def __init__(self,x,y,color,player_id,speed_mul=1.0):
        self.start_x,self.start_y=float(x),float(y)
        self.x,self.y=float(x),float(y)
        self.dir=0; self.color=color; self.player_id=player_id; self.alive=True
        self.shoot_cooldown=0
        self.w=self.h=TILE-2
        self.lives=3 if player_id in ('p1','p2') else 1
        self.speed=self.BASE_SPEED*speed_mul
        # ── Per-frame movement priority tracking ──────────────────────────────
        # Keeps the last requested direction so we don't freeze when two keys held
        self._move_dir = None

    def respawn(self):
        self.x,self.y=self.start_x,self.start_y
        self.alive=True; self.shoot_cooldown=90; self._move_dir=None

    def can_shoot(self): return self.shoot_cooldown<=0

    def shoot(self,cooldown=25):
        if not self.can_shoot(): return None
        self.shoot_cooldown=cooldown
        dx,dy=DIR_VEC[self.dir]
        bx=self.x+self.w//2-3+dx*(TILE//2)
        by=self.y+self.h//2-3+dy*(TILE//2)
        return Bullet(bx,by,self.dir,self.player_id)

    def move(self,direction,grid):
        self.dir=direction
        dx,dy=DIR_VEC[direction]
        nx=self.x+dx*self.speed; ny=self.y+dy*self.speed
        if self._can_move(nx,ny,grid):
            self.x,self.y=nx,ny
            if dx==0: self.x=round(self.x/(TILE//2))*(TILE//2)
            else:     self.y=round(self.y/(TILE//2))*(TILE//2)

    def _can_move(self,nx,ny,grid):
        m=2
        for cx,cy in [(nx+m,ny+m),(nx+self.w-m,ny+m),
                      (nx+m,ny+self.h-m),(nx+self.w-m,ny+self.h-m)]:
            tx,ty=int(cx//TILE),int(cy//TILE)
            if not (0<=tx<COLS and 0<=ty<ROWS): return False
            if grid[ty][tx] in (T_BRICK,T_STEEL,T_FORT): return False
        return True

    def rect(self): return pygame.Rect(int(self.x),int(self.y),self.w,self.h)

    def draw(self,surf):
        if not self.alive: return
        draw_tank(surf,int(self.x),int(self.y),self.dir,self.color,
                  self.player_id in ('p1','p2'))

# ─── Bot AI ───────────────────────────────────────────────────────────────────
class BotAI:
    def __init__(self,tank,diff='normal'):
        self.tank=tank; self.diff=DIFFICULTY[diff]
        self.think_timer=0; self.move_dir=2
        self.stuck_timer=0; self.last_pos=(tank.x,tank.y); self.patrol_timer=0

    def _dist(self,ax,ay,bx,by): return abs(ax-bx)+abs(ay-by)

    def _dir_toward(self,tx,ty,ex,ey):
        dx,dy=tx-ex,ty-ey
        if abs(dx)>abs(dy): return 1 if dx>0 else 3
        else:               return 2 if dy>0 else 0

    def _line_of_sight(self,grid,targets):
        t=self.tank; dx,dy=DIR_VEC[t.dir]
        cx,cy=t.x+TILE//2,t.y+TILE//2
        for step in range(1,COLS):
            cx2,cy2=cx+dx*TILE*step//2,cy+dy*TILE*step//2
            tx2,ty2=int(cx2//TILE),int(cy2//TILE)
            if not (0<=tx2<COLS and 0<=ty2<ROWS): break
            if grid[ty2][tx2] in (T_STEEL,T_BRICK): break
            for tgt in targets:
                if tgt.alive and tgt.rect().collidepoint(cx2,cy2): return True
        return False

    def update(self,grid,player_tanks,bullets):
        t=self.tank
        if not t.alive: return None
        d=self.diff
        self.think_timer-=1; self.patrol_timer-=1
        if abs(t.x-self.last_pos[0])<1 and abs(t.y-self.last_pos[1])<1:
            self.stuck_timer+=1
        else: self.stuck_timer=0
        self.last_pos=(t.x,t.y)
        if self.stuck_timer>30:
            self.move_dir=random.randint(0,3); self.stuck_timer=0
        if self.think_timer<=0:
            lo,hi=d['bot_think']; self.think_timer=random.randint(lo,hi)
            living=[p for p in player_tanks if p.alive]
            if living:
                nearest=min(living,key=lambda p:self._dist(p.x,p.y,t.x,t.y))
                dist=self._dist(nearest.x,nearest.y,t.x,t.y)
                if dist<d['chase_dist']*TILE:
                    self.move_dir=self._dir_toward(nearest.x,nearest.y,t.x,t.y)
                elif self.patrol_timer<=0:
                    self.patrol_timer=random.randint(60,120)
                    self.move_dir=random.choice([0,1,2,3])
        t.move(self.move_dir,grid)
        if t.shoot_cooldown>0: t.shoot_cooldown-=1
        living=[p for p in player_tanks if p.alive]
        if living and t.can_shoot():
            nearest=min(living,key=lambda p:self._dist(p.x,p.y,t.x,t.y))
            aligned_h=abs(t.y-nearest.y)<TILE
            aligned_v=abs(t.x-nearest.x)<TILE
            if aligned_h: t.dir=1 if nearest.x>t.x else 3
            elif aligned_v: t.dir=2 if nearest.y>t.y else 0
            if (aligned_h or aligned_v) and self._line_of_sight(grid,living):
                return t.shoot(d['shoot_cd'])
            elif random.random()<d['bot_shoot_chance']:
                return t.shoot(d['shoot_cd'])
        return None

# ─── Particles ────────────────────────────────────────────────────────────────
def spawn_explosion(cx,cy,big=False):
    parts=[]
    for _ in range(20 if big else 12):
        a=random.uniform(0,math.tau); sp=random.uniform(1,4 if big else 3)
        parts.append({'x':float(cx),'y':float(cy),'vx':math.cos(a)*sp,'vy':math.sin(a)*sp,
                      'r':random.randint(3,8 if big else 5),'life':random.randint(15,35),
                      'max_life':35,'color':random.choice([(255,200,0),(255,120,0),(255,60,0)])})
    return parts

# ─── HUD ──────────────────────────────────────────────────────────────────────
def draw_hud(surf, font, small_font, game):
    ox=COLS*TILE
    pygame.draw.rect(surf,C_HUD_BG,(ox,0,HUD_W,BASE_H))
    pygame.draw.line(surf,C_GRAY,(ox,0),(ox,BASE_H),2)
    y=12
    t=font.render("TANK",True,C_YELLOW)
    surf.blit(t,(ox+HUD_W//2-t.get_width()//2,y)); y+=26
    t2=small_font.render("BATTLE",True,C_ORANGE)
    surf.blit(t2,(ox+HUD_W//2-t2.get_width()//2,y)); y+=20
    dc=DIFFICULTY[game.diff]['color']
    dl=small_font.render(DIFFICULTY[game.diff]['label'],True,dc)
    pygame.draw.rect(surf,tuple(c//3 for c in dc),(ox+10,y,HUD_W-20,18),border_radius=4)
    surf.blit(dl,(ox+HUD_W//2-dl.get_width()//2,y+1)); y+=24
    pygame.draw.line(surf,C_GRAY,(ox+10,y),(ox+HUD_W-10,y),1); y+=8
    for pid,color,label,ks in [('p1',C_GOLD,'P1','WASD+F'),('p2',C_SILVER,'P2','ARR+/')]:
        tank=game.players.get(pid)
        if tank is None: continue
        lbl=font.render(label,True,color); surf.blit(lbl,(ox+12,y))
        for i in range(max(0,tank.lives)):
            draw_tank(surf,ox+62+i*22,y-2,0,color,True)
        y+=26; k=small_font.render(ks,True,C_GRAY); surf.blit(k,(ox+12,y)); y+=18
    pygame.draw.line(surf,C_GRAY,(ox+10,y),(ox+HUD_W-10,y),1); y+=8
    e_lbl=font.render("ENEMIES",True,C_RED)
    surf.blit(e_lbl,(ox+HUD_W//2-e_lbl.get_width()//2,y)); y+=22
    for i in range(len(game.enemies)):
        ex2=ox+14+(i%4)*34; ey2=y+(i//4)*24
        col=C_RED if game.enemies[i].alive else C_GRAY
        draw_tank(surf,ex2,ey2,2,col,False)
    y+=((len(game.enemies)-1)//4+1)*24+6
    pygame.draw.line(surf,C_GRAY,(ox+10,y),(ox+HUD_W-10,y),1); y+=8
    s_lbl=font.render("SCORE",True,C_WHITE)
    surf.blit(s_lbl,(ox+HUD_W//2-s_lbl.get_width()//2,y)); y+=22
    s_val=font.render(str(game.score),True,C_YELLOW)
    surf.blit(s_val,(ox+HUD_W//2-s_val.get_width()//2,y)); y+=28
    st=small_font.render(f"Stage {game.stage}",True,C_GRAY)
    surf.blit(st,(ox+HUD_W//2-st.get_width()//2,y)); y+=24
    # Scale hint
    hint=small_font.render("Tab±zoom",True,(50,50,60))
    surf.blit(hint,(ox+HUD_W//2-hint.get_width()//2,BASE_H-20))

# ─── Credits (bottom-right of menu) ──────────────────────────────────────────
def draw_credits(surf, small_font):
    credit_color = (60, 60, 70)   # very dim, barely visible
    line_h = 18
    start_y = BASE_H - len(CREDITS)*line_h - 8
    for i, name in enumerate(CREDITS):
        txt = small_font.render(name, True, credit_color)
        x   = BASE_W - txt.get_width() - 10
        y   = start_y + i*line_h
        surf.blit(txt, (x, y))

# ─── Settings screen ──────────────────────────────────────────────────────────
class Settings:
    DIFF_ORDER=['easy','normal','hard']
    MIN_BOTS,MAX_BOTS=1,12
    def __init__(self,mode):
        self.mode=mode; self.diff_idx=1; self.bot_count=6; self.cursor=0
    @property
    def diff(self): return self.DIFF_ORDER[self.diff_idx]

    def handle_key(self,key):
        if key in (pygame.K_UP,pygame.K_w):
            self.cursor=(self.cursor-1)%3
        elif key in (pygame.K_DOWN,pygame.K_s):
            self.cursor=(self.cursor+1)%3
        elif key in (pygame.K_LEFT,pygame.K_a):
            if self.cursor==0: self.diff_idx=(self.diff_idx-1)%3
            elif self.cursor==1: self.bot_count=max(self.MIN_BOTS,self.bot_count-1)
        elif key in (pygame.K_RIGHT,pygame.K_d):
            if self.cursor==0: self.diff_idx=(self.diff_idx+1)%3
            elif self.cursor==1: self.bot_count=min(self.MAX_BOTS,self.bot_count+1)
        elif key in (pygame.K_RETURN,pygame.K_SPACE):
            if self.cursor==2: return 'start'
            elif self.cursor==0: self.diff_idx=(self.diff_idx+1)%3
            elif self.cursor==1: self.bot_count=min(self.MAX_BOTS,self.bot_count+1)
        return None

def draw_settings(surf,font,big_font,small_font,settings,blink):
    surf.fill(C_MENU_BG)
    title=big_font.render("SETTINGS",True,C_YELLOW)
    surf.blit(title,(BASE_W//2-title.get_width()//2,60))
    mode_lbl=font.render(f"{'1 PLAYER' if settings.mode==1 else '2 PLAYERS'}",True,C_ORANGE)
    surf.blit(mode_lbl,(BASE_W//2-mode_lbl.get_width()//2,120))
    items=[("DIFFICULTY",None),("BOT COUNT",None),("  START GAME","")]
    base_y=200
    for i,(label,_) in enumerate(items):
        sel=(i==settings.cursor)
        col=C_WHITE if sel else C_GRAY
        lbl=font.render(label,True,col)
        x=BASE_W//2-lbl.get_width()//2; y=base_y+i*90
        surf.blit(lbl,(x,y))
        if sel and blink:
            surf.blit(font.render(">",True,C_YELLOW),(x-36,y))
        if i==0:
            for j,dk in enumerate(Settings.DIFF_ORDER):
                dc=DIFFICULTY[dk]['color']; dl=DIFFICULTY[dk]['label']
                active=(j==settings.diff_idx)
                bx=BASE_W//2-160+j*110; by=y+34
                pygame.draw.rect(surf,tuple(c//3 for c in dc) if active else (40,40,50),
                                 (bx,by,100,32),border_radius=6)
                if active: pygame.draw.rect(surf,dc,(bx,by,100,32),2,border_radius=6)
                txt=font.render(dl,True,dc if active else C_GRAY)
                surf.blit(txt,(bx+50-txt.get_width()//2,by+6))
        elif i==1:
            bx=BASE_W//2-140; by=y+34
            surf.blit(font.render("<",True,C_YELLOW if sel else C_GRAY),(bx,by))
            cnt=font.render(str(settings.bot_count),True,C_WHITE)
            surf.blit(cnt,(BASE_W//2-cnt.get_width()//2,by))
            surf.blit(font.render(">",True,C_YELLOW if sel else C_GRAY),(BASE_W//2+120,by))
            for k in range(settings.bot_count):
                dx2=BASE_W//2-settings.bot_count*10+k*20
                pygame.draw.circle(surf,C_RED,(dx2,by+40),7)
    hint=small_font.render("←→ change value    ↑↓ move    Enter confirm    Esc back",True,C_GRAY)
    surf.blit(hint,(BASE_W//2-hint.get_width()//2,BASE_H-40))
    draw_credits(surf, small_font)

# ─── Main Menu ────────────────────────────────────────────────────────────────
def draw_menu(surf,font,big_font,small_font,selected,blink):
    surf.fill(C_MENU_BG)
    title=big_font.render("TANK BATTLE",True,C_YELLOW)
    surf.blit(title,(BASE_W//2-title.get_width()//2,80))
    sub=font.render("1990 EDITION",True,C_ORANGE)
    surf.blit(sub,(BASE_W//2-sub.get_width()//2,132))
    draw_tank(surf,BASE_W//2-120,175,2,C_GOLD,True)
    draw_tank(surf,BASE_W//2+90,175,2,C_SILVER,True)
    opts=["1 PLAYER","2 PLAYERS"]
    for i,opt in enumerate(opts):
        col=C_WHITE if i==selected else C_GRAY
        lbl=font.render(opt,True,col)
        x=BASE_W//2-lbl.get_width()//2; y=270+i*60
        surf.blit(lbl,(x,y))
        if i==selected and blink:
            surf.blit(font.render(">",True,C_YELLOW),(x-34,y))
            surf.blit(font.render("<",True,C_YELLOW),(x+lbl.get_width()+14,y))
    ctrl_y=430
    for lbl,val,col in [("P1:","WASD move  F shoot",C_GOLD),
                        ("P2:","Arrows move  / shoot",C_SILVER),
                        ("","Enter=select  Esc=quit",C_GRAY)]:
        if lbl: surf.blit(small_font.render(lbl,True,col),(BASE_W//2-170,ctrl_y))
        surf.blit(small_font.render(val,True,C_GRAY),(BASE_W//2-100,ctrl_y))
        ctrl_y+=22
    # Credits — dim, bottom-right
    draw_credits(surf, small_font)

def draw_gameover(surf,font,big_font,small_font,won,score,blink):
    surf.fill(C_MENU_BG)
    msg="YOU WIN!" if won else "GAME OVER"
    col=C_YELLOW if won else C_RED
    t=big_font.render(msg,True,col)
    surf.blit(t,(BASE_W//2-t.get_width()//2,160))
    sc=font.render(f"Score: {score}",True,C_WHITE)
    surf.blit(sc,(BASE_W//2-sc.get_width()//2,268))
    if blink:
        c=small_font.render("Enter = play again     Esc = menu",True,C_GRAY)
        surf.blit(c,(BASE_W//2-c.get_width()//2,370))
    draw_credits(surf, small_font)

# ─── Game ─────────────────────────────────────────────────────────────────────
SPAWN_POS=[(1*TILE,0),(12*TILE,0),(23*TILE,0),(6*TILE,0),(18*TILE,0),
           (3*TILE,0),(21*TILE,0),(8*TILE,0),(16*TILE,0),(10*TILE,0),(14*TILE,0),(5*TILE,0)]

class Game:
    P1_SPAWN=(9*TILE,22*TILE)
    P2_SPAWN=(15*TILE,22*TILE)

    def __init__(self,mode,diff='normal',bot_count=6,sounds=None):
        self.mode=mode; self.diff=diff
        self.grid=build_map(); self.score=0; self.stage=1
        self.over=False; self.won=False; self.fort_dead=False
        self.particles=[]; self.sounds=sounds or {}
        self.players={}
        self.players['p1']=Tank(*self.P1_SPAWN,C_GOLD,'p1')
        if mode==2: self.players['p2']=Tank(*self.P2_SPAWN,C_SILVER,'p2')
        self.enemies=[]; self.bots=[]; self.enemy_queue=bot_count
        self.spawn_timer=90; self.bullets=[]
        spd=DIFFICULTY[diff]['bot_speed_mul']
        for pos in SPAWN_POS[:min(3,bot_count)]:
            if self.enemy_queue>0:
                e=Tank(*pos,C_RED,'enemy',spd); e.dir=2
                self.enemies.append(e); self.bots.append(BotAI(e,diff))
                self.enemy_queue-=1

    def _play(self,name):
        s=self.sounds.get(name)
        if s:
            try: s.play()
            except: pass

    def _try_spawn(self):
        if self.enemy_queue<=0: return
        alive=sum(1 for e in self.enemies if e.alive)
        if alive>=4: return
        spd=DIFFICULTY[self.diff]['bot_speed_mul']
        pos=random.choice(SPAWN_POS[:3])
        e=Tank(*pos,C_RED,'enemy',spd); e.dir=2
        er=e.rect()
        for p in self.players.values():
            if p.alive and er.colliderect(p.rect()): return
        self.enemies.append(e); self.bots.append(BotAI(e,self.diff))
        self.enemy_queue-=1

    def handle_shoot(self,pid):
        t=self.players.get(pid)
        if t and t.alive:
            b=t.shoot()
            if b: self.bullets.append(b); self._play('shoot')

    def update(self, keys):
        if self.over: return

        # ── Player 1 movement — priority: last key wins, no lockout ──────────
        p1=self.players.get('p1')
        if p1 and p1.alive:
            # Collect all pressed directions, pick the first valid one
            p1_dirs=[]
            if keys[pygame.K_w]: p1_dirs.append(0)
            if keys[pygame.K_d]: p1_dirs.append(1)
            if keys[pygame.K_s]: p1_dirs.append(2)
            if keys[pygame.K_a]: p1_dirs.append(3)
            # When multiple keys held, keep last used direction if still held
            if p1_dirs:
                if p1._move_dir in p1_dirs:
                    p1.move(p1._move_dir, self.grid)
                else:
                    p1._move_dir = p1_dirs[-1]
                    p1.move(p1._move_dir, self.grid)
            else:
                p1._move_dir = None
            if p1.shoot_cooldown>0: p1.shoot_cooldown-=1

        # ── Player 2 movement ─────────────────────────────────────────────────
        p2=self.players.get('p2')
        if p2 and p2.alive:
            p2_dirs=[]
            if keys[pygame.K_UP]:    p2_dirs.append(0)
            if keys[pygame.K_RIGHT]: p2_dirs.append(1)
            if keys[pygame.K_DOWN]:  p2_dirs.append(2)
            if keys[pygame.K_LEFT]:  p2_dirs.append(3)
            if p2_dirs:
                if p2._move_dir in p2_dirs:
                    p2.move(p2._move_dir, self.grid)
                else:
                    p2._move_dir = p2_dirs[-1]
                    p2.move(p2._move_dir, self.grid)
            else:
                p2._move_dir = None
            if p2.shoot_cooldown>0: p2.shoot_cooldown-=1

        # ── Bots ──────────────────────────────────────────────────────────────
        living_players=[p for p in self.players.values() if p.alive]
        for bot in self.bots:
            b=bot.update(self.grid,living_players,self.bullets)
            if b: self.bullets.append(b); self._play('shoot')

        # ── Bullets ───────────────────────────────────────────────────────────
        for b in self.bullets:
            hit=b.update(self.grid)
            if hit in ('brick','steel'): self._play('hit')

        for b in list(self.bullets):
            if not b.alive: continue
            br=pygame.Rect(int(b.x),int(b.y),b.w,b.h)
            if b.owner in ('p1','p2'):
                for e in self.enemies:
                    if e.alive and br.colliderect(e.rect()):
                        e.alive=False; b.alive=False; self.score+=100
                        self.particles+=spawn_explosion(e.x+TILE//2,e.y+TILE//2,True)
                        self._play('explode'); break
            elif b.owner=='enemy':
                for pid,p in self.players.items():
                    if p.alive and br.colliderect(p.rect()):
                        b.alive=False; p.lives-=1
                        self.particles+=spawn_explosion(p.x+TILE//2,p.y+TILE//2,True)
                        self._play('explode')
                        if p.lives>0: p.respawn()
                        else: p.alive=False
                        break
            if b.alive:
                for ty_r in range(ROWS):
                    for tx_r in range(COLS):
                        if self.grid[ty_r][tx_r]==T_FORT:
                            if br.colliderect(pygame.Rect(tx_r*TILE,ty_r*TILE,TILE,TILE)):
                                self.grid[ty_r][tx_r]=T_EMPTY
                                self.fort_dead=True; b.alive=False
                                self.particles+=spawn_explosion(
                                    tx_r*TILE+TILE//2,ty_r*TILE+TILE//2,True)
                                self._play('explode')

        self.bullets=[b for b in self.bullets if b.alive]
        for p in self.particles:
            p['x']+=p['vx']; p['y']+=p['vy']; p['vy']+=0.15; p['life']-=1
        self.particles=[p for p in self.particles if p['life']>0]
        self.spawn_timer-=1
        if self.spawn_timer<=0: self.spawn_timer=180; self._try_spawn()
        if self.fort_dead: self.over=True; self.won=False; return
        if all(not p.alive for p in self.players.values()):
            self.over=True; self.won=False; return
        if self.enemy_queue<=0 and not any(e.alive for e in self.enemies):
            self.over=True; self.won=True

    def draw(self, surf):
        surf.fill(C_BG)
        for ty in range(ROWS):
            for tx in range(COLS):
                t=self.grid[ty][tx]; rx,ry=tx*TILE,ty*TILE
                if t==T_BRICK: draw_brick(surf,rx,ry)
                elif t==T_STEEL: draw_steel(surf,rx,ry)
                elif t==T_FORT:
                    if self.fort_dead: draw_fort_dead(surf,rx,ry)
                    else: draw_fort(surf,rx,ry)
        for e in self.enemies: e.draw(surf)
        for p in self.players.values(): p.draw(surf)
        for b in self.bullets: b.draw(surf)
        draw_explosion(surf, self.particles)
        pygame.draw.rect(surf,C_DARK,(0,0,COLS*TILE,BASE_H),3)

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    global SCALE_IDX
    pygame.init()
    pygame.mixer.init(frequency=22050,size=-16,channels=1,buffer=512)
    pygame.display.set_caption("Tank Battle 1990")

    # Logical surface (always BASE_W x BASE_H)
    logic_surf = pygame.Surface((BASE_W, BASE_H))

    def get_win_size():
        s=SCALES[SCALE_IDX]
        return int(BASE_W*s), int(BASE_H*s)

    win_w,win_h=get_win_size()
    screen=pygame.display.set_mode((win_w,win_h), pygame.RESIZABLE)
    clock=pygame.time.Clock()

    try:
        big_font   = pygame.font.SysFont("Consolas,Courier New,monospace",48,bold=True)
        font       = pygame.font.SysFont("Consolas,Courier New,monospace",22,bold=True)
        small_font = pygame.font.SysFont("Consolas,Courier New,monospace",16)
    except:
        big_font   = pygame.font.Font(None,54)
        font       = pygame.font.Font(None,28)
        small_font = pygame.font.Font(None,20)

    sounds={}
    try:
        sounds['shoot']  =make_shoot_sound()
        sounds['explode']=make_explode_sound()
        sounds['hit']    =make_hit_sound()
    except Exception as e:
        print(f"Sound init skipped: {e}")

    state=GameMode.MENU; selected=0; settings=None; game=None
    blink=True; blink_t=0

    while True:
        dt=clock.tick(FPS)
        blink_t+=dt
        if blink_t>500: blink=not blink; blink_t=0

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit(); sys.exit()

            # ── Window resize by dragging ──────────────────────────────────
            if event.type==pygame.VIDEORESIZE:
                screen=pygame.display.set_mode((event.w,event.h),pygame.RESIZABLE)

            if event.type==pygame.KEYDOWN:
                # ── Tab = zoom in, Shift+Tab = zoom out ────────────────────
                if event.key==pygame.K_TAB:
                    mods=pygame.key.get_mods()
                    if mods & pygame.KMOD_SHIFT:
                        SCALE_IDX=max(0,SCALE_IDX-1)
                    else:
                        SCALE_IDX=min(len(SCALES)-1,SCALE_IDX+1)
                    nw,nh=get_win_size()
                    screen=pygame.display.set_mode((nw,nh),pygame.RESIZABLE)

                # ── ESC ────────────────────────────────────────────────────
                elif event.key==pygame.K_ESCAPE:
                    if state==GameMode.PLAY: state=GameMode.MENU
                    elif state==GameMode.SETTINGS: state=GameMode.MENU
                    elif state==GameMode.GAMEOVER: state=GameMode.MENU
                    else: pygame.quit(); sys.exit()

                # ── Menu ───────────────────────────────────────────────────
                elif state==GameMode.MENU:
                    if event.key in (pygame.K_UP,pygame.K_w): selected=(selected-1)%2
                    elif event.key in (pygame.K_DOWN,pygame.K_s): selected=(selected+1)%2
                    elif event.key in (pygame.K_RETURN,pygame.K_SPACE):
                        settings=Settings(selected+1); state=GameMode.SETTINGS

                # ── Settings ───────────────────────────────────────────────
                elif state==GameMode.SETTINGS:
                    result=settings.handle_key(event.key)
                    if result=='start':
                        game=Game(settings.mode,settings.diff,settings.bot_count,sounds)
                        state=GameMode.PLAY

                # ── Game over ──────────────────────────────────────────────
                elif state==GameMode.GAMEOVER:
                    if event.key==pygame.K_RETURN:
                        game=Game(game.mode,game.diff,settings.bot_count,sounds)
                        state=GameMode.PLAY

                # ── In-game shoot ──────────────────────────────────────────
                elif state==GameMode.PLAY and game:
                    if event.key==pygame.K_f:
                        game.handle_shoot('p1')
                    if event.key in (pygame.K_SLASH,pygame.K_KP_DIVIDE):
                        game.handle_shoot('p2')

        # Update
        if state==GameMode.PLAY and game:
            keys=pygame.key.get_pressed()
            game.update(keys)
            if game.over: state=GameMode.GAMEOVER

        # Draw to logical surface
        if state==GameMode.MENU:
            draw_menu(logic_surf,font,big_font,small_font,selected,blink)
        elif state==GameMode.SETTINGS:
            draw_settings(logic_surf,font,big_font,small_font,settings,blink)
        elif state==GameMode.PLAY and game:
            game.draw(logic_surf)
            draw_hud(logic_surf,font,small_font,game)
        elif state==GameMode.GAMEOVER and game:
            game.draw(logic_surf)
            draw_hud(logic_surf,font,small_font,game)
            overlay=pygame.Surface((BASE_W,BASE_H),pygame.SRCALPHA)
            overlay.fill((0,0,0,160)); logic_surf.blit(overlay,(0,0))
            draw_gameover(logic_surf,font,big_font,small_font,game.won,game.score,blink)

        # Scale logical surface → actual window
        sw,sh=screen.get_size()
        scaled=pygame.transform.scale(logic_surf,(sw,sh))
        screen.blit(scaled,(0,0))
        pygame.display.flip()

if __name__=="__main__":
    main()