# Standard Library Imports
import sys
import pickle
import os

# Third-Party Imports
import pygame

# Local Imports
from core.ui import *


class Track:

    def __init__(self):
        self.path = [[],[]]
        self.start = [0, 0]
        self.big_font = None
        self.small_font = None
        self.width = None
        self.height = None
        self.button_height = 40
        self.button_width = 200

    def create_track(self, display, clock, big_font, small_font, width, height):
        self.width = width
        self.height = height
        self.big_font = big_font
        self.small_font = small_font

        display.fill((255, 255, 255))

        if self.load_track(display):
            self.draw_line(display)
            pygame.display.update()
            return

        loop = True
        step = 0
        feedback = ""

        while loop:

            display.fill((255, 255, 255))
            if step == 0:
                instruction = f"Left click to add points to first border, right click to confirm"
            elif step == 1:
                instruction = f"Left click to add points to second border, right click to confirm"
            else:
                instruction = "Set the starting position with Left-click, right click to confirm. make it far enough from borders"



            feedback_message = f"Press 'Z' to undo, 'Q' to quit without saving"
        
            self.display_message(display, instruction, 'black', x=10, y=10)
            self.display_message(display, feedback_message, 'black', x=10, y=40)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        close()
                    elif event.key == pygame.K_z:
                        step = self.take_back(step)
                        feedback = "Last point removed"

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if event.button == 3:
                        if step == 2:
                            if self.start == [0, 0]:
                                feedback = "please choose a starting point"
                                break

                            loop = False
                            break
                        
                        if len(self.path[step]) < 3:
                            feedback = 'you need at least 3 points to make a closed track'
                            break

                        step += 1 
                        feedback = f"0 points added" if step < 2 else ''

                    elif event.button == 1:
                        if step == 2:
                            self.start = pos
                            feedback = "Starting position set"
                        else:
                            self.path[step].append(pos)
                            feedback = f"{len(self.path[step])} points added"


            self.draw_line(display)
        

            self.display_message(display, feedback, 'blue', x=10, y=70)


            pygame.display.update()
            clock.tick(60)


        self.display_message(display, "Track creation complete. Saving...", 'green', x=10, y=100)

        pygame.display.update()
        self.save_track(display)
        
    def take_back(self,i):
        if i == 2:
            return 1
        try:
            self.path[i].pop()
            return i
        except:
            return 0

    def draw_line(self,display):
        pygame.draw.rect(display, (255,160,122) , (*self.start, 5, 5))
        for i in range(2):
            if len(self.path[i]) > 1:
                pygame.draw.lines(display, (52, 73, 94), True, self.path[i], 5)
            
    def save_track(self, display):

        display.fill((255, 255, 255)) 

        feedback = r'dont use the caracters <>:"/\|?*    ( / for linux)'
        message = (
            "If you save, your track will be saved at:\n"
            "  tracks/name_you_typed.pkl\n"
            "\n"
            "To keep premade tracks, \navoid using the names:\n"
            "track_1 ... track_4"
        )

        self.display_message(display, message, color='black', x=10, y=20, offset=20)

            
        start_sim = Button('start', self.button_width, self.button_height, (self.width/2 - self.button_width/2, self.height/2 - self.button_height/2),  5, self.big_font)
            
        save = Button('save', self.button_width, self.button_height, (self.width/2 - self.button_width/2, self.height/2 + self.button_height), 5, self.big_font)

        path = TextField((self.width/2 - self.button_width/2, self.height/2 + 5/2*self.button_height), self.button_width, self.button_height, self.big_font)
        path.text = 'type your file name here'

        pygame.display.update()

        while (not save.used) and (not start_sim.used):

            display.fill((255, 255, 255)) 

            events = pygame.event.get()

            self.display_message(display, message, 'black', x = 10, y = 20, offset = 15)

            save.draw(display, events)
            start_sim.draw(display, events)
            path.draw(display, events)

            if (path.text + '.pkl').lower() in [i.lower() for i in os.listdir('tracks')]:
                feedback = 'this will overwrite ' + (path.text + '.pkl')
            else:
                feedback = r'dont use the caracters <>:"/\|?*    ( / for linux)'
            
            self.display_message(display, feedback, 'blue', self.width/2 - self.button_width/2, self.height/2 + 7/2*self.button_height)

            pygame.display.update()


        self.make_directory('tracks')

        if save.used:
            try:
                with open(f'tracks/{path.text}.pkl', 'wb') as f:
                    pickle.dump(self.path, f)
                    pickle.dump(self.start, f)

                    path.text = f'saved at: tracks/{path.text}.pkl'
                return True

            except (FileNotFoundError, pickle.UnpicklingError):
                return False
               
    def load_track(self, display):

        display.fill((255, 255, 255)) 

        self.display_message(display, f'you can load from premade files: you have {len(os.listdir("tracks/"))} availabe', color = 'black', x = 10, y = 15)

        start_sim = Button('make track', 
                           self.button_width, self.button_height, 
                           (self.width/2 - self.button_width/2, self.height/2 - self.button_height/2), 
                           5, self.big_font
        )

        buttons = [FileButton(file, 200, 20, (15,i*30 + 60), self.small_font, 230, 'Black') for i,file in enumerate(os.listdir('tracks/'))]


        pygame.display.update()

        found = False

        if len(buttons) == 0:
            return False



        while (not (start_sim.used or found)):

            events = pygame.event.get()

            display.fill((255, 255, 255)) 

            self.display_message(display, f'load from available files: you have {len(buttons)} availabe', 'black', x = 10, y = 15)

            start_sim.draw(display, events)

            for button in buttons:
                button.draw(display, events)

                if button.used:
                    found = button.path
            


            pygame.display.update()


        if found:
            try:
                with open(f'tracks/{found}', 'rb') as f:
                    self.path = pickle.load(f)
                    self.start = pickle.load(f)
                return True

            except (FileNotFoundError, pickle.UnpicklingError):
                return False
                

        return False

    def display_message(self, display, message, color, x=10, y=100, offset=20, line_spacing=15):
        """Displays a multiline message on the screen with customized spacing."""
    
        # Splitting and stripping each line for consistent formatting
        lines = message.strip().splitlines()
        y_offset = y
    
        # Display each line with an offset and line spacing
        for line in lines:
            line_text = line.strip()  # Remove any excess whitespace
            text_surface = self.small_font.render(line_text, True, color)
            display.blit(text_surface, (x, y_offset))
        
            # Adjust vertical position for next line
            y_offset += offset + line_spacing

    @staticmethod
    def make_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

   
def close():
    pygame.quit()
    sys.exit()