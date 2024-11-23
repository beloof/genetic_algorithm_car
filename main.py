# Third-Party Imports
import pygame

# Local Imports
from core.simulation import *

mutation_rate = 50
mutation_coef = 1
count = 9

width = 1100
height = 700

pygame.init()

small_font = pygame.font.SysFont("Agency FB", 20)
big_font = pygame.font.SysFont("Verdana", 30)

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.display.set_caption('car ai')

simulation(mutation_rate, mutation_coef, width, height, display, clock, big_font, small_font, count)
