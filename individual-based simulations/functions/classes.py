import numpy as np


class Environment:
    def __init__(self, eps, alpha, betao, betav0, betatau, etad, etae, cd, ce, rho, gamma, Pmut, mutationstep):
        # Initialize environment parameters
        self.eps, self.alpha, self.betao, self.betav0, self.betatau = eps, alpha, betao, betav0, betatau
        self.etad, self.etae, self.cd, self.ce, self.rho, self.gamma = etad, etae, cd, ce, rho, gamma
        self.Pmut, self.mutationstep = Pmut, mutationstep


class Individual:
    def __init__(self, o, v, tau, kv, tauv, K, N, E):
        # individual's traits
        self.o, self.v, self.tau = o, v, tau
        # parental investment into teaching and knowledge
        self.tauv, self.kv = tauv, kv
        # population's variables and parameters
        self.K, self.N, self.E = K, N, E

    def get_fecundity(self):
        o, v, tau, tauv, kv, K, N, E = self.o, self.v, self.tau, self.tauv, self.kv, self.K, self.N, self.E
        # Calculate the knowledge acquired by social learning
        kSL = np.exp(-o * E.betao) * (1 - np.exp(-v * (E.betav0 + E.betatau * tauv))) * kv * (1 - E.eps) + \
              (1 - np.exp(-o * E.betao)) * K * (1 - E.eps)
        # Calculate the knowledge acquired by social and individual learning
        k = kSL + E.alpha * (1 - o - v)
        # Calculate the developmental costs of teaching
        Cd = self.E.cd * self.tau ** self.E.etad
        # Calculate fitness f
        f = k - Cd
        return f

    def get_effective_costs(self, offspring):
        # Calculate the effective costs of teaching
        Ce = self.E.ce * (self.tau * offspring.v) ** self.E.etae
        return Ce

    def get_k(self):
        o, v, tau, tauv, kv, K, N, E = self.o, self.v, self.tau, self.tauv, self.kv, self.K, self.N, self.E
        # Calculate the knowledge acquired by social learning
        kSL = np.exp(-o * E.betao) * (1 - np.exp(-v * (E.betav0 + E.betatau * tauv))) * kv * (1 - E.eps) + \
              (1 - np.exp(-o * E.betao)) * K * (1 - E.eps)
        # Calculate the knowledge acquired by social and individual learning
        k = kSL + E.alpha * (1 - o - v)
        return k


def ancestral_generation(o0, v0, tau0, E, eps, alpha, betao, betav0, betatau, rho, N):
    # Calculate initial values for K0 and k0 based on l0, v0 and tau0
    if o0 != 0 or v0 != 0:
        K0 = alpha * (1 - o0 - v0) / (rho * eps)
        k0 = ((1 - np.exp(-o0 * betao)) * K0 * (1 - eps) + (1 - v0 - o0) * alpha) / (
                1 - (1 - eps) * np.exp(-o0 * betao) * (1 - np.exp(-v0 * (betav0 + betatau * tau0))))
    else:
        K0 = alpha / rho
        k0 = alpha

    # Generate a list of individuals with the specified parameters
    G = [Individual(o0, v0, tau0, k0, tau0, K0, N, E) for i in range(N)]
    return G
