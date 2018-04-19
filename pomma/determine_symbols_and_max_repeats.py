from functools import reduce
from operator import iadd  # aka the += operator
from itertools import groupby


def determine_symbols_and_max_repeats(sequences):
    """determines unique set of symbols used in sequences, and maximum number
    of repeats of those symbols (consecutive repeats, not just repeats in the 
    sense of occurrences). Any symbol with a maximum number of repeats > 1 is
    considered a symbol that repeats. These repeating symbols will be fit with
    states that adapt.
    To make fitting easier, maps symbols to a set of consecutive integers
    from 0 to n where n is the number of symbols, 
    then applies that mapping to sequences.

    Parameters
    ----------
    sequences : list
     of lists. Representations of sequences of symbols.
     Lists can be of ints or of str (single characters).
     If str, will be converted to int. 

    Returns
    -------
    symbols_and_max_repeats: dict
        with following key, value pairs:
            symbols : set
                of ints, unique set of symbols used in sequences
            symbols_int_map: dict
                mapping from symbols to integers 0,1,2,...,n
                where n is the number of symbols
            seqs_mapped : list
                lList of lists of int. Result of "converting" sequences
                to ints by applying symbols_int_map to it.
            max_repeats : dict
                where each key is a symbol and the corresponding value is
                the maximum number of consecutive repeats of that symbol
                found in any of the sequences
            repeat_symbols : list
                of int, symbols with repeat strings with max_repeats > 1
    """
    if type(sequences) != list:
        raise TypeError('sequences should be a list, not {}'.format(type(sequences)))
    if not all([type(seq) == list for seq in sequences]):
        raise TypeError('sequences should be a list of lists')
    # "reduce(iadd, sequences)" concatenates sequences, a list of lists
    seqs_concat = reduce(iadd, sequences)
    # map unique set of symbols to consecutive integers starting from 0
    symbols = set(seqs_concat)
    symbols_int_map = dict(zip(symbols,
                               range(len(symbols))))
    # apply mapping to sequences
    seqs_mapped = []
    for seq in sequences:
        seq_mapped = [symbols_int_map[symbol]
                      for symbol in seq]
        seqs_mapped.append(seq_mapped)
    seqs_mapped = seqs_mapped

    # find maximum number of consecutive repeats for each symbol
    repeat_counts = []
    for seq_mapped in seqs_mapped:
        counts_this_seq = [(k, sum(1 for i in g)) for k, g in groupby(seq_mapped)]
        repeat_counts.extend(counts_this_seq)
    max_repeats = {}
    for symbol, symbol_int in symbols_int_map.items():
        all_counts_this_symbol = [tuple_count
                                  for tuple_symbol, tuple_count in repeat_counts
                                  if tuple_symbol == symbol_int]
        max_repeat = max(all_counts_this_symbol)
        max_repeats[symbol] = max_repeat
    repeat_symbols = [symbol
                      for symbol, max_repeat in max_repeats.items()
                      if max_repeat > 1]

    symbols_and_max_repeats = {
        'symbols': symbols,
        'seqs_mapped': seqs_mapped,
        'max_repeats': max_repeats,
        'repeat_symbols': repeat_symbols
    }
    return symbols_and_max_repeats
