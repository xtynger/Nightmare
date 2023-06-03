import pygame as pg
from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect
import pytweening as tween
from itertools import chain
import math
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
		if dir == 'x':
			hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
			if hits:
				if hits[0].rect.centerx > sprite.hit_rect.centerx:
				#if sprite.vel.x > 0:
					sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2.0
				#if sprite.vel.x < 0:
				if hits[0].rect.centerx < sprite.hit_rect.centerx:
					sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2.0
				sprite.vel.x = 0
				sprite.hit_rect.centerx = sprite.pos.x
		if dir == 'y':
			hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
			if hits:
				#if sprite.vel.y > 0:
				if hits[0].rect.centery > sprite.hit_rect.centery:
					sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
				#if sprite.vel.y < 0:
				if hits[0].rect.centery < sprite.hit_rect.centery:
					sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.0
				sprite.vel.y = 0
				sprite.hit_rect.centery = sprite.pos.y

class Spritesheet:
	#utility clas for loading and parshing (reading and understanding from a file) spritesheets
	def __init__(self, filename):
		self.spritesheet = pg.image.load(filename).convert_alpha()


	def get_image(self, x, y, width, height):
		#grab an image our of a larger spritesheet
		image = pg.Surface((width, height))
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		image = pg.transform.scale(image, (width // 2, height // 2 )) #usar el doble slash en los calculos hace que, si
																		# te da un numero con fraccion (int), no de error por esperar un (tr). asi que solo le 
																		#asignas doble // si es en este caso, division para que redondee el numero final a in par
		return image

class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = PLAYER_LAYER
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		#self.image = game.player_img
		self.last_update = 0
		self.current_frame = 0
		self.walking = False
		self.idle = True
		self.attacking = False
		self.load_images()

		self.image_original = self.standing_frames[0]
		self.image = self.image_original.copy()

		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.x = self.rect.x
		self.y = self.rect.y
		self.hit_rect = PLAYER_HIT_RECT
		self.hit_rect.center = self.rect.center
		self.current_frame = 0
		self.vel = vec(0, 0)
		self.pos = vec(x, y)			#ORIGINAL:  vec(x, y)
		self.rot = 0
		self.last_shot = 0
		self.health = PLAYER_HEALTH
		self.weapon = 'knife'
		self.damaged = False # A WAY TO MAKE QUICK SWITCHES ARE THE FLAGS TRUE OR FALSE, THAT BY CHANGING IT WITH SOME KEY OR ACTION, IT CHANGES TO OPPOSITE
		self.score = 0
		self.lives = 3
		self.clip = False

		self.day_time = pg.time.get_ticks()


	def load_images(self):
		self.standing_frames = [self.game.spritesheet.get_image(0, 87, 120, 80),
								self.game.spritesheet.get_image(0, 175.5, 120, 88),
								self.game.spritesheet.get_image(0, 263, 120, 88),
								self.game.spritesheet.get_image(0, 351, 120, 88),
								self.game.spritesheet.get_image(0, 526, 120, 88),
								self.game.spritesheet.get_image(0, 614, 120, 88),
								self.game.spritesheet.get_image(0, 702, 120, 88),
								self.game.spritesheet.get_image(0, 789, 120, 88),
								self.game.spritesheet.get_image(0, 877, 120, 88),
								self.game.spritesheet.get_image(0, 965, 120, 88),
								self.game.spritesheet.get_image(0, 1053, 120, 88),
								self.game.spritesheet.get_image(0, 1140, 120, 88),
								self.game.spritesheet.get_image(0, 1228, 120, 88),
								self.game.spritesheet.get_image(0, 1316, 120, 88),
								self.game.spritesheet.get_image(0, 1404, 120, 88),
								self.game.spritesheet.get_image(0, 1491, 120, 88),
								self.game.spritesheet.get_image(0, 1579, 120, 88),
								self.game.spritesheet.get_image(0, 1667, 120, 88),
								]

		for frame in self.standing_frames:
			frame.set_colorkey(BLACK)
		#self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
								#self.game.spritesheet.get_image(692, 1458, 120, 207)]
		#for frame in self.walk_frames_r:
			#frame.set_colorkey(BLACK)
		#self.walk_frames_l = []
		#for frame in self.walk_frames_r:
		#	self.walk_frames_l.append(pg.transform.flip(frame, True, False))
	#	self.jump_frame = [self.game.spritesheet.get_image(382, 763, 150, 181)]


	def get_keys(self):
		self.rot_speed = 0
		self.vel =vec(0, 0)
		now = pg.time.get_ticks()
		keys = pg.key.get_pressed()		
		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.rot_speed = PLAYER_ROT_SPEED
			if now - self.last_update > 50:
				self.last_update = now
				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
				new_image = pg.transform.rotate(self.image_original, self.rot) # NECESARY TO ANIMATE
				old_center = self.rect.center # NECESARY TO ANIMATE
				self.image = new_image
				self.rect = self.image.get_rect()
				self.rect.center = old_center
			#self.vel.x = -PLAYER_SPEED
		if keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.rot_speed = -PLAYER_ROT_SPEED
			if now - self.last_update > 50:
				self.last_update = now
				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
				new_image = pg.transform.rotate(self.image_original, self.rot) # NECESARY TO ANIMATE
				old_center = self.rect.center # NECESARY TO ANIMATE
				self.image = new_image
				self.rect = self.image.get_rect()
				self.rect.center = old_center
			#self.vel.x = PLAYER_SPEED
		if keys[pg.K_UP] or keys[pg.K_w]:
			self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot) #ADDING ROTATE PARAMETER MAKES IT WALK TOWARDS THE DIRECTION YOU TURN TO

			#self.vel.y = -PLAYER_SPEED
		if keys[pg.K_DOWN] or keys[pg.K_s]:
			self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot) #ADDING ROTATE PARAMETER MAKES IT WALK TOWARDS THE DIRECTION YOU TURN TO
			#self.vel.y = PLAYER_SPEED


		if keys[pg.K_LSHIFT] or keys[pg.K_q]:
			self.vel = vec(PLAYER_SPEED + 250, 0).rotate(-self.rot)


							################### CALCULA CONDICIONES PARA DISPARAR, SI SE TIENE BALAS O NO ################### 

		if keys[pg.K_SPACE]  and self.weapon != 'knife' and WEAPONS[self.weapon]['charger_size'] > 0:  ###PROPIO PARA CONTEO DE BALAS
			self.clip = True  #### PROPIO PARA CONTEO DE BALAS USANDO FLAGS
			self.shoot()
			#EFFECT_SOUNDS['no_ammo.wav'].play()

		

		
		if keys[pg.K_1] and self.game.gun == True:
			self.weapon = 'pistol'
			
		if keys[pg.K_2] and self.game.shotgun == True:
			self.weapon = 'shotgun'

		if keys[pg.K_3] and self.game.rifle == True:
			self.weapon = 'rifle'


################### ################### ################### ################### ################### ################### ################### 
##################### CODIGO PROPIO EN PARTE, PARA DETERMINAR QUE SI SE TIENE BALAS, SE EJECUTE TODO, SINO, NO DISPARA ####################
################### ################### ################### ################### ################### ################### ################### 


	def shoot(self):
		if self.clip:  ####PROPIO PARA CONTEO DE BALAS ################### ###################  PROPIO
			try:		##PROPOP PARA CONTEO DE BALAS  ################### ###################  PROPIO
				now = pg.time.get_ticks()
				if now - self.last_shot > WEAPONS[self.weapon]['rate']:
					self.last_shot = now
					dir = vec(1,0).rotate(-self.rot)
					pos = self.pos + BARREL_OFFSET.rotate(-self.rot) #INDICA LA POSICION DONDE SE DIBUJA EL DISPARO PARA APARENTAR QUE SALE DEL ARMA
					self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
					for i in range(WEAPONS[self.weapon]['bullet_count']):
						spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
						Bullet(self.game, pos, dir.rotate(spread))  #, WEAPONS[self.weapon]['damage']  (agregar eso para calcular mejor el da;o de balas sueltas al cambiar arma)
						snd = choice(self.game.weapon_sounds[self.weapon])
						if snd.get_num_channels() > 2:
							snd.stop()
						
############################################################################################################################################################
############################# C O D I G O   P R O P I O   P A R A   C A N C E L A R   D I S P A R O S  S I  N O  H A Y  B A L A S ###########################
############################################################################################################################################################	

						if WEAPONS[self.weapon]['charger_size'] > 0:
							WEAPONS[self.weapon]['charger_size'] -= 1
						if WEAPONS[self.weapon]['charger_size'] <= 0:
							WEAPONS[self.weapon]['charger_size'] == 0
							self.clip = False
						snd.play()	
					MuzzleFlash(self.game, pos) #agregar , dir.rotate() dentro para probar
			except:									################### ################### PROPIO
				self.clip = False


				               ################### ################### PROPIO
							
############################################################################################################################################################
############################################################################################################################################################						

					

	def hit(self):
		self.damaged = True
		self.damage_alpha = chain(DAMAGE_ALPHA * 4)

	def update(self):
		self.get_keys()
		self.animate()
		#print(self.pos)
		#self.day_night_clock()
		




		self.rect = self.image.get_rect()
		self.rect.center = self.pos
		self.pos += self.vel * self.game.dt
		self.hit_rect.centerx = self.pos.x
		#self.rect.x = self.pos.x
		collide_with_walls(self, self.game.walls,'x')
		#self.rect.y = self.pos.y
		self.hit_rect.centery = self.pos.y
		collide_with_walls(self, self.game.walls,'y')
		self.rect.center = self.hit_rect.center
		self.mask = pg.mask.from_surface(self.image) ################### ###################  PROPIO, NECESARIO PARA COLISION PERFECTA DE PIXELES
		



##################################################################################################
########################C O D I G O   P R O P I O    F U N C I O N A L ###########################
#############################CAMBIO DE IMAGEN SEGUN ARMA DEL PLAYER###############################
##################################################################################################
		


		
		if self.weapon =='knife':
			# self.image = self.image
			new_image = pg.transform.rotate(self.game.player.image, self.rot)
			#if self.vel == vec(0, 0):

		if self.weapon =='pistol':
			self.image = self.game.player_img1
			self.image = pg.transform.rotate(self.game.player_img1, self.rot)

		if self.weapon =='shotgun':
			self.image = self.game.player_img2
			self.image = pg.transform.rotate(self.game.player_img2, self.rot)

		if self.weapon =='rifle':
			self.image = self.game.player_img3
			self.image = pg.transform.rotate(self.game.player_img3, self.rot)



##################################################################################################
##################################################################################################
##################################################################################################	



		if self.damaged:
			try:
				self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT) #PROBAR EL SPECIAL FLAG FUNCION PARA MANIPULAR COLORES
			except:
				self.damaged = False

	def animate(self):
		now = pg.time.get_ticks()

		#show idle animation on place
		if self.idle:
			if now - self.last_update > 50:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
				#bottom = self.rect.bottom
				self.image = self.standing_frames[self.current_frame]
				self.rect = self.image.get_rect()
				#self.rect.bottom = bottom
		self.mask = pg.mask.from_surface(self.image) #esto crea una mascara entorno a la imagen para poder hacer colisoon perfecta por pixeles


	def day_night_clock(self):

		self.day_time = pg.time.get_ticks()
		
		if self.day_time > DAYTIME:
			self.day_time -= DAYTIME
			self.game.night = True

			if self.game.night:
				self.game.render_fog()
   
			if self.day_time > NIGHTTIME:
				self.day_time -= NIGHTTIME
				self.game.night = False

				if self.day_time > DAYTIME:
					self.day_time -= DAYTIME
					self.game.night = True

					if self.game.night:
						self.game.render_fog()

					if self.day_time > NIGHTTIME:
						self.day_time -= NIGHTTIME
						self.game.night = False

						if self.day_time > DAYTIME:
							self.day_time -= DAYTIME
							self.game.night = True

							if self.game.night:
								self.game.render_fog()

							if self.day_time > NIGHTTIME:
								self.day_time -= NIGHTTIME
								self.game.night = False

								if self.day_time > DAYTIME:
									self.day_time -= DAYTIME
									self.game.night = True

									if self.game.night:
										self.game.render_fog()

									if self.day_time > NIGHTTIME:
										self.day_time -= NIGHTTIME
										self.game.night = False

										if self.day_time > DAYTIME:
											self.day_time -= DAYTIME
											self.game.night = True

											if self.game.night:
												self.game.render_fog()

											if self.day_time > NIGHTTIME:
												self.day_time -= NIGHTTIME
												self.game.night = False

												if self.day_time > DAYTIME:
													self.day_time -= DAYTIME
													self.game.night = True

													if self.game.night:
														self.game.render_fog()


		
		print(self.day_time)


	def add_health(self, amount):
		self.health += amount
		if self.health > PLAYER_HEALTH:
			self.health = PLAYER_HEALTH

	#def weapon_set(self):
################### ################### ################### ################### ################### ################### ################### ################### 
#####################################	P R U E B A    D E   A N I M A C I O N    D E   P E R S O N A J E #####################################################
################### ################### ################### ################### ################### ################### ################### ################### 





###############################################################################################################################################################
###############################################################################################################################################################

class Mob(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = MOB_LAYER
		self.groups = game.all_sprites, game.mobs
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.mob_img.copy()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.hit_rect = MOB_HIT_RECT.copy()
		self.hit_rect.center = self.rect.center
		self.pos = vec(x, y)   #sin el  * TILESIZE el mob aparecera donde el rectangulo de la capa obstacles del juego, determine
		self.vel = vec(0, 0) 
		self.acc = vec(0, 0)
		self.rect.center = self.pos
		self.rot = 0
		self.health = MOB_HEALTH
		self.speed = choice(MOB_SPEEDS)
		self.target = game.player

	def avoid_mobs(self):
		for mob in self.game.mobs:
			if mob != self:
				dist = self.pos - mob.pos
				if 0 < dist.length() < AVOID_RADIUS:
					self.acc += dist.normalize()

	def update(self):
		
		target_dist = self.target.pos - self.pos
		self.mask = pg.mask.from_surface(self.image)
		if target_dist.length_squared() < DETECT_RADIUS**2:
			if random() < 0.002:
				choice(self.game.zombie_moan_sounds).play()
			self.rot = target_dist.angle_to(vec(1,0))
			self.image = pg.transform.rotate(self.game.mob_img, self.rot)
			self.rect = self.image.get_rect()
			self.rect.center = self.pos
			self.acc = vec(1, 0).rotate(-self.rot)
			self.avoid_mobs()
			self.acc.scale_to_length(self.speed)
			self.acc += self.vel * -1
			self.vel += self.acc * self.game.dt
			self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
			self.hit_rect.centerx = self.pos.x
			collide_with_walls(self, self.game.walls, 'x')
			self.hit_rect.centery = self.pos.y
			collide_with_walls(self, self.game.walls, 'y')
			self.rect.center = self.hit_rect.center

############################AGREGADO POR MI PARA INCLUIR SALPICADURAS AL DISPARARLES##############################

		if pg.sprite.spritecollideany(self, self.game.bullets):
			self.game.map_img.blit(self.game.split, self.pos - vec(32,32))

###################################################################################################################

		if self.health <= 0:
			choice(self.game.zombie_hit_sounds).play()
			self.kill()

			self.game.player.score += 50 #############################################ESTA LINEA AGREGA SCORE AL MATAR MOBS ################

			self.game.map_img.blit(self.game.splat, self.pos - vec(32,32)) ############### CODIGO PROPIO PARA AGREGAR MANCHA AL MORIR UN MOB

	def draw_health(self):
		if self.health > 60:
			col = GREEN
		elif self.health > 30:
			col = YELLOW
		else:
			col = RED

		width = int(self.rect.width * self.health / MOB_HEALTH)
		self.health_bar = pg.Rect(0, 0, width, 7)
		if self.health < MOB_HEALTH:
			pg.draw.rect(self.image, col, self.health_bar)

class Bullet(pg.sprite.Sprite):
	def __init__(self, game, pos, dir):
		self._layer = BULLET_LAYER
		self.groups = game.all_sprites, game.bullets
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
		self.rect = self.image.get_rect()
		self.hit_rect = self.rect
		self.pos = vec(pos)
		self.rect.center = pos

		#spread = uniform(-GUN_SPREAD, GUN_SPREAD)
		self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.2)
		self.spawn_time = pg.time.get_ticks()
		#self.damage = damage

	def update(self):
		self.mask = pg.mask.from_surface(self.image)
		self.pos += self.vel * self.game.dt
		self.rect.center = self.pos
		if pg.sprite.spritecollideany(self, self.game.walls):
			self.kill()

		if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
			self.kill()

		

class Wall(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = WALL_LAYER
		self.groups = game.all_sprites, game.walls
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.wall_img
		#self.image = pg.Surface((TILESIZE, TILESIZE))
		#self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h):
		self.groups = game.walls
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		#self.image = game.wall_img
		#self.image = pg.Surface((TILESIZE, TILESIZE))
		#self.image.fill(GREEN)
		self.rect = pg.Rect(x, y, w, h)
		self.hit_rect = self.rect
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y





class MuzzleFlash(pg.sprite.Sprite):
	def __init__(self, game, pos):
		self._layer = EFFECTS_LAYER
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		size = randint(20, 50)
		self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
		#self.image = pg.transform.rotate(-self.game.player_img, self.rot)
		#self.image = pg.transform.rotate(choice(game.gun_flashes), (size, size))
		self.rect = self.image.get_rect()
		self.hit_rect =  self.rect
		self.pos = pos
		self.rect.center = pos
		self.spawn_time = pg.time.get_ticks()
		#(self.game.player.pos - self.pos)


	def update(self):
		#self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
		#self.rot = game.player.rot
		if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
			self.kill()

class Item(pg.sprite.Sprite):
	def __init__(self, game, pos, type):
		self._layer = ITEMS_LAYER
		self.groups = game.all_sprites, game.items
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.item_images[type]
		self.rect = self.image.get_rect()
		self.hit_rect = self.rect
		self.type = type
		self.pos = pos
		self.rect.center = pos
		self.tween = tween.easeInOutSine
		self.step = 0
		self.dir = 1

	def update(self):
		#bobbing motion
		offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
		self.rect.centery = self.pos.y + offset * self.dir
		self.step += BOB_SPEED
		if self.step > BOB_RANGE:
			self.step = 0
			self.dir *= -1
