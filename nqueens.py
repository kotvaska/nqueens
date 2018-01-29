# -*- coding: utf-8 -*-
# !/usr/bin/python3
import copy
import math
import random

debug = False


class Board:
    def __init__(self, board_size=8, mut_prob=1.0):
        self.board_size = board_size
        self.mut_prob = mut_prob

        self.fitness = 0

        self.queens = ["{0:03b}".format(i) for i in range(self.board_size)]
        self.move_gen(self.board_size / 2)

    def move_gen(self, count):
        for i in range(int(count)):
            j = random.randint(0, self.board_size - 1)
            k = random.randint(0, self.board_size - 1)
            self.queens[j], self.queens[k] = self.queens[k], self.queens[j]

        self.compute_fitness()

    def mutate(self):
        self.move_gen(2)

        if random.uniform(0, 1) < self.mut_prob:
            self.move_gen(1)

    def compute_fitness(self):
        conflicts = 0

        for i in range(self.board_size):
            for j in range(i + 1, self.board_size):
                if math.fabs(int(self.queens[i], 2) - int(self.queens[j], 2)) == j - i:
                    conflicts += 1

        self.fitness = 1 - (conflicts / (len(self.queens) * 8))

    def visualization(self):
        board = ""
        for row in range(self.board_size):
            queen = self.queens.index("{0:03b}".format(row))

            for col in range(self.board_size):
                if col == queen:
                    board += "Q"
                else:
                    board += "+"
            board += "\n"
        return board


class Solver_8_queens:

    def __init__(self, pop_size=1000, cross_prob=0.85, mut_prob=0.05):
        self.board_size = 8
        self.fitness = 1
        self.population_size = pop_size
        self.generation_size = -1
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

        self.population = []
        self.__generation_count = 0

    def __found_match(self):
        for population in self.population:
            if population.fitness >= self.fitness:
                return True
        return False

    def __random_selection(self):
        population_list = [(i, item.fitness) for i, item in enumerate(self.population)]
        population_list.sort(key=lambda item: item[1], reverse=True)
        return population_list[:int(len(population_list) / 3)]

    def __first_generation(self):
        for i in range(self.population_size):
            self.population.append(Board(self.board_size, self.mut_prob))

        self.__print_population()

    def __next_generation(self):
        self.__generation_count += 1
        selections = self.__random_selection()
        new_population = []

        while len(new_population) < self.population_size:
            sel = random.choice(selections)[0] if random.uniform(0, 1) < self.cross_prob \
                else random.randint(0, self.population_size - 1)
            new_population.append(copy.deepcopy(self.population[sel]))
        self.population = new_population

        for population in self.population:
            population.mutate()

        self.__print_population(selections)

    def __print_population(self, selections=None):
        if debug is False:
            return

        print("Population #%d" % self.__generation_count)

        if selections is None:
            selections = []

        print("Using: %s" % str([sel[0] for sel in selections]))

        count = 0
        for population in self.population:
            print("%8d : (%d) %s" % (count, population.fitness, str(population.queens)))
            count += 1

    def solve(self, min_fitness=1.0, max_epochs=100):
        best_fit = None
        epoch_num = None
        visualization = None

        self.generation_size = self.generation_size if max_epochs is None else max_epochs
        self.fitness = self.fitness if min_fitness is None else min_fitness
        self.population = []
        self.__generation_count = 0

        self.__first_generation()

        while True:
            if self.__found_match() is True:
                break
            if -1 < self.generation_size <= self.__generation_count:
                break

            self.__next_generation()

        self.population.sort(key=lambda item: item.fitness, reverse=True)
        if self.population[0].fitness >= self.fitness:
            best_fit = self.population[0].fitness
            epoch_num = self.__generation_count
            visualization = self.population[0].visualization()

        return best_fit, epoch_num, visualization
