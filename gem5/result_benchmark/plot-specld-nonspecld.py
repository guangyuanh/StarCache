import numpy as np
import matplotlib.pyplot as plt
import scipy.stats.mstats
import os
from plot_utils import plot_metric_split

if __name__ == '__main__':
    name = ['starldcommitted_500M', 'starldcommittedspec_500M',
            'starldcommittednonspec_500M', 'starldsqinvnonspec_500M',
            'starldsqinvnotneeded_500M', 'starldsqinvsent_500M', 'numsqinv_500M']
    figure_label = ['CommitNonSpec', 'CommitSpec', 'SquashSpec w/o SFill-Inv', 'SquashSpec w/ SFill-Inv']
    methods = [
             'starfarr'
            ]
    assert len(methods) == 1, 'Currently only support plotting for one config'
    benchmarks = ['GemsFDTD', 'astar', 'bwaves', 'bzip2',
        'cactusADM', 'calculix', 'gamess', 'gcc', 'gobmk',
        'gromacs', 'h264ref', 'hmmer', 'lbm',
        'leslie3d', 'libquantum', 'mcf', 'milc', 'namd',
        'omnetpp', 'povray', 'sjeng', 'sphinx3', 'wrf',
        'zeusmp']
    n_m = len(methods)
    n_b = len(benchmarks)
    n_d = len(name)
    print('n_m: ', n_m, 'n_b: ', n_b, 'n_data: ', n_d)

    def readstats(metric_name):
        data = np.zeros((n_b, n_m))
        f_prefix = 'dir_checkpoint/greps/starcache/'+metric_name+'_'
        for i in range(n_m):
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
                    data[j, i] = float(line[1])
        return data

    data = []
    for i in range(n_d):
        data.append(np.zeros(n_b))
        data[i][:] = readstats(name[i])[:, 0]
    assert np.array_equal(data[0], data[1]+data[2])

    # non-spec ld should not be squashed
    assert np.amax(data[3]) == 0

    data_sqldnosqinv = data[4]+data[5]-data[6]
    data_total = data[0]+data[3]+data[4]+data[5]
    data_split = [data[2]*1.0         /data_total,
                  data[1]*1.0         /data_total,
                  data_sqldnosqinv*1.0/data_total,
                  data[6]*1.0         /data_total]

    print('Split of all loads: ')
    total_split = 0.0
    for i in range(len(data_split)):
        avg_split = np.mean(data_split[i])
        print(figure_label[i]+': '+str(avg_split*100.0))
        total_split += avg_split
    assert total_split == 1.0, 'total_split: '+str(total_split)

    benchmarks_g = benchmarks
    for i in range(len(benchmarks_g)):
        if i%3 == 1:
            benchmarks_g[i] = '\n'+ benchmarks_g[i]
        if i%3 == 2:
            benchmarks_g[i] = '\n\n'+ benchmarks_g[i]

    plot_metric_split(data_split, figure_label, benchmarks_g, methods, 'Number of Loads', 'specld_totalsplit_'+methods[0]+'.jpg')
