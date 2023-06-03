import pygame as pg
import sys
from random import choice, random
from os import path
from settings import *
from sprites import *
from tilemap import *

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

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'maps')
        self.tittle_font = path.join(img_folder, 'zombie.ttf')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((100, 0, 0, 180))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.player_img = pg.transform.scale(self.player_img, (70,65))
        self.player_img2 = pg.image.load(path.join(img_folder, PLAYER_IMG2)).convert_alpha()
        self.player_img2 = pg.transform.scale(self.player_img2, (80,70))
        self.player_img3 = pg.image.load(path.join(img_folder, PLAYER_IMG3)).convert_alpha()
        self.player_img3 = pg.transform.scale(self.player_img3, (80,65))
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (7,7)) 
        #self.bullet_img = 
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob_img = pg.transform.scale(self.mob_img, (80,80))
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

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'tile1.xml'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        for tile_object in self.map.tmxdata.objects: #el parametro .objects es para usar esa capa especifica de objetos que creamos
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player': #ESTO INDICA DONDE DIBUJAR EL PLAYER
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie': #ESTO INDICA DONDE DIBUJAR EL ENEMIGO
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,  #ESTO DA FORMA FISICA COLISIONABLE A LOS RECTANGULOS QUE DIBUJES COMO EL NOMBRE SE;ALADO
                             tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height) #para insertar la "camara" al movimiento
        self.draw_debug = False
        self.paused = False
        self.night = False
        self.effects_sounds['level_start'].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
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
                
        

        #Mobs hit Player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
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
###################################################################################################
###################################################################################################


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


    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps())) #SHOW FPS TO THE SCREEN
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
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

        #to set night condition:
        if self.night:
            self.render_fog()



        #HUD FUNCTIONS

        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        self.draw_text('Zombies: {}'.format(len(self.mobs)), self.hud_font, 30, WHITE, WIDTH - 10, 10, align="ne")

      #################DRAW CRITICAL COLOR ON SCREEN IF HURT#########################
        #if self.player.health <= 30:
        #    self.screen.blit(self.dim_screen, (0,0))
#########################TO PAUSE GAME ##################################################################

        if self.paused:
            self.screen.blit(self.dim_screen, (0,0))
            self.draw_text("Paused", self.tittle_font, 105, GREEN , WIDTH / 2, HEIGHT / 2, align="center")
######################################################################
        pg.display.flip()



    def events(self):
        # catch all events here 
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
#

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.tittle_font, 100, RED, WIDTH /2, HEIGHT /2, align="center")
        self.draw_text("Press any key to start", self.tittle_font, 40, WHITE, WIDTH /2, HEIGHT * 3 / 4, align="center")
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