import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, SymLogNorm, Normalize
import sys
import os
import scipy.stats

if __name__ == '__main__':
    fname = sys.argv[1]
    os.system('./exe_process_fr_d '+fname)
    fname = fname + '.csv'

    data = np.loadtxt(fname)
    assert data.shape[0] == 4096
    n_set = data.shape[1]
    print('Number of cache lines: ', n_set)

    yticks = range(256)
    keptticks = yticks[::16]
    yticks = ['' for y in yticks]
    yticks[::16] = keptticks

    xticks = range(n_set)
    keptticks = xticks[::int(len(xticks)/8)]
    xticks = ['' for x in xticks]
    xticks[::int(len(xticks)/8)] = keptticks

    key_msb = [ \
        0,  1,  13, 6, \
        14, 13, 0,  5, \
        15, 9,  1,  0, \
        4,  4,  15, 11]

    # first 16 lines are affected by secret-dependent accesses
    n_score_block = 16

    assert fname[-4:] == '.csv'
    fig_dir = 'fr_dcache_fig/'+fname[:-4]+'/'
#    fig_dir = 'fr_dcache_fig_'+fname[:-4]+'_ylim/'
    if not os.path.exists(fig_dir):
        print('Making diretory: ', fig_dir)
        os.makedirs(fig_dir)
    for i in range(16):
        plot_data = data[i*256:(i+1)*256]
        plt.figure(figsize = (8,6))
        ax = sns.heatmap(plot_data,
                #norm = SymLogNorm(linthresh=0.03),
                norm = LogNorm(vmin = 20,vmax = 200),
                #cmap = "Greens",
                yticklabels=yticks, xticklabels=xticks,#)
                vmin = 20,
                vmax = 200)
        #cbar = ax.collections[0].colorbar
        #cbar.ax.tick_params(labelsize=20)
        #cbar_ax = ax.figure.axes[-1]
        #cbar_ax.tick_params(labelsize = 20)
        plt.xlabel('Block of Shared Memory', fontsize = 24)
        plt.ylabel('Input Byte', fontsize = 24)
        plt.xticks(fontsize = 24, rotation = 0)
        plt.yticks(fontsize = 24, rotation = 0)
        plt.savefig(fig_dir+'Byte'+str(i)+'.jpg', bbox_inches='tight')
        #plt.show()
        plt.close()
