# code to create first-order Markov models of song syntax and generate output from models

import os
from glob import glob
import re
from collections import defaultdict

import numpy as np


def make_trans_mat(labels, labelset, endchar='E'):
    """compute first-order Markov transition matrix from labels (as returned by load_labels)

    Parameters
    ----------
    labels : list
        of str
    labelset : set
        only compute transitions between labels in this set, ignore any other character in labels
    endchar : str
        character to denote end of a string, default is E.
        Used to discard this row since E by definition never transitions to anything else.

    Returns
    -------
    trans_mat : ndarray
        Matrix of m rows of i elements x n rows of j elements,
        where each element i,j is the probability
        of transitioning from labelset[i] to labelset[j]
    """

    size = len(labelset)

    trans = defaultdict(float)
    for label in labels:
        for ind in range(len(label) - 1):
            if label[ind] in labelset and label[ind + 1] in labelset:
                trans[label[ind], label[ind + 1]] += 1

    trans_mat = np.zeros((size, size))
    for i, i_char in enumerate(labelset):
        for j, j_char in enumerate(labelset):
            if (i_char, j_char) in trans:
                trans_mat[i, j] = trans[(i_char, j_char)]

    # remove end row since there's no transitions from end to anything else
    end_row_ind = labelset.index(endchar)
    trans_mat = np.delete(trans_mat, (end_row_ind,), 0)

    # divide each row by sum of row.
    # add np.newaxis to get broadcasting to work.
    trans_mat = trans_mat / trans_mat.sum(axis=1)[:, np.newaxis]

    return trans_mat


def generate_sequences(trans_mat, labelset, num=10000, startchar='S', endchar='E',
                       model='Markov'):
    """uses transition matrix to generate sequences
    """

    # get index of end state so we know when we're in it
    endchar_ind = labelset.index(endchar)
    sequences = []

    if model == 'Markov':
        # convert trans_mat into a list of dicts
        # because each row can have a different number of non-zero probabilities.
        # Seems more efficient to not compute which probabilities we need every time
        # we return to the same row.
        trans_mat_list = []
        for row in trans_mat:
            stateprob_dict = {}
            stateprob_dict['states'] = np.where(row)[0]
            stateprob_dict['probs'] = np.cumsum(row[stateprob_dict['states']])
            trans_mat_list.append(stateprob_dict)

        startchar_ind = labelset.index(startchar)

        for iter in range(num):
            sequence = ''
            # label_ind means "index in labelset"
            # while state_ind means "index in state from trans_mat_list"
            label_ind = startchar_ind
            while True:
                # could just use np.random.choice to pick next state
                # but trying to reproduce Jin Khozvenikov as closely as possible
                r = np.random.uniform()
                probs = trans_mat_list[label_ind]['probs']
                state_ind = np.where(r < probs)[0][0]
                states = trans_mat_list[label_ind]['states']
                label_ind = states[state_ind]
                if label_ind == endchar_ind:
                    break
                else:
                    sequence += labelset[label_ind]

            sequences.append(sequence)

    return sequences