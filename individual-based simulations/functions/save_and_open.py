import json
import os

from functions.classes import *


def save_generation(G, n, data_folder, eig=np.array([1, 1, 1]), list_traits=['o', 'v', 'tau'],
                    list_traits_max=[1, 1, 2],
                    list_traits_min=[0, 0, 0]):
    #
    list_border_value_trait_proj = [
        eig[0] * o_border + eig[1] * v_border + eig[2] * tau_border for o_border in
        [list_traits_min[0], list_traits_max[0]]
        for v_border in [list_traits_min[1], list_traits_max[1]] for tau_border in
        [list_traits_min[2], list_traits_max[2]]
    ]
    trait_proj_min = min(list_border_value_trait_proj)
    trait_proj_max = max(list_border_value_trait_proj)

    # Check if the folder to save data exists. Otherwise, it creates the folder.
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    if not os.path.exists(data_folder + '/G'):
        os.mkdir(data_folder + '/G')
    if not os.path.exists(data_folder + '/density'):
        os.mkdir(data_folder + '/density')
    if not os.path.exists(data_folder + '/mean_values'):
        os.mkdir(data_folder + '/mean_values')

    # Save all individuals in generation n
    file_name = data_folder + '/G/' + str(n) + '.txt'
    data_txt = ''
    list_ind_attributes = [attr for attr in dir(G[0]) if
                           not callable(getattr(G[0], attr)) and not attr.startswith("__")]
    list_ind_attributes.remove('E')

    # Create empty lists for each attribute
    for attr in list_ind_attributes:
        locals()[f'list_{attr}'] = []

    # Iterate over individuals in generation G
    for i, ind in enumerate(G):
        # Iterate over attributes of each individual
        for attr in list_ind_attributes:
            data_txt += attr + '=' + str(getattr(ind, attr)) + ' '
            locals()[f'list_{attr}'].append(getattr(ind, attr))
        data_txt = data_txt[:-1] + '\n'

    # Write data to file
    file = open(file_name, 'a')
    file.write(data_txt)
    file.close()

    # Erase previous generation
    file_to_erase_name = data_folder + '/G/' + str(n - 10) + '.txt'
    if os.path.exists(file_to_erase_name) and (n - 10) % 500 != 0:
        os.remove(file_to_erase_name)

    # Save density
    resolution = 2500

    for trait in list_traits:
        locals()[f'array_distribution_{trait}'] = np.zeros(resolution)

    array_distribution_trait_proj_eig = np.zeros(resolution)

    # Update distribution arrays based on individual traits
    for ind in G:
        for i, trait in enumerate(list_traits):
            locals()[f'array_distribution_{trait}'][int((getattr(ind, trait) - list_traits_min[i]) /
                                                        (list_traits_max[i] - list_traits_min[i]) * (
                                                                resolution - 1))] += 1
        trait_proj_eign = np.dot(np.array([ind.v, ind.o, ind.tau]), eig)
        array_distribution_trait_proj_eig[int((trait_proj_eign - trait_proj_min) /
                                              (trait_proj_max - trait_proj_min) * (
                                                      resolution - 1))] += 1

    # Save distribution arrays to files
    for trait in list_traits:
        if not os.path.exists(f"{data_folder}/density/{trait}"):
            os.mkdir(f"{data_folder}/density/{trait}")
        np.save(f"{data_folder}/density/{trait}/{n}", locals()[f'array_distribution_{trait}'])

    if not os.path.exists(f"{data_folder}/density/trait_proj_eig"):
        os.mkdir(f"{data_folder}/density/trait_proj_eig")
    np.save(f"{data_folder}/density/trait_proj_eig/{n}", array_distribution_trait_proj_eig)

    # Save mean and covariance values
    data_txt = ''
    for attr in list_ind_attributes:
        data_txt += f"{attr}={np.mean(locals()[f'list_{attr}'])} "
    for attr1 in list_ind_attributes:
        for attr2 in list_ind_attributes:
            data_txt += f"C_{attr1}_{attr2}={np.cov(locals()[f'list_{attr1}'], locals()[f'list_{attr2}'])[0][1]} "
    data_txt = data_txt[:-1]
    file_name = data_folder + '/mean_values/' + str(n) + '.txt'
    file = open(file_name, 'a')
    file.write(data_txt)
    file.close()


def open_last_generation(data_folder, E):
    # Initialize an empty list to store individuals
    G = []

    # List all files in the '/G' folder
    list_files = os.listdir(data_folder + '/G')
    if '.DS_Store' in list_files:
        list_files.remove('.DS_Store')
    # Extract generation numbers from the filenames
    list_gen = [int(i[:-4]) for i in list_files]

    # Find the last generation
    last_gen = max(list_gen)

    # Construct the filename of the data file for the last generation
    data_file_name = data_folder + '/G/' + str(last_gen) + '.txt'

    # Open the data file for the last generation
    open_data = open(data_file_name, 'r')

    # Read the data file and split it into a list of lines
    list_data = open_data.read().split('\n')

    # Iterate over each line in the data file
    for line_txt in list_data:
        # Check if the line is not empty
        if line_txt != '':
            # Initialize a dictionary to store individual attributes
            dict_attributes = {}

            # Split the line into a list of attribute-value pairs
            list_attributes_txt = line_txt.split(' ')

            # Iterate over each attribute-value pair
            for i in list_attributes_txt:
                # Split the attribute-value pair
                attr_txt = i.split('=')

                # Create a local variable for each attribute with its corresponding value
                locals()[f'{attr_txt[0]}'] = float(attr_txt[1])

                # Add the attribute-value pair to the dictionary
                dict_attributes[attr_txt[0]] = float(attr_txt[1])

            # Set the 'E' attribute to the specified value
            dict_attributes['E'] = E

            # Create an Individual object with the attributes from the dictionary
            G.append(Individual(**dict_attributes))

    # Return the last generation number and the list of individuals
    return last_gen, G


def get_traits_distribution_across_generations(data_folder):
    # List all files in the '/density/o' folder
    list_files = os.listdir(data_folder + '/density/o')

    # Remove system-generated files if present
    if '.DS_Store' in list_files:
        list_files.remove('.DS_Store')

    # Extract generation numbers from the filenames
    list_gen = [int(i[:-4]) for i in list_files]

    # Find the last generation
    last_gen = max(list_gen)

    # Set the resolution for the distribution arrays
    resolution = 2500

    # Initialize distribution arrays for each trait across generations
    array_distribution_across_generations_o = np.zeros((last_gen // 10 + 1, resolution))
    array_distribution_across_generations_v = np.zeros((last_gen // 10 + 1, resolution))
    array_distribution_across_generations_tau = np.zeros((last_gen // 10 + 1, resolution))
    array_distribution_across_generations_trait_proj = np.zeros((last_gen // 10 + 1, resolution))

    # Iterate over each file in reverse order (from last to first generation)
    for file_name in reversed(list_files):
        # Load distribution arrays for each trait from the corresponding file
        array_distribution_o = np.load(data_folder + '/density/o/' + file_name)
        array_distribution_v = np.load(data_folder + '/density/v/' + file_name)
        array_distribution_tau = np.load(data_folder + '/density/tau/' + file_name)
        array_distribution_trait_proj = np.load(data_folder + '/density/trait_proj_eig/' + file_name)

        # Extract the generation number from the filename
        gen = int(file_name[:-4])

        # Update the distribution arrays across generations
        array_distribution_across_generations_o[gen // 10, :] = array_distribution_o
        array_distribution_across_generations_v[gen // 10, :] = array_distribution_v
        array_distribution_across_generations_tau[gen // 10, :] = array_distribution_tau
        array_distribution_across_generations_trait_proj[gen // 10, :] = array_distribution_trait_proj

    # Return the distribution arrays for each trait across generations
    return array_distribution_across_generations_o, array_distribution_across_generations_v, array_distribution_across_generations_tau, array_distribution_across_generations_trait_proj


def save_data_for_mathematica(data_folder, ngmin=0,
                              ngmax=None):  # Example usage: plot_mean_values_evolution("your_data_folder_path_here")

    if not os.path.exists(data_folder + '/Mathematica'):
        os.mkdir(data_folder + '/Mathematica')

    # Get the list of generations from the mean values folder
    list_gen_ = sorted([int(i[:-4]) for i in os.listdir(data_folder + '/mean_values') if i != '.DS_Store'])
    list_gen = []
    for gen in list_gen_:
        if gen % 100 == 0:
            list_gen.append(gen)

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
    imin = ngmin // 100
    imax = (list_gen[-1] // 100) if ngmax is None else (ngmax // 100)

    for var, var_name in zip(list_vars, list_vars_name):
        with open(data_folder + '/Mathematica/' + var_name + ".json", 'w') as file:
            json.dump(locals()[f'list_{var_name}_mean'][imin:imax], file)

    with open(data_folder + '/Mathematica/gen.json', 'w') as file:
        json.dump(list_gen[0:imax - imin], file)
