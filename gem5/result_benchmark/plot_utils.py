import numpy as np
import matplotlib.pyplot as plt
import scipy.stats.mstats
import os

def save_csv_data(save_name, save_data, save_fmt = None):
    if save_name[-3:] == 'jpg' or save_name[-3:] == 'png':
        csv_name = save_name[:-3]+'csv'
    else:
        csv_name = save_name+'.csv'

    '''
    if np.amax(np.abs(save_data)) <= 1.0:
        save_fmt = '%0.3f'
    elif np.amax(np.abs(save_data)) <= 100.0:
        save_fmt = '%0.2f'
    else:
        save_fmt = '%0.1f'
    '''

    print('Save data to ', csv_name)
    if save_fmt is None:
        np.savetxt(csv_name, save_data, delimiter = ',')
    else:
        np.savetxt(csv_name, save_data, delimiter = ',', fmt = save_fmt)

def plot_metric_split(data, metric, benchmarks, methods, ylabel, save_name):
    assert len(data) == len(metric)
    n_b = data[0].shape[0]
    n_stack = len(data)
    cur_sum = np.zeros(data[0].shape)
    sums=[cur_sum]
    for i in range(len(data)):
        assert data[i].ndim == 1
        cur_sum = cur_sum + data[i]
        sums.append(cur_sum)

    #barwidth = 1.0/(n_m+2)
    fig, ax = plt.subplots(1, 1, figsize = (16,5.5))

    ax1 = ax
    x = np.arange(n_b)
    colorlst = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    #assert n_bar  == 3
    #assert n_line == 3
    #assert n2     == 3
    for i in range(n_stack):
        #ax1.bar(x+barwidth*(i-n_m/2), data_bar[:, i], width = barwidth,
        ax1.bar(x, data[i], bottom = sums[i],
                label = metric[i], color = colorlst[i])

    ax1.set_xlabel('Benchmarks', fontweight = 'bold', fontsize = 18)
    #ax1.set_xlim((-0.8, n_b-0.2))
    #ax1.set_ylim((0.8, 1.6))
    ax1.tick_params(labelright=True, labelbottom=True, labelleft=True,
            labelsize=15)
    ax1.grid(axis = 'y', linestyle = '--')
    ax1.set_ylabel(ylabel, fontweight = 'bold', fontsize = 18)

    ax1.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0),
          ncol=len(metric), fancybox=True, shadow=False, fontsize=13)
    ax1.set_xticks(x, benchmarks, fontsize = 15)
    #ax1.set_yticks(fontsize = 15)

    plt.show(block = False)
    plt.savefig(save_name, bbox_inches='tight')
    plt.close()
    print('Save figure to ', save_name)

    save_data = np.zeros((n_b, n_stack))
    for i in range(n_stack):
        save_data[:, i] = data[i]
    save_csv_data(save_name, save_data)

def readstats_single(metric_name, method, benchmarks):
    n_b = len(benchmarks)
    data = np.zeros((n_b))
    f_prefix = 'dir_checkpoint/greps/sht/'+metric_name+'_'
    f_name = f_prefix+method+'.grep'
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
            data[j] = float(line[1])
    return data

def print_mmm_1d(data, description, labels = None, print_decimal = 4, avg_alg = 'mean'):
    assert data.ndim == 1, data.shape
    n_d = data.shape[0]
    if labels == None:
        labels = ' '*n_d
    else:
        assert len(labels) == n_d, len(labels)

    if avg_alg == 'mean':
        avg = np.mean(data)
    elif avg_alg == 'gmean':
        avg = scipy.stats.mstats.gmean(data)
    else:
        print('Wrong string for computing average!')

    if print_decimal == 0:
        print(description+': \t',
            'mean: '+str(int(avg))+'\t',
            'min: ' +str(int(np.amin(data)))+'@'+labels[np.argmin(data)]+'\t',
            'max: ' +str(int(np.amax(data)))+'@'+labels[np.argmax(data)])
    else:
        assert print_decimal > 0, print_decimal
        print(description+': \t',
            'mean: '+str(np.around(avg, print_decimal))+'\t',
            'min: ' +str(np.around(np.amin(data), print_decimal))+'@'+labels[np.argmin(data)]+'\t',
            'max: ' +str(np.around(np.amax(data), print_decimal))+'@'+labels[np.argmax(data)])

def check_equal(data1, data2 = None, description = None, labels = None):
    assert data1.ndim == 1, data1.shape
    n_d = data1.shape[0]
    if description == None:
        description = 'No label'
    if data2 is None:
        data2 = np.zeros(data1.shape)
        description += ' compare with zeros'
    if labels == None:
        labels = ' '*n_d
    else:
        assert len(labels) == n_d, len(labels)
    assert data1.shape == data2.shape, str(data1.shape)+' '+str(data2.shape)
    idx = np.argmax(np.abs(data1, data2))
    assert np.array_equal(data1, data2), description+': '+str(data1[idx])+' vs '+\
        str(data2[idx])+' @'+str(idx)+' '+labels[idx]
