import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import scipy.stats

if __name__ == '__main__':
    fname = sys.argv[1]
    os.system('./exe_process_prime_probe '+fname+' 64')
    fname = fname + '.csv'

    data = np.loadtxt(fname)
    assert data.shape[0] == 4096
    n_set = data.shape[1]
    print('Number of cache sets: ', n_set)

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

    #assert fname[-4:] == '.txt'
    fig_dir = 'ppfig/'+fname[:-4]+'/'
    if not os.path.exists(fig_dir):
        print('Making diretory: ', fig_dir)
        os.makedirs(fig_dir)
    for i in range(16):
        plt.figure(figsize = (8,6))
        plot_data = data[i*256:(i+1)*256]
        plt_vmax = np.percentile(plot_data, 98)
        plt_vmin = np.percentile(plot_data, 2)
        ax = sns.heatmap(plot_data, vmax=plt_vmax, vmin=plt_vmin,
                yticklabels=yticks, xticklabels=xticks)
        cbar_ax = ax.figure.axes[-1]
        cbar_ax.tick_params(labelsize = 20)
        plt.xlabel('Index Bits of Cache Line', fontsize = 24)
        plt.ylabel('Input Byte', fontsize = 24)
#        plt.locator_params(axis = 'x', nbins = 8)
#        plt.locator_params(axis = 'y', nbins = 20)
        plt.xticks(fontsize = 20, rotation = 0)
        plt.yticks(fontsize = 20, rotation = 0)
        #plt.show()
        plt.savefig(fig_dir+'Byte'+str(i)+'.jpg', bbox_inches='tight')
        plt.close()
