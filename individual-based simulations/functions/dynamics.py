import random

from functions.classes import *


# Function to calculate total knowledge K based on mean individuals' traits
def get_K(G, E):
    rho, alpha, eps = E.rho, E.alpha, E.eps
    # Calculate sorted list of sum of investment in social learning traits
    listSL = sorted([i.o + i.v for i in G] + [1])

    # Calculate the total knowledge produced by individual learning
    if rho != 0:
        KIL = 0
        sumoverlap = 0
        for i in range(len(G)):
            sumoverlap += rho ** i
            KIL += (listSL[i + 1] - listSL[i]) * alpha * sumoverlap
    else:
        SL = min(listSL)
        KIL = alpha * (1 - SL)

    # Calculate the total knowledge produced by social learning
    if np.mean(listSL[:-1]) == 0:
        KSL = 0
    else:
        KSL = G[0].K * (1 - eps)

    # Return the total knowledge K
    return KIL + KSL


# Function to generate the next generation of individuals
def next_generation(G, o_evolve=True, v_evolve=True, tau_evolve=True):
    # Extract parameters from the first individual's environment
    E = G[0].E
    Pmut, mutationstep = E.Pmut, E.mutationstep

    # Calculate the total knowledge K
    K = get_K(G, E)

    # Calculate the expected number of offspring
    listfe = [i.get_fecundity() for i in G]
    expected_offspring_number = sum(listfe)

    # Sample the number of offspring from a Poisson distribution
    No = np.random.poisson(expected_offspring_number)

    # Calculate probabilities of selecting individuals for reproduction
    sumfe = np.sum(listfe)
    pfe = [fe / sumfe for fe in listfe]
    G_reprod = list(np.random.choice(G, No, p=pfe))

    # Generate offspring based on selected individuals and traits evolution
    G_offspring = []
    for ni, ind in enumerate(G_reprod):
        if ni < No * Pmut:
            # Mutate traits if within mutation probability
            if o_evolve:
                omut = np.clip(random.gauss(ind.o, mutationstep), 0, 1)
            else:
                omut = ind.o
            if v_evolve:
                vmut = np.clip(random.gauss(ind.v, mutationstep), 0, 1)
            else:
                vmut = ind.v
            if tau_evolve:
                tauoffspring = max(random.gauss(ind.tau, mutationstep), 0)
            else:
                tauoffspring = ind.tau

            # Ensure the sum of o and v traits does not exceed 1
            if omut + vmut < 1:
                ooffspring, voffspring = omut, vmut
            else:
                ooffspring, voffspring = ind.o, ind.v

        else:
            ooffspring, voffspring, tauoffspring = ind.o, ind.v, ind.tau
        # Create offspring with mutated traits
        offspring = Individual(ooffspring, voffspring, tauoffspring, ind.get_k(), ind.tau, K, No, E)
        # Determine if the offspring survive
        PS = (1 - ind.get_effective_costs(offspring)) / (1 + E.gamma * No)
        if np.random.random() < PS:
            G_offspring.append(offspring)

    N = len(G_offspring)
    G_offspring_corr = []

    for off in G_offspring:
        G_offspring_corr.append(Individual(off.o, off.v, off.tau, off.kv, off.tauv, off.K, N, E))
    # Return the next generation
    return G_offspring_corr
