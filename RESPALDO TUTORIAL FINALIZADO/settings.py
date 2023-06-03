import pygame as pg
vec = pg.math.Vector2


# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARKRED = (140, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
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
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'survivor-idle_handgun_0.png'
PLAYER_IMG2 = 'survivor-idle_shotgun_0.png'
PLAYER_IMG3 = 'survivor-idle_rifle_0.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(35, 10)


#WEAPON settings
BULLET_IMG = 'bullet1.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
'bullet_count': 1}

WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
'bullet_count': 12}

#enemy settings

MOB_IMG = 'skeleton-attack_0.png'
MOB_SPEEDS = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 40
AVOID_RADIUS = 50
DETECT_RADIUS = 400

#EFFECTS

MUZZLE_FLASHES = ['m_1.png', 'm_2.png', 'm_3.png', 'm_4.png',
				 'm_5.png', 'm_6.png', 'm_7.png', 'm_8.png',
				  'm_9.png', 'm_10.png', 'm_11.png', 'm_12.png',
				   'm_13.png', 'm_14.png', 'm_15.png', 'm_16.png', ]

SPLAT_IMAGE = 'red_splat.png'
SPLIT = 'split.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 50)] #to draw a values list, form 1st value, to 2nd value, in steps of 3rd value, gonna use it on drawing dmg color
NIGHT_COLOR = (15,15,15)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "fog3.png"

#Layers 
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

#Items 
ITEM_IMAGES = {'health': 'medikit.png',
			   'shotgun': 'shotgun3.png'}

HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.6

#MUSIC AND SOUNDS
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
					  'zombie-roar-3.wav', 'zombie-roar-4.wav', 'zombie-roar-5.wav',
					  'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
				 'shotgun': ['shotgun.wav']}


WEAPON_SOUNDS_GUN = ['sfx_weapon_singleshot2.wav']
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
				  'health_up': 'health_pack.wav',
				  'gun_pickup': 'sfx_weapon_singleshot2.wav'}


#EFFECTS_SOUNDS = 