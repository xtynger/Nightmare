import pygame as pg
import sys
from random import choice, random
from os import path
from settings import *
from sprites import *
from tilemap import *
from pygame.locals import *
import time



#HUD functions


    

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048) # TO PRELOAD MIXED AND USE CUSTOM SETTINGS FOR IT
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        #sdpg.key.set_repeat(500, 100)
        self.load_data()
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((100, 0, 0, 180))






    def draw_text(self, text, font_name, size, color, x, y, align):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

 

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        self.music_folder = path.join(game_folder, 'music')

        ########TO SAVE HIGHSCORE############################
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        #######################################################        #######################################################        #######################################################

        self.map_folder = path.join(game_folder, 'maps')
        self.tittle_font = path.join(img_folder, 'zombie.ttf')
        self.extra_font = path.join(img_folder, 'ferrum.otf')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')

        self.spritesheet_a = Spritesheet(path.join(img_folder, SPRITESHEET_IK)) ############## TEST 
        self.spritesheet_b = Spritesheet(path.join(img_folder, SPRITESHEET_WK)) ############## TEST 
        self.spritesheet_c = Spritesheet(path.join(img_folder, SPRITESHEET_AK)) ############## TEST 
        self.spritesheet_d = Spritesheet(path.join(img_folder, SPRITESHEET_AR)) ############## TEST 
        self.spritesheet_e = Spritesheet(path.join(img_folder, SPRITESHEET_IR)) ############## TEST 
        self.spritesheet_wr = Spritesheet(path.join(img_folder, SPRITESHEET_WR)) ############## TEST 

        
        
        self.spritesheet_iz = Spritesheet(path.join(img_folder, SPRITESHEET_IZ)) ############## TEST 
        self.spritesheet_wz = Spritesheet(path.join(img_folder, SPRITESHEET_WZ)) ############## TEST 
        self.spritesheet_az = Spritesheet(path.join(img_folder, SPRITESHEET_AZ)) ############## TEST
        self.spritesheet_as = Spritesheet(path.join(img_folder, SPRITESHEET_AS)) ############## TEST

        self.spritesheet_ip = Spritesheet(path.join(img_folder, SPRITESHEET_IP)) ############## TEST 
        self.spritesheet_is = Spritesheet(path.join(img_folder, SPRITESHEET_IS)) ############## TEST 
        self.spritesheet_wp = Spritesheet(path.join(img_folder, SPRITESHEET_WP)) ############## TEST 
        self.spritesheet_ws = Spritesheet(path.join(img_folder, SPRITESHEET_WS)) ############## TEST 

        self.spritesheet_ih = Spritesheet(path.join(img_folder, SPRITESHEET_IH)) ############## TEST 


        #######################################################        #######################################################        #######################################################

        self.menu = pg.image.load(path.join(img_folder, MENU))
        self.menu = pg.transform.scale(self.menu, (WIDTH, HEIGHT))
        self.menu_rect = self.menu.get_rect()

        self.menu2 = pg.image.load(path.join(img_folder, MENU2))
        self.menu2_rect = self.menu2.get_rect()

        self.gameover = pg.image.load(path.join(img_folder, GAMEOVER))
        self.gameover = pg.transform.scale(self.gameover, (1000,600))
        self.gameover_rect = self.gameover.get_rect()

        self.hud_bar1 = pg.image.load(path.join(img_folder, HUD_BARS_BACKGROUND))
        self.hud_bar1 = pg.transform.scale(self.hud_bar1, (120,130))
        self.hud_bar1_rect = self.hud_bar1.get_rect()

        self.victory = pg.image.load(path.join(img_folder, VICTORY))
        self.victory = pg.transform.scale(self.victory, (1000,600))
        self.victory_rect = self.victory.get_rect()


        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((100, 0, 0, 100))
        self.dim_screen2 = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen2.fill((20, 0, 0, 150))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, (90,70))
        self.player_img1 = pg.image.load(path.join(img_folder, PLAYER_IMG1)).convert_alpha()
        self.player_img1 = pg.transform.scale(self.player_img1, (80,60))
        self.player_img2 = pg.image.load(path.join(img_folder, PLAYER_IMG2)).convert_alpha()
        self.player_img2 = pg.transform.scale(self.player_img2, (90,70))
        self.player_img3 = pg.image.load(path.join(img_folder, PLAYER_IMG3)).convert_alpha()
        self.player_img3 = pg.transform.scale(self.player_img3, (80,60))
     
        self.shield_icon = pg.image.load(path.join(img_folder, SHIELD_ICON )).convert_alpha()
        self.shield_icon = pg.transform.scale(self.shield_icon, (30, 30))
        self.shield_rect = self.shield_icon.get_rect()
        
        self.health_icon = pg.image.load(path.join(img_folder, HEALTH_ICON )).convert_alpha()
        self.health_icon = pg.transform.scale(self.health_icon, (30, 30))
        self.health_rect = self.health_icon.get_rect()
        
        self.stamina_icon = pg.image.load(path.join(img_folder, STAMINA_ICON )).convert_alpha()
        self.stamina_icon = pg.transform.scale(self.stamina_icon, (30, 30))
        self.stamina_rect = self.stamina_icon.get_rect() 

        self.water_icon = pg.image.load(path.join(img_folder, WATER_ICON )).convert_alpha()
        self.water_icon = pg.transform.scale(self.water_icon, (30, 30))
        self.water_rect = self.water_icon.get_rect()        

        self.food_icon = pg.image.load(path.join(img_folder, FOOD_ICON )).convert_alpha()
        self.food_icon = pg.transform.scale(self.food_icon, (20, 20))
        self.food_rect = self.food_icon.get_rect()

################### ################### ################### ################### ################### ################### ################### ################### 
#################### C O D E   T O   S E T    I M A G E S   T O   B E   D R A W N, IT MUST INCLUDE ITS RECT TOO #############################################

        self.slots_img = pg.image.load(path.join(img_folder, SLOTS)).convert_alpha()
        self.slots_img = pg.transform.scale(self.slots_img, (90  , 60))
        self.slots_rect = self.slots_img.get_rect()

        self.slots2_img = pg.image.load(path.join(img_folder, SLOTS)).convert_alpha()
        self.slots2_img = pg.transform.scale(self.slots2_img, (90  , 60))
        self.slots2_rect = self.slots2_img.get_rect()


        self.pistol_slot = pg.image.load(path.join(img_folder, PISTOL)).convert_alpha()
        self.pistol_slot = pg.transform.scale(self.pistol_slot, (40, 30))
        self.pistol_rect = self.pistol_slot.get_rect()
        

        self.shotgun_slot = pg.image.load(path.join(img_folder, SHOTGUN)).convert_alpha()
        self.shotgun_slot = pg.transform.scale(self.shotgun_slot, (100, 20))
        self.shotgun_rect = self.shotgun_slot.get_rect()

        self.rifle_slot = pg.image.load(path.join(img_folder, RIFLE)).convert_alpha()
        self.rifle_slot = pg.transform.scale(self.rifle_slot, (50, 20))
        self.rifle_rect = self.rifle_slot.get_rect()

        self.medkit_slot = pg.image.load(path.join(img_folder, MEDKIT))
        self.medkit_slot = pg.transform.scale(self.medkit_slot, (40, 25))
        self.medkit_rect = self.medkit_slot.get_rect() 

        self.text_slot = pg.image.load(path.join(img_folder, TEXT_SLOT)).convert_alpha()
        self.text_slot = pg.transform.scale(self.text_slot, (800, 120))
        self.text_rect = self.text_slot.get_rect()

        self.lives_img = pg.image.load(path.join(img_folder, LIVES_IMAGE)).convert_alpha()
        #self.lives_img = pg.transform.scale(self.lives_img, (60, 25))
        self.lives_rect = self.lives_img.get_rect()

        self.kevlar = pg.image.load(path.join(img_folder, KEVLAR)).convert_alpha()
        self.kevlar_rect = self.kevlar.get_rect()

        #self.knife = pg.image.load(path.join(img_folder, KNIFE)).convert_alpha()
       # self.knife_rect = self.knife.get_rect()

        self.knife_slot = pg.image.load(path.join(img_folder, KNIFE)).convert_alpha()
        self.knife_slot = pg.transform.scale(self.knife_slot, (50, 30))
        self.knife_rect = self.knife_slot.get_rect()

        self.clock_slot =  pg.image.load(path.join(img_folder, CLOCK)).convert_alpha()
        self.clock_slot = pg.transform.scale(self.clock_slot, (100, 30))
        self.clock_rect = self.clock_slot.get_rect()

################### ################### ################### ################### ################### ################### ################### ################### 
##################### ################### ################### I N V E N T A R I O  ################### ################### ################### ################### 

        self.inventory = pg.image.load(path.join(img_folder, INVENTORY)).convert_alpha()
       # self.inventory = pg.transform.scale(inventory, (750,650))
        self.inventory_rect = self.inventory.get_rect()

        self.inventory_slot = pg.image.load(path.join(img_folder,INVENTORY_SLOT)).convert_alpha()
        self.inventory_slot_rect = self.inventory_slot.get_rect()

        self.big_slot = pg.image.load(path.join(img_folder, INVENTORY_BIG_SLOT)).convert_alpha()
        self.big_slot_rect = self.big_slot.get_rect()



################### ################### ################### ################### ################### ################### ################### ################### 
##################### ########## P R U E B A  P A R A   E X P L O S I O N E S ################ ################### ################### ################### 
       

        self.statmenu = pg.image.load(path.join(img_folder, STATMENU))
        self.statmenu_rect = self.statmenu.get_rect()



        self.statmenu2 = pg.image.load(path.join(img_folder, STATMENU2))
        self.statmenu2_rect = self.statmenu2.get_rect()




##################### ################### ################### ################### ################### ################### ################### ################### 



        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (5,5)) 

        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE ))
        self.splat = pg.image.load(path.join(img_folder, SPLAT_IMAGE)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (100, 100))
        self.split = pg.image.load(path.join(img_folder, SPLIT)).convert_alpha()



        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())

        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
            
        #FOR NIGHT EFFECT AND FOG
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()

       # self.light_mask = pg.image.transform().convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        ##########################Sounds Loading ##################################################

        #pg.mixer.music.set_volume(1.0)
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))

        #SOUNDS LOADING WEAPONS
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)


        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.3)
            self.zombie_moan_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

    def player_spawn(self):
        for tile_object in self.map.tmxdata.objects: #el parametro .objects es para usar esa capa especifica de objetos que creamos
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player': #ESTO INDICA DONDE DIBUJAR EL PLAYER
                self.player = Player(self, obj_center.x, obj_center.y)

    def zombie_spawn(self):
        for tile_object in self.map.tmxdata.objects: #el parametro .objects es para usar esa capa especifica de objetos que creamos
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'zombie': #ESTO INDICA DONDE DIBUJAR EL ENEMIGO
                Mob(self, obj_center.x, obj_center.y)

    def wall_spawn(self):
                
        for tile_object in self.map.tmxdata.objects: #el parametro .objects es para usar esa capa especifica de objetos que creamos
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,  #ESTO DA FORMA FISICA COLISIONABLE A LOS RECTANGULOS QUE DIBUJES COMO EL NOMBRE SE;ALADO
                             tile_object.width, tile_object.height)
    def item_spawn(self):
        for tile_object in self.map.tmxdata.objects: #el parametro .objects es para usar esa capa especifica de objetos que creamos
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name in ['health', 'shotgun', 'rifle', 'pistol', 'shotgun_ammo', 'pistol_ammo', 'rifle_ammo', 'kevlar', 'knife', 'food']:
                Item(self, obj_center, tile_object.name)

    def chat_spawn(self):
        for tile_object in self.map.tmxdata.objects: #el parametro .objects es para usar esa capa especifica de objetos que creamos
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'chat':
                Obstacle(self,tile_object.x, tile_object.y,
                                tile_object.width, tile_object.height)

    def game_flags(self):
        self.draw_debug = False
        self.paused = False
        self.night = False
        self.day = True
        self.gun = False
        self.shotgun = False
        self.rifle = False
        self.knife = False 
        self.shop = False
        self.click = False
        self.text = False
        self.attacking_zombie = False
        self.intro_message = True
        self.pulse_watch = False
        self.char_tab = False


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.chats = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'tile1.xml'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_spawn()
        self.zombie_spawn()
        self.item_spawn()
        self.chat_spawn()
        self.wall_spawn()
        self.game_flags()
        pg.mixer.music.load(path.join(self.music_folder, BG_MUSIC))
        #pg.mixer.music.load(path.join(self.music_folder, MENU_MUSIC))
        pg.mixer.music.set_volume(20)


        self.camera = Camera(self.map.width , self.map.height) #para insertar la "camara" al movimiento
        #self.effects_sounds['level_start'].play()


    def temp_text(self):
        self.alive = True
        pg.mixer.music.play(loops=-1)
        timer = pg.time.Clock()
        timer.tick()
        self.time_count = TIME_COUNT
        self.message_delay = MSG_DELAY
        #self.intro()
        while self.alive:

            self.time_count += timer.tick()
            if self.time_count  < self.message_delay:
                try:
                    self.text = True
                    print(self.time_count, 'less')
                except:
                    pass


    def action(self):
        self.text = True
        self.time_count = 0



    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        #self.intro()
        ########################### G A M E   L O O P   F O R   C L O C K ############
      

        while self.playing:



            ######################################################################################
            #for D in range(0,7):

            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            #self.player.day_night_clock()
            if not self.paused:
                self.update()
            self.draw()



    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player) #CHANGE THE OBJECT AND THE CAMERA WILL FOLLOW IT
        self.mouse_pos = pg.mouse.get_pos()
        self.collisions()
        #game over?
        if len(self.mobs) == 0:
            self.playing = False




    def collisions(self):

#################################### P L A Y E R   H I T S    W E A P O N S###################################

        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            self.action()
            if hit.type == 'knife':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'knife'
                self.knife = True


            if hit.type == 'pistol':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'pistol'
                self.gun = True

            if hit.type == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
                self.shotgun = True

            if hit.type == 'rifle':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'rifle'
                self.rifle = True



##############################################################################################################################
######################### I F   P L A Y E R   H I T S   A M M O   I T E M S ##################################################
##############################################################################################################################


            if hit.type == 'health':
                hit.kill()
                self.effects_sounds['health_up'].play()
                WEAPONS['medkit']['ammount'] += 1
            




            if hit.type == 'kevlar' and self.player.armor < 100:
               
                hit.kill()
                self.player.add_armor(WEAPONS['kevlar']['armor'])
                self.effects_sounds['health_up'].play()


            if hit.type == 'pistol_ammo':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                #WEAPONS[self.player.weapon]['charger_size'] += randint(5, 20)             ##### LINEA CORRECTA FUNCIONAL, COMENTADA PARA HACER PRUEBAS
                WEAPONS['pistol']['total_bullets'] += randint(5, 20)

            if hit.type == 'shotgun_ammo': #and self.player.weapon == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                #WEAPONS[self.player.weapon]['charger_size'] += randint(24, 68)             ##### LINEA CORRECTA FUNCIONAL, COMENTADA PARA HACER PRUEBAS                                     
                WEAPONS['shotgun']['total_bullets'] += randint(24, 68)


            if hit.type == 'rifle_ammo': #and self.player.weapon == 'rifle':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                #WEAPONS[self.player.weapon]['charger_size'] += randint(20, 60)             ##### LINEA CORRECTA FUNCIONAL, COMENTADA PARA HACER PRUEBAS                 
                WEAPONS['rifle']['total_bullets'] += randint(20, 60)


############################### M O B S   H I T S   P L A Y E R #############################################################

        #Mobs hit Player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        #COPIA DE LINEA ORIGINAL      hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)       
        ######### PERFECT PIXEL COLLISSION HAPPENNING HERE ##############
        #collide_circle_ratio(0.7) FOR RADIAL CHANGE FOR THIS
        for hit in hits:
            self.player.attacked = True
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.armor -= MOB_DAMAGE / 2
            hit.vel = vec(0, 0)
            self.mobs.attacking = True
            if self.player.armor <= 0:
                self.player.health -= MOB_DAMAGE
                if self.player.health <= 0:
                    self.player.lives -= 1
                    self.player.health = PLAYER_HEALTH
                    self.player.armor = PLAYER_ARMOR 
                    self.player.pos = [68.3694, 701.876]   #NECESARIO MEJORAR ESTE CODIGO
            if self.player.lives == -1:
                self.playing = False


        if hits and not self.player.attacking:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

############## C O D I G O   P R O P I O   P A R A    H A C E R   D A Ñ O    C O N    C U C H I L L O  ############### ############
####################################### ############################## ################################ ###########################           
        hits = pg.sprite.spritecollide(self.player, self.mobs , False, pg.sprite.collide_mask)     
        #COPIA DE LINEA ORIGINAL      hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)    
        ######### PERFECT PIXEL COLLISSION HAPPENNING HERE ###############
        # collide_circle_ratio(0.7) FOR RADIAL CHANGE FOR THIS
        if self.player.attacking:
            for hit in hits:
                hit.health -= WEAPONS[self.player.weapon]['damage']
                hit.vel = vec(0, 0)
                for mob in self.mobs:
                    mob.pos -= vec(PLAYER_KNOCKBACK, 0).rotate(-hits[0].rot)
                    #mob.vel = vec(0,0)

####################################  B U L L E T S   H I T S   M O B S ##############################################################
        #Bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            hit.vel = vec(0, 0)
            self.player.score += 2 
            self.player.exp += 10

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        #draw the light mask (gradient) onto de fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center 


        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0,0), special_flags=pg.BLEND_MULT)

    def draw_player_armor(self,surf, x, y, pct):
        #timer = pg.time.Clock()
        #time_count = 0
        #timer.tick()
        if pct < 0:
            pct = 0
        BAR_LENGHT = 100
        BAR_HEIGHT = 10
        fill = pct * BAR_LENGHT
        outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill,BAR_HEIGHT)
        #if pct > 0.6:
        col = DARKGRAY
        #elif pct > 0.3:
           # col = YELLOW
        #else:
            #col = RED
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)


    def draw_player_health(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGHT = PLAYER_HEALTH_CURRENT_CAP
        BAR_HEIGHT = 10
        fill = pct * BAR_LENGHT
        outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill,BAR_HEIGHT)
        if pct > 0.6:
            col = GREEN
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)


    def draw_player_stamina(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGHT = 100
        BAR_HEIGHT = 10
        fill = pct * BAR_LENGHT
        outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill,BAR_HEIGHT)
        col = CYAN
        for i in str(BAR_LENGHT):
            if pct > 0.8:
                col = CYAN
            elif pct > 0.6:
                col = LIGHT_BLUE
            elif pct > 0.4:
                col = LIGHT_BLUE2
            elif pct > 0.2:
                col = LIGHT_BLUE3
            else:
                col = LIGHT_BLUE4
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)
            
    def draw_player_water(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGHT = 100
        BAR_HEIGHT = 10
        fill = pct * BAR_LENGHT
        outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill,BAR_HEIGHT)
        if pct > 0.6:
            col = LIGHT_BLUE
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)
            
    def draw_player_food(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGHT = 100
        BAR_HEIGHT = 10
        fill = pct * BAR_LENGHT
        outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill,BAR_HEIGHT)
        if pct > 0.6:
            col = BROWN_CHOCOLATE
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)    

    def draw_player_exp(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGHT = 600
        BAR_HEIGHT = 10
        fill = pct * BAR_LENGHT
        outline_rect = pg.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill,BAR_HEIGHT)


        if pct > 0.6:
            col = YELLOW
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        pg.draw.rect(surf, col, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)

            
######################## PARA HACER REGENERAR AUTOMATICAMENTE LA BARRA #############################

        #if self.player.armor != 100:
            #timer.tick()
            #time_count += timer.tick()
            #self.player.armor += (max(1,min(BAR_LENGHT, 1)))  #IMPORTANTE PARA ESTABLECER LIMITE DE CRECIMIENTO PARA BARRAS
            
            #if self.player.armor >= 100:
                #time_count = 0
                #timer.tick()

###########################################C O D I G O    P E R S O N A L ###############################################       
############################################## E N   A D E L A N T E ####################################################
################F U N C I O N A L   T O   D R A W   I M A G E S,  IN THIS CASE, LIVES, SLOTS AND MORE ###################
######################### T O   D R A W   S L O T S   A N D   N A M E S    I N   S C R E E N ############################
################### T O    D R A W    W E A P O N  S L O T S  W H E N   P I C K   W E A P O N S  3/3 ####################


    def slot_clock(self):  
        self.screen.blit(self.slots_img, (400 , HEIGHT - 400), self.slots_rect)  #dibujar cuadros transparentes
        self.slots_img.fill((20,20,20,150))  #rellenar los cuadros
        self.screen.blit(self.clock_slot,(400 , HEIGHT - 400 ), self.clock_rect)
     
    def text_bar(self):
        self.screen.blit(self.text_slot, (0, HEIGHT - self.text_rect.height), self.text_rect)  #dibujar cuadros transparentes

    def inventory(self):
        self.screen.blit(self.inventory, (100 , 100 ), self.inventory_rect)  #dibujar cuadros transparentes
        self.inventory.fill((20,20,20,150))  #rellenar los cuadros


    def slot_knife(self):  
        self.screen.blit(self.slots_img, (WIDTH - 150 , HEIGHT - 500), self.slots_rect)  #dibujar cuadros transparentes
        self.slots_img.fill((20,20,20,150))  #rellenar los cuadros
        self.draw_text("K N I V E", self.digital_font, 15, WHITE , WIDTH - 120, HEIGHT - 490, align="center")  #dibujar nombre del arma
        if self.knife:
            self.screen.blit(self.knife_slot,(WIDTH - 130 , HEIGHT - 490), self.knife_rect)
        if self.knife and self.player.weapon == 'knife':
            self.draw_text("K N I V E", self.digital_font, 15, RED , WIDTH - 120, HEIGHT - 490, align="center")  #dibujar nombre del arma

    def slot_pistol(self):  
        self.screen.blit(self.slots_img, (WIDTH - 150 , HEIGHT - 400), self.slots_rect)  #dibujar cuadros transparentes
        self.slots_img.fill((20,20,20,150))  #rellenar los cuadros
        self.draw_text("P I S T O L", self.digital_font, 15, WHITE , WIDTH - 115, HEIGHT - 390, align="center")  #dibujar nombre del arma
        if self.gun:
            self.screen.blit(self.pistol_slot,(WIDTH - 130 , HEIGHT - 390), self.knife_rect)
        if self.gun and self.player.weapon == 'pistol':
            self.draw_text("P I S T O L", self.digital_font, 15, RED , WIDTH - 115, HEIGHT - 390, align="center")  #dibujar nombre del arma

    def slot_shotgun(self):
        self.screen.blit(self.slots_img, (WIDTH - 150 , HEIGHT - 300), self.slots_rect)  #dibujar cuadros transparentes
        self.slots_img.fill((20,20,20,150))  #rellenar los cuadros
        self.draw_text("S h o t g u n", self.digital_font, 15, WHITE , WIDTH - 110, HEIGHT - 290, align="center")  #dibujar nombre del arma
        if self.shotgun:
            self.screen.blit(self.shotgun_slot,(WIDTH - 140 , HEIGHT - 280), self.knife_rect)
        if self.shotgun and self.player.weapon == 'shotgun':
            self.draw_text("S h o t g u n", self.digital_font, 15, RED , WIDTH - 110, HEIGHT - 290, align="center")  #dibujar nombre del arma

    def slot_rifle(self):
        self.screen.blit(self.slots_img, (WIDTH - 150 , HEIGHT - 200), self.slots_rect)  #dibujar cuadros transparentes
        self.slots_img.fill((20,20,20,150))  #rellenar los cuadros
        self.draw_text("A K 7 4 U", self.digital_font, 15, WHITE , WIDTH - 110, HEIGHT - 190, align="center")  #dibujar nombre del arma
        if self.rifle:
            self.screen.blit(self.rifle_slot,(WIDTH - 130 , HEIGHT - 180), self.knife_rect)
        if self.rifle and self.player.weapon == 'rifle':
            self.draw_text("A K 7 4 U", self.digital_font, 15, RED , WIDTH - 110, HEIGHT - 190, align="center")  #dibujar nombre del arma

    def slot_medkit(self):
        self.screen.blit(self.slots_img, (WIDTH - 150, HEIGHT - 100 ), self.slots_rect)  #dibujar cuadros transparentes
        self.slots_img.fill((20,20,20,150))  #rellenar los cuadros
        self.screen.blit(self.medkit_slot,(WIDTH - 130 , HEIGHT - 80 ), self.medkit_rect)
        self.draw_text("M E D K i T", self.digital_font, 15, WHITE , WIDTH - 110, HEIGHT - 90, align="center")  #dibujar nombre del arma

    def draw_lives(self, surface, x, y, lives, rect): 
        self.__layer = ITEMS_LAYER
        for i in range(self.player.lives): 
            self.lives_rect = self.lives_img.get_rect()  
            self.lives_rect.x = x + 40 * i 
            self.lives_rect.y = y 
            pg.Surface.blit(self.screen, self.lives_img, self.lives_rect)


    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps())) #SHOW FPS TO THE SCREEN
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
####################### VIDA DE MOBS, NOCHE, DEBUG, ETC, OTROS RELACIONADOS, ESCRIBIR ACA################

        #self.draw_grid() #UNCOMENT AGAIN IF NEED TO SEE THE GRID 

        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                #self.draw_text('{}'.format(str(WEAPONS[self.player.weapon]['damage'])), self.hud_font, 15, WHITE, 10, 120, align="nw")
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect),1 )

 
        if self.night:
            self.render_fog()  

        ### TO PRINT EVENT TEXT #######
        if self.text:
            self.text_bar()
            self.draw_text('{}'.format(str(WEAPONS[self.player.weapon]['description'])), self.hud_font, 20, WHITE, 200, HEIGHT - 80, align="nw")

      ######################## T O    I N V E N T O R Y    I T E M S #################################################
        if self.char_tab: 

            self.screen.blit(self.statmenu2, (300 ,100), self.statmenu2_rect)
            self.draw_text('{}'.format("%.0f" % self.player.strenght), self.digital_font, 30, WHITE,405, 215, align="center")
            self.draw_text('{}'.format("%.0f" % self.player.dexterity), self.digital_font, 30, WHITE,405, 250, align="center")
            self.draw_text('{}'.format("%.0f" % self.player.luck), self.digital_font, 30, WHITE,405, 290, align="center")
            self.draw_text('{}'.format("%.0f" % self.player.hunger), self.digital_font, 30, WHITE,405, 325, align="center")
            #self.draw_text('{}'.format("%.0f" % self.player.stamina), self.digital_font, 30, WHITE,405, 360, align="center")

            self.draw_text(('STR'), self.digital_font, 15, RED, 345, 215, align="center")
            self.draw_text(('DEX'), self.digital_font, 15, RED, 345, 250, align="center")
            self.draw_text(('LUCK'), self.digital_font, 15, RED, 345, 290, align="center")
            self.draw_text(('HUNGER'), self.digital_font, 15, RED, 345, 325, align="center")

            if self.knife:
                self.draw_text(('KNIFE'), self.digital_font, 20, RED, 600, 212, align="center")
                self.draw_text('{}'.format("%.0f" % WEAPONS['knife']['damage']), self.digital_font, 30, WHITE,545, 215, align="center")
            else:
                self.draw_text(('KNIFE'), self.digital_font, 20, LIGHTGREY, 600, 212, align="center")
                self.draw_text(('- -'), self.hud_font, 30, LIGHTGREY,545, 210, align="center")

            if self.gun:
                self.draw_text(('PISTOL'), self.digital_font, 15, RED, 600, 250, align="center")
                self.draw_text('{}'.format("%.0f" % WEAPONS['pistol']['damage']), self.digital_font, 30, WHITE,545, 250, align="center")                
            else:
                self.draw_text(('PISTOL'), self.digital_font, 15, LIGHTGREY, 600, 250, align="center")
                self.draw_text(('- -'), self.hud_font, 30, LIGHTGREY,545, 245, align="center")

            if self.rifle:
                self.draw_text('{}'.format("%.0f" % WEAPONS['rifle']['damage']), self.digital_font, 30, WHITE,545, 285, align="center")
                self.draw_text(('RIFLE'), self.digital_font, 15, RED, 600, 285, align="center")

            else:
                self.draw_text(('RIFLE'), self.digital_font, 15,LIGHTGREY, 600, 285, align="center")
                self.draw_text(('- -'), self.hud_font, 30, LIGHTGREY,545, 280, align="center")

            if self.shotgun:
                self.draw_text('{}'.format("%.0f" % WEAPONS['shotgun']['damage']), self.digital_font, 30, WHITE,545, 320, align="center")
                self.draw_text(('SHOTGUN'), self.digital_font, 15, RED, 600, 320, align="center")
            else:
                self.draw_text(('SHOTGUN'), self.digital_font, 15,LIGHTGREY, 600, 320, align="center")
                self.draw_text(('- -'), self.hud_font, 30, LIGHTGREY,545, 315, align="center")

#########################TO PAUSE GAME ##################################################################
######################  T O   M A K E   P A U S E   M E N U #############################################
        


        if self.text and self.paused:    ##############  T O    D R A W    M E N U    A N D    I N V E N T O R Y #########################
                self.draw_text('Details: {}'.format(str(WEAPONS[self.player.weapon]['description'])), self.hud_font, 20, BLACK, 250, 80, align="nw")
          

        if self.paused:
            #(Surface, color, Rect, width=0)
            self.slot_big = self.screen.blit(self.big_slot, (650,90), self.big_slot_rect)
            if self.rifle:
                self.inventory.blit(self.rifle_slot, (15,105), self.rifle_rect)
            if self.knife:
                self.inventory.blit(self.knife_slot, (80,105), self.knife_rect)

            self.screen.blit(self.inventory, (100 , 100 ), self.inventory_rect)  #dibujar cuadros transparentes
            self.draw_text("Inventory", self.extra_font, 60, RED, WIDTH / 2, HEIGHT / 2 - 280, align="center")

################### D R A W I N G    S T A T U S    I C O N S ###################################################

        if not self.paused:

            #LEFT SIDES HUD - BACKGROUND
            self.screen.blit(self.hud_bar1, (1 , 1), self.hud_bar1_rect)  #dibujar cuadros transparentes
            self.hud_bar1.fill((20,20,20,150))

            #LEFT SIDES HUD - STATUS BARS
            self.draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
            self.draw_player_armor(self.screen, 10,40, self.player.armor / PLAYER_ARMOR)
            self.draw_player_stamina(self.screen, 10, 70, self.player.stamina / PLAYER_STAMINA)
            self.draw_player_food(self.screen, 10, 100, self.player.hunger / PLAYER_HUNGER)
            self.draw_player_exp(self.screen, 250, 30, self.player.exp / self.player.exp_cap)
            #self.draw_player_water(self.screen, 10, 100, self.player.thirst / PLAYER_THIRST)
 
            #LEFT SIDES HUD - STATUS ICONS
            self.screen.blit(self.health_icon,(4 , 4 ), self.health_rect)
            self.screen.blit(self.shield_icon,(4 , 34 ), self.shield_rect)
            self.screen.blit(self.stamina_icon,(4 , 64 ), self.stamina_rect)
            self.screen.blit(self.food_icon,(4 , 94 ), self.food_rect)

            ##STATUS BAR DESCRIPTIONS #
            self.draw_text('{}'.format("HP " + "%.0f" % self.player.health), self.digital_font, 20, WHITE,55, 30, align="center")
            self.draw_text('{}'.format("DP " + "%.0f" % self.player.armor), self.digital_font, 20, WHITE,55, 60, align="center")
            self.draw_text('{}'.format("Sta:" + " %.0f  " % self.player.stamina + " / " + " %.0f   " %self.player.stamina_cap),self.hud_font, 10, WHITE,80, 85, align="center")
            #self.draw_text('{}'.format("%.0f" % self.player.armor), self.digital_font, 30, RED,50, 60, align="center")
            self.draw_text('{}'.format("%.0f" % self.player.sp), self.digital_font, 30, RED,30, 300, align="center")
            self.draw_text('{}'.format("%.0f" % self.player.st), self.digital_font, 30, RED,30, 330, align="center")

            #self.draw_text('{}'.format("%.0f" % self.player.exp + "%.0f" % self.player.exp_cap / 100), self.digital_font, 30, RED,500, 100, align="center")

            #CENTER TOP HUD - EXP AND LEVEL BAR
            self.draw_text('{}'.format("%.0f" % self.player.level), self.digital_font, 30, WHITE,230, 30, align="center")
            self.draw_text('{}'.format("EXP:" + " %.0f  " % self.player.exp + " / " + " %.0f   " % self.player.exp_cap ),self.hud_font, 10, RED,480, 35, align="center")

            #RIGHT SIDE HUD - WEAPON AND ITEM INFO
            self.draw_lives(self.screen, 10, 154, self.player.lives, self.lives_rect) 
            self.slot_knife()
            self.slot_pistol()
            self.slot_shotgun()
            self.slot_rifle()
            self.slot_medkit()
            self.draw_text(str(WEAPONS['pistol']['gun_comb']) + " /  " + str(WEAPONS['pistol']['charger_size']) + '('+str(WEAPONS['pistol']['total_bullets'])+')', self.extra_font, 20, WHITE, WIDTH - 100 , HEIGHT - 350 , align="center")   #funcional, comentada para hacer pruebas
            self.draw_text(str(WEAPONS['shotgun']['gun_comb']) + " /  " + str(WEAPONS['shotgun']['charger_size']) + '('+str(WEAPONS['shotgun']['total_bullets'])+')', self.extra_font, 20, WHITE, WIDTH - 100 , HEIGHT - 250 , align="center")   #funcional, comentada para hacer pruebas
            self.draw_text(str(WEAPONS['rifle']['gun_comb']) + " /  " + str(WEAPONS['rifle']['charger_size']) + '('+str(WEAPONS['rifle']['total_bullets'])+')', self.extra_font, 20, WHITE, WIDTH - 100 , HEIGHT - 150 , align="center")   #funcional, comentada para hacer pruebas
            self.draw_text('Zombies: {}'.format(len(self.mobs)), self.hud_font, 30, WHITE, WIDTH - 10, 10, align="ne")
            self.draw_text("" + str(WEAPONS['medkit']['ammount']), self.extra_font, 20, WHITE, WIDTH - 140 , HEIGHT - 50 , align="center")
            if self.pulse_watch:
                self.screen.blit(self.clock_slot,(WIDTH - 120 , 100 ), self.clock_rect)
                self.draw_text('{}'.format(str(self.player.watch)), self.hud_font, 20, WHITE, WIDTH - 70, 105, align="n")


###############################################################################################

        pg.display.flip()
    

    def events(self):
        # catch all events here 
        #self.mouse = ((0,0), 0, 0, 0)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.KEYUP:
                if event.key == pg.K_r and self.player.weapon != 'knife' and self.player.weapon != 'hand':
                    #self.player.reload()
                    self.player.reload()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_9:
                    Game.screen = pg.display.set_mode((WIDTH, HEIGHT),pg.FULLSCREEN)
                if event.key == pg.K_0:
                    Game.screen = pg.display.set_mode((WIDTH, HEIGHT))

    
                if event.key == pg.K_h: #DIBUJAR CUADROS VISIBLES A LOS RECTANGULOS EN EL JUEGO
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    #self.text_bar()
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night

                if event.key == pg.K_c:
                    self.pulse_watch = not self.pulse_watch

                if event.key == pg.K_i:
                    self.char_tab = not self.char_tab

                if event.key == pg.K_m:
                    self.shop = not self.shop
                    #self.inventory()

            ############################ C O D I G O   P A R A   D A R   F L A G S   C O N   M O U S E    ##############################
            ########################### E    I M P R I M I R    T E X T O    E N   P A N T A L L A  ########  P  R  O  P  I  O #########

        #pg.display.flip()

        #for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                self.click = not self.click

                # checks if mouse position is over the button
                if self.paused and WEAPONS['rifle'] and self.rifle_rect.collidepoint(mouse_pos) and self.click:
                    self.text = not self.text  

        pg.display.flip()
           #if event.type == MOUSEBUTTONDOWN:
                #if event.mouse[0]:
                #self.player.shoot()
        #print event.button
                    #print(pg.mouse.get_pos())
                   # self.player.pos = pg.mouse.get_pos()
                    #self.player.rot -= pg.mouse.get_pos()

    def intro(self):
        #waiting = False
        self.screen.blit(self.text_slot, (0, HEIGHT - self.text_rect.height), self.text_rect)
        self.draw_text("Seems like this is gonna be hard, i wonder where is everybody..", self.extra_font, 20, WHITE, 200, HEIGHT - 80, align="w")
        self.draw_text(" first i need to find a weapon, and try to get some meds", self.extra_font, 20, WHITE, 200, HEIGHT - 60, align="w")
        pg.display.flip()
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False


    def show_start_screen(self):

        self.screen.blit(self.menu, self.menu_rect)
        
        pg.mixer.music.load(path.join(self.music_folder, MENU_MUSIC))
        #pg.mixer.music.set_volume(1)
        pg.mixer.music.play(loops=-1)

        self.draw_text("CODE N1GHTM4R3", self.extra_font , 60, RED, WIDTH / 2, HEIGHT / 4, align="center")
        self.draw_text("press any key to Continue", self.extra_font, 35, RED, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        self.draw_text("Version 0.2.2409218B", self.extra_font, 20, WHITE, 600 , HEIGHT - 40, align="w") 

    
        #self.menu_sfx.play()     
        pg.display.flip()
        waiting = True
        while waiting:

            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP:
                    self.screen.blit(self.dim_screen, (0,0))
                    self.screen.blit(self.dim_screen2, (0,0))
                    self.draw_text("CONTROLS", self.tittle_font, 60, WHITE, WIDTH / 2 , 50 , align="center")
                    self.draw_text("[W,A,S,D] to Move", self.extra_font, 30, WHITE, 40, 80, align="w")
                    self.draw_text("[Up, Left, Down, Right] Arrows to Move", self.extra_font, 30, WHITE, 40, 110, align="w")
                    self.draw_text("[2] for Knife", self.extra_font, 35, WHITE, 40, 140, align="w")
                    self.draw_text("[3] for Pistol", self.extra_font, 35, WHITE, 40, 170, align="w")
                    self.draw_text("[4] for Shotgun", self.extra_font, 35, WHITE, 40, 200, align="w")
                    self.draw_text("[5] for Rifle", self.extra_font, 35, WHITE, 40, 230, align="w")
                    self.draw_text("[6] for Medkit (use)", self.extra_font, 35, WHITE, 40, 260, align="w")
                    self.draw_text("[Space] to Fire", self.extra_font, 30, WHITE, 40, 290, align="w")
                    self.draw_text("[P] to Pause/Show Inventory", self.extra_font, 30, WHITE, 40, 320, align="w")
                    
                    self.draw_text("TIPS", self.tittle_font, 60, WHITE, WIDTH / 2, 400, align="center")
                    self.draw_text("-Weapons and Items can be found on the ground", self.extra_font, 30, WHITE, 40, 450, align="w")
                    self.draw_text("-After you pick them up, can be selected by pressing its number", self.extra_font, 30, WHITE, 40, 485, align="w")
                    self.draw_text("-You can see item's details by clicking them up during the pause Menu", self.extra_font, 30, WHITE, 40, 520, align="w")
                    pg.display.flip()
                    waiting = True
                    while waiting:
                        self.clock.tick(FPS)
                        for event in pg.event.get():
                            if event.type == pg.QUIT:
                                pg.quit()
                            if event.type == pg.KEYUP: 
                                waiting = False


    def show_go_screen(self):
        if self.player.lives > 1:

            self.screen.blit(self.gameover, self.gameover_rect)
        #self.screen.fill(BLACK)
            #self.draw_text("GAME OVER", self.tittle_font, 100, RED, WIDTH /2, HEIGHT /2, align="center")
            self.draw_text("Press any key to start", self.tittle_font, 40, WHITE, WIDTH /2, HEIGHT * 3 / 4, align="center")

        #if lself.mobs <= 0:
            self.screen.blit(self.victory, self.victory_rect)
            self.draw_text("Press any key to start", self.tittle_font, 40, WHITE, WIDTH /2, HEIGHT * 3 / 4, align="center")

        #self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        #self.draw_text("Score " + str(self.highscore), self.tittle_font, 20, WHITE, WIDTH /2, HEIGHT / 4, align="n")
        if self.player.score > self.highscore:
            self.highscore = self.player.score
            self.draw_text("You got a New Highscore!! " + str(self.highscore), self.tittle_font, 20, WHITE, WIDTH /2, HEIGHT - 3/4, align="n")
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.player.score))
        else:
            self.draw_text("Score " + str(self.player.score), self.tittle_font, 20, WHITE, WIDTH /2, HEIGHT /3 , align="n")

        pg.display.flip()
        self.wait_for_key()


    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()

while True:
    g.new()
    g.run()
    g.show_go_screen()
