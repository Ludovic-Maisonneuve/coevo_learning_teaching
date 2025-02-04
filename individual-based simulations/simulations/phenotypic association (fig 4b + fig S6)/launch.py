import time

from functions.dynamics import *
from functions.visualize_data import *

## Parameters
eps = 0.1
alpha = 2
betav0 = 7
betao = 4
betatau = 10
etad = 2
etae = 2
cd = 0.1
ce = 0.1
rho = 0.5
N = int(10 ** 3)
gamma = 10 ** (-4) / 2

Pmut = 0.002
mutationstep = 0.01

# Initial conditions
o0, v0, tau0 = 0.197404, 0.191947, 1.32304

# Number of generations
gmax = 1000000

# Creating an instance of the Environment class
E = Environment(eps, alpha, betao, betav0, betatau, etad, etae, cd, ce, rho, gamma, Pmut, mutationstep)

# Folder to store simulation results
data_folder = 'results'

## Creating the ancestral population
G = ancestral_generation(o0, v0, tau0, E, eps, alpha, betao, betav0, betatau, rho, N)

## Return to previous simulation
if os.path.exists(data_folder + '/G'):
    g0, G = open_last_generation(data_folder, E)
else:
    g0 = 0
    save_generation(G, 0, data_folder)

tic = time.perf_counter()
v_evolve = True
l_evolve = True
tau_evolve = True

for gi in range(g0 + 1, gmax + 1):
    G = next_generation(G, v_evolve=v_evolve, o_evolve=l_evolve, tau_evolve=tau_evolve)
    if gi % 100 == 0:
        save_generation(G, gi, data_folder)
    if gi % 100 == 0:
        toc = time.perf_counter()
        print('##', 'Generation:', gi, '##')
        print(f"get 100 iterations in {toc - tic:0.4f} seconds")
        print('##   ##')
        tic = time.perf_counter()
