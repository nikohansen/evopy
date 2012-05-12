''' 
This file is part of evopy.

Copyright 2012, Jendrik Poloczek

evopy is free software: you can redistribute it
and/or modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

evopy is distributed in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
Public License for more details.

You should have received a copy of the GNU General Public License along with
evopy.  If not, see <http://www.gnu.org/licenses/>.
'''

from evopy.individuals.individual import Individual
from random import random, sample, gauss

class SphereProblem():

    _d = 2 
    _size = 1000

    def termination(self, generations, fitness_of_best):
        return (2 - 1 * pow(10, -2) < fitness_of_best < 2 + 1 * pow(10, -2))

    # return true if solution is valid, otherwise false.
    def is_feasible(self, x):
        return sum(x.value) - 2.0 >= 0

    # return fitness, 0 is best.
    def fitness(self, x):
        return sum(map(lambda x : pow(x,2), x.value)) 

    def sortedbest(self, children):
        return sorted(children, key=lambda child : self.fitness(child))

    # return combined child of parents x,y
    def combine(self, pair): 
        v1 = pair[0].value
        v2 = pair[1].value
        return Individual(map(lambda i,j : (i+j)/2.0, v1, v2))

    # mutate child with gauss devriation 
    def mutate(self, child, sigma):
        old_val = child.value
        new_val = map(lambda value : value + gauss(0, sigma), old_val)
        child.value = new_val
        return child

    # python generator for inifinte list of parent population
    def population_generator(self):
        d = self._d
        size = self._size

        while(True):
            value = map(lambda x : ((x * random()) - 0.5) * size *2, [1] * d)
            yield(Individual(value))

    # python generator for infinite list of feasible and infeasible 
    # children. mutated and recombined with given parents.
    def children_generator(self, parents, sigma):
        while(True):
            child = self.mutate(self.combine(sample(parents,2)), sigma)
            yield child
