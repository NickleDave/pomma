# module to calculate descriptive statistics of label sequences

import re
from collections import defaultdict

import numpy as np


def get_repeat_distribs(sequences, labels):
    """gets distribution of repeats from a list of sequences,
    for each label in labelset

    Parameters
    ----------
    sequences : list
        of str
    labels : str
        each label for which repeat distribution should be computed
        e.g. 'abcdefghjki' will return distributions for a, b, ..., i

    Returns
    -------
    distribs : dict
        where keys are labels and values are:
            unique_repeats : ndarray
                unique strings of repeats that occur,
                e.g., array(['a', 'aa', 'aaaa', 'aaaaaa'])
            counts : ndarray
                counts for each unique string of repeats in unique_repeats
                e.g., array([2000, 1000, 59, 4])
    """
    # can just concatenate into one string, as long as S and E are at beginning and end
    seqs_concat = ''.join(sequences)
    distribs = {}
    for label in labels:
        pattern = '' + label + '{2,}'
        seq_search = re.findall(pattern, seqs_concat)
        unique_repeats, counts = np.unique(seq_search, return_counts=True)
        if unique_repeats.shape[0] == 1 and unique_repeats[0] == label:
            # i.e., if not actually a repeating syllable
            continue
        else:
            distribs[label] = {'unique_repeats': unique_repeats,
                               'counts': counts}
    return distribs


def switch_key_val(i):
    return i[1], i[0]


def get_ngram_distribs(sequences, labelset, n_range=range(2, 8),
                       startchar='S', endchar='E', real_ngram_distribs=None):
    """get distributions of ngrams

    Parameters
    ----------
    sequences : list
        of str, either labels from actual song or generated by model
    labelset : str
        set of labels used, including characters that indicate
        start and end of song bouts.
    startchar : str
        character that indicates start of bout, default is 'S'. Needed
        to ensure these characters aren't counted as part of n-grams.
    endchar : str
        character that indicates end of bout, default is 'E'.  Needed
        to ensure these characters aren't counted as part of n-grams.
    real_ngram_distribs : list
        of tuples, output from running this function on the actual data.
        If provided, the function counts only the ngrams in sequences that
        occur in real_ngram_distribs.
        If None, the function counts all ngrams in sequences.

    Returns
    -------
    distribs : dict
        where the key is the value of n for the ngram
        and the value is a dict with the following keys:
            counts : list
                list of two-element tuples, where first element is ngram
                and the second is the number of occurences of that ngram
            distrib : ndarray
                counts, normalized by total number of ngrams of size n
    """
    labelset = set(labelset)
    labelset -= {startchar, }
    labelset -= {endchar, }

    distribs = {}
    for n in n_range:

        if real_ngram_distribs:
            ngrams_to_find = [ngram
                              for ngram, count in real_ngram_distribs[n]['counts']]
            ngram_dict = dict(zip(ngrams_to_find,
                                  [0] * len(ngrams_to_find)))
        else:
            ngrams_to_find = None
            ngram_dict = defaultdict(int)

        for sequence in sequences:
            for ind in range(len(sequence) - (n - 1)):
                ngram = sequence[ind:ind + n]
                if ngrams_to_find:
                    # used when calculating ngram distribs for
                    # sequences generated by model
                    # and already have ngrams from data
                    if ngram in ngrams_to_find:
                        ngram_dict[ngram] += 1
                else:
                    # if ngrams_to_find is None, compute distribs
                    # for all ngrams found, as long as 
                    # all characters in ngram are in labelset
                    if set(ngram) < labelset:
                        # if all chars in ngram are in labelset
                        ngram_dict[ngram] += 1

        counts = sorted(ngram_dict.items(), key=switch_key_val, reverse=True)
        counts_list = [tupl[1] for tupl in counts]
        distrib = np.asarray(counts_list) / sum(counts_list)

        distribs[n] = {'counts': counts,
                       'distrib': distrib}
    return distribs


def get_step_prob(sequences, labelset, startchar='S', endchar='E'):
    """get probability of a given syllable occurring at each step in a sequence
    Parameters
    ----------
    sequences : list
        of str, either labels from actual song or generated by model
    labelset : str
        set of labels used, including characters that indicate
        start and end of song bouts.
    startchar : str
        character that indicates start of bout, default is 'S'. Needed
        to ensure these characters aren't counted as part of n-grams.
    endchar : str
        character that indicates end of bout, default is 'E'.  Needed
        to ensure these characters aren't counted as part of n-grams.    

    Returns
    -------
    step_probs : dict
        where each key is a label from labelset
        and the value is a vector with length equal to the longest sequences
            and each element is the probability of the label occuring at that
            step across seoquences
    """
    labelset = set(labelset) - set(startchar)
    seq_lengths = [len(seq) for seq in sequences]
    max_length = np.max(seq_lengths)
    step_probs = {}
    for label in labelset:
        step_probs[label] = np.zeros((max_length,))

    for sequence in sequences:
        for ind, label in enumerate(sequence):
            if label in step_probs:
                step_probs[label][ind] += 1

    for label in step_probs.keys():
        step_probs[label] = step_probs[label] / step_probs[label].sum()

    return step_probs