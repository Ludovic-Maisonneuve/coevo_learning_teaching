from functions.visualize_data import *

#Make figure S6

## Parameters
eps = 0.1
alpha = 2
betav0 = 3
betao = 2
betatau = 5
etad = 2
etae = 2
cd = 0.25
ce = 0.25
rho = 0.8
N = int(10 ** 3)
gamma = 10 ** (-4) / 2

Pmut = 0.002
mutationstep = 0.01

# Initial conditions
l0, v0, tau0 = 0.549081, 0.229579, 0

# Number of generations
gmax = 550000

# Creating an instance of the Environment class
E = Environment(eps, alpha, betao, betav0, betatau, etad, etae, cd, ce, rho, gamma, Pmut, mutationstep)


data_folder = 'results'
if not os.path.exists('figures'):
    os.mkdir('figures')

SMALL_SIZE = 14
MEDIUM_SIZE = 18
BIGGER_SIZE = 23

plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

list_v = []
list_o = []
list_tau = []
list_k = []
list_IL = []
list_fe = []
list_ce = []

for gen in range(20000, 20001, 500):
    data_file_name = data_folder + '/G/' + str(gen) + '.txt'
    open_data = open(data_file_name, 'r')
    list_data = open_data.read().split('\n')
    for line_txt in list_data:
        if line_txt != '':
            dict_data = {}
            list_data = line_txt.split(' ')

            list_vars_name = [i.split('=')[0] for i in list_data]
            list_vars = [float(i.split('=')[1]) for i in list_data]

            for var_name, var in zip(list_vars_name, list_vars):
                dict_data[var_name] = var

            o = dict_data['o']
            v = dict_data['v']
            tau = dict_data['tau']
            tauv = dict_data['tauv']
            k = dict_data['kv']
            kv=k
            K = dict_data['K']
            N=  dict_data['N']
            ind = Individual(o, v, tau, kv, tauv, K, N, E)
            fe = ind.get_fecundity()
            ce = ind.get_effective_costs(ind)

            list_v.append(v)
            list_o.append(o)
            list_tau.append(tau)
            list_k.append(k)
            list_IL.append(1 - v - o)
            list_fe.append(fe)
            list_ce.append(ce)

list_w = []
fmean = np.mean(list_fe)
for i in range(len(list_o)):
    w = list_fe[i] #* (1 - list_ce[i]) / (1 + E.gamma * fmean * len(list_l))
    list_w.append(w)


Blues = matplotlib.cm.get_cmap('YlGnBu')
kmax = max(list_k)
kmin = min(list_k)

def color_k(k):
    x = (k - kmin) / (kmax - kmin)
    return Blues(x)

list_color_k = []
for k in list_k:
    list_color_k.append(color_k(k))

wmax = max(list_w)
wmin = min(list_w)

def color_w(w):
    x = (w - wmin) / (wmax - wmin)
    #x = ((5 * x) // 1) / 5
    return Blues(x)

list_color_w = []
for w in list_w:
    list_color_w.append(color_w(w))

alph = 0.9

# Assuming list_tau and list_IL are your x and y data points, and list_color_k is your color list
fig, axs = plt.subplots()
alph = 0.5  # Example alpha
axs.scatter(list_tau, list_IL, s=15, alpha=alph, color=list_color_k)

# Setting locator params
axs.locator_params(axis='y', nbins=3)
axs.locator_params(axis='x', nbins=3)

# Calculating and setting aspect ratio
x0, x1 = axs.get_xlim()
y0, y1 = axs.get_ylim()
axs.set_aspect(abs(x1 - x0) / abs(y1 - y0))

plt.savefig('figures/Figure_S6_a.png')


fig, axs = plt.subplots()
cm = plt.cm.get_cmap('YlGnBu')
sc = plt.scatter(list_o, list_tau, c=list_k, vmin=kmin, vmax=kmax, s=2, cmap=cm)
plt.colorbar(sc)
axs.locator_params(axis='y', nbins=3)
axs.locator_params(axis='x', nbins=3)
x0, x1 = axs.get_xlim()
y0, y1 = axs.get_ylim()
axs.set_aspect(abs(x1 - x0) / abs(y1 - y0))
plt.savefig('figures/colorbar_k.png')

fig, axs = plt.subplots()
cm = plt.cm.get_cmap('YlGnBu')
sc = plt.scatter(list_tau, list_IL, c=list_w, alpha=alph, s=15, vmin=wmin, vmax=wmax, cmap=cm)
axs.locator_params(axis='y', nbins=3)
axs.locator_params(axis='x', nbins=3)
x0, x1 = axs.get_xlim()
y0, y1 = axs.get_ylim()
axs.set_aspect(abs(x1 - x0) / abs(y1 - y0))
plt.savefig('figures/Figure_S6_b.png')

fig, axs = plt.subplots()
cm = plt.cm.get_cmap('YlGnBu')
sc = plt.scatter(list_o, list_tau, c=list_w, alpha=alph, s=15, vmin=wmin, vmax=wmax, cmap=cm)
plt.colorbar(sc)
axs.locator_params(axis='y', nbins=3)
axs.locator_params(axis='x', nbins=3)
x0, x1 = axs.get_xlim()
y0, y1 = axs.get_ylim()
axs.set_aspect(abs(x1 - x0) / abs(y1 - y0))
plt.savefig('figures/colorbar_fe.png')

data_folder = 'results'
save_data_for_mathematica(data_folder)