# utility functions for plotting

import matplotlib.pyplot as plt


def plot_trans_mat(trans_mat, labelset, endchar='E'):
    """plots first order transition matrix
    labelset : set
        only compute transitions between labels in this set, ignore any other character in labels
    endchar : str
        character to denote end of a string, default is E.
        Used to discard this row since E by definition never transitions to anything else.
    """
    fig, ax = plt.subplots()
    tm_plot = ax.imshow(trans_mat)
    plt.colorbar(tm_plot)
    ax.set_xticks(range(len(labelset)))
    ax.set_xticklabels(labelset)
    ax.set_yticks(range(len(labelset)-1))
    ax.set_yticklabels([label for label in labelset if label != endchar])
