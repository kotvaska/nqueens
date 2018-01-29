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
        self.move_gen(self.board_size / 2)

    def move_gen(self, count):
        count = int(count)

        for i in range(count):
            j = random.randint(0, self.board_size - 1)
            k = random.randint(0, self.board_size - 1)
            self.queens[j], self.queens[k] = self.queens[k], self.queens[j]

        self.compute_fitness()

    def mutate(self):
        self.move_gen(2)

        if random.uniform(0, 1) < self.mut_prob:
            self.move_gen(1)

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
        self.fitness = int((self.board_size * self.board_size) / 2)
        self.population_size = pop_size
        self.generation_size = -1
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

        self.population = []
        self.generation_count = 0

    def __found_match(self):
        for population in self.population:
            if population.fitness == self.fitness:
                return True
        return False

    def __random_selection(self):
        population_list = []
        for i in range(len(self.population)):
            population_list.append((i, self.population[i].fitness))
        population_list.sort(key=lambda pop_item: pop_item[1], reverse=True)
        return population_list[:int(len(population_list) / self.cross_prob)]

    def __first_generation(self):
        for i in range(self.population_size):
            self.population.append(Board(self.fitness, self.board_size, self.mut_prob))

        self.__print_population()

    def __next_generation(self):
        self.generation_count += 1
        selections = self.__random_selection()
        new_population = []

        while len(new_population) < self.population_size:
            sel = random.choice(selections)[0]
            new_population.append(copy.deepcopy(self.population[sel]))
        self.population = new_population

        for population in self.population:
            population.mutate()

        self.__print_population(selections)

    def __print_population(self, selections=None):
        print("Population #%d" % self.generation_count)

        if selections is None:
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

        self.generation_size = self.generation_size if max_epochs is None else max_epochs
        self.fitness = self.fitness if min_fitness is None else min_fitness
        self.population = []
        self.generation_count = 0

        self.__first_generation()

        while True:
            if self.__found_match() is True:
                break
            if -1 < self.generation_size <= self.generation_count:
                break

            self.__next_generation()

        if -1 < self.generation_size <= self.generation_count:
            print("Couldn't find result in %d generations" % self.generation_count)
        elif self.__found_match():
            for population in self.population:
                if population.fitness == self.fitness:
                    best_fit = population.fitness
                    epoch_num = self.generation_count
                    visualization = population.visualization()

        return best_fit, epoch_num, visualization
