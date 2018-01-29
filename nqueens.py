# -*- coding: utf-8 -*-
# !/usr/bin/python3
import copy
import math
import random


class Board:
    def __init__(self, fitness, board_size=8, mut_prob=1.0):
        self.board_size = board_size
        self.desired_fitness = fitness
        self.mut_prob = mut_prob

        self.fitness = 0

        self.queens = list(range(self.board_size))
        self.move(self.board_size / 2)

    def move(self, count):
        count = int(count)

        for i in range(count):
            j = random.randint(0, self.board_size - 1)
            k = random.randint(0, self.board_size - 1)
            self.queens[j], self.queens[k] = self.queens[k], self.queens[j]

        self.compute_fitness()

    def regenerate(self):
        self.move(2)

        if random.uniform(0, 1) < self.mut_prob:
            self.move(1)

    def compute_fitness(self):
        self.fitness = self.desired_fitness

        for i in range(self.board_size):
            for j in range(i + 1, self.board_size):
                if math.fabs(self.queens[i] - self.queens[j]) == j - i:
                    self.fitness -= 1

    def visualization(self):
        board = ""
        for row in range(self.board_size):
            queen = self.queens.index(row)

            for col in range(self.board_size):
                if col == queen:
                    board += "Q"
                else:
                    board += "+"
            board += "\n"
        return board


class Solver_8_queens:

    def __init__(self, pop_size=1000, cross_prob=0.11, mut_prob=0.05):
        self.board_size = 8
        self.population_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

    def found_match(self):
        for population in self.population:
            if population.fitness == self.fitness:
                return True
        return False

    def random_selection(self):
        population_list = []
        for i in range(len(self.population)):
            population_list.append((i, self.population[i].fitness))
        population_list.sort(key=lambda pop_item: pop_item[1], reverse=True)
        return population_list[:int(len(population_list) / 3)]

    def first_generation(self):
        for i in range(self.population_size):
            self.population.append(Board(self.fitness, self.board_size, self.mut_prob))

        self.print_population()

    def next_generation(self):
        self.generation_count += 1
        selections = self.random_selection()
        new_population = []

        while len(new_population) < self.population_size:
            sel = random.choice(selections)[0]
            new_population.append(copy.deepcopy(self.population[sel]))
        self.population = new_population

        for population in self.population:
            population.regenerate()

        self.print_population(selections)

    def print_population(self, selections=None):
        print("Population #%d" % self.generation_count)

        if selections == None:
            selections = []

        print("Using: %s" % str([sel[0] for sel in selections]))

        count = 0
        for population in self.population:
            print("%8d : (%d) %s" % (count, population.fitness, str(population.queens)))
            count += 1

    def solve(self, min_fitness=0.9, max_epochs=100):
        best_fit = None
        epoch_num = None
        visualization = None

        self.generation_size = max_epochs
        self.fitness = min_fitness
        self.population = []
        self.generation_count = 0

        self.first_generation()

        while True:
            if self.found_match() == True:
                break
            if -1 < self.generation_size <= self.generation_count:
                break

            self.next_generation()

        if self.generation_size <= self.generation_count:
            print("Couldn't find result in %d generations" % self.generation_count)
        elif self.found_match():
            for population in self.population:
                if population.fitness == self.fitness:
                    best_fit = population.fitness
                    epoch_num = self.generation_count
                    visualization = population.visualization()

        return best_fit, epoch_num, visualization
