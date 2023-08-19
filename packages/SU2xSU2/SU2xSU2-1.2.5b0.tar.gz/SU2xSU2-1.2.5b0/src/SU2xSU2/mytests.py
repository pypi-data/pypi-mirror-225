import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import matplotlib as mpl
from cycler import cycler

from SU2xSU2 import SU2xSU2

# define model and lattice parameters 
model_paras = {'L':16, 'a':1, 'ell':5, 'eps':1/5, 'beta':0.6}
model = SU2xSU2(**model_paras)
# define simulation parameters and measurements
sim_paras = {'M':500, 'thin_freq':1, 'burnin_frac':0.0, 'accel':True, 'starting_config_path':'data\chain_state\config.npy', 'RNG_state_path':'data\chain_state\RNG_state.obj',
            'chain_state_dir':'data/new_state/'}
model.run_HMC(**sim_paras) 


# test style sheet
def plot_test():
    plt.style.use('./scientific.mplstyle')
    # plt.rcParams.update({'text.usetex': True}) # requires latex instalation
    fig = plt.figure()
    x, y = np.arange(10), np.arange(10)
    for i in np.arange(5):
        plt.errorbar(x, y+i, fmt='.', yerr=0.1, label='%d'%i)

    plt.legend()
    plt.show()

# plot_test()

# print(mpl.__file__)
# print(plt.style.available) # does not give the styles listed in stylelib of venv installation but also those of global mpl installation

