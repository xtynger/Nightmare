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
CYAN2 = (0, 255, 255)
CYAN = (50, 150, 150)

# game settings
WIDTH = 800   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 600  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60


HS_FILE = "highscore.txt"

TITLE = "Nightmare Hills"
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#wall settings

WALL_IMG = 'block_06.png'
MENU = 'background.png'
GAMEOVER = 'Gameover.png'
DAYTIME = 2000
NIGHTTIME = 2000

#player settings
PLAYER_HEALTH = 100
PLAYER_ARMOR = 100
PLAYER_EXP = 1
PLAYER_LEVEL = 1
PLAYER_STAMINA = 30
PLAYER_SPEED = 250
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'survivor-idle_knife_0.png'
PLAYER_IMG1 = 'survivor-idle_handgun_0.png'
PLAYER_IMG2 = 'survivor-idle_shotgun_0.png'
PLAYER_IMG3 = 'survivor-idle_rifle_0.png'
PLAYER_CAR = 'Police.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 13)


SPRITESHEET_IDDLE_K = "iddle_knife.png"
SPRITESHEET_MOVING_K = "moving_knife.png"


NEXT_STAGE_IMAGE = "next.png"



#WEAPON settings
BULLET_IMG = 'bullet1.png'
WEAPONS = {}

WEAPONS['knife'] = {'bullet_speed': 0,
                     'bullet_lifetime': 0,
                     'rate': 0,
                     'kickback': 50,
                     'spread': 5,
                     'damage': 50,
                     'bullet_size': 'sm',
                     'bullet_count': 1,
                     'charger_size': 0}




WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 15,
                     'bullet_size': 'lg',
                     'bullet_count': 1,
                     'charger_size': 9}

WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12,
                      'charger_size': 8}

WEAPONS['rifle'] = {'bullet_speed': 700,
                      'bullet_lifetime': 1000,
                      'rate': 100,
                      'kickback': 300,
                      'spread': 7,
                      'damage': 8,
                      'bullet_size': 'sm',
                      'bullet_count': 1,
                      'charger_size': 30}

WEAPONS['vehicle'] = {'gas': 700,
                      'kickback': 300,
                      'damage': 8,
                      'bullet_count': 0,
                      'charger_size': 300}

WEAPONS['medkit'] = {'health': 80,
                    'ammount': 0}
#enemy settings

MOB_IMG = 'skeleton-attack_0.png'
MOB_SPEEDS = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 40
MOB_ARMOR = 30
MOB_EXP = 100
#
AVOID_RADIUS = 70
DETECT_RADIUS = 400

#EFFECTS

MUZZLE_FLASHES = ['m_1.png', 'm_2.png', 'm_3.png', 'm_4.png',
				 'm_5.png', 'm_6.png', 'm_7.png', 'm_8.png',
				  'm_9.png', 'm_10.png', 'm_11.png', 'm_12.png',
				   'm_13.png', 'm_14.png', 'm_15.png', 'm_16.png', ]



IDDLE_KNIFE = ['sik00.png','sik01.png', 'sik02.png', 'sik03.png', 'sik04.png',
				 'sik05.png', 'sik06.png', 'sik07.png', 'sik08.png',
				  'sik09.png', 'sik010.png', 'sik011.png', 'sik012.png',
				   'sik013.png', 'sik014.png', 'sik015.png', 'sik016.png',
				   'sik017.png', 'sik018.png', 'sik019.png' ]

MOVE_KNIFE = ['survivor-move_knife_0.png', 'survivor-move_knife_0.png', 'survivor-move_knife_0.png', 
              'survivor-move_knife_0.png', 'survivor-move_knife_0.png', 'survivor-move_knife_0.png', 
              'survivor-move_knife_0.png', 'survivor-move_knife_0.png', 'survivor-move_knife_0.png', 
              'survivor-move_knife_0.png', 'survivor-move_knife_0.png', 'survivor-move_knife_0.png', 
              'survivor-move_knife_0.png', 'survivor-move_knife_0.png', 'survivor-move_knife_0.png', 
              'survivor-move_knife_0.png', 'survivor-move_knife_0.png', 'survivor-move_knife_0.png', 
              'survivor-move_knife_0.png' ]



SPLAT_IMAGE = 'red_splat.png'
SPLIT = 'split.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 50)] #to draw a values list, form 1st value, to 2nd value, in steps of 3rd value, gonna use it on drawing dmg color
NIGHT_COLOR = (15,15,15)
LIGHT_RADIUS = (250, 250)
LIGHT_MASK = "shadow3.png"
ALPHA = 0.5

#Layers 
WALL_LAYER = 1
ITEMS_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
BULLET_LAYER = 3
EFFECTS_LAYER = 4


#SLOTS FOR ITEMS

PISTOL = 'pistol.png'
RIFLE = 'ak3.png'
SHOTGUN = 'shotgun.png'
SLOTS = 'SLOTS.png'
MEDKIT = 'medikit.png'
BACKPACK = 'backpack.png'
INVENTORY = 'inventory5.png'

LIVES_IMAGE = 'burger.png'
#Items 
ITEM_IMAGES = {'health': 'medikit.png',
			   'shotgun': 'shotgunA.png',
			   'rifle': 'ak3.png',
			   'pistol': 'pistol.png',
			   'shotgun_ammo': 'shotgun_ammo.png',
			   'pistol_ammo': 'pistol_ammo.png',
			   'rifle_ammo': 'rifle_ammo.png',
         'vehicle': 'Police.png'}

HEALTH_PACK_AMOUNT = 75
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
				 'shotgun': ['shotgun.wav'],
				 'rifle': ['rifle.wav']}


WEAPON_SOUNDS_GUN = ['sfx_weapon_singleshot2.wav']
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
				  'health_up': 'health_pack.wav',
				  'no_ammo': 'dry.wav',
				  'gun_pickup': 'sfx_weapon_singleshot2.wav'}


#ANIMATION FILES

                                                                                            
#EFFECTS_SOUNDS = 