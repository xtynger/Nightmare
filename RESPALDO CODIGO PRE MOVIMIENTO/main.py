import pygame as pg
import sys
from random import choice, random
from os import path
from settings import *
from sprites import *
from tilemap import *
from os import path
from pygame.locals import *
import time



#HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGHT = 100
    BAR_HEIGHT = 20
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

    def load_images(self):
        self.standing_frames = []
 

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')

        ########TO SAVE HIGHSCORE############################
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        #######################################################

        self.map_folder = path.join(game_folder, 'maps')
        self.tittle_font = path.join(img_folder, 'zombie.ttf')
        self.extra_font = path.join(img_folder, 'ferrum.otf')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')


        self.menu = pg.image.load(path.join(img_folder, MENU))
        self.menu_rect = self.menu.get_rect()

        self.gameover = pg.image.load(path.join(img_folder, GAMEOVER))
        self.gameover = pg.transform.scale(self.gameover, (800,600))
        self.gameover_rect = self.gameover.get_rect()
        #menu = pg.transform.scale(menu, (750,650))
        #menu_rect = menu.get_rect()

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
        #self.player_car = pg.image.load(path.join(img_folder, PLAYER_CAR)).convert_alpha()
        #self.player_car = pg.transform.scale(self.player_car, (200,100))
        

################### ################### ################### ################### ################### ################### ################### ################### 
#################### C O D E   T O   S E T    I M A G E S   T O   B E   D R A W N, IT MUST INCLUDE ITS RECT TOO #############################################
        self.slots_img = pg.image.load(path.join(img_folder, SLOTS)).convert_alpha()
        self.slots_img = pg.transform.scale(self.slots_img, (90  , 60))
        self.slots_rect = self.slots_img.get_rect()

        self.slots2_img = pg.image.load(path.join(img_folder, SLOTS)).convert_alpha()
        self.slots2_img = pg.transform.scale(self.slots2_img, (90  , 60))
        self.slots2_rect = self.slots2_img.get_rect()


        self.pistol_slot = pg.image.load(path.join(img_folder, PISTOL)).convert_alpha()
        self.pistol_slot = pg.transform.scale(self.pistol_slot, (50, 30))
        self.pistol_rect = self.pistol_slot.get_rect()
        

        self.shotgun_slot = pg.image.load(path.join(img_folder, SHOTGUN)).convert_alpha()
        self.shotgun_slot = pg.transform.scale(self.shotgun_slot, (75, 35))
        self.shotgun_rect = self.shotgun_slot.get_rect()

        self.rifle_slot = pg.image.load(path.join(img_folder, RIFLE)).convert_alpha()
        self.rifle_slot = pg.transform.scale(self.rifle_slot, (70, 30))
        self.rifle_rect = self.rifle_slot.get_rect()

        self.lives_img = pg.image.load(path.join(img_folder, LIVES_IMAGE)).convert_alpha()
        #self.lives_img = pg.transform.scale(self.lives_img, (60, 25))
        self.lives_rect = self.lives_img.get_rect()
################### ################### ################### ################### ################### ################### ################### ################### 
##################### ################### ################### ################### ################### ################### ################### ################### 

        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (5,5)) 
        #self.bullet_img = 
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (65,65))
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE ))
        self.splat = pg.image.load(path.join(img_folder, SPLAT_IMAGE)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (100, 100))
        self.split = pg.image.load(path.join(img_folder, SPLIT)).convert_alpha()



        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join
                        (img_folder, img)).convert_alpha())

        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join
                        (img_folder, ITEM_IMAGES[item])).convert_alpha()
        #FOR NIGHT EFFECT AND FOG
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        #Sounds Loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        pg.mixer.music.set_volume(1.0)
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

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.cars = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'tile1.xml'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_spawn()

        for tile_object in self.map.tmxdata.objects: #el parametro .objects es para usar esa capa especifica de objetos que creamos
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            #if tile_object.name == 'player': #ESTO INDICA DONDE DIBUJAR EL PLAYER
                #self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie': #ESTO INDICA DONDE DIBUJAR EL ENEMIGO
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,  #ESTO DA FORMA FISICA COLISIONABLE A LOS RECTANGULOS QUE DIBUJES COMO EL NOMBRE SE;ALADO
                             tile_object.width, tile_object.height)



            if tile_object.name in ['health', 'shotgun', 'rifle', 'pistol', 'shotgun_ammo', 'pistol_ammo', 'rifle_ammo']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height) #para insertar la "camara" al movimiento
        self.effects_sounds['level_start'].play()
        self.draw_debug = False
        self.paused = False
        self.night = False

############################################################################################################
################## FLAG STATEMENTS TO SET WEAPON SLOTS DRAWING #########################################
############################################################################################################
        self.gun = False
        self.shotgun = False
        self.rifle = False
        self.night = False 
        self.driving = False

##############################################################################################################################       



    def run(self):
        # game loop - set self.playing = False to end the game

        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
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

        #game over?
        if len(self.mobs) == 0:
            self.playing = False



##################################################################################################
################# C    O    L    I    S    I    O     N    E    S###########################
##################################################################################################
        

        #Player hits items


        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)

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

            if hit.type == 'pistol':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'pistol'
                self.gun = True

            
                                 


                #self.screen.blit(self.pistol_slot, (WIDTH / 8 - 25, HEIGHT - 80 ), self.pistol_rect)
########################### P R U E B A S   D E   D R A W    I T E M S ##############################################################

            #self.screen.blit(self.pistol_slot, (WIDTH / 8 - 25, HEIGHT - 80 ), self.pistol_rect)     
            #self.slot_1.blit(screen, 20, 20, player.weapon, pistol_slot) 
            #self.game.map_img.blit(self.game.split, self.pos - vec(32,32))
            #self.game.map_img.blit(self.pistol_slot, 20, 20, player.weapon, self.pistol_slot) 

##########################################################################################################################################################################################
########################################################## C O D I G O   P R O P I O    P A R A   M U N I C I O N E S#############################################################################
##########################################################################################################################################################################################

            if hit.type == 'pistol_ammo': #and self.player.weapon == 'pistol':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                #WEAPONS[self.player.weapon]['charger_size'] += randint(5, 20)             ##### LINEA CORRECTA FUNCIONAL, COMENTADA PARA HACER PRUEBAS
                WEAPONS['pistol']['charger_size'] += randint(5, 20)

            if hit.type == 'shotgun_ammo': #and self.player.weapon == 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                #WEAPONS[self.player.weapon]['charger_size'] += randint(24, 68)             ##### LINEA CORRECTA FUNCIONAL, COMENTADA PARA HACER PRUEBAS                                     
                WEAPONS['shotgun']['charger_size'] += randint(24, 68)

            if hit.type == 'rifle_ammo': #and self.player.weapon == 'rifle':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                #WEAPONS[self.player.weapon]['charger_size'] += randint(20, 60)             ##### LINEA CORRECTA FUNCIONAL, COMENTADA PARA HACER PRUEBAS                 
                WEAPONS['rifle']['charger_size'] += randint(20, 60)

##########################################################################################################################################################################################
##########################################################################################################################################################################################
##########################################################################################################################################################################################


        #Mobs hit Player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)    ######### PERFECT PIXEL COLLISSION HAPPENNING HERE ################  collide_circle_ratio(0.7) FOR RADIAL CHANGE FOR THIS
        #COPIA DE LINEA ORIGINAL      hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)    
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            #if self.player.health <= 0:
                #self.playing = False
            if self.player.health <= 0:
                self.player.lives -= 1
                self.player.health = PLAYER_HEALTH 
                self.player.pos = [68.3694, 701.876]   #NECESARIO MEJORAR ESTE CODIGO
            if self.player.lives == -1:
                self.playing = False


        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        #Bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            hit.vel = vec(0, 0)


            
###################################################################################################
#################### C O D I G O   P A R A   S U M A R   S C O R E#######################################

            self.player.score += 2    #ESTA LINEA HACE QUE SE SUMEN PUNTOS AL SCORE##################################
           #self.draw_text('+: {}'.format(str(self.player.score - 2),self.mob.pos - vec(32,32)), self.hud_font, 30, WHITE)  
            #self.draw_text('+: {}'.format(str(self.player.score - 2), self.hud_font, 15, WHITE, self.Mob.pos, align='center'))

###################################################################################################



    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

#########################################C O D I G O    P E R S O N A L ################################################          
############################################## E N   A D E L A N T E ###################################################
#########F U N C I O N A L   T O   D R A W   I M A G E S,  IN THIS CASE, LIVES, SLOTS AND MORE ########################


          


    def render_fog(self):
        #draw the light mask (gradient) onto de fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0,0), special_flags=pg.BLEND_MULT)
               # if self.player.day:
            #pg.time.get_ticks() - self.player.day_time > 2000
            #self.player.night
        #if self.night:



           # if self.player.night and pg.time.get_ticks() - self.player.day_time > 2000:
                #self.player.day and not self.player.night

        #self.day = False
        #if self.night and pg.time.get_ticks() - self.day_time > 5000: 
            #self.day = True
            

##########################################################################################################################################################
################################# T O   D R A W   S L O T S   A N D   N A M E S    I N   S C R E E N #####################################################
##############################################################################################################################
############################ T O    D R A W    W E A P O N  S L O T S  W H E N   P I C K   W E A P O N S  3/3 ####################



        #self.screen.blit(self.pistol_slot, (20 , HEIGHT - 80 ), self.pistol_rect)
       # self.slot1 = self.screen.blit(self.dim_screen2, (20 , HEIGHT - 80 , 80 , 60))    #pg.draw.rect(self.screen, (20, 20, 20, 0), (20 , HEIGHT - 80 , 80 , 60), 0)  
       # 
       # self.slot1.fill((20,0,0,150))
        #self.screen.blit(self.dim_screen, (20 , HEIGHT - 80 , 80 , 60))
        #pg.draw.rect(self.screen, BLACK, (WIDTH / 3 - 150 , HEIGHT - 80 , 80 , 60), 0)      #SLOT 2
        #pg.draw.rect(self.screen, BLACK, (210, HEIGHT - 80 , 80 , 60), 0)                   #SLOT 3

        #self.image = pygame.Surface((50, 50))           #imagen para el main de la clase
        #self.image.fill(VERDE)




    def slot_pistol(self):  
        self.screen.blit(self.slots_img, (20 , HEIGHT - 80 ), self.slots_rect)  #dibujar cuadros transparentes
        self.slots_img.fill((20,20,20,150))  #rellenar los cuadros
        self.draw_text("GLOCK", self.extra_font, 15, WHITE , 40, HEIGHT - 28, align="center")  #dibujar nombre del arma
        if self.gun:
            self.screen.blit(self.pistol_slot,(40 , HEIGHT - 65 ), self.pistol_rect)
            #self.draw_text("" + str(WEAPONS[self.player.weapon]['charger_size']), self.tittle_font, 20, RED, 185 , HEIGHT - 35 , align="center")
            self.draw_text("" + str(WEAPONS['pistol']['charger_size']), self.tittle_font, 20, RED, 86 , HEIGHT - 35 , align="center")
    
    def slot_shotgun(self):
        self.screen.blit(self.slots_img, (120 , HEIGHT - 80), self.slots_rect)
        self.slots_img.fill((20,20,20,150))
        self.draw_text("TWELVE", self.extra_font, 15, WHITE , 145 , HEIGHT - 28, align="center")
        if self.shotgun:
            self.screen.blit(self.shotgun_slot, (125 , HEIGHT - 70), self.shotgun_rect)
            #self.draw_text("" + str(WEAPONS[self.player.weapon]['charger_size']), self.tittle_font, 20, RED, 185 , HEIGHT - 35 , align="center")   #funcional, comentada para hacer pruebas
            self.draw_text("" + str(WEAPONS['shotgun']['charger_size']), self.tittle_font, 20, RED, 185 , HEIGHT - 35 , align="center")

    def slot_rifle(self):
        self.screen.blit(self.slots_img, (220 , HEIGHT - 80 ), self.slots_rect)
        self.slots_img.fill((20,20,20,150))
        self.draw_text("AK47", self.extra_font, 15, WHITE , 240, HEIGHT - 28, align="center")
        if self.rifle:
            self.screen.blit(self.rifle_slot, (225, HEIGHT - 70 ), self.rifle_rect)
            #self.draw_text("" + str(WEAPONS[self.player.weapon]['charger_size']), self.tittle_font, 20, RED, 270 , HEIGHT - 35 , align="center")   #funcional, comentada para hacer pruebas
            self.draw_text("" + str(WEAPONS['rifle']['charger_size']), self.tittle_font, 20, RED, 270 , HEIGHT - 35 , align="center")

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
        #self.draw_lives(self.screen, 20, 20, self.player.lives, self.lives_img)
        self.draw_lives(self.screen, 10, 40, self.player.lives, self.lives_rect) 
        self.slot_pistol()
        self.slot_shotgun()
        self.slot_rifle()
        if self.night:
            self.render_fog()

        #draw_lives(screen, 20, 20, player.lives, player_mini_img)   #ejemplo de SHMUP!
        #self.screen.blit(self.lives_img, (20,100), self.lives_rect) #PARA DIBUJAR IMAGENES CUALQUIERA, USAR EJEMPLO

####################### VIDA DE MOBS, NOCHE, DEBUG, ETC, OTROS RELACIONADOS, ESCRIBIR ACA################

        #self.draw_grid() #UNCOMENT AGAIN IF NEED TO SEE THE GRID 

        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect),1 )

        #to set night <condition:></condition:> 
        if self.night:
            self.render_fog()  


        #HUD FUNCTIONS

        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text('score: {}'.format(str(self.player.score)), self.hud_font, 15, WHITE, WIDTH / 2, 10, align="n") #LINEA DE SCORE INVENTADA POR MI #################################################################
        self.draw_text('clip: {}'.format(str(WEAPONS[self.player.weapon]['charger_size'])), self.hud_font, 15, WHITE, 10, 70, align="nw")   #LINEA INVENTADA POR MI PARA DIBUJAR CONTEO DE BALAS ###############
        self.draw_text('Zombies: {}'.format(len(self.mobs)), self.hud_font, 30, WHITE, WIDTH - 10, 10, align="ne")

#####################################################################################################################
########### C O N T A D O R E S   D E   T E X T O   I N D E P E N D I E N T E S ####################################
####################################################################################################################

#################DRAW CRITICAL COLOR ON SCREEN IF HURT#########################
        #if self.player.health <= 30:
        #    self.screen.blit(self.dim_screen, (0,0))

#########################TO PAUSE GAME ##################################################################
######################  T O   M A K E   P A U S E   M E N U #############################################


        if self.paused:
            #(Surface, color, Rect, width=0)
            self.screen.blit(self.dim_screen2, (0,0))
			#self.screen.blit(self.slots_img, (WIDTH /2 , HEIGHT / 2 ), self.slots_rect)  #dibujar cuadros transparentes
			#self.slots_img.fill((20,20,20,150))
            #pg.draw.rect(self.screen, WHITE, (WIDTH / 2 - 150, HEIGHT /2 - 150, 300, 300))
            #self.draw_text("Paused", self.tittle_font, 40, GREEN , WIDTH / 2, HEIGHT / 2 - 120, align="center")
            self.draw_text("Paused", self.tittle_font, 100, GREEN , WIDTH / 2, HEIGHT / 2 - 120, align="center")

###############################################################################################
###############################################################################################
###############################################################################################
        pg.display.flip()
    

    def events(self):
        # catch all events here 
        #self.mouse = ((0,0), 0, 0, 0)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
    
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
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night


                


    def show_start_screen(self):

        self.screen.blit(self.menu, self.menu_rect)
        

        self.draw_text("CODE N1GHTM4R3", self.tittle_font, 60, RED, WIDTH / 2, HEIGHT / 4, align="center")
                       # "GAME OVER", self.tittle_font, 100, RED, WIDTH /2, HEIGHT /2, align="center")
        #self.draw_text("Press Space-bar to shoot", self.tittle_font, 30, BLACK, WIDTH / 2, HEIGHT - 30, align="center")
        self.draw_text("press any key to Continue", self.extra_font, 35, RED, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        self.draw_text("Version 0.1.23052018B", self.extra_font, 20, WHITE, 600 , HEIGHT - 40, align="w")
        ##self.draw_text(self.screen, "version 1.31 beta. 2018", 10, WIDTH - 100, HEIGHT - 30)
    
                
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
                    self.draw_text("[1] for Pistol", self.extra_font, 35, WHITE, 40, 140, align="w")
                    self.draw_text("[2] for Shotgun", self.extra_font, 35, WHITE, 40, 170, align="w")
                    self.draw_text("[3] for Rifle", self.extra_font, 35, WHITE, 40, 200, align="w")
                    self.draw_text("[Space] to Fire", self.extra_font, 30, WHITE, 40, 230, align="w")
                    self.draw_text("[P] to Pause", self.extra_font, 30, WHITE, 40, 260, align="w")
                    
                    self.draw_text("TIPS", self.tittle_font, 60, WHITE, WIDTH / 2, 400, align="center")
                    self.draw_text("-Weapons can be found on the ground ", self.extra_font, 30, WHITE, 40, 450, align="w")
                    self.draw_text("-Aafter you pick them up, can be selected by pressing its number", self.extra_font, 30, WHITE, 40, 480, align="w")
                    self.draw_text("-In this beta version, the knife is not a weapon", self.extra_font, 30, WHITE, 40, 510, align="w")

                    self.draw_text("[Space] to Fire", self.extra_font, 30, WHITE, 40, 2300, align="w")
                    self.draw_text("[Space] to Fire", self.extra_font, 30, WHITE, 40, 2300, align="w")
                    ##self.draw_text(self.screen, "version 1.31 beta. 2018", 10, WIDTH - 100, HEIGHT - 30)
                    #self.screen.blit(menu, menu_rect)
                    #self.paused = True
                    #self.screen.blit(self.dim_screen, (0,0))
                    #self.draw_text("HARD NIGHT", self.tittle_font, 40, WHITE, WIDTH /2, HEIGHT * 3 / 4, align="center")
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
        self.screen.blit(self.gameover, self.gameover_rect)
        #self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.tittle_font, 100, RED, WIDTH /2, HEIGHT /2, align="center")
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