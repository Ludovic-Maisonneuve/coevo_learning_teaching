# Importing necessary modules
import time

from functions.dynamics import *
from functions.save_and_open import *

## Parameters

eps = 0.05
alpha = 1
betav0 = 2
betao = 1
betatau = 8
etad = 2
etae = 2
cd = 1
ce = 0.5
rho = 0.05
N = 10 ** 3
gamma = 10 ** (-4) / 2
list_traits_max = [1, 1, 3]
eigenvalueH = np.array([-0.00894056, -0.780535, 0.625048])

Pmut = 0.002
mutationstep = 0.01

# Initial conditions
o0, v0, tau0 = 0.156755, 0.423958, 0.817091

# Number of generations
gmax = 250000

# Creating an instance of the Environment class
E = Environment(eps, alpha, betao, betav0, betatau, etad, etae, cd, ce, rho, gamma, Pmut, mutationstep)

# Folder to store simulation results
data_folder = 'results'

# Creating the ancestral population
G = ancestral_generation(o0, v0, tau0, E, eps, alpha, betao, betav0, betatau, rho, N)

# Returning to the previous simulation if it exists
if os.path.exists(data_folder + '/G'):
    g0, G = open_last_generation(data_folder, E)
else:
    g0 = 0
    save_generation(G, 0, data_folder, eig=eigenvalueH, list_traits_max=list_traits_max)

# Timing the simulation
tic = time.perf_counter()

for gi in range(g0 + 1, gmax + 1):
    G = next_generation(G)

    # Saving the population every 10 generations
    if gi % 10 == 0:
        save_generation(G, gi, data_folder, eig=eigenvalueH, list_traits_max=list_traits_max)

    # Printing information every 10 generation
    if gi % 10 == 0:
        toc = time.perf_counter()
        print('##', 'Generation:', gi, '##')
        print(f"get 1000 iterations in {toc - tic:0.4f} seconds")
        print('##   ##')
        tic = time.perf_counter()
