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
path.append("../..")

from evopy.strategies.dses import DSES

def get_method():
    """
    return DSES(\
        mu = 15, 
        lambd = 100,
        pi = 70,
        theta = 0.7,
        epsilon = 1.0,
        combination = SAIntermediate(),
        mutation = GaussSigma(),
        selection = SmallestFitness(),
        view = DSESView(),
        selfadaption = Selfadaption(tau0 = 1.0, tau1 = 0.1))
    """
    return True
if __name__ == "__main__":
    m = get_method()
    #m.run()