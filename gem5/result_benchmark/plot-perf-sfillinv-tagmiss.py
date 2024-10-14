import numpy as np
import matplotlib.pyplot as plt
import scipy.stats.mstats

def plot_metric(data, metric, benchmarks, methods, save_name, n_orig, n_starfarr, n_starnews):
    data_bar  = data[0]
    data_line = data[1]
    data2     = data[2]
    # data shape should be (n_benchmark, n_method)
    assert data_bar.ndim == 2
    assert data_line.ndim == 2
    assert data2.ndim == 2
    n_b    = data_bar.shape[0]
    n_bar  = data_bar.shape[1]
    n_line = data_line.shape[1]
    n2     = data2.shape[1]
    assert data_line.shape[0] == n_b-1
    assert data2.shape[0] == n_b-1
    assert len(methods) == n_bar
    assert len(benchmarks) == n_b

    barwidth = 1.0/(n_m+1)
    legend_fontsize = 15
    legend_x = 0.5
    legend_y = 0.9
    xlabel_size = 17
    single_figsize = (20, 4)

    fig, ax1 = plt.subplots(1, 1, figsize = single_figsize)
    x = np.arange(n_b)
    x_noavg = np.arange(n_b-1)
    colorlst = ['grey', 'red', 'tab:pink', 'lightsteelblue',
            'cornflowerblue', 'royalblue', 'darkblue']
    hatchlst = ['', '', '-', '', '', '', '']
    #assert n_bar  == 3
    #assert n_line == 3
    #assert n2     == 3
    for i in range(n_bar):
        ax1.bar(x+barwidth*(i-n_m/2), data_bar[:, i], width = barwidth,
                label = methods[i], color = colorlst[i], hatch = hatchlst[i])

    #ax1.set_xlabel('Benchmarks', fontweight = 'bold', fontsize = 18)
    ax1.set_xlim((-0.8, n_b-0.2))
    ax1.set_ylim((0.8, 1.6))
    ax1.tick_params(labelright=True, labelbottom=True, labelleft=True,
            labelsize=xlabel_size)
    ax1.grid(axis = 'y', linestyle = '--')
    ax1.set_ylabel(metric[0], fontweight = 'bold', fontsize = 18)

    ax1.legend(loc='lower center', bbox_to_anchor=(legend_x, legend_y+0.1),
          ncol=n_bar, fancybox=True, shadow=False, fontsize=legend_fontsize)
    ax1.set_xticks(x, benchmarks, fontsize = xlabel_size)
    #ax1.set_yticks(fontsize = 15)
    plt.savefig(save_name+'_1', bbox_inches='tight')
    plt.close()

    fig, ax2 = plt.subplots(1, 1, figsize = single_figsize)
    #ax2 = ax[1]
    #ax2 = ax1.twinx()
    for i in range(n_orig, n_line):
        ax2.bar(x_noavg+barwidth*(i-n_m/2), data_line[:, i], width = barwidth,
                label = methods[i], color = colorlst[i], hatch = hatchlst[i])
    ax2.set_xlim((-0.8, n_b-1.2))
    ax2.set_ylim((0, np.amax(data_line)*1.1))
    ax2.set_ylabel(metric[1], fontweight = 'bold', fontsize = 18)
    ax2.tick_params(labelright=True, labelbottom=True, labelleft=True,
            labelsize=xlabel_size)
    ax2.grid(axis = 'y', linestyle = '--')

    ax2.legend(loc='lower center', bbox_to_anchor=(legend_x, legend_y),
          ncol=n_bar, fancybox=True, shadow=False, fontsize=legend_fontsize)
    ax2.set_xticks(x_noavg, benchmarks[:-1], fontsize = xlabel_size)
    #ax2.set_yticks(fontsize = 15)
    plt.savefig(save_name+'_2', bbox_inches='tight')
    plt.close()

    fig, ax3 = plt.subplots(1, 1, figsize = single_figsize)
    #ax3 = ax[2]
    for i in range(n_orig + n_starfarr, n2):
        ax3.bar(x_noavg+barwidth*(i-n_m/2), data2[:, i], width = barwidth,
                label = methods[i], color = colorlst[i], hatch = hatchlst[i])
    ax3.set_xlim((-0.8, n_b-1.2))
    ax3.set_ylim((0, np.amax(data2)*1.1))
    ax3.set_ylabel(metric[2], fontweight = 'bold', fontsize = 18)
    ax3.tick_params(labelright=True, labelbottom=True, labelleft=True,
            labelsize=xlabel_size)
    ax3.grid(axis = 'y', linestyle = '--')

    ax3.legend(loc='lower center', bbox_to_anchor=(legend_x, legend_y),
          ncol=n_bar, fancybox=True, shadow=False, fontsize=legend_fontsize)
    ax3.set_xticks(x_noavg, benchmarks[:-1], fontsize = xlabel_size)
    #ax3.set_yticks(fontsize = 15)

    #plt.show(block = False)
    plt.savefig(save_name+'_3', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    dir0  = 'perf/'
    name0 = 'perf_500M'
    dir1  = 'starcache/'
    name1 = 'numsqinv_500M'
    dir2  = 'starcache/'
    name2 = 'tagmissspec_500M'
    figure_title = ['Relative Performance', '#SFill-Inv(in millions)',
            '#Load with a mapping hit\n and tag miss (in millions)']
    n_orig = 1
    n_starfarr = 1
    n_starnews = 4
    methods = [
            'salru',
            'starfarr',
            'starnews_k0',
            'starnews_k2',
            'starnews_k4',
            'starnews_k6',
               ]
    methods_labels = [
             'SA-LRU',
            'STAR-FARR-T1',
            'STAR-NEWS-k0',
            'STAR-NEWS-k2',
            'STAR-NEWS-k4',
            'STAR-NEWS-k6',
            ]
    benchmarks = ['GemsFDTD', 'astar', 'bwaves', 'bzip2',
        'cactusADM', 'calculix', 'gamess', 'gcc', 'gobmk',
        'gromacs', 'h264ref', 'hmmer', 'lbm',
        'leslie3d', 'libquantum', 'mcf', 'milc', 'namd',
        'omnetpp', 'povray', 'sjeng', 'sphinx3', 'wrf',
        'zeusmp']
    #benchmarks_g = benchmarks + ['gmean']
    n_m = len(methods)
    assert len(methods) == n_orig + n_starfarr + n_starnews
    n_b = len(benchmarks)
    data_bar  = np.zeros((n_b, n_m))
    rdata_bar = np.zeros((n_b+1, n_m)) # relative data
    data_line = np.zeros((n_b, n_m))
    data2     = np.zeros((n_b, n_m))
    print('n_m: ', n_m, 'n_b: ', n_b)

    def readstats(metric_name, start_idx):
        data = np.zeros((n_b, n_m))
        f_prefix = 'dir_checkpoint/greps/'+metric_name+'_'
        for i in range(start_idx, n_m):
            f_name = f_prefix+methods[i]+'.grep'
            with open(f_name, 'r') as f:
                lines = f.readlines()
                assert len(lines) == n_b, f_name+' n_line: '+str(len(lines))
                for j in range(n_b):
                    line = lines[j].split()
                    assert line[0][5:5+len(benchmarks[j])] == benchmarks[j],\
                        'Wrong benchmark name: '+\
                        f_name+':line '+str(j)+' '+line[0][5:5+len(benchmarks[j])]+\
                        ' vs '+benchmarks[j]
                    #assert line[1].isnumeric(), f_name+':line '+str(j)
                    data[j, i] = float(line[1])
        return data

    # normalized execution time
    data_bar[:n_b, :]  = readstats(dir0+name0, 0) # all benchmarks

    # number of SFill-Inv
    data_line[:n_b, :] = readstats(dir1+name1, n_orig) # skip orig config

    # number of mapping hit but tag miss
    data2[:,:]         = readstats(dir2+name2, n_orig + n_starfarr) # skip orig and starfarr

    for i in range(n_b):
        rdata_bar[i, :] = data_bar[i, :]/data_bar[i, 0]
    for i in range(n_m):
        rdata_bar[n_b, i] = scipy.stats.mstats.gmean(rdata_bar[:n_b, i])
    data_line = data_line / 1000000.0
    data1     = data_line
    data2     = data2     /1000000.0
    for i in range(n_m):
        rdata_single = rdata_bar[:n_b, i]
        print(methods[i]+' '+figure_title[0]+\
                ' avg: '+str(np.around(scipy.stats.mstats.gmean(rdata_single)*100.0, 2))+\
                ' max: '+str(np.around(np.amax(rdata_single)*100.0, 2))+\
                '@'+benchmarks[np.argmax(rdata_single)]+\
                ' min: '+str(np.around(np.amin(rdata_single)*100.0, 2))+\
                '@'+benchmarks[np.argmin(rdata_single)])
    np.savetxt('groupplot_'+name0+'.csv', rdata_bar, delimiter = ',')

    assert np.amin(data2[:, n_orig + n_starfarr]) > 0
    for i in range(n_orig + n_starfarr, n_m):
        rdata2 = 1 - data2[:, i]/data2[:, n_orig + n_starfarr] # relative to k0
        assert rdata2.shape[0] == n_b
        assert rdata2[-1] == 1 - data2[-1, i]/data2[-1, n_orig + n_starfarr]
        print(methods[i]+' '+figure_title[2]+\
            ' avg reduction: '+str(np.mean(rdata2))+\
            ' max reduction: '+str(np.amax(rdata2))+'@'+benchmarks[np.argmax(rdata2)]+\
            ' min reduction: '+str(np.amin(rdata2))+'@'+benchmarks[np.argmin(rdata2)])

    np.savetxt('groupplot_'+name0+'.csv', rdata_bar, delimiter = ',', fmt='%.4f')
    np.savetxt('groupplot_'+name1+'.csv', data_line, delimiter=',', fmt='%d')
    np.savetxt('groupplot_'+name2+'.csv', data2,     delimiter=',', fmt='%d')

    benchmarks_g = benchmarks + ['gmean']
    for i in range(len(benchmarks_g)):
        if i%3 == 1:
            benchmarks_g[i] = '\n'+ benchmarks_g[i]
        if i%3 == 2:
            benchmarks_g[i] = '\n\n'+ benchmarks_g[i]
    plot_metric([rdata_bar, data_line, data2], figure_title, benchmarks_g, methods_labels, 'groupplot_'+name0+'_'+name1+'_'+name2, n_orig, n_starfarr, n_starnews)
