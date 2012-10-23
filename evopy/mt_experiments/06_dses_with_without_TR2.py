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

from sys import path
path.append("../../")

import pdb 
from numpy import matrix, array

from evopy.strategies.ori_dses import ORIDSES 
from sklearn.cross_validation import KFold
from sklearn.cross_validation import LeaveOneOut

from evopy.strategies.ori_dses_svc import ORIDSESSVC
from evopy.problems.tr_problem import TRProblem
from evopy.simulators.simulator import Simulator

from evopy.metamodel.dses_svc_linear_meta_model import DSESSVCLinearMetaModel
from evopy.operators.scaling.scaling_standardscore import ScalingStandardscore
from evopy.operators.scaling.scaling_dummy import ScalingDummy
from evopy.metamodel.cv.svc_cv_sklearn_grid_linear import SVCCVSkGridLinear

from evopy.termination.or_combinator import ORCombinator
from evopy.termination.accuracy import Accuracy
from evopy.termination.generations import Generations
from evopy.termination.convergence import Convergence 

from evopy.helper.timeseries_aggregator import TimeseriesAggregator

from multiprocessing import cpu_count
from evopy.external.playdoh import map as pmap

from pylab import * 

def get_method_without_SVC():
    method = ORIDSES(\
        mu = 15,
        lambd = 100,
        theta = 0.3,
        pi = 70,
        initial_sigma = matrix([[4.5, 4.5]]),
        delta = 4.5,
        tau0 = 0.5, 
        tau1 = 0.6,
        initial_pos = matrix([[10.0, 10.0]])) 

    return method

def get_method_with_SVC():

    sklearn_cv = SVCCVSkGridLinear(\
        C_range = [2 ** i for i in range(-5, 5, 2)],
        cv_method = LeaveOneOut(20))

    meta_model = DSESSVCLinearMetaModel(\
        window_size = 10,
        scaling = ScalingStandardscore(),
        crossvalidation = sklearn_cv,
        repair_mode = 'mirror')

    method = ORIDSESSVC(\
        mu = 15,
        lambd = 100,
        theta = 0.3,
        pi = 70,
        initial_sigma = matrix([[4.5, 4.5]]),
        delta = 4.5,
        tau0 = 0.5, 
        tau1 = 0.6,
        initial_pos = matrix([[10.0, 10.0]]),
        beta = 0.9,
        meta_model = meta_model) 

    return method

def process(simulator):
    return simulator.simulate()

method_names = ["DSES", "DSES-SVC"]
methods = [get_method_without_SVC, get_method_with_SVC]

simulators = []
cfcs = []

for method in method_names:
    simulators_for_method = []
    index = method_names.index(method)
    for i in range(0, 10):
        optimizer = methods[index]()
        problem = TRProblem()
        conditions = [Accuracy(problem.optimum_fitness(),\
            10**-4), Convergence(10**-4)]
        simulators_for_method.append(\
            Simulator(optimizer, problem, ORCombinator(conditions)))
    simulators.append(simulators_for_method)

for method in method_names:
    index = method_names.index(method)
    cfc_for_method = []        
    for simulator in simulators[index]:
        simulator.simulate()
        cfc_for_method.append(sum(simulator.logger.all()['count_cfc']))   
    cfcs.append(cfc_for_method)

xticks(range(0, len(method_names)), method_names)
boxplot(cfcs) 
show()
