# TODO

- More unit tests

- Improve simulator logging functionality
    - simulator subprocess should collect useful stdout and stderr to debug issues
    - sim_logging should tidy up logs

# Probably good, but not essential

- Better phyddle banner graphics, info, etc.

- Print all non-default file/command settings in header

- Better file format and file location checking and errors
    - check all files and dirs exist before run
    - check all csv/nexus/tree formats after reading

- Have phyddle report error when cmd_sim fails
    - e.g. if script is set up wrong, how to report?

- Base class for pipeline step?
    - virtual functions for set_args, load_input, run, make_results, save_results

- Utilities to combine hdf5 and csv tensors
    - e.g. if we have hdf5 from multiple servers, how to combine them
    - also, tools to convert hdf5 -> csv and csv -> hdf5

- Nickname for fileset within project, -n
    - '?' to generate a random name
    - adjective + species
    - also, autogen project name
    - random naem for new project?

- Summary text file of all results in one easily greppable file to be processed

- Plot network performance
    - weight/bias
    - activation?
    - trained network or across epochs?
    - Plot for node loadings.

- Ensure Format can handle multiple characters and states
    - main issue is e.g. num char = 3
    - num states = [3, 5, 2]

# Longterm

- Handling multiple trees/matrices per example dataset

- Model comparison

- Ancestral states


# Open questions

- What example models/platforms for simulation scripts.
    - Languages: Python, R, RevBayes, MASTER, Julia, shell
    - Models: CTMC, birth-death, SSE, SIR
    - Programs: gen3sis, MESS, SLiM, FAVITES, FossilSim

- How to distribution MASTER Python wrappers
    - package with phyddle in subdir
    - separate repository, full package, etc.


# DONE

- Add default config to allow for three layers of assignment
    - default -> my_config -> CLI
    - perhaps distribute a default config that people can tweak

- Automatically index replicates for sim/fmt
    - Current: --start_idx 100 --end_idx 1000 
    - Alternative: --add_sim_rep 10000, then figure out based on os.path.files()
    - Then Format can be done on first 90%, leave out last 10%, then can work that into training/test split

- Downsampling of large trees.
    - If tree is larger than max tree width category size, downsample to match max size.
    - User sets downsampling strategy, e.g. uniform, diversified, etc.
    - Downsampling enters downsampling_proportion into aux_data

- Change how test dataset is generated and used
    - Currently, test dataset is sampled during Train
    - Instead, have test data split out during Format and saved to file
    - Then have test data fed through Estiamte to produce results
    - This allows us to compare model performance against different batches of test data

- Common functions for normalize/denormalize/exp/log/etc.

- strip out tree_width_cats

- General problem handling bool argparse args
    - https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse

- PCA
    - loadings
    - PCA for state tensor too?
    - https://statisticsglobe.com/visualization-pca-python
    - https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contour.html

- Runtime information
    - start/end time for each step

- Add support for phyddle binary using __main__()
    - basics working
    - replace import with exec
