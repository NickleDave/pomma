# class for fiting POMMA models to Bengalese finch song syntax
# adapted from Matlab code by Dezhe Jin

import numpy as np


class POMMAFitter:
    def __init__(self, **kwargs):
        """
        
        Parameters
        ----------
        prob_prune : float
            Transition probabilities less than prob_prune are pruned at the final step of fitting
            Default is 0.01
        frac_in_prune : float
            States 
            
        """
        prop_defaults = {
            'prob_prune': 0.01,
            'frac_in_prune': 0.01,
            'prob_small': 1e0**-3,
            'tolerance': 1e-3,
            'max_steps': 10000,
            'num_random_starts': 20,
            'fract_split': 0.5,
            'p_value': 0.95,
            'num_boot': 500,
            'm_compare': 30,
            'num_seq': 5000,
            'max_extra_states': 15,
            'start_symbol': 1000,
            'end_symbol': 1001,
        }

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

    def fit(sequences):
        symbols = set(sequences)
        num_symbols = len(symbols)
        symbols_int_map = dict(zip(symbols,
                                   range(num_symbols)))
        seqs_mapped = []
        for seq in sequences:
            seq_mapped = [symbols_int_map(symbol)
                          for symbol in seq]
            seqs_mapped.append(seq_mapped)

    def _prune():
        """prunes any transitions with probabilities less than prob_prune
        final step of fitting POMMA.

        prob_prune : float
            between 0 and 1.
            Default is 0.01

        """ 

