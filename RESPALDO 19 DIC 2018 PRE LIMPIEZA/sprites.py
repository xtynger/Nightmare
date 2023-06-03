import pygame as pg
from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect
import pytweening as tween
from itertools import chain
import math
import time
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
																		#te da un numero con fraccion (int), no de error por esperar un (str). asi que solo le 
																		#asignas doble // si es en este caso, division para que redondee el numero final a impar
		return image

class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = PLAYER_LAYER
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.last_update = 0
		self.current_frame = 0
		self.walking = False
		self.idle = False
		self.attacking = False
		self.attacked = False
		self.load_images()

		self.inmune = False
		self.recovery_time = 3000


		self.image_original = self.idle_knife[0]
		self.image = self.image_original.copy()

		self.rect = self.image.get_rect()
		self.rect.center = (x , y)
		self.hit_rect = PLAYER_HIT_RECT
		self.hit_rect.center = self.rect.center
		self.current_frame = 0
		self.vel = vec(0, 0)
		self.pos = vec(x, y)			#ORIGINAL:  vec(x, y)
		self.rot = 0
		self.last_shot = 0
		self.health = PLAYER_HEALTH 
		self.armor = PLAYER_ARMOR
		self.stamina = PLAYER_STAMINA
		self.thirst = PLAYER_THIRST
		self.stamina_cap = PLAYER_STAMINA_CAP
		self.hunger = PLAYER_HUNGER
		self.weapon = 'hand'
		self.damaged = False # A WAY TO MAKE QUICK SWITCHES ARE THE FLAGS TRUE OR FALSE, THAT BY CHANGING IT WITH SOME KEY OR ACTION, IT CHANGES TO OPPOSITE
		self.score = 0
		self.lives = 3
		self.clip = False
		self.charger_up = False
		self.tired = False
		self.running = False
		self.day_time = pg.time.get_ticks()
		self.D = 00
		self.H = 00
		self.M = 00
		self.S = 00
		self.m = 0
		self.DT = 30
		self.HT = 24
		self.MT = 59
		self.ST = 59
		self.mt = 1
	
		self.reloading = False
		self.reloaded = False
		################## PLAYER STATS SYSTEM

		self.strenght = STRENGHT 
		self.dexterity = DEXTERITY
		self.luck = LUCK
		self.st = PLAYER_STAT_POINTS
		self.sp = PLAYER_SKILL_POINTS

		self.exp = PLAYER_EXP
		self.exp_cap = PLAYER_EXP_CAP
		self.level = PLAYER_LVL 

	def load_images(self):
		self.idle_knife = [self.game.spritesheet_a.get_image(0, 87, 120, 90 ),		#1
							self.game.spritesheet_a.get_image(0, 175.5, 120, 90),	#2
							self.game.spritesheet_a.get_image(0, 263, 120, 90),		#3
							self.game.spritesheet_a.get_image(0, 351, 120, 90),		#4
							self.game.spritesheet_a.get_image(0, 526, 120, 90),		#5
							self.game.spritesheet_a.get_image(0, 614, 120, 90),		#6
							self.game.spritesheet_a.get_image(0, 702, 120, 90),		#7
							self.game.spritesheet_a.get_image(0, 789, 120, 90),		#8
							self.game.spritesheet_a.get_image(0, 877, 120, 90),		#9
							self.game.spritesheet_a.get_image(0, 965, 120, 90),		#10
							self.game.spritesheet_a.get_image(0, 1053, 120, 90),	#11
							self.game.spritesheet_a.get_image(0, 1140, 120, 90),	#12
							self.game.spritesheet_a.get_image(0, 1228, 120, 90),	#13
							self.game.spritesheet_a.get_image(0, 1316, 120, 90),	#14
							self.game.spritesheet_a.get_image(0, 1404, 120, 90),	#15
							self.game.spritesheet_a.get_image(0, 1491, 120, 90),	#16
							self.game.spritesheet_a.get_image(0, 1579, 120, 90),	#17
							self.game.spritesheet_a.get_image(0, 1667, 120, 87),	#18
							]
		self.idle_hand = [self.game.spritesheet_ih.get_image(0, 87, 120, 90 ),		#1
							self.game.spritesheet_ih.get_image(0, 175.5, 120, 90),	#2
							self.game.spritesheet_ih.get_image(0, 263, 120, 90),	#3
							self.game.spritesheet_ih.get_image(0, 351, 120, 90),	#4
							self.game.spritesheet_ih.get_image(0, 526, 120, 90),	#5
							self.game.spritesheet_ih.get_image(0, 614, 120, 90),	#6
							self.game.spritesheet_ih.get_image(0, 702, 120, 90),	#7
							self.game.spritesheet_ih.get_image(0, 789, 120, 90),	#8
							self.game.spritesheet_ih.get_image(0, 877, 120, 90),	#9
							self.game.spritesheet_ih.get_image(0, 965, 120, 90),	#10
							self.game.spritesheet_ih.get_image(0, 1053, 120, 90),	#11
							self.game.spritesheet_ih.get_image(0, 1140, 120, 90),	#12
							self.game.spritesheet_ih.get_image(0, 1228, 120, 90),	#13
							self.game.spritesheet_ih.get_image(0, 1316, 120, 90),	#14
							self.game.spritesheet_ih.get_image(0, 1404, 120, 90),	#15
							self.game.spritesheet_ih.get_image(0, 1491, 120, 90),	#16
							self.game.spritesheet_ih.get_image(0, 1579, 120, 90),	#17
							self.game.spritesheet_ih.get_image(0, 1667, 120, 87),	#18
							]

		self.idle_rifle = [self.game.spritesheet_e.get_image(0, 0, 133, 80 ),		#1
							self.game.spritesheet_e.get_image(0, 80, 133, 80 ),		#1
							self.game.spritesheet_e.get_image(0, 160, 133, 80),		#2
							self.game.spritesheet_e.get_image(0, 240, 133, 80),		#3
							self.game.spritesheet_e.get_image(0, 320, 133, 80),		#4
							self.game.spritesheet_e.get_image(0, 398, 133, 78),		#5
							self.game.spritesheet_e.get_image(0, 477, 133, 79),		#6
							self.game.spritesheet_e.get_image(0, 558, 133, 81),		#7
							self.game.spritesheet_e.get_image(0, 638, 133, 80),		#8
							self.game.spritesheet_e.get_image(0, 716, 133, 78),		#9
							self.game.spritesheet_e.get_image(0, 797, 133, 81),		#10
							self.game.spritesheet_e.get_image(0, 876, 133, 79),		#11
							self.game.spritesheet_e.get_image(0, 955, 133, 79),		#12
							self.game.spritesheet_e.get_image(0, 1034, 133, 79),	#13
							self.game.spritesheet_e.get_image(0, 1112, 133, 78),	#14
							self.game.spritesheet_e.get_image(0, 1193, 133, 78),	#15
							self.game.spritesheet_e.get_image(0, 1271, 133, 78),	#16
							self.game.spritesheet_e.get_image(0, 1350, 133, 79),	#17
							self.game.spritesheet_e.get_image(0, 1430, 133, 80),	#18
							self.game.spritesheet_e.get_image(0, 1508, 133, 78),	#18
							#self.game.spritesheet_e.get_image(0, 1587, 133, 70),	#18
							]	

		self.idle_shotgun = [self.game.spritesheet_is.get_image(0, 82, 132, 80 ),		#1
							self.game.spritesheet_is.get_image(0, 160, 132, 78),		#2
							self.game.spritesheet_is.get_image(0, 239, 132, 79),		#3
							self.game.spritesheet_is.get_image(0, 318, 132, 79),		#4
							self.game.spritesheet_is.get_image(0, 397, 132, 79),		#5
							self.game.spritesheet_is.get_image(0, 476, 132, 79),		#6
							self.game.spritesheet_is.get_image(0, 555, 132, 79),		#7
							self.game.spritesheet_is.get_image(0, 634, 132, 79),		#8
							self.game.spritesheet_is.get_image(0, 714, 132, 80),		#9
							self.game.spritesheet_is.get_image(0, 793, 132, 80),		#10
							self.game.spritesheet_is.get_image(0, 874, 132, 79),	#11
							self.game.spritesheet_is.get_image(0, 954, 132, 80),	#12
							self.game.spritesheet_is.get_image(0, 1033, 132, 79),	#13
							self.game.spritesheet_is.get_image(0, 1112, 132, 79),	#14
							self.game.spritesheet_is.get_image(0, 1192, 132, 80),	#15
							self.game.spritesheet_is.get_image(0, 1270, 132, 78),	#16
							self.game.spritesheet_is.get_image(0, 1350, 132, 80),	#17
							self.game.spritesheet_is.get_image(0, 1429, 132, 79),	#18
							self.game.spritesheet_is.get_image(0, 1508, 132, 79),	#18
							#self.game.spritesheet_is.get_image(0, 1586, 132, 78),	#18
							]

		self.idle_pistol = [self.game.spritesheet_ip.get_image(0, 0, 108, 78),		#1
							self.game.spritesheet_ip.get_image(0, 78, 108, 78),		#1
							self.game.spritesheet_ip.get_image(0, 157, 108, 79),	#2
							self.game.spritesheet_ip.get_image(0, 237, 108, 80),	#3
							self.game.spritesheet_ip.get_image(0, 316, 108, 79),	#4
							self.game.spritesheet_ip.get_image(0, 396, 108, 80),	#5
							self.game.spritesheet_ip.get_image(0, 474, 108, 78),	#6
							self.game.spritesheet_ip.get_image(0, 553, 108, 79),	#7
							self.game.spritesheet_ip.get_image(0, 632, 108, 79),	#8
							self.game.spritesheet_ip.get_image(0, 711, 108, 79),	#9
							self.game.spritesheet_ip.get_image(0, 789, 108, 78),	#10
							self.game.spritesheet_ip.get_image(0, 866, 108, 77),	#11
							self.game.spritesheet_ip.get_image(0, 945, 108, 79),	#12
							self.game.spritesheet_ip.get_image(0, 1023, 108, 78),	#13
							self.game.spritesheet_ip.get_image(0, 1101, 108, 78),	#14
							self.game.spritesheet_ip.get_image(0, 1180, 108, 79),	#15
							self.game.spritesheet_ip.get_image(0, 1260, 108, 80),	#16
							self.game.spritesheet_ip.get_image(0, 1339, 108, 79),	#17
							self.game.spritesheet_ip.get_image(0, 1418, 108, 79),	#18
							self.game.spritesheet_ip.get_image(0, 1497, 108, 79),	#18
							#self.game.spritesheet_e.get_image(0, 1577, 108, 80),	#18
							]

		self.walking_knife = [self.game.spritesheet_b.get_image(0, 0, 118, 88),   	#1
							self.game.spritesheet_b.get_image(0, 87, 118, 88),		#2
							self.game.spritesheet_b.get_image(0, 177, 118, 92),		#3
							self.game.spritesheet_b.get_image(0, 267, 118, 89),		#4
							self.game.spritesheet_b.get_image(0, 356, 118, 89),		#5
							self.game.spritesheet_b.get_image(0, 445, 118, 89),		#6
							self.game.spritesheet_b.get_image(0, 534, 118, 89),		#7
							self.game.spritesheet_b.get_image(0, 621, 118, 87),		#8
							self.game.spritesheet_b.get_image(0, 710, 118, 88),		#9
							self.game.spritesheet_b.get_image(0, 797, 118, 88),		#10
							self.game.spritesheet_b.get_image(0, 885, 118, 87),		#11
							self.game.spritesheet_b.get_image(0, 973, 118, 88),		#12
							self.game.spritesheet_b.get_image(0, 1059, 118, 86),	#13
							self.game.spritesheet_b.get_image(0, 1145, 118, 86),	#14
							self.game.spritesheet_b.get_image(0, 1232, 118, 87),	#15
							self.game.spritesheet_b.get_image(0, 1320, 118, 89),	#16
							self.game.spritesheet_b.get_image(0, 1406, 118, 85),	#17
							self.game.spritesheet_b.get_image(0, 1494, 118, 88),	#18
							self.game.spritesheet_b.get_image(0, 1580, 118, 87),	#19
							self.game.spritesheet_b.get_image(0, 1667, 118, 88),	#20
							#self.game.spritesheet_b.get_image(0, 1752, 118, 87),
							]

		self.walking_hand = [self.game.spritesheet_ih.get_image(0, 0, 118, 88),   	#1
							self.game.spritesheet_ih.get_image(0, 87, 118, 88),		#2
							self.game.spritesheet_ih.get_image(0, 177, 118, 92),	#3
							self.game.spritesheet_ih.get_image(0, 267, 118, 89),	#4
							self.game.spritesheet_ih.get_image(0, 356, 118, 89),	#5
							self.game.spritesheet_ih.get_image(0, 445, 118, 89),	#6
							self.game.spritesheet_ih.get_image(0, 534, 118, 89),	#7
							self.game.spritesheet_ih.get_image(0, 621, 118, 87),	#8
							self.game.spritesheet_ih.get_image(0, 710, 118, 88),	#9
							self.game.spritesheet_ih.get_image(0, 797, 118, 88),	#10
							self.game.spritesheet_ih.get_image(0, 885, 118, 87),	#11
							self.game.spritesheet_ih.get_image(0, 973, 118, 88),	#12
							self.game.spritesheet_ih.get_image(0, 1059, 118, 86),	#13
							self.game.spritesheet_ih.get_image(0, 1145, 118, 86),	#14
							self.game.spritesheet_ih.get_image(0, 1232, 118, 87),	#15
							self.game.spritesheet_ih.get_image(0, 1320, 118, 89),	#16
							self.game.spritesheet_ih.get_image(0, 1406, 118, 85),	#17
							self.game.spritesheet_ih.get_image(0, 1494, 118, 88),	#18
							self.game.spritesheet_ih.get_image(0, 1580, 118, 87),	#19
							self.game.spritesheet_ih.get_image(0, 1667, 118, 88),	#20
							#self.game.spritesheet_b.get_image(0, 1752, 118, 87),
							]

		self.walking_pistol = [self.game.spritesheet_wp.get_image(0, 0, 110, 77 ),		#1
							self.game.spritesheet_wp.get_image(0, 82, 110, 77),			#1
							self.game.spritesheet_wp.get_image(0, 159, 110, 80),		#2
							self.game.spritesheet_wp.get_image(0, 240, 110, 79),		#3
							self.game.spritesheet_wp.get_image(0, 318, 110, 79),		#4
							self.game.spritesheet_wp.get_image(0, 398, 110, 79),		#5
							self.game.spritesheet_wp.get_image(0, 479, 110, 79),		#6
							self.game.spritesheet_wp.get_image(0, 558, 110, 79),		#7
							self.game.spritesheet_wp.get_image(0, 638, 110, 78),		#8
							self.game.spritesheet_wp.get_image(0, 718, 110, 79),		#9
							self.game.spritesheet_wp.get_image(0, 799, 110, 79),		#10
							self.game.spritesheet_wp.get_image(0, 879, 110, 79),		#11
							self.game.spritesheet_wp.get_image(0, 959, 110, 79),		#12
							self.game.spritesheet_wp.get_image(0, 1038, 110, 80),		#13
							self.game.spritesheet_wp.get_image(0, 1118, 110, 78),		#14
							self.game.spritesheet_wp.get_image(0, 1199, 110, 80),		#15
							self.game.spritesheet_wp.get_image(0, 1278, 110, 79),		#16
							self.game.spritesheet_wp.get_image(0, 1358, 110, 79),		#17
							self.game.spritesheet_wp.get_image(0, 1438, 110, 78),		#18
							self.game.spritesheet_wp.get_image(0, 1517, 110, 78),		#18
							#self.game.spritesheet_wp.get_image(0, 1597, 110, 79),		#18
							]

		self.walking_rifle = [self.game.spritesheet_wr.get_image(0, 0, 133, 77 ),		#1
							self.game.spritesheet_wr.get_image(0, 77, 133, 77),			#1
							self.game.spritesheet_wr.get_image(0, 157, 133, 80),		#2
							self.game.spritesheet_wr.get_image(0, 236, 133, 79),		#3
							self.game.spritesheet_wr.get_image(0, 315, 133, 79),		#4
							self.game.spritesheet_wr.get_image(0, 394, 133, 79),		#5
							self.game.spritesheet_wr.get_image(0, 473, 133, 79),		#6
							self.game.spritesheet_wr.get_image(0, 552, 133, 79),		#7
							self.game.spritesheet_wr.get_image(0, 630, 133, 78),		#8
							self.game.spritesheet_wr.get_image(0, 709, 133, 79),		#9
							self.game.spritesheet_wr.get_image(0, 788, 133, 79),		#10
							self.game.spritesheet_wr.get_image(0, 867, 133, 79),		#11
							self.game.spritesheet_wr.get_image(0, 946, 133, 79),		#12
							self.game.spritesheet_wr.get_image(0, 1026, 133, 80),		#13
							self.game.spritesheet_wr.get_image(0, 1104, 133, 78),		#14
							self.game.spritesheet_wr.get_image(0, 1184, 133, 80),		#15
							self.game.spritesheet_wr.get_image(0, 1263, 133, 79),		#16
							self.game.spritesheet_wr.get_image(0, 1342, 133, 79),		#17
							self.game.spritesheet_wr.get_image(0, 1420, 133, 78),		#18
							self.game.spritesheet_wr.get_image(0, 1498, 133, 78),		#18
							#self.game.spritesheet_wr.get_image(0, 1577, 133, 79),		#18
							]

		self.walking_shotgun = [self.game.spritesheet_ws.get_image(0, 0, 110, 77 ),		#1
								self.game.spritesheet_ws.get_image(0, 82, 110, 77),			#1
								self.game.spritesheet_ws.get_image(0, 159, 110, 80),		#2
								self.game.spritesheet_ws.get_image(0, 240, 110, 79),		#3
								self.game.spritesheet_ws.get_image(0, 318, 110, 79),		#4
								self.game.spritesheet_ws.get_image(0, 398, 110, 79),		#5
								self.game.spritesheet_ws.get_image(0, 479, 110, 79),		#6
								self.game.spritesheet_ws.get_image(0, 558, 110, 79),		#7
								self.game.spritesheet_ws.get_image(0, 638, 110, 78),		#8
								self.game.spritesheet_ws.get_image(0, 718, 110, 79),		#9
								self.game.spritesheet_ws.get_image(0, 799, 110, 79),		#10
								self.game.spritesheet_ws.get_image(0, 879, 110, 79),		#11
								self.game.spritesheet_ws.get_image(0, 959, 110, 79),		#12
								self.game.spritesheet_ws.get_image(0, 1038, 110, 80),		#13
								self.game.spritesheet_ws.get_image(0, 1118, 110, 78),		#14
								self.game.spritesheet_ws.get_image(0, 1199, 110, 80),		#15
								self.game.spritesheet_ws.get_image(0, 1278, 110, 79),		#16
								self.game.spritesheet_ws.get_image(0, 1358, 110, 79),		#17
								self.game.spritesheet_ws.get_image(0, 1438, 110, 78),		#18
								self.game.spritesheet_ws.get_image(0, 1517, 110, 78),		#18
								#self.game.spritesheet_wp.get_image(0, 1597, 110, 79),		#18
								]

		self.attacking_knife = [self.game.spritesheet_c.get_image(0, 0, 126, 92),
								self.game.spritesheet_c.get_image(0, 92, 126,  117),
								self.game.spritesheet_c.get_image(0, 209, 126, 95),
								self.game.spritesheet_c.get_image(0, 304, 126, 90),
								self.game.spritesheet_c.get_image(0, 394, 126,  114),
								#self.game.spritesheet_c.get_image(0, 508, 126, 85),
								#self.game.spritesheet_c.get_image(0, 593, 126,  130),
								#self.game.spritesheet_c.get_image(0, 729, 126, 85),
								#self.game.spritesheet_c.get_image(0, 808, 126,  125),
								#self.game.spritesheet_c.get_image(0, 934, 126, 90),
								self.game.spritesheet_c.get_image(0, 1033, 126, 85),
								self.game.spritesheet_c.get_image(0, 1118, 126, 90),
								#self.game.spritesheet_c.get_image(0, 1208, 126, 90),
								#self.game.spritesheet_c.get_image(0, 1298, 126, 90),
								#self.game.spritesheet_c.get_image(0, 1390, 126, 135),
								#self.game.spritesheet_c.get_image(0, 1522, 126, 135),
								]

		self.shoting_rifle = [self.game.spritesheet_d.get_image(0, 0, 126, 78),
								self.game.spritesheet_d.get_image(0, 78, 126,  79),
								self.game.spritesheet_d.get_image(0, 157, 126, 79),
								]

		self.attacking_shotgun = [self.game.spritesheet_as.get_image(0, 0, 126, 78),
								self.game.spritesheet_as.get_image(0, 78, 126,  79),
								self.game.spritesheet_as.get_image(0, 157, 126, 79),
								]

		for frame in self.idle_knife:
			frame.set_colorkey(RED)
		for frame in self.walking_knife:
			frame.set_colorkey(RED)

		for frame in self.attacking_knife:
			frame.set_colorkey(RED)		
		for frame in self.shoting_rifle:
			frame.set_colorkey(RED)		
		for frame in self.idle_rifle:
			frame.set_colorkey(RED)

		for frame in self.idle_rifle:
			frame.set_colorkey(RED)

		for frame in self.walking_rifle:
			frame.set_colorkey(RED)


		for frame in self.walking_pistol:
			frame.set_colorkey(RED)


		for frame in self.idle_pistol:
			frame.set_colorkey(RED)

		for frame in self.idle_hand:
			frame.set_colorkey(RED)

		for frame in self.walking_hand:
			frame.set_colorkey(RED)

		for frame in self.walking_shotgun:
			frame.set_colorkey(RED)

		for frame in self.idle_shotgun:
			frame.set_colorkey(RED)

		for frame in self.attacking_shotgun:
			frame.set_colorkey(RED)




		#self.walk_frames_r = [self.game.spritesheet.get_image(678, 860, 120, 201),
								#self.game.spritesheet.get_image(692, 1458, 120, 207)]
		#for frame in self.walk_frames_r:
			#frame.set_colorkey(BLACK)
		#self.walk_frames_l = []
		#for frame in self.walk_frames_r:
		#	self.walk_frames_l.append(pg.transform.flip(frame, True, False))
		#self.jump_frame = [self.game.spritesheet.get_image(382, 763, 150, 181)]

	def get_keys(self):
		self.rot_speed = 0
		self.vel =vec(0, 0)

		now = pg.time.get_ticks()
		keys = pg.key.get_pressed()	

		if keys[pg.K_LEFT] or keys[pg.K_a]:
			self.rot_speed = PLAYER_ROT_SPEED * 2

			#self.vel.x = -PLAYER_SPEED
		if keys[pg.K_RIGHT] or keys[pg.K_d]:
			self.rot_speed = -PLAYER_ROT_SPEED * 2

			#self.vel.x = PLAYER_SPEED
		if not self.tired and keys[pg.K_UP] or not self.tired and  keys[pg.K_w]:
			#self.walking == True
			#self.stamina -= 0.1
			self.vel = vec(PLAYER_SPEED * self.dexterity, 0).rotate(-self.rot) #ADDING ROTATE PARAMETER MAKES IT WALK TOWARDS THE DIRECTION YOU TURN TO
			if self.walking and keys[pg.K_LSHIFT]:
				self.vel = vec(PLAYER_SPEED + 550, 0).rotate(-self.rot)
				self.running = True
			else:
				self.running = False
				#self.stamina -= 0.5

			#self.vel.y = -PLAYER_SPEED
		if keys[pg.K_DOWN] or keys[pg.K_s]:
			self.vel = vec(-PLAYER_SPEED - 20, 0).rotate(-self.rot) #ADDING ROTATE PARAMETER MAKES IT WALK TOWARDS THE DIRECTION YOU TURN TO
			#self.vel.y = PLAYER_SPEED

		######## CALCULA CONDICIONES PARA DISPARAR, SI SE TIENE BALAS O NO ################### 

		if keys[pg.K_SPACE]  and self.weapon != 'knife' and self.weapon != 'hand' and WEAPONS[self.weapon]['gun_comb'] > 0:  ###PROPIO PARA CONTEO DE BALAS
			self.clip = True  #### PROPIO PARA CONTEO DE BALAS USANDO FLAGS
			self.shoot()


		
		if keys[pg.K_1] and self.game.knife == True:
			self.weapon = 'knife'
		if keys[pg.K_2] and self.game.gun == True:
			self.weapon = 'pistol'
			
		if keys[pg.K_3] and self.game.shotgun == True:
			self.weapon = 'shotgun'

		if keys[pg.K_4] and self.game.rifle == True:
			self.weapon = 'rifle'

		if keys[pg.K_5] and WEAPONS['medkit']['ammount'] > 0 and self.health < 100:
			self.add_health(WEAPONS['medkit']['health'])
			WEAPONS['medkit']['ammount'] -= 1

		if keys[pg.K_6] and self.st > 0:
			self.st -= 1
			self.strenght += 1
		############################## S E C C I O N   D E   A N I M A C I O N   F L A G S ############################################################################
		###############################################################################################################################################
		############################## I D L E S / W A L K I N G S ############################################################################

		if self.vel == vec(0,0):
			self.walking = False
			self.idle = True
			self.attacking = False 
			if keys[pg.K_SPACE]:
				self.attacking = True

		if self.vel != vec(0,0):# self.vel = vec(0, 0)
			self.walking = True
			self.idle = False
			self.attacking = False
			if keys[pg.K_SPACE]:
				self.attacking = True
		else:
			self.walking = False
			self.idle = True
			if keys[pg.K_SPACE]:
				self.attacking = True

		if keys[pg.K_SPACE]:
			self.attacking = True
			self.walking = False
			self.idle = False

		else:
			self.attaking = False
		if self.walking and self.stamina > 1:
			self.stamina -= 0.1

		if self.running and self.stamina <= 100 and self.stamina :
			self.stamina -= 1

		if self.stamina <= 0:
			self.running = False

		########### ################### ################### ################### ################### ################### ################### 
		############# CODIGO PROPIO EN PARTE, PARA DETERMINAR QUE SI SE TIENE BALAS, SE EJECUTE TODO, SINO, NO DISPARA ####################
		########### ################### ################### ################### ################### ################### ################### 

	def reload(self):
		timer = pg.time.Clock()
		timer.tick()
		self.reloading_time = RELOADING_TIME
		self.reloaded_time = RELOADING_TIME
		self.relo_cycle = RELOADING_CYCLE
		self.reloading = True
		print(self.reloading)

		if self.weapon == 'shotgun':
			if WEAPONS[self.weapon]['gun_comb'] <= WEAPONS[self.weapon]['charger_size'] -1:
				WEAPONS[self.weapon]['gun_comb'] += 1
				WEAPONS[self.weapon]['total_bullets'] -= 1
		if self.weapon != 'shotgun':
			if WEAPONS[self.weapon]['gun_comb'] <= 0 and WEAPONS[self.weapon]['total_bullets'] >= WEAPONS[self.weapon]['charger_size']:
				WEAPONS[self.weapon]['gun_comb'] += WEAPONS[self.weapon]['charger_size']
				WEAPONS[self.weapon]['total_bullets'] -= WEAPONS[self.weapon]['charger_size']
	
				if self.weapon == 'rifle':
					self.game.effects_sounds['reloading_rifle'].play()


			elif WEAPONS[self.weapon]['gun_comb'] <= 0 and WEAPONS[self.weapon]['total_bullets'] <= WEAPONS[self.weapon]['charger_size']:
				WEAPONS[self.weapon]['gun_comb'] += WEAPONS[self.weapon]['total_bullets']
				WEAPONS[self.weapon]['total_bullets'] = 0

	def shoot(self):
		if self.clip:  ####PROPIO PARA CONTEO DE BALAS ################### ###################  PROPIO
			try:		##PROPOP PARA CONTEO DE BALAS  ################### ###################  PROPIO
				now = pg.time.get_ticks()
				if now - self.last_shot > WEAPONS[self.weapon]['rate']:
					self.last_shot = now
					dir = vec(1,0).rotate(-self.rot)
					pos = self.pos + BARREL_OFFSET.rotate(-self.rot) #INDICA LA POSICION DONDE SE DIBUJA EL DISPARO PARA APARENTAR QUE SALE DEL ARMA
					self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
					#if self.weapon != 'shotgun':
					for i in range(WEAPONS[self.weapon]['bullet_count']):
						spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
						Bullet(self.game, pos, dir.rotate(spread))  #, WEAPONS[self.weapon]['damage']  (agregar eso para calcular mejor el da;o de balas sueltas al cambiar arma)
						snd = choice(self.game.weapon_sounds[self.weapon])#choice(self.player_hit_sounds).play()						
						if snd.get_num_channels() > 2:
							snd.stop()

						if WEAPONS[self.weapon]['gun_comb'] > 0:
							WEAPONS[self.weapon]['gun_comb'] -= 1
						if WEAPONS[self.weapon]['gun_comb'] <= 0:
							WEAPONS[self.weapon]['gun_comb'] == 0
							self.clip = False
						
						snd.play()	
					MuzzleFlash(self.game, pos) #agregar , dir.rotate() dentro para probar
			except:									################### ################### PROPIO
				self.clip = False

####################################################################################################################################################						

	def clock_timer(self):
		self.watch = (' %d' %(self.H), (self.M), (self.S)) 

		#self.H, + self.M, + self.S
		if self.game.playing:
			self.m += 0.1
			if self.m > self.mt:
				self.S += 1
				self.m = 0
				#S += 1
				if self.S > self.ST:
					self.M += 1
					self.S = 0
					if self.M > self.MT:
						self.H += 1  
						self.M = 0
						if self.H > self.HT:
							self.H = 0

	def status(self):
		self.text = True
		self.time_count = 0

	def hit(self):
		self.damaged = True
		self.damage_alpha = chain(DAMAGE_ALPHA * 4)

	def update(self):
		self.get_keys()
		self.animate()

		mouse = pg.mouse.get_pressed()

		if mouse[0] and self.game.player.rect.collidepoint(self.game.mouse_pos):
			#self.shoot()
			#self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
			print('working')
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
		

		if not self.walking and self.stamina < 100:
			self.stamina += 0.2

		if self.tired:
			self.walking = False


		if self.stamina <= 1:
			self.tired = True
			
		if self.tired and self.stamina >= 30:
			self.tired = False


		if self.game.playing:
			#self.thirst -= 0.01
			self.hunger -= 0.1
			if self.hunger <= 0:
				self.hunger = 0

		if self.exp >= self.exp_cap:
			self.exp = 0
			self.exp_cap += self.exp_cap / 100 * 60
			self.level += 1
			self.sp += 1
			self.st += 3
			print(self.level)
			print(self.exp_cap)
			print('level up')


		if self.hunger <= 0:
			self.health -= 0.3
			if self.health <= 0:
				self.lives -= 1
				self.game.playing = False


		if self.damaged:
				try:	
					for frame in frames:
						frame.set_colorkey(RED)  ############## S O L U C I O N   P A R A   E L I M I N A R   F O N D O    A    I M A G E N E S   A L   S U F R I R   D A Ñ O #######
						self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT) #PROBAR EL SPECIAL FLAG FUNCION PARA MANIPULAR COLORES				
				except:
					self.damaged = False
		self.clock_timer()

		for numberi in  str(STRENGHT):
			self.health + 3

	def animate(self):
		now = pg.time.get_ticks()

		if self.idle and self.weapon == 'hand' or self.walking and self.weapon == 'hand':
			if now - self.last_update > 50:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.idle_hand)
				#bottom = self.rect.bottom
				self.image = self.idle_hand[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			##############################################################################################################################

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

			##############################################################################################################################

		#show idle animation on place
		if self.idle and self.weapon == 'knife':
			if now - self.last_update > 50:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.idle_knife)
				#bottom = self.rect.bottom
				self.image = self.idle_knife[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			##############################################################################################################################

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

			##############################################################################################################################

		if self.idle and self.weapon == 'pistol':
			if now - self.last_update > 50:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.idle_pistol)
				#bottom = self.rect.bottom
				self.image = self.idle_pistol[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			##############################################################################################################################

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

			##############################################################################################################################
		################################# A T T A C K  R I F L E  A N I M A T I O N###########################################################################

		if self.idle and self.weapon == 'rifle':
			if now - self.last_update > 40:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.idle_rifle)
				#bottom = self.rect.bottom
				self.image = self.idle_rifle[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
				#print(self.current_frame)
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			############################################################################################################################## shoting_rifle

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

			##############################################################################################################################
		################################# A T T A C K  R I F L E  A N I M A T I O N###########################################################################

		if self.idle and self.weapon == 'shotgun' or self.walking and self.weapon == 'shotgun':
			if now - self.last_update > 40:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.idle_shotgun)
				#bottom = self.rect.bottom
				self.image = self.idle_shotgun[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
				#print(self.current_frame)
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			############################################################################################################################## shoting_rifle

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

			##############################################################################################################################

		if self.walking and self.weapon == 'knife':
			if now - self.last_update > 40:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.walking_knife)
				#bottom = self.rect.bottom
				self.image = self.walking_knife[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			##############################################################################################################################

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR
				#print(self.current_frame)

			##############################################################################################################################

		if self.attacking and self.weapon == 'knife':
			if now - self.last_update > 70:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.attacking_knife)
				#bottom = self.rect.bottom
				self.image = self.attacking_knife[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			############################################################################################################################## 

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

		################################# A T T A C K  R I F L E  A N I M A T I O N###########################################################################

		if self.attacking and self.weapon == 'rifle':
			if now - self.last_update > 60:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.shoting_rifle)
				#bottom = self.rect.bottom
				self.image = self.shoting_rifle[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			############################################################################################################################## shoting_rifle

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

			##############################################################################################################################
		################################# A T T A C K  R I F L E  A N I M A T I O N###########################################################################

		if self.attacking and self.weapon == 'shotgun':
			if now - self.last_update > 60:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.attacking_shotgun)
				#bottom = self.rect.bottom
				self.image = self.attacking_shotgun[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			############################################################################################################################## shoting_rifle

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

			##############################################################################################################################

		if self.walking and self.weapon == 'rifle':
			if now - self.last_update > 50:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.walking_rifle)
				#bottom = self.rect.bottom
				self.image = self.walking_rifle[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
				#print(self.current_frame)
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			############################################################################################################################## shoting_rifle

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR


		if self.walking and self.weapon == 'pistol' or self.attacking and self.weapon == 'pistol':
			if now - self.last_update > 60:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.walking_pistol)
				#bottom = self.rect.bottom
				self.image = self.walking_pistol[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
				#print(self.current_frame)
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			############################################################################################################################## shoting_rifle

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

			##############################################################################################################################
			

			##############################################################################################################################
		################################# A T T A C K  R I F L E  A N I M A T I O N###########################################################################

		if self.idle and self.weapon == 'rifle':
			if now - self.last_update > 50:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.idle_rifle)
				#bottom = self.rect.bottom
				self.image = self.idle_rifle[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
				#print(self.current_frame)
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			############################################################################################################################## shoting_rifle

				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

			##############################################################################################################################
		
				#self.rect.bottom = bottom
		self.mask = pg.mask.from_surface(self.image) #esto crea una mascara entorno a la imagen para poder hacer colisoon perfecta por pixeles

	def day_night_clock(self):

		time = pg.time.get_ticks()
		
		if not self.game.night and time > DAYTIME:
			time -= DAYTIME
			self.game.night = True

		if self.game.night:
			#self.game.render_fog()
			time -= NIGHTTIME
   
		if self.game.night and time > NIGHTTIME:
			time -= DAYTIME
			self.game.night = False
			#return



		
		print(time)

	def add_health(self, amount):
		self.health += amount
		if self.health > PLAYER_HEALTH:
			self.health = PLAYER_HEALTH

	def add_armor(self, amount):
		self.armor += amount
		if self.armor > PLAYER_ARMOR:
			self.armor = PLAYER_ARMOR

################### ################### ################### ################### ################### ################### ################### ################### 
#######################################	P R U E B A    D E   A N I M A C I O N    D E   P E R S O N A J E #####################################################
################### ################### ################### ################### ################### ################### ################### ################### 

class Shop_menu(pg.sprite.Sprite):
	def __init__(self, center):   
		pg.sprite.Sprite.__init__(self)
		self.type = random.choice(['shield', 'gun'])
		self.image = powerup_images[self.type]
		self.image.set_colorkey(NEGRO)
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.speedy = 3 
###############################################################################################################################################################

###############################################################################################################################################################

class Mob(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self._layer = MOB_LAYER
		self.groups = game.all_sprites, game.mobs
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.last_update = 0
		self.current_frame = 0
		self.load_images()
		self.image_original = self.idle_zombie[1]
		self.image = self.image_original.copy()
		#self.image = game.mob_img.copy()
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.hit_rect = MOB_HIT_RECT.copy()
		self.hit_rect.center = self.rect.center
		self.pos = vec(x, y)   #sin el  * TILESIZE el mob aparecera donde el rectangulo de la capa obstacles del juego, determine
		self.vel = vec(0, 0) 
		self.acc = vec(0, 0)
		self.rect.center = (x,y)#self.pos
		self.rot = 0
		self.health = MOB_HEALTH
		self.speed = choice(MOB_SPEEDS)
		self.target = game.player
		self.rot_speed = 0
		self.attack_delay = pg.time.get_ticks()


		self.walking = False 
		self.idle = True 
		self.attacking = False
		self.in_range = False
		self.on_delay = False
		self.roaming = True

	def load_images(self):

		self.idle_zombie = [self.game.spritesheet_iz.get_image(0, 0, 100, 90),		#1
							self.game.spritesheet_iz.get_image(0, 90, 100, 90),		#2
							self.game.spritesheet_iz.get_image(0, 175, 100, 90),	#3
							self.game.spritesheet_iz.get_image(0, 264, 100, 90),	#4
							self.game.spritesheet_iz.get_image(0, 351, 100, 90),	#5
							self.game.spritesheet_iz.get_image(0, 438, 100, 90),	#6
							self.game.spritesheet_iz.get_image(0, 525, 100, 90),	#7
							self.game.spritesheet_iz.get_image(0, 613, 100, 90),	#8
							self.game.spritesheet_iz.get_image(0, 700, 100, 90),	#9
							self.game.spritesheet_iz.get_image(0, 788, 100, 90),	#10
							self.game.spritesheet_iz.get_image(0, 875, 100, 90),	#11
							self.game.spritesheet_iz.get_image(0, 965, 100, 90),	#12
							self.game.spritesheet_iz.get_image(0, 1053, 100, 90),	#13
							self.game.spritesheet_iz.get_image(0, 1142, 100, 90),	#14
							self.game.spritesheet_iz.get_image(0, 1230, 100, 90),	#15
							self.game.spritesheet_iz.get_image(0, 1318, 100, 90),	#16
							self.game.spritesheet_iz.get_image(0, 1406, 100, 90),	#17
							#self.game.spritesheet_iz.get_image(0, 1494, 100, 87),	#18
							]


		self.walking_zombie = [self.game.spritesheet_wz.get_image(0, 0, 100, 103),		#1
								self.game.spritesheet_wz.get_image(0, 100, 100, 100),	#2
								self.game.spritesheet_wz.get_image(0, 204, 100, 104),	#3
								self.game.spritesheet_wz.get_image(0, 310, 100, 106),	#4
								self.game.spritesheet_wz.get_image(0, 415, 100, 105),	#5
								self.game.spritesheet_wz.get_image(0, 521, 100, 106),	#6
								self.game.spritesheet_wz.get_image(0, 626, 100, 105),	#7
								self.game.spritesheet_wz.get_image(0, 730, 100, 104),	#8
								self.game.spritesheet_wz.get_image(0, 835, 100, 105),	#9
								self.game.spritesheet_wz.get_image(0, 938, 100, 103),	#10
								self.game.spritesheet_wz.get_image(0, 1042, 100, 104),	#11
								self.game.spritesheet_wz.get_image(0, 1147, 100, 105),	#12
								self.game.spritesheet_wz.get_image(0, 1253, 100, 106),	#13
								self.game.spritesheet_wz.get_image(0, 1359, 100, 106),	#14
								self.game.spritesheet_wz.get_image(0, 1462, 100, 103),	#15
								self.game.spritesheet_wz.get_image(0, 1565, 100, 103),	#16
								self.game.spritesheet_wz.get_image(0, 1665, 100, 100),	#17
								#self.game.spritesheet_iz.get_image(0, 1767, 100, 102),	#18
								]


		self.attacking_zombie = [self.game.spritesheet_az.get_image(0, 0, 100, 88),		#1
								self.game.spritesheet_az.get_image(0, 88, 100, 90),		#2
								self.game.spritesheet_az.get_image(0, 188, 100, 117),	#3
								self.game.spritesheet_az.get_image(0, 305, 88, 117),	#4
								self.game.spritesheet_az.get_image(0, 422, 88, 117),	#5
								self.game.spritesheet_az.get_image(0, 540, 88, 80),		#6
								self.game.spritesheet_az.get_image(0, 615, 100, 75),	#7
								self.game.spritesheet_az.get_image(0, 696, 100, 81),	#8
								self.game.spritesheet_az.get_image(0, 783, 100, 87),	#9
								#self.game.spritesheet_az.get_image(0, 870, 100, 87),	#9
								]

		for frame in self.idle_zombie:
			frame.set_colorkey(RED)

		for frame in self.walking_zombie:
			frame.set_colorkey(RED)		

		for frame in self.attacking_zombie:
			frame.set_colorkey(RED)

	def avoid_mobs(self):
		for mob in self.game.mobs:
			if mob != self:
				dist = self.pos - mob.pos
				if 0 < dist.length() < AVOID_RADIUS:
					self.acc += dist.normalize()

######################################################################################################
	def attack_flags(self):
		if self.on_delay and self.in_range:
			self.attacking  = False

		if not self.on_delay and self.in_range:
			self.attacking = True


######################################################################################################

	def animation_flags(self):

		target_dist = self.target.pos - self.pos
		radius = self.target.pos - self.pos

##############################################
###### PRUEBAS PARA DEAMBUALR ##############################################

		if radius.length_squared() > MOB_ATK_RANGE**2 and radius.length_squared() > PLAYER_RADIUS**2:
			self.roaming = True
		else:
			self.roaming = False

############################################################################################

		if radius.length_squared() < MOB_ATK_RANGE**2:
			self.attacking = True
		else:
			self.attacking = False

##############################################
###### PRUEBAS PARA DEAMBUALR ##############################################

		if self.roaming:
			self.walking = True
			self.idle = False
			self.attacking = False

############################################################################

		#if self.walking:
		if self.vel == vec(0,0):
			self.walking = False
			self.idle = True
			self.attacking = False

			#self.animate()
			if target_dist.length_squared() < PLAYER_RADIUS**2:
				self.idle = False 
				self.walking = True
			if radius.length_squared() < MOB_ATK_RANGE**2:
				self.attacking = True
		
		#if self.idle:		
		if self.vel != vec(0,0):# self.vel = vec(0, 0)
			self.walking  = True
			self.idle = False
			if target_dist.length_squared() < PLAYER_RADIUS**2:
				#time.sleep(2.1)
				#self.attacking = True
				self.idle = False 
				self.walking = True
		


######################################################################################################


######################################################################################################
	def update(self):
		target_dist = self.target.pos - self.pos
		self.animation_flags()
	#####################################################################
		################## A T T A C K   D E L A Y   C L O C K ############################################
		timer = pg.time.Clock()
		timer.tick()
		timer2 = pg.time.Clock()
		timer2.tick()
		self.attack_delay = ATTACK_DELAY
		self.attack_duration = ATTACK_DURATION
		self.attack_clock = ATTACK_CLOCK
		self.attack_cycle = ATTACK_CYCLE


		##########################################################################################
		################################# CODIGO PRUEBA PARA HACER DELAY ENTRE LOS ATAQUES DEL ENEMIGO ###############

		if target_dist.length_squared() < DETECT_RADIUS**2 and not self.roaming:
			self.animate()
			if random() < 0.002:
				choice(self.game.zombie_moan_sounds).play()
			if self.in_range and not self.on_delay:
				self.attack_duration += timer.tick()
				if self.attack_duration  < self.attack_cycle:
					self.attacking = True

				if self.attack_duration > self.attack_cycle:
					self.on_delay = True
       	 		#self.attacking = False

			if self.on_delay and self.in_range:
				self.attack_delay += timer2.tick()
				if self.attack_delay < self.attack_duration:
					self.attacking = False
			self.rot = target_dist.angle_to(vec(1,0))
			#self.image = pg.transform.rotate(self.game.mob_img, self.rot)
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


		if self.roaming:
			self.animate()
			#if random() < 0.002:
			#	choice(self.game.zombie_moan_sounds).play()
			if self.in_range and not self.on_delay:
				self.attack_duration += timer.tick()
				if self.attack_duration  < self.attack_cycle:
					self.attacking = True

				if self.attack_duration > self.attack_cycle:
					self.on_delay = True

       	 		#self.attacking = False

			if self.on_delay and self.in_range:
				self.attack_delay += timer2.tick()
				if self.attack_delay < self.attack_duration:
					self.attacking = False
			#self.rot = random.randint(0,360)
			#self.rot = random(0,359).target_dist.angle_to(vec(5,5)) #target_dist.angle_to(vec(1,0))
			#self.image = pg.transform.rotate(self.game.mob_img, self.rot)
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
		self.mask = pg.mask.from_surface(self.image)

		############################AGREGADO POR MI PARA INCLUIR SALPICADURAS AL DISPARARLES##############################

		if pg.sprite.spritecollideany(self, self.game.bullets):
			self.game.map_img.blit(self.game.split, self.pos - vec(32,32))

		############################################################################################################		
		if self.health <= 0:
			choice(self.game.zombie_hit_sounds).play()
			self.kill()
			self.game.player.score += 50 #############################################ESTA LINEA AGREGA SCORE AL MATAR MOBS ################
			self.game.map_img.blit(self.game.splat, self.pos - vec(32,32)) ############### CODIGO PROPIO PARA AGREGAR MANCHA AL MORIR UN MOB

	def animate(self):
		now = pg.time.get_ticks()
		#show idle animation on place
		if self.vel == vec(0,0):
			self.idle = True

		if self.idle:
			if now - self.last_update > 60:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.idle_zombie)
				#bottom = self.rect.bottom
				self.image = self.idle_zombie[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   			
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR
		#####################################################################################################################
		if self.walking:
			if now - self.last_update > 60:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.walking_zombie)
				#bottom = self.rect.bottom
				self.image = self.walking_zombie[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR
		######################################################################################################################
		if self.attacking:
			if now - self.last_update > 50:
				self.last_update = now
				self.current_frame = (self.current_frame + 1) % len(self.attacking_zombie)
				#bottom = self.rect.bottom
				self.image = self.attacking_zombie[self.current_frame]
				self.rect = self.image.get_rect()
				#self.latest = self.image   
			
			######################################  ##################################	##########################################
			########### L I N E A S   D E F I N I T I V A S   P A R A   R O T A C I O N   E N   A N I M A C I O N ############
			##############################################################################################################################
				self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
				self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

		######################################################################################################################
		



		self.mask = pg.mask.from_surface(self.image)
		pg.display.flip()

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


class Explosion(pg.sprite.Sprite): 
	def __init__(self, game, center, size): 
		pg.sprite.Sprite.Super().__init__(self) 
		self.game = game
		self.size = size  
		self.image = self.game.explosion_anim[size][0]  
		self.rect = self.image.get_rect() 
		self.rect.center = center 
		self.frame = 0  
		self.last_update = pg.time.get_ticks() 
		self.frame_rate = 60 

	def update(self):

		now = pg.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(self.game.explosion_anim[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = self.gamexplosion_anim[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center


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
		self.rot = 0
		self.rot_speed = 0


	def update(self):
		#self.rot = (self.game.player.pos - self.pos).angle_to(vec(1,0))
		#self.rot = game.player.rot
		self.rot = (self.rot + self.rot_speed * self.game.dt) % 360 #PRUEBA PARA ROTAR
		self.image = pg.transform.rotate(self.image, self.rot) #PRUEBA PARA ROTAR

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
