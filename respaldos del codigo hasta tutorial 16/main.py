import pygame as pg
import sys
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
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        #sdpg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'tile1.xml'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_img = pg.transform.scale(self.bullet_img, (15,15)) 
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE ))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join
                        (img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join
                        (img_folder, ITEM_IMAGES[item])).convert_alpha()


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        #self.player = Player(self, 10, 10)  #SPAM PLAYER SPOT
        #for x in range(0,10): #SPAWN MANUALLY WALL
            #Wall(self, x,5)

      ########## ##TO DRAW A TXT MAP WITH VARIABLES SET BY YOU################# 

        #for row, tiles in enumerate(self.map.data): #ENUMERA Y CUENTA CADA CARACTER DEL TEXTO
         #   for col, tile in enumerate(tiles): #ENUMETA CADA FILA Y COLUMNA EN ELLOS
          #      if tile == '1': #LE DICE QUE IDENTIFICAR PRIMERO
           #         Wall(self, col, row) #Y POR QUE REEMPLAZARLO
            #    if tile == 'M': #LE DICE QUE IDENTIFICAR PRIMERO
             #       Mob(self, col, row) #Y POR QUE REEMPLAZARLO
              #      
               # if tile == 'P':
                #    self.player = Player(self, col, row)
        ###############PARA LEER LAS CAPAS DEL MAPA DIBUJADO#########
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
            if tile_object.name in ['health']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height) #para insertar la "camara" al movimiento
        self.draw_debug = False

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player) #CHANGE THE OBJECT AND THE CAMERA WILL FOLLOW IT

        #Player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT)
        #Mobs hit Player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        #Bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
        

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

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



        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)

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

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
g.show_go_screen()