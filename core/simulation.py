# Standard Library Imports
import sys

# Third-Party Imports
import pygame

# Local Imports
from core.car import Population
from core.track import Track
from core.ui import *


def simulation(mutation_rate, mutation_coef, crossover_rate, elitism, width, height, display, clock, big_font, small_font, count):

    best_score = 0
    generation = 0
    loop = True

    track = Track()
    track.create_track(display,clock, big_font, small_font, width, height)

    population = Population()
    population.create_population(track,count)

    load_best = Button('load best', 110, 25 , (10, height - 30), 5, small_font)
    load_data = Button('load data', 110, 25 , (10, height - 75), 5, small_font)
    save_best = Button('save best', 110, 25 , (130, height - 30), 5, small_font)
    save_data = Button('save data', 110, 25 , (130, height - 75), 5, small_font)
    restart = Button('restart', 110, 25 , (10, height/2 - 35), 5, small_font)
    leave = Button('quit', 110, 25 , (10, height/2 - 80), 5, small_font)

    info_msg = (
        "save best will save current generation at 'data/Trained_Best' only if its best score is better than the currently saved one\n"
        "save data will save current generation at 'data/Trained' regardless\n"
        "they will both save the best car if its score is better than the currently saved one\n"
        "load data and load best will load the saved data it there is any\n"
        "note that scores are capped at 200"
    )


    info = InfoPrompt(info_msg, (10,height/2), small_font, 'black')

    feedback = ""

    while loop:
        display.fill((255, 255, 255))

        track.draw_line(display)
        population.move(track)
        population.draw(display)

        events = pygame.event.get()

        load_best.draw(display, events)
        load_data.draw(display, events)
        save_best.draw(display, events)
        save_data.draw(display, events)
        restart.draw(display, events)
        leave.draw(display, events)


        info.draw(display)

        for event in events:
            if event.type == pygame.QUIT:
                close()


        if save_best.used:
            population.save_best_generation()
            save_best.used = False
            feedback = 'saved best'

        if save_data.used:
            population.save_generation()
            save_data.used = False
            feedback = 'saved'

        if load_data.used:
            load_data.used = False
            feedback = f'loaded {len(population.population)} cars' if population.load_generation() else "couldn't load data"

        if load_best.used:
            load_best.used = False
            feedback = f'loaded best {len(population.population)} cars' if population.load_best_generation() else "couldn't load best"
        
        if restart.used:
            restart.used = False
            simulation(mutation_rate, mutation_coef, crossover_rate, elitism, width, height, display, clock, big_font, small_font, count)
            feedback = 'restarted'
        
        if leave.used:
            close()


        track.display_message(display, feedback, 'blue', x=10, y=height - 150)
        
        
        
        temp = population.evolve(track, mutation_rate, mutation_coef, crossover_rate, elitism)

        if temp is not None :
            if(temp < best_score):
                print('problem')
            best_score = temp
            generation += 1
        
        
        text1 = small_font.render(f"best score: {best_score:.2f}", True, 'red')
        text2 = small_font.render(f"generation: {generation}", True, 'red')
        
        display.blit(text1, (10,50))
        display.blit(text2, (10,100))
        
        population.display_info(width, display, small_font)
        pygame.display.update()

        clock.tick()

def run_best(display, clock, big_font, small_font, width, height):
    track = Track()
    track.create_track(display,clock, big_font, small_font, width, height)

    population = Population()
    population.create_population(track,1)
    population.population[0].load_best_brain()

    while not population.population[0].crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    close()
                elif event.key == pygame.K_r:
                    run_best(width, display, clock, big_font, small_font)

        

        display.fill((255, 255, 255))
        track.draw_line(display)
        population.move(track)
        population.draw(display)
        
        
        text1 = small_font.render(f"score:{population.population[0].score:.2f}", True, 'red')

        display.blit(text1, (10,50))
        
        population.display_info(width, display, small_font)
        pygame.display.update()
        clock.tick()



def close():
    pygame.quit()
    sys.exit()



