# Standard Library Imports
import os
import shutil
import random
from math import sin, cos, radians, sqrt, log
import pickle
import copy

# Third-Party Imports
import matplotlib.pyplot as plt
import pygame
import numpy as np

# Local Imports
from core.brain import Brain



class Car:

    def __init__(self, track, color=(241, 196, 15)):
        
        self.x = track.start[0]
        self.y = track.start[1]
        self.w = 25
        self.h = 13
        self.angle = 0
        self.angle_step = 5
        self.speed = 2

        self.coord = None

        self.color = color

        self.sensors = [[0, 0]]*5
        
        self.brain = Brain([5, 8, 8, 3])
        self.crashed = False

        self.score = 0
        self.fitness = 0

    def reset(self,track): 
        self.x = track.start[0]
        self.y = track.start[1]

        self.coord = None
        self.angle = 0

        self.score = 0.0
        self.fitness = 0
        self.crashed = False
        return self
        
    def translation(self, coord):
        return [coord[0] + self.x, coord[1] + self.y]
        
    def rotation(self, coord, angle, anchor=(0, 0)):
        corr = 180
        return ((coord[0] - anchor[0])*cos(angle + radians(corr)) - (coord[1] - anchor[1])*sin(angle + radians(corr)),
                (coord[0] - anchor[0])*sin(angle + radians(corr)) + (coord[1] - anchor[1])*cos(angle + radians(corr)))

    def think(self):
        inputBrain = []
        
        for i in self.sensors:
            inputBrain.append(((self.x - i[0])**2 + (self.y - i[1])**2)**0.5)
        result = self.brain.feed_forward(inputBrain)
        self.angle += result*self.angle_step

    def ray(self, p1, p2, phi):

        ray_end_x = self.x + 2000 * cos(radians(phi))
        ray_end_y = self.y + 2000 * sin(radians(phi))
    
        return self.intersection(p1, p2, [self.x, self.y], [ray_end_x, ray_end_y])
    
    def line(self,p1, p2):
        
        A = (p1[1] - p2[1])
        B = (p2[0] - p1[0])
        C = (p1[0]*p2[1] - p2[0]*p1[1])
        
        return A, B, -C

    def intersection(self, p1, p2, p3, p4):
        
        line1 = self.line(p1, p2)
        line2 = self.line(p3, p4)
    
        det_main = line1[0] * line2[1] - line1[1] * line2[0]
        det_x = line1[2] * line2[1] - line1[1] * line2[2]
        det_y = line1[0] * line2[2] - line1[2] * line2[0]
    
        if det_main != 0:
            x = det_x / det_main
            y = det_y / det_main

            within_segment1 = ((min(p3[0], p4[0]) - 0.01 <= x <= max(p3[0], p4[0]) + 0.01) and 
                               (min(p3[1], p4[1]) - 0.01 <= y <= max(p3[1], p4[1]) + 0.01))
            within_segment2 = ((min(p1[0], p2[0]) - 0.01 <= x <= max(p1[0], p2[0]) + 0.01) and 
                               (min(p1[1], p2[1]) - 0.01 <= y <= max(p1[1], p2[1]) + 0.01))
        
            if within_segment1 and within_segment2:
                distance = sqrt((p3[0] - x) ** 2 + (p3[1] - y) ** 2)
                return x, y, distance
            
        return None, None, float('inf')
            
    def move(self, track):
        if not self.crashed:
            self.x = self.x + self.speed*cos(radians(self.angle))
            self.y = self.y + self.speed*sin(radians(self.angle))
            self.score += 0.06

            self.sensors = [[self.x, self.y]]*5
            
            first_border = track.path[0]
            second_border = track.path[1]
            
            for j in range(len(self.sensors)):
                distance = float('inf')
                for i in range(-1,len(first_border)-1):
                    x,y,temp_distance = self.ray(first_border[i],first_border[i+1],self.angle-90 + 45 * j)

                    if temp_distance < distance:
                        distance = temp_distance
                        self.sensors[j] = [x,y]

                for i in range(-1,len(second_border)-1):
                    x,y,temp_distance = self.ray(second_border[i],second_border[i+1],self.angle-90 + 45 *j)

                    if temp_distance<distance:
                        distance=temp_distance
                        self.sensors[j] = [x,y]

            points = [(0, 0), (0, self.h), (self.w, self.h), (self.w, 0)]
            self.coord = []
            for point in points:
                self.coord.append(self.translation(self.rotation(point, radians(self.angle), (self.w/2, self.h/2))))

            for j in range(-1,3):
                for i in range(-1,len(first_border)-1):
                    x,y,temp_distance = self.intersection(first_border[i],first_border[i+1],self.coord[j],self.coord[j+1])

                    if temp_distance != float('inf'):
                        self.crashed = True
                        self.fitness = max(1,log(self.score + 2))

            for j in range(-1,3):
                for i in range(-1,len(second_border)-1):
                    x,y,temp_distance = self.intersection(second_border[i],second_border[i+1],self.coord[j],self.coord[j+1])

                    if temp_distance != float('inf'):
                        self.crashed = True
                        self.fitness = max(0,log(self.score + 2))

            if self.score > 200:
                self.crashed = True
                self.fitness = max(0,log(self.score + 2))

            self.think()
            
    def save_best_brain(self, directory = ""):

        prev_score = float('-inf')

        try:
            with open(directory + "data/best_brain/bestScore", "r") as fp:
                prev_score = float(fp.read())
        except:
            pass

        Population.ensure("data")
        Population.ensure("data/best_brain")

        if self.score > prev_score:

            with open(directory + "data/best_brain/best_score.pkl", "wb") as f:
                pickle.dump(self.score, f)

            with open(directory + "data/best_brain/best_biases.pkl", "wb") as f:
                pickle.dump(self.brain.biases, f)

            with open(directory + "data/best_brain/best_weights.pkl", "wb") as f:
                pickle.dump(self.brain.weights, f)
    
    def load_best_brain(self, directory = ""):
        with open(directory + "data/Best_Brain/best_score.pkl", "r") as f:
            self.score = pickle.load(f)

        with open(directory + "data/Best_Brain/best_biases.pkl", "r") as f:
            self.brain.biases = pickle.load(f)

        with open(directory + "data/Best_Brain/best_weights.pkl", "r") as f:
            self.brain.weights = pickle.load(f)

    def draw(self,display):
        sensorColor = (46, 64, 83)
        for j in self.sensors:
            pygame.draw.line(display, sensorColor, (self.x, self.y), j)
            pygame.draw.ellipse(display, sensorColor, (j[0], j[1], 5, 5))
        
        pygame.draw.polygon(display, self.color, self.coord)

    def display_info(self, pos, display, font1):
        text = font1.render("Score: " + str("{0:.2f}".format(self.score)), True, self.color)
        display.blit(text, pos)


class Population:

    def __init__(self):
        self.population = []
        self.probabilities = []
        self.crashed = []
        self.track = None
        self.seed=42

    def create_population(self, track, count, seed = None):

        self.seed = seed
        self.track = track
        color = self.get_dim_colors(count, self.seed)
        
        self.probabilities = [0]*count
        
        self.population = []

        for i in range(len(color)):
            car = Car(track, color[i])
            self.population.append(car)
            
    def move(self, track):  
        for car in self.population:
            car.move(track)

    def evolve(self, track, mutation_rate, mutation_coef, crossover_rate, elitism):
        for car in self.population:
            if not car.crashed:
                return


        for i in range(len(self.population)):
            plt.scatter(i,self.population[i].fitness)
        
        return self.reproduction(track, mutation_rate, mutation_coef, crossover_rate, elitism)
    

    def reproduction(self, track, mutation_rate, mutation_coef, crossover_rate, elitism):
        
        self.normalize_fitness()

        elitism_count = max(1,int(elitism*len(self.population)))
        
        best_cars = list(sorted(self.population, key= lambda x : x.fitness, reverse= True))
        best_score = best_cars[0].score

        
        best_cars_saved = list()

        for i in range(elitism_count):
            car = Car(track, best_cars[i].color)
            car.brain.biases = best_cars[i].brain.biases.copy()
            car.brain.weights = best_cars[i].brain.weights.copy()
            best_cars_saved.append(car)

        
        new_generation = Population()
        new_generation.population.extend(best_cars_saved)
        
        
        i = elitism_count
        while len(new_generation.population) < len(self.population)-1:
        
            parent_index_a = self.pick_one()
            parent_index_b = self.pick_one()

            child_a = Car(track, self.population[i].color)
            child_b = Car(track, self.population[i+1].color)

            child_a.brain, child_b.brain = self.population[parent_index_a].brain.crossover(
                self.population[parent_index_b].brain,
                crossover_rate,
                self.seed
            )
            
            child_a.brain.mutation(mutation_rate, mutation_coef, self.seed)
            child_b.brain.mutation(mutation_rate, mutation_coef, self.seed)

            new_generation.population.extend([child_a, child_b])

            i += 2

        if len(new_generation.population) != len(self.population):
            i = self.pick_one()
            child = Car(track, self.population[-1].color)
            child.brain.weights = copy.deepcopy(self.population[i].brain.weights)
            child.brain.biases = copy.deepcopy(self.population[i].brain.biases)
            child.brain.mutation(mutation_rate, mutation_coef, self.seed)
            new_generation.population.extend([child])

        self.population = list(new_generation.population)
        self.probabilities = [0]*len(self.population)


        return best_score
    

    def normalize_fitness(self):
        summation = 0


        for car in self.population:
            summation += car.fitness

        for i in range(len(self.population)):
            self.probabilities[i] = self.population[i].fitness/summation
    
    def best_score(self):
        best = float('-inf')

        for car in self.population:
            if car.score > best:
                best = car.score

    def draw(self, display):
        for car in self.population:
            car.draw(display)

    def display_info(self, width, display, font1): 

        for i, car in enumerate(self.population):
            car.display_info((width - 100, 50 + i*25), display, font1)

    def show(self, generation):
        for i in self.population:
            plt.scatter([generation],i.fitness)

    def pick_one(self):
        prob = random.uniform(0, 1)

        for i in range(len(self.population)):
            prob -= self.probabilities[i]
            if prob < 0:
                return i
        
        return -1

    def load_generation(self):

        try:
            n = self.count_files("data/Trained/scores")
        except:
            return False

        if n == 0:
            return False

        self.create_population(self.track, n)

        for i in range(n):
            with open(f"data/Trained/scores/score{i}.pkl", "rb") as f:
                self.population[i].score = pickle.load(f)
            with open(f"data/Trained/biases/bias{i}.pkl", "rb") as f:
                self.population[i].brain.biases = pickle.load(f)
            with open(f"data/Trained/weights/weight{i}.pkl", "rb") as f:
                self.population[i].brain.weights = pickle.load(f)

        return True

    def load_best_generation(self):

        try:
            n = self.count_files("data/Trained_Best/scores")
        except:
            return False

        if n == 0:
            return False

        self.create_population(self.track,n)

        for i in range(n):
            with open(f"data/Trained_Best/scores/score{i}.pkl", "rb") as f:
                self.population[i].score = pickle.load(f)
            with open(f"data/Trained_Best/weights/weight{i}.pkl", "rb") as f:
                self.population[i].brain.weights = pickle.load(f)
            with open(f"data/Trained_Best/biases/bias{i}.pkl", "rb") as f:
                self.population[i].brain.biases = pickle.load(f)

        return True

    def save_generation(self):

        self.ensure("data")
        self.ensure("data/Trained")
        self.clear_directory("data/Trained/scores")
        self.clear_directory("data/Trained/biases")
        self.clear_directory("data/Trained/weights")


        for i, car in enumerate(self.population):
            with open("data/Trained/scores/score" + str(i) + ".pkl", "wb") as f:
                pickle.dump(car.score, f)
            with open("data/Trained/biases/bias" + str(i) + ".pkl", "wb") as f:
                pickle.dump(car.brain.biases, f)
            with open("data/Trained/weights/weight" + str(i) + ".pkl", "wb") as f:
                pickle.dump(car.brain.weights, f)


        index = 0
        for i in range(len(self.population)):
            if self.population[i].score > self.population[index].score:
                index = i

        self.population[i].save_best_brain()

    def save_best_generation(self):

        try:
            temp = Population()
            temp.load_best_generation()

            if temp.best_score() > self.best_score():
                return
        except:
            pass

        self.ensure("data")
        self.ensure("data/Trained_Best")
        self.clear_directory("data/Trained_Best/scores")
        self.clear_directory("data/Trained_Best/biases")
        self.clear_directory("data/Trained_Best/weights")


        for i, car in enumerate(self.population):
            with open("data/Trained_Best/scores/score" + str(i) + ".pkl", "wb") as f:
                pickle.dump(car.score, f)
            with open("data/Trained_Best/biases/bias" + str(i) + ".pkl", "wb") as f:
                pickle.dump(car.brain.biases, f)
            with open("data/Trained_Best/weights/weight" + str(i) + ".pkl", "wb") as f:
                pickle.dump(car.brain.weights, f)


        index = 0
        for i in range(len(self.population)):
            if self.population[i].score > self.population[index].score:
                index = i

        self.population[i].save_best_brain()
    
    @staticmethod        
    def get_dim_colors(n, seed = None):
                
        if seed is not None:
            np.random.seed(seed)
            random.seed(seed)

        return [
            (
                random.randint(0, 200),
                random.randint(0, 200),
                random.randint(0, 200)
            )
            for _ in range(n)
        ]

    @staticmethod
    def clear_directory(directory):
        try:
            shutil.rmtree(directory)
        except:
            pass

        if not os.path.exists(directory):
            os.makedirs(directory)
           
    @staticmethod
    def ensure(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def count_files(directory):
        return len(os.listdir(directory))