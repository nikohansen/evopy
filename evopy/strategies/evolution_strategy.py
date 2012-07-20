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

from numpy import array

class EvolutionStrategy(object):

    class Logger():
        def __init__(self, scope):
            self.bindings = {}
            self.logs = {}
            self.scope = scope

        def add_binding(self, var_name, name):
            self.bindings[name] = var_name
            self.logs[name] = []

        def log(self):
            for k, v in self.bindings.iteritems():
                self.logs[k].append(self.scope.__getattribute__(v))                

    def __init__(self, mu, lambd):
        self._mu = mu
        self._lambd = lambd
    
        self.logger = self.Logger(self)      
        self.logger.add_binding('_best_fitness', 'best_fitness')
        self.logger.add_binding('_worst_fitness', 'worst_fitness')
        self.logger.add_binding('_mean_fitness', 'mean_fitness')
        self.logger.add_binding('_selected_children', 'selected_children')
        self.logger.add_binding('_count_constraint_infeasibles', 'infeasibles')

        self._count_constraint_infeasibles = 0
        self._count_repaired = 0

    def get_statistics(self, only_last = False):
        select = lambda stats : stats[-1] if only_last else stats

        statistics = {}
        for name, trajectory in self.logger.logs.iteritems():
            statistics[name] = select(trajectory)

        return statistics
