''' 
This file is part of evopy.

Copyright 2012 - 2013, Jendrik Poloczek

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
path.append("../../../..")

from copy import deepcopy
from numpy import matrix, log10

from evopy.strategies.ori_dses_svc_repair import ORIDSESSVCR
from evopy.strategies.ori_dses_svc import ORIDSESSVC
from evopy.strategies.ori_dses import ORIDSES
from evopy.simulators.simulator import Simulator

from evopy.problems.sphere_problem_origin_r1 import SphereProblemOriginR1
from evopy.problems.sphere_problem_origin_r2 import SphereProblemOriginR2
from evopy.problems.schwefels_problem_26 import SchwefelsProblem26
from evopy.problems.tr_problem import TRProblem

from evopy.metamodel.dses_svc_linear_meta_model import DSESSVCLinearMetaModel
from sklearn.cross_validation import KFold
from evopy.operators.scaling.scaling_standardscore import ScalingStandardscore
from evopy.operators.scaling.scaling_dummy import ScalingDummy
from evopy.metamodel.cv.svc_cv_sklearn_grid_linear import SVCCVSkGridLinear

from evopy.operators.termination.or_combinator import ORCombinator
from evopy.operators.termination.accuracy import Accuracy
from evopy.operators.termination.generations import Generations
from evopy.operators.termination.convergence import Convergence 

def get_method_SphereProblemR1_svc(beta):
    sklearn_cv = SVCCVSkGridLinear(\
        C_range = [2 ** i for i in range(-3, 14, 2)],
        cv_method = KFold(20, 5))

    meta_model = DSESSVCLinearMetaModel(\
        window_size = 10,
        scaling = ScalingStandardscore(),
        crossvalidation = sklearn_cv,
        repair_mode = 'none')

    method = ORIDSESSVC(\
        mu = 15,
        lambd = 100,
        theta = 0.3,
        pi = 15,
        initial_sigma = matrix([[4.5, 4.5]]),
        delta = 4.5,
        tau0 = 0.5, 
        tau1 = 0.6,
        initial_pos = matrix([[10.0, 10.0]]),
        beta = beta,
        meta_model = meta_model) 

    return method

def get_method_SphereProblemR2_svc(beta):
    sklearn_cv = SVCCVSkGridLinear(\
        C_range = [2 ** i for i in range(-3, 14, 2)],
        cv_method = KFold(20, 5))

    meta_model = DSESSVCLinearMetaModel(\
        window_size = 10,
        scaling = ScalingStandardscore(),
        crossvalidation = sklearn_cv,
        repair_mode = 'none')

    method = ORIDSESSVC(\
        mu = 15,
        lambd = 100,
        theta = 0.3,
        pi = 15,
        initial_sigma = matrix([[4.5, 4.5]]),
        delta = 4.5,
        tau0 = 0.5, 
        tau1 = 0.6,
        initial_pos = matrix([[10.0, 10.0]]),
        beta = beta,
        meta_model = meta_model) 

    return method

def get_method_TR_svc(beta):
    sklearn_cv = SVCCVSkGridLinear(\
        C_range = [2 ** i for i in range(-3, 14, 2)],
        cv_method = KFold(20, 5))

    meta_model = DSESSVCLinearMetaModel(\
        window_size = 10,
        scaling = ScalingStandardscore(),
        crossvalidation = sklearn_cv,
        repair_mode = 'none')

    method = ORIDSESSVC(\
        mu = 15,
        lambd = 100,
        theta = 0.3,
        pi = 15,
        initial_sigma = matrix([[4.5, 4.5]]),
        delta = 4.5,
        tau0 = 0.5, 
        tau1 = 0.6,
        initial_pos = matrix([[10.0, 10.0]]),
        beta = beta,
        meta_model = meta_model) 

    return method

def get_method_Schwefel26_svc(beta):
    sklearn_cv = SVCCVSkGridLinear(\
        C_range = [2 ** i for i in range(-3, 14, 2)],
        cv_method = KFold(20, 5))

    meta_model = DSESSVCLinearMetaModel(\
        window_size = 10,
        scaling = ScalingStandardscore(),
        crossvalidation = sklearn_cv,
        repair_mode = 'none')

    method = ORIDSESSVC(\
        mu = 15,
        lambd = 100,
        theta = 0.3,
        pi = 15,
        initial_sigma = matrix([[4.5, 4.5]]),
        delta = 4.5,
        tau0 = 0.5, 
        tau1 = 0.6,
        initial_pos = matrix([[100.0, 100.0]]),
        beta = beta,
        meta_model = meta_model) 

    return method

betas = map(lambda b : b / 10.0, range(0, 11))

def create_problem_optimizer_map(typeofelements):
    t = typeofelements    
    beta_map = {}
    for beta in betas:
        beta_map[beta] = deepcopy(t)
    return {\
        TRProblem: deepcopy(beta_map),\
        SphereProblemOriginR1: deepcopy(beta_map),\
        SphereProblemOriginR2: deepcopy(beta_map),\
        SchwefelsProblem26: deepcopy(beta_map)}

samples = 100
termination = Generations(50)

problems = [TRProblem, SphereProblemOriginR1,\
    SphereProblemOriginR2, SchwefelsProblem26]

optimizers = {\
    TRProblem: get_method_TR_svc,
    SphereProblemOriginR1: get_method_SphereProblemR1_svc,
    SphereProblemOriginR2: get_method_SphereProblemR2_svc,
    SchwefelsProblem26: get_method_Schwefel26_svc}

beta_map = {}
for beta in betas:
    beta_map[beta] = []
 
simulators = {\
    TRProblem: deepcopy(beta_map),
    SphereProblemOriginR1: deepcopy(beta_map),
    SphereProblemOriginR2: deepcopy(beta_map),
    SchwefelsProblem26: deepcopy(beta_map)
}

cfcs = create_problem_optimizer_map([])
