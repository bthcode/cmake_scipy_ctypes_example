#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

def simple_scatter( ax, x_vals, y_vals, color_vals, size_vals, num_colors=8, num_sizes=8, size_min=0, size_max=50 ):

    # calculate a series of masks on color
    color_masks = []
    min_color_val = color_vals.min()
    max_color_val = color_vals.max()
    color_idxs = np.linspace(min_color_val, max_color_val, num_colors)
    for i, val in enumerate(color_idxs[1:]):
        mask = (color_vals > color_idxs[i-1]) & (color_vals <= color_idxs[i])
        color_masks.append(mask)

    # calculate a series of masks on size
    size_masks = []
    size_min_val = size_vals.min()
    size_max_val = size_vals.max()
    size_idxs = np.linspace(size_min_val, size_max_val, num_sizes)
    for i, val in enumerate(size_idxs[1:]):
        mask = (size_vals > size_idxs[i-1]) & (size_vals <= size_idxs[i])
        size_masks.append(mask)

    sizes = np.linspace(size_min, size_max, num_sizes)
    colors = iter(cm.rainbow(np.linspace(0,1,num_colors)))

    for idx, mask in enumerate(color_masks):
        c = next(colors)
        for idx2, mask2 in enumerate(size_masks):
            m = mask & mask2
            size = sizes[idx2]
            ax.plot(x_vals[m], y_vals[m], c=c, marker='.', linestyle='None',  markersize = size)

# end simple_scatter


if __name__=="__main__":
    n_points = 20000
    x_vals = np.arange(n_points)
    y_vals = np.random.random(n_points)
    color_inputs = np.random.random(n_points)
    size_inputs = np.random.random(n_points) 

    fig = plt.figure()
    ax = fig.add_subplot(111)
    simple_scatter( ax, x_vals, y_vals, y_vals, x_vals, num_colors=20, num_sizes=20, size_max=20, size_min=1)
    plt.show()

