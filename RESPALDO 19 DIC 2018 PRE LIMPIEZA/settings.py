import pygame as pg
vec = pg.math.Vector2


# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (93, 109, 126)
GRAY = (128,128,128)
LIGHTGREY = (180,180,180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARKRED = (140, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
LIGHT_BLUE = (0,191,255)
LIGHT_BLUE2 = (0,150,255)
LIGHT_BLUE3 = (0,100,255)
LIGHT_BLUE4 = (0,50,255)
BROWN_CHOCOLATE = (210,105,30)
WHITE_AZURE = (240,255,255)
CYAN_LESS = (0,10,0)
# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 600  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60

MSG_DELAY = 5000
TIME_COUNT = 0

CD = 5000

HS_FILE = "highscore.txt"

TITLE = "Nightmare Hills"
BGCOLOR = DARKGRAY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

#wall settings

WALL_IMG = 'block_06.png'
MENU = 'background.png'
MENU2 = 'next.png'
GAMEOVER = 'Gameover.png'
VICTORY = 'victory.png'
CLOCK = 'clock.png'
STATMENU = 'statmenu.png'
STATMENU2 = 'stats2.png'
HUD_BARS_BACKGROUND = 'colorlessbackground.png'

DAYTIME = 0
NIGHTTIME = 0
CYCLE_CLOCK = 30000

RELOADING_TIME = 0
RELOADED_TIME = 0
RELOADING_CYCLE = 1000

########### ZOMBIE CLOCKS ##########

ATTACK_DELAY = 0
ATTACK_DURATION = 0
ATTACK_CYCLE = 2000
ATTACK_CLOCK = 0
#############################

#player settings
PLAYER_HEALTH = 50
PLAYER_HEALTH_CURRENT_CAP = 50
PLAYER_ARMOR = 0.1
PLAYER_SPEED = 50
PLAYER_RADIUS = 60
PLAYER_KNOCKBACK = 100
PLAYER_ROT_SPEED = 150
PLAYER_STAMINA = 100
PLAYER_STAMINA_CAP = 100
PLAYER_THIRST = 100
PLAYER_HUNGER = 100

PLAYER_STAT_POINTS = 0
PLAYER_SKILL_POINTS = 0
PLAYER_EXP = 0
PLAYER_LVL = 1
PLAYER_EXP_CAP = 50

BARREL_OFFSET = vec(30, 13)
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# PLAYER STATS
STRENGHT = 5  #health, armor, damage reduction
DEXTERITY = 5 #speed, turn speed, acceleration
LUCK = 5  #accuracy, critical, damage


#PLAYER IMAGES

PLAYER_IMG = 'idle_player.png'
PLAYER_IMG1 = 'survivor-idle_handgun_0.png'
PLAYER_IMG2 = 'survivor-idle_shotgun_0.png'
PLAYER_IMG3 = 'survivor-idle_rifle_0.png'
PLAYER_CAR = 'Police.png'



### C  L O C K   S E T T I N G S ###



#WEAPON settings
BULLET_IMG = 'bullet1.png'
WEAPONS = {}


WEAPONS['knife'] = { 'name': 'knife',
                     'bullet_speed': 0,
                     'bullet_lifetime': 0,
                     'rate': 0,
                     'kickback': 0,
                     'spread': 5,
                     'damage': 20,
                     'bullet_size': 'sm',
                     'bullet_count': 1,
                     'charger_size': 0,
                     'description': 'A steel knive from the special forces',
                     'magazine': 0,
                     'img': 'knife.png',
                     'rect': 'img.get_rect()'}

WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 30,
                     'spread': 5,
                     'damage': 15,
                     'bullet_size': 'lg',
                     'bullet_count': 1,
                     'charger_size': 9,
                     'description': 'A decent 9mm pistol, this will be good for now.',
                     'magazine:': 2,

                      'charger_size': 9, #cargador maximo
                      'gun_comb': 0, #cargador actual
                      'total_bullets': 0} #total de balas guardadas


WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12,
                      'charger_size': 1,
                      'description': 'Great, some firepower to beat this things.',
                      'magazine:': 9,
                      'shells' : 1,
                      
                      'charger_size': 8, #cargador maximo
                      'gun_comb': 0, #cargador actual
                      'total_bullets': 0} #total de balas guardadas


WEAPONS['rifle'] = {'bullet_speed': 3000,
                      'bullet_lifetime': 1000,
                      'rate': 100,
                      'kickback': 70,
                      'spread': 5,
                      'damage': 8,
                      'bullet_size': 'sm',
                      'bullet_count': 1,
                      'description': 'Hump.. seems like this is gonna be my best friend for a while.',

                      'charger_size': 30, #cargador maximo
                      'gun_comb': 0, #cargador actual
                      'total_bullets': 0} #total de balas guardadas

WEAPONS['vehicle'] = {'gas': 700,
                      'kickback': 300,
                      'damage': 8,
                      'kickback': 300,
                      'bullet_count': 0,
                      'charger_size': 300
                      }

WEAPONS['hand'] = {'damage': 0, 
                    'charger_size': 0,
                    'description': 'Is just my bare hands... i need to get a real weapon quick.',
                    'magazine': 0}

WEAPONS['medkit'] = {'health': 80,
                    'ammount': 0}

WEAPONS['kevlar'] = {'armor': 50,
                    'ammount': 0}

#enemy settings

MOB_IMG = 'skeleton-attack_0.png'
MOB_SPEEDS = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100000
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
MOB_ATK_DURATION = 3000
MOB_ATK_RANGE = 200
AVOID_RADIUS = 70
DETECT_RADIUS = 400

#EFFECTS
###### SPRITESHEETS #####
# HAND
SPRITESHEET_IH = 'idle_hand.png'
#KNIFE
SPRITESHEET_IK = 'iddle_knife.png'
SPRITESHEET_WK = 'walking_knife.png'
SPRITESHEET_AK = 'attacking_knife.png'

#PISTOL
SPRITESHEET_IP = 'idle_pistol.png'
SPRITESHEET_WP = 'walking_pistol.png'
#RIFLE
SPRITESHEET_IR = 'idle_rifle.png'
SPRITESHEET_WR = 'walking_rifle.png'
SPRITESHEET_AR = 'shoting_ak.png'
#SHOTGUN
SPRITESHEET_AS = 'attacking_shotgun.png'
SPRITESHEET_WS = 'walking_shotgun.png'
SPRITESHEET_IS = 'idle_shotgun.png'
#SPRITEHSEET_MS

SPRITESHEET_IZ = 'idle_zombie.png'
SPRITESHEET_WZ = 'moving_zombie.png'
SPRITESHEET_AZ = 'attacking_zombie.png'

               #'rifle': 'ak3.png',
               #'pistol': 'pistol.png',
               #'shotgun_ammo': 'shotgun_ammo.png',
               #'pistol_ammo': 'pistol_ammo.png',
               #'rifle_ammo': 'rifle_ammo.png',
               #'vehicle': 'Police.png'}



MUZZLE_FLASHES = ['m_1.png', 'm_2.png', 'm_3.png', 'm_4.png',
				 'm_5.png', 'm_6.png', 'm_7.png', 'm_8.png',
				  'm_9.png', 'm_10.png', 'm_11.png', 'm_12.png',
				   'm_13.png', 'm_14.png', 'm_15.png', 'm_16.png', ]

EXPLOSION_IMAGE = ['RE00.png', 'RE01.png', 'RE02.png', 'RE03.png', 'RE04.png', 
                  'RE05.png', 'RE06.png', 'RE07.png', 'RE08.png', ]




SPLAT_IMAGE = 'red_splat.png'
SPLIT = 'split.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 50)] #to draw a values list, form 1st value, to 2nd value, in steps of 3rd value, gonna use it on drawing dmg color
NIGHT_COLOR = (15,15,15)
LIGHT_RADIUS = (350, 350)
LIGHT_MASK = "shadow.png"
ALPHA = 0.9

#Layers 
WALL_LAYER = 1
ITEMS_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
BULLET_LAYER = 3
EFFECTS_LAYER = 4
MAIN_LAYER = 6

#SLOTS FOR ITEMS

PISTOL = 'pistol.png'
RIFLE = 'ak3.png'
SHOTGUN = 'shotgun.png'
SLOTS = 'SLOTS.png'
MEDKIT = 'medikit.png'
TEXT_SLOT = 'chat_bar.png'
KEVLAR = 'armor.png'
KNIFE = 'knife.png'
SHIELD_ICON = 'shield.png'
HEALTH_ICON = 'cure.png'
STAMINA_ICON = 'point.png'
WATER_ICON = 'water.png'
FOOD_ICON = 'burger.png'


LIVES_IMAGE = 'burger.png'
#Items 
ITEM_IMAGES = {'health': 'medikit.png',
         'shotgun': 'shotgunA.png',
         'rifle': 'ak3.png',
         'pistol': 'pistol.png',
         'shotgun_ammo': 'shotgun_ammo.png',
         'pistol_ammo': 'pistol_ammo.png',
         'rifle_ammo': 'rifle_ammo.png',
         'vehicle': 'Police.png',
         'kevlar': 'armor.png',
         'knife': 'knife.png',
         'food': 'foodbag.png'}




HEALTH_PACK_AMOUNT = 75
BOB_RANGE = 15
BOB_SPEED = 0.6

#MUSIC AND SOUNDS
BG_MUSI2 = 'espionage.ogg'
BG_MUSIC = 'suspense_city.ogg'

MENU_MUSIC = 'suspense_menu.ogg'

PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']

ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
					  'zombie-roar-3.wav', 'zombie-roar-4.wav', 'zombie-roar-5.wav',
					  'zombie-roar-6.wav', 'zombie-roar-7.wav']

ZOMBIE_HIT_SOUNDS = ['splat-15.wav']

WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
        				 'shotgun': ['shotgun.wav'],
        				 'rifle': ['rifle.wav'],
                 'knife': ['knife_attack1.wav', 'knife_attack2.wav']}


WEAPON_SOUNDS_GUN = ['sfx_weapon_singleshot2.wav']

EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
				  'health_up': 'health_pack.wav',
				  'no_ammo': 'dry.wav',
				  'gun_pickup': 'sfx_weapon_singleshot2.wav',
          'no_clip': 'empty_gun.ogg',
          'reloading_rifle': 'rifle_reload.wav',
          }


#SHOP ITEMS AND FILES

ITEMS = {'health': ['medikit.png'],
         'shotgun': ['shotgunA.png'],
         'rifle': ['ak3.png'],
         'pistol': ['pistol.png'],
         'shotgun_ammo': ['shotgun_ammo.png'],
         'pistol_ammo': ['pistol_ammo.png'],
         'rifle_ammo': ['rifle_ammo.png']}




INVENTORY = 'inventory2.png'
INVENTORY_SLOT = 'inventory_slot.png'
INVENTORY_BIG_SLOT = 'big_slot.png'

