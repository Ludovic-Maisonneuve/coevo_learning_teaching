from functions.visualize_data import *

data_folder = 'results'
if not os.path.exists('figures'):
    os.mkdir('figures')

SMALL_SIZE = 18
MEDIUM_SIZE = 22
BIGGER_SIZE = 27

plt.rc('font', size=SMALL_SIZE)  # controls default text sizes
plt.rc('axes', titlesize=BIGGER_SIZE)  # fontsize of the axes title
plt.rc('axes', labelsize=BIGGER_SIZE)  # fontsize of the x and y labels
plt.rc('xtick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
plt.rc('ytick', labelsize=MEDIUM_SIZE)  # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)  # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

# Make figure 4 d

plot_traits_evolution(data_folder, ngmin=25000, ngmax=120000, density_max=50, plot_v=False, plot_o=False,
                      plot_tau=False, plot_trait_proj=True)
plt.tight_layout()
plt.savefig('figures/Figure_4_d.png')


# Make figure 4 c

def scatter_hist_square_colorbar(x, y, ax, ax_histx, ax_histy, list_k, kmin, kmax):
    # Create a square scatter plot
    cm = plt.cm.get_cmap('YlGnBu')
    sc = ax.scatter(x, y, c=list_k, vmin=kmin, vmax=kmax, s=25, cmap=cm)
    plt.colorbar(sc)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ax.set_aspect((xmax - xmin) / (ymax - ymin))

    # Histogram along x-axis
    ax_histx.hist(x)
    ax_histx.set_xlim(ax.get_xlim())

    # Histogram along y-axis
    ax_histy.hist(y, orientation='horizontal')
    ax_histy.set_ylim(ax.get_ylim())

    ax_histx.spines['top'].set_visible(False)
    ax_histx.spines['right'].set_visible(False)

    ax_histy.spines['top'].set_visible(False)
    ax_histy.spines['right'].set_visible(False)

    ax_histx.xaxis.set_tick_params(labelbottom=False)
    ax_histy.yaxis.set_tick_params(labelleft=False)


def scatter_hist_square(x, y, ax, ax_histx, ax_histy, list_color_k):
    # Create a square scatter plot
    ax.scatter(x, y, color=list_color_k)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    ax.set_aspect((xmax - xmin) / (ymax - ymin))

    # Histogram along x-axis
    ax_histx.hist(x, color='black')
    ax_histx.set_xlim(ax.get_xlim())

    # Histogram along y-axis
    ax_histy.hist(y, orientation='horizontal', color='black')
    ax_histy.set_ylim(ax.get_ylim())


gen1 = 25000 + 0
gen2 = 25000 + 16000
gen3 = 25000 + 32000

kmaxplot = 7
kminplot = 6.2

for gensnap in [gen1, gen2, gen3]:
    list_v = []
    list_o = []
    list_tau = []
    list_k = []
    list_IL = []

    for gen in range(gensnap, gensnap + 1, 500):
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
                k = dict_data['kv']
                K = dict_data['K']

                list_v.append(v)
                list_o.append(o)
                list_tau.append(tau)
                list_k.append(k)
                list_IL.append(1 - v - o)
    #
    Blues = matplotlib.cm.get_cmap('YlGnBu')
    kmax = max(list_k)
    kmin = min(list_k)


    def color_k(k):
        x = (k - kmin) / (kmax - kmin)
        # x = ((5 * x) // 1) / 5
        return Blues(x)


    list_color_k = []
    for k in list_k:
        list_color_k.append(color_k(k))

    # Create a Figure, which doesn't have to be square.
    fig = plt.figure(layout='constrained')
    # Create the main axes, leaving 25% of the figure space at the top and on the
    # right to position marginals.
    ax = fig.add_gridspec(top=0.75, right=0.75).subplots()
    ax.set_xlim([0.52, 0.77])
    ax.set_ylim([0, 0.4])
    ax.set_xticks([0.5, 0.7])
    ax.set_yticks([0.1, 0.3], labels=[0, 0.3])
    # The main axes' aspect can be fixed.
    ax.set(aspect=1)
    # Create marginal axes, which have 25% of the size of the main axes.  Note that
    # the inset axes are positioned *outside* (on the right and the top) of the
    # main axes, by specifying axes coordinates greater than 1.  Axes coordinates
    # less than 0 would likewise specify positions on the left and the bottom of
    # the main axes.
    ax_histx = ax.inset_axes([0, 1.05, 1, 0.25], sharex=ax)
    ax_histy = ax.inset_axes([1.05, 0, 0.25, 1], sharey=ax)
    # Draw the scatter plot and marginals.
    scatter_hist_square(list_tau, list_IL, ax, ax_histx, ax_histy, list_color_k)
    scatter_hist_square_colorbar(list_tau, list_IL, ax, ax_histx, ax_histy, list_k, kminplot, kmaxplot)

    if gensnap == gen1:
        plt.savefig('figures/Figure_4_c_1.pdf')
    elif gensnap == gen2:
        plt.savefig('figures/Figure_4_c_2.pdf')
    else:
        plt.savefig('figures/Figure_4_c_23.pdf')

# Make figure S7

# Create a Figure, which doesn't have to be square.
fig = plt.figure(layout='constrained')
ax = fig.add_gridspec(top=0.75, right=0.75).subplots()
ax.set_xlim([0.52, 0.77])
ax.set_xticks([0.5, 0.7])
ax.set(aspect=1)
ax_histx = ax.inset_axes([0, 1.05, 1, 0.25], sharex=ax)
ax_histy = ax.inset_axes([1.05, 0, 0.25, 1], sharey=ax)
# Draw the scatter plot and marginals.
scatter_hist_square(list_tau, list_v, ax, ax_histx, ax_histy, list_color_k)
scatter_hist_square_colorbar(list_tau, list_v, ax, ax_histx, ax_histy, list_k, kminplot, kmaxplot)

plt.savefig('figures/Figure_S7_a.pdf')

# Create a Figure, which doesn't have to be square.
fig = plt.figure(layout='constrained')
ax = fig.add_gridspec(top=0.75, right=0.75).subplots()
ax.set_xlim([0.52, 0.77])
ax.set_xticks([0.5, 0.7])
ax.set(aspect=1)
ax_histx = ax.inset_axes([0, 1.05, 1, 0.25], sharex=ax)
ax_histy = ax.inset_axes([1.05, 0, 0.25, 1], sharey=ax)
# Draw the scatter plot and marginals.
scatter_hist_square(list_tau, list_o, ax, ax_histx, ax_histy, list_color_k)
scatter_hist_square_colorbar(list_tau, list_o, ax, ax_histx, ax_histy, list_k, kminplot, kmaxplot)

plt.savefig('figures/Figure_S7_b.pdf')

save_data_for_mathematica(data_folder, ngmin=25000, ngmax=120000)
