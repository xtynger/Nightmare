		timer = pg.time.Clock()
		timer.tick()
		self.reloading_time = RELOADING_TIME
		self.reloaded_time = RELOADING_TIME
		self.relo_cycle = RELOADING_CYCLE
		self.reloading = True
		print(self.reloading)
		while self.reloading and  WEAPONS[self.weapon]['gun_comb'] <= 7:
			print(self.reloading_time)
			#while self.reloading:

	        ########################## DAYTIME AND WEATHER CLOCK #################################
	        ################# DAY CLOCK
			if self.reloading:
				self.reloaded = False
				self.reloading_time += timer.tick() 
                #print(self.day_count, 'day')
				if self.reloading_time  > self.relo_cycle:
					if WEAPONS[self.weapon]['gun_comb'] <= 7:
						WEAPONS[self.weapon]['gun_comb'] += 1
						WEAPONS[self.weapon]['total_bullets'] -= 1
						self.reloading = False
						self.reloaded = True                      
						self.reloading_time = 0  
						self.reloaded_time = 0                   
            ################# NIGHT CLOCK
			if self.reloaded:
				self.reloading = False
				self.reloaded_time += timer.tick() 
                #print(self.night_count, 'night')
				if self.reloaded_time  > self.relo_cycle:
					self.reloading = True
					self.reloading_time = 0