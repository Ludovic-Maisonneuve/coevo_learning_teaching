Programs for the Article:
"The Coevolution of Learning Schedules and Teaching Enhances Cumulative Knowledge and Drives a Teacher-Innovator Syndrome"
Authors: Ludovic Maisonneuve, Laurent Lehmann, Charles Mullon
Published in Proceedings of the Royal Society B (DOI: 10.1098/rspb.2024.2470)

Contents:

1. evolutionary analyses:  
   This folder contains the necessary files to perform the evolutionary analyses and generate most of the figures.  
   - evolutionary_analyses.nb: A Mathematica notebook for conducting evolutionary analyses and creating nearly all the figures.  
   - numerical_functions.nb: A Mathematica notebook containing functions to compute evolutionary equilibria.  
   - data_saved: A folder with saved data produced for the evolutionary analyses.  
   - data_ind_based_sim: A folder containing data from individual-based simulations. This data is used by evolutionary_analyses.nb to generate figures.

2. individual-based simulations:  
   This folder contains the Python scripts to perform individual-based simulations.  
   - functions: A folder containing Python scripts to define functions for performing individual-based simulations, saving data, and plotting.  
     - classes.py: Defines the classes used in the model.  
     - dynamics.py: Defines functions to iterate the individual-based simulations.  
     - save_and_open.py: Defines functions to save and open data.  
     - visualize_data.py: Defines functions to plot data.  
   - simulations: A folder containing files that perform the simulations.  
     - stabilising selection (fig 3cd): Contains the scripts used to perform the individual-based simulations under stabilising selection to produce Figures 3cd.  
       - launch.py: Launches the simulation and saves the data.  
       - export data for mathematica.py: Exports the data in a format compatible with the evolutionary_analyses.nb Mathematica notebook.  
     - phenotypic association (fig 4b + fig S6): Contains the scripts used to perform the individual-based simulations for plotting the phenotypic association in Figure 4b and S6.  
       - launch.py: Launches the simulation and saves the data.  
       - plot and export data for mathematica: Generates Figure S6 and exports the data in a format compatible with the evolutionary_analyses.nb Mathematica notebook.  
     - evolutionary branching (fig 4cde + fig S7): Contains the scripts used to perform the individual-based simulations for disruptive selection to produce Figures 4cde and S7.  
       - launch.py: Launches the simulation and saves the data.  
       - plot and export data for mathematica.py: Generates Figures 4cd and S7 and exports the data in a format compatible with the evolutionary_analyses.nb Mathematica notebook.


