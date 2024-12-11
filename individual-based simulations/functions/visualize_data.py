import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from functions.save_and_open import *


def indice_born_trait(array_density):
    # Find the indices of the first and last non-zero elements in the array
    return min(np.nonzero(array_density)[0]), max(np.nonzero(array_density)[0])


def plot_traits_evolution(data_folder, ngmin=0, ngmax=None, density_max=100, plot_o=True, plot_v=True, plot_tau=True,
                          plot_trait_proj=False,
                          taumax=2):
    # Get the traits distribution across generations
    array_distribution_across_generations_o, array_distribution_across_generations_v, array_distribution_across_generations_tau, array_distribution_across_generations_trait_proj = get_traits_distribution_across_generations(
        data_folder)

    # Get array dimensions and resolution
    resolution = np.shape(array_distribution_across_generations_o)[1]
    nb_of_gen = np.shape(array_distribution_across_generations_o)[0] * 10

    # Define the range of generations to consider
    indice_genmin = ngmin // 10
    indice_genmax = (nb_of_gen // 10) if ngmax is None else (ngmax // 10)

    # Compute the sum of trait distributions over generations
    array_sum_distribution_over_generations_o = np.sum(
        array_distribution_across_generations_o[indice_genmin:indice_genmax + 1, :], axis=0)
    array_sum_distribution_over_generations_v = np.sum(
        array_distribution_across_generations_v[indice_genmin:indice_genmax + 1, :], axis=0)
    array_sum_distribution_over_generations_tau = np.sum(
        array_distribution_across_generations_tau[indice_genmin:indice_genmax + 1, :], axis=0)
    array_sum_distribution_over_generations_trait_proj = np.sum(
        array_distribution_across_generations_trait_proj[indice_genmin:indice_genmax + 1, :], axis=0)

    # Get limit values for each trait
    indice_omin, indice_omax = indice_born_trait(array_sum_distribution_over_generations_o)
    indice_vmin, indice_vmax = indice_born_trait(array_sum_distribution_over_generations_v)
    indice_taumin, indice_taumax = indice_born_trait(array_sum_distribution_over_generations_tau)
    indice_traitprojmin, indice_traitprojmax = indice_born_trait(array_sum_distribution_over_generations_trait_proj)

    # Create arrays for trait values
    list_o = np.linspace(0, 1, resolution)
    list_v = np.linspace(0, 1, resolution)
    list_tau = np.linspace(0, taumax, resolution)
    list_trait_proj = np.linspace(-0.78947556, 1.250096, resolution)

    # Create colormap
    Blues = matplotlib.cm.get_cmap('Blues')
    L = [np.array([1, 1, 1, 1]) if t == 0 else Blues(t) for t in np.linspace(0, 1, 501)]
    cm = LinearSegmentedColormap.from_list('cmap', L, N=501)

    # Make plot
    count = sum([plot_o, plot_v, plot_tau, plot_trait_proj])
    cv = 1 if plot_o else 0
    ctau = 2 if plot_o and plot_v else (0 if not plot_o and not plot_v else 1)

    fig, axs = plt.subplots(1, count)
    axs.spines['top'].set_visible(False)
    axs.spines['right'].set_visible(False)
    plt.locator_params(axis='y', nbins=4)
    plt.locator_params(axis='x', nbins=3)

    # Plot o values if requested
    if plot_o:
        if count == 1:
            axs.imshow(
                array_distribution_across_generations_o[indice_genmin:indice_genmax + 1, indice_omin:indice_omax].T,
                extent=[0 * 10, (indice_genmax - indice_genmin) * 10, list_o[indice_omin], list_o[indice_omax]],
                aspect=1 / 1.62 * (indice_genmax * 10 - indice_genmin * 10 + 1) / (
                        list_o[indice_omax] - list_o[indice_omin]), cmap=cm, vmin=0, vmax=density_max,
                origin='lower')
        else:
            axs[0].imshow(
                array_distribution_across_generations_o[indice_genmin:indice_genmax + 1, indice_omin:indice_omax].T,
                extent=[0 * 10, (indice_genmax - indice_genmin) * 10, list_o[indice_omin], list_o[indice_omax]],
                aspect=1 / 1.62 * (indice_genmax * 10 - indice_genmin * 10 + 1) / (
                        list_o[indice_omax] - list_o[indice_omin]), cmap=cm, vmin=0, vmax=density_max,
                origin='lower')

    # Plot v values if requested
    if plot_v:
        if count == 1:
            axs.imshow(
                array_distribution_across_generations_v[indice_genmin:indice_genmax + 1, indice_vmin:indice_vmax].T,
                extent=[0 * 10, (indice_genmax - indice_genmin) * 10, list_v[indice_vmin], list_v[indice_vmax]],
                aspect=1 / 1.62 * (indice_genmax * 10 - indice_genmin * 10 + 1) / (
                        list_v[indice_vmax] - list_v[indice_vmin]), cmap=cm, vmin=0, vmax=density_max,
                origin='lower')
        else:
            axs[cv].imshow(
                array_distribution_across_generations_v[indice_genmin:indice_genmax + 1, indice_vmin:indice_vmax].T,
                extent=[0 * 10, (indice_genmax - indice_genmin) * 10, list_v[indice_vmin], list_v[indice_vmax]],
                aspect=1 / 1.62 * (indice_genmax * 10 - indice_genmin * 10 + 1) / (
                        list_v[indice_vmax] - list_v[indice_vmin]), cmap=cm, vmin=0, vmax=density_max,
                origin='lower')

    # Plot tau values if requested
    if plot_tau:
        if count == 1:
            axs.imshow(
                array_distribution_across_generations_tau[indice_genmin:indice_genmax + 1,
                indice_taumin:indice_taumax].T,
                extent=[0 * 10, (indice_genmax - indice_genmin) * 10, list_tau[indice_taumin],
                        list_tau[indice_taumax]],
                aspect=1 / 1.62 * (indice_genmax * 10 - indice_genmin * 10 + 1) / (
                        list_tau[indice_taumax] - list_tau[indice_taumin]), cmap=cm, vmin=0,
                vmax=density_max,
                origin='lower')
        else:
            axs[ctau].imshow(
                array_distribution_across_generations_tau[indice_genmin:indice_genmax + 1,
                indice_taumin:indice_taumax].T,
                extent=[0 * 10, (indice_genmax - indice_genmin) * 10, list_tau[indice_taumin],
                        list_tau[indice_taumax]],
                aspect=1 / 1.62 * (indice_genmax * 10 - indice_genmin * 10 + 1) / (
                        list_tau[indice_taumax] - list_tau[indice_taumin]), cmap=cm, vmin=0,
                vmax=density_max,
                origin='lower')

    if plot_trait_proj:
        fig, axs = plt.subplots(1, 1)
        axs.spines['top'].set_visible(False)
        axs.spines['right'].set_visible(False)
        plt.locator_params(axis='y', nbins=4)
        plt.locator_params(axis='x', nbins=3)
        axs.imshow(
            array_distribution_across_generations_trait_proj[indice_genmin:indice_genmax + 1,
            indice_traitprojmin:indice_traitprojmax].T,
            extent=[0 * 10, (indice_genmax - indice_genmin) * 10, list_trait_proj[indice_traitprojmin],
                    list_trait_proj[indice_traitprojmax]],
            aspect=1 / 1.62 * (indice_genmax * 10 - indice_genmin * 10 + 1) / (
                    list_trait_proj[indice_traitprojmax] - list_trait_proj[indice_traitprojmin]), cmap=cm, vmin=0,
            vmax=density_max,
            origin='lower')


def plot_mean_values_evolution(data_folder, list_plot, list_colors=None, ngmin=0, ngmax=None,
                               plot_legend=True):  # Example usage: plot_mean_values_evolution("your_data_folder_path_here")
    # Get the list of generations from the mean values folder
    list_gen = sorted([int(i[:-4]) for i in os.listdir(data_folder + '/mean_values') if i != '.DS_Store'])

    # Iterate over generations and extract mean values
    for gen in list_gen:
        data_file_name = f"{data_folder}/mean_values/{gen}.txt"
        with open(data_file_name, 'r') as open_data:
            # Split data into values and variable names
            list_data = [value for value in open_data.read().split(' ')]
            list_vars_name = [i.split('=')[0] for i in list_data]
            list_vars = [float(i.split('=')[1]) for i in list_data]
        # Initialize lists for the first generation
        if gen == 0:
            for var_name in list_vars_name:
                locals()[f'list_{var_name}_mean'] = []

        # Append mean values to the corresponding lists
        for var, var_name in zip(list_vars, list_vars_name):
            locals()[f'list_{var_name}_mean'].append(var)

    # Define the range of generations to plot
    imin = ngmin // 10
    imax = (list_gen[-1] // 10) if ngmax is None else (ngmax // 10)

    # Plot mean values with or without colors

    # Check if custom colors are provided
    if list_colors is None:
        # Iterate over lists of variables to plot
        for list_vars_plot in list_plot:
            # Create a new figure and axis
            fig, axs = plt.subplots(1, 1)

            # Iterate over variables in the current list
            for var in list_vars_plot:
                # Plot mean values for the variable
                axs.plot(list_gen[0:imax - imin], locals()[f'list_{var}_mean'][imin:imax], label=var)

            # Add legend if specified
            if plot_legend:
                axs.legend()
    else:
        # Iterate over lists of variables and corresponding colors
        for list_vars_plot, list_colors_single_plot in zip(list_plot, list_colors):
            # Create a new figure and axis
            fig, axs = plt.subplots(1, 1)

            # Iterate over variables and colors in the current lists
            for var, c in zip(list_vars_plot, list_colors_single_plot):
                # Plot mean values for the variable with the specified color
                # PB here
                axs.plot(list_gen[0:imax - imin], locals()[f'list_{var}_mean'][imin:imax], label=var, color=c)

            # Add legend if specified
            if plot_legend:
                axs.legend()

    # Display the plot
    # plt.show()


def get_list_mean(data_folder, list_var):  # Example usage: plot_mean_values_evolution("your_data_folder_path_here")
    # Get the list of generations from the mean values folder
    list_gen = sorted([int(i[:-4]) for i in os.listdir(data_folder + '/mean_values') if i != '.DS_Store'])

    # Iterate over generations and extract mean values
    for gen in list_gen:
        data_file_name = f"{data_folder}/mean_values/{gen}.txt"
        with open(data_file_name, 'r') as open_data:
            # Split data into values and variable names
            list_data = [value for value in open_data.read().split(' ')]
            list_vars_name = [i.split('=')[0] for i in list_data]
            list_vars = [float(i.split('=')[1]) for i in list_data]
        # Initialize lists for the first generation
        if gen == 0:
            for var_name in list_vars_name:
                locals()[f'list_{var_name}_mean'] = []

        # Append mean values to the corresponding lists
        for var, var_name in zip(list_vars, list_vars_name):
            locals()[f'list_{var_name}_mean'].append(var)

    results = []
    for var_name in list_var:
        results.append(locals()[f'list_{var_name}_mean'])
    return tuple(results)
