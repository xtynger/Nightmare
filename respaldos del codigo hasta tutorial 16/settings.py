import pygame as pg
vec = pg.math.Vector2
import random
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 800   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 600  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#wall settings

WALL_IMG = 'block_06.png'

#player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(35, 10)
KICKBACK = 5
GUN_SPREAD = 5
BULLET_DAMAGE = 10

#Gun settings
BULLET_IMG = 'light_bullet.png'
BULLET_SPEED = 300
BULLET_LIFETIME = 2000
BULLET_RATE = 10

#enemy settings

MOB_IMG = 'zoimbie1_hold.png'
MOB_SPEEDS = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 10
AVOID_RADIUS = 50

#EFFECTS

MUZZLE_FLASHES = ['m_1.png', 'm_2.png', 'm_3.png', 'm_4.png',
				 'm_5.png', 'm_6.png', 'm_7.png', 'm_8.png',
				  'm_9.png', 'm_10.png', 'm_11.png', 'm_12.png',
				   'm_13.png', 'm_14.png', 'm_15.png', 'm_16.png', ]
FLASH_DURATION = 30

#Layers 
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

#Items 
ITEM_IMAGES = {'health': 'medikit.png'}
HEALTH_PACK_AMOUNT = 20