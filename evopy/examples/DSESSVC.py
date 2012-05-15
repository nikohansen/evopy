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

from sklearn.cross_validation import KFold
from evopy.problems.sa_sphere_problem import SASphereProblem
from evopy.operators.scaling.scaling_standardscore import ScalingStandardscore
from evopy.operators.mutation.gauss_sigma import GaussSigma
from evopy.operators.combination.sa_intermediate import SAIntermediate
from evopy.operators.selection.smallest_fitness_new_first import SmallestFitnessNewFirst
from evopy.operators.selfadaption.selfadaption import Selfadaption
from evopy.views.cv_ds_view import CVDSView
from evopy.metamodel.cv.svc_cv_sklearn_grid import SVCCVSkGrid
from evopy.strategies.dses_svc import DSESSVC

sklearn_cv = SVCCVSkGrid(\
    gamma_range = [2 ** i for i in range(-15, 3, 2)],
    C_range = [2 ** i for i in range(-5, 15, 2)],
    cv_method = KFold(50, 5))

method = DSESSVC(\
    SASphereProblem(),
    mu = 15,
    lambd = 100,
    theta = 0.7,
    pi = 70, 
    epsilon = 1.0,
    combination = SAIntermediate(),\
    mutation = GaussSigma(),\
    selection = SmallestFitnessNewFirst(),
    view = CVDSView(),
    beta = 0.9,
    window_size = 25,
    append_to_window = 25,
    crossvalidation = sklearn_cv,
    scaling = ScalingStandardscore(),
    selfadaption = Selfadaption())
     
method.run()

