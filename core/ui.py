# Third-Party Imports
import pygame

class Button:

	def __init__(self, text, width, height, pos, elevation, font):
		#Core attributes 
		self.pressed = False
		self.used = False
		self.elevation = elevation
		self.dynamic_elevation = elevation
		self.original_y_pos = pos[1]

		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = '#54C392'

		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#15B392'

		#text
		self.text_surf = font.render(text,True,'#FFFFFF')
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self, display, events):
		# elevation logic 

		self.top_rect.y = self.original_y_pos - self.dynamic_elevation
		self.text_rect.center = self.top_rect.center 

		self.text_rect.y -= 2

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

		pygame.draw.rect(display,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(display,self.top_color, self.top_rect,border_radius = 12)

		display.blit(self.text_surf, self.text_rect)

		self.check_click(events)

	def check_click(self, events):

		if self.used:
				self.top_color = '#808080'
				return


		mouse_pos = pygame.mouse.get_pos()
		if self.top_rect.collidepoint(mouse_pos):
			self.top_color = '#D74B4B'  
		else:
			self.dynamic_elevation = self.elevation
			self.top_color = '#54C392'

		for event in events:
			if self.top_rect.collidepoint(mouse_pos):
				self.top_color = '#D74B4B'  

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					self.dynamic_elevation = 0
					self.pressed = True

				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					if self.pressed: 
						self.pressed = False
						self.dynamic_elevation = self.elevation
						self.used = True


class FileButton:

	def __init__(self, path, width, height, pos, font, max_count, color):

		self.pressed = False
		self.used = False
		self.path = path
		self.max_count = max_count
		self.text_color = color
		self.font = font

		self.rect = pygame.Rect(pos,(width,height))
		self.text_surf = self.font.render(self.resize(self.path, self.max_count), True, self.text_color)
		self.text_rect = self.text_surf.get_rect(topleft=(self.rect.left + 5, self.rect.centery - self.text_surf.get_height() // 2))

		self.color = '#D3D3D3'

	def draw(self, display, events):

		pygame.draw.rect(display,self.color, self.rect)

		self.text_surf = self.font.render(self.resize(self.path, self.max_count), True, self.text_color)
		self.text_rect = self.text_surf.get_rect(topleft=(self.rect.left + 5, self.rect.centery - self.text_surf.get_height() // 2))

   
		display.blit(self.text_surf, self.text_rect)

		self.check_click(events)

	def check_click(self, events):

		if self.used:
				self.color = '#808080'
				return
		

		mouse_pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(mouse_pos):
			self.color = '#89CFF0'  
		else:
			self.color = '#D3D3D3'

		for event in events:
			if self.rect.collidepoint(mouse_pos):
				self.color = '#89CFF0'  

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
					self.pressed = True

				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:  
					if self.pressed: 
						self.pressed = False
						self.used = True
						return self.used 

	@staticmethod
	def resize(text,n):
		if len(text) > n:
			return text[0:n] + '...'
		return text


class TextField:

	def __init__(self, pos, width, height, font):

		self.highlighted = False
		self.box = pygame.Rect(pos, (width,height))
		self.base_color = '#D3D3D3'
		self.hover_color = '#89CFF0'
		self.current_color = self.base_color
		self.font = font
		self.text = ''
		self.width = width
		self.height = height
		

		self.text_surf = self.font.render(self.text, True, 'black')
		self.text_rect = self.text_surf.get_rect()
		self.text_rect.left += 2
		
	def draw(self, display, events):

		pygame.draw.rect(display, self.current_color, self.box)

		self.text_surf = self.font.render(self.text, True, 'black')
		self.text_rect = self.text_surf.get_rect(topleft=(self.box.left + 5, self.box.centery - self.text_surf.get_height() // 2))
		self.box.w = max(self.width, self.text_surf.get_width()+10)


		display.blit(self.text_surf, self.text_rect)
		self.check(events)

	def check(self, events):
		
		if pygame.mouse.get_pressed()[0]: 
			mouse_pos = pygame.mouse.get_pos()
			if self.box.collidepoint(mouse_pos):
				self.current_color = self.hover_color
				self.highlighted = True
				self.text = ''
			else: 
				self.current_color = self.base_color
				self.highlighted = False
		
		for event in events:
			if (event.type == pygame.KEYDOWN) and self.highlighted:
  
				if event.key == pygame.K_BACKSPACE: 
					self.text = self.text[:-1] 
				else: 
					self.text += event.unicode

class InfoPrompt:
	def __init__(self, text, pos, font, color):
		self.pos = pos
		self.font = font
		self.text = text
		self.color = color
		self.rect = None
		self.active = False

	def draw(self, display):

		img = pygame.image.load('icon/info.png')
		img = pygame.transform.scale(img, (40,40))
		
		self.rect = img.get_rect()
		self.rect.topleft = self.pos

		display.blit(img, self.pos)
		

		if self.active:
			display_message(display, self.text, 'black', self.font, x= self.pos[0] + 50, y=self.pos[1])

		self.check()

	def check(self):

		mouse_pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(mouse_pos):
			self.active = True
		else:
			self.active = False


def display_message(display, message, color, font, x=10, y=100, offset=20, line_spacing=15):
	"""Displays a multiline message on the screen with customized spacing."""
    

	lines = message.strip().splitlines()
	y_offset = y
    

	for line in lines:
		line_text = line.strip()  
		text_surface = font.render(line_text, True, color)
		display.blit(text_surface, (x, y_offset))
        

		y_offset += offset + line_spacing