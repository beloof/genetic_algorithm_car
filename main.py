# Third-Party Imports
import pygame

# Local Imports
from core.simulation import *





elitism = 0.1
crossover_rate = 0.95
mutation_rate = 0.5
mutation_coef = 1
count = 15

width = 1100
height = 700

pygame.init()

small_font = pygame.font.SysFont("Agency FB", 20)
big_font = pygame.font.SysFont("Verdana", 30)

display = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.display.set_caption('car ai')

simulation(mutation_rate, mutation_coef, crossover_rate, elitism, width, height, display, clock, big_font, small_font, count)
