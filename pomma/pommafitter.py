# class for fitting POMMA models to Bengalese finch song syntax
# adapted from Matlab code by Dezhe Jin

import numpy as np

from .determine_symbols_and_max_repeats import determine_symbols_and_max_repeats

class POMMAfitter:
    def __init__(self, **kwargs):
        """
        Parameters
        ----------
        prob_prune : float
            Transition probabilities less than prob_prune are pruned at the final step of fitting.
            Default is 0.01.
        frac_in_prune : float
            States with fraction of visits less than frac_in_prune are pruned at final step of fitting.
            Default is 0.01.
        prob_small : float
            Any probability less than prob_small is disregarded when deriving model states.
            Default is 0.001.
        tolerance : float
            Tolerance for the change of transition probabilities during the Expectation Maximization (E-M).
            Default is 0.001.
        max_steps : int
            Maximum number of steps during E-M. Default is 10,000.
        num_random_starts : int
            Number of random starts to derive the best model. Default is 20.
        percent_split : float
            Percent of samples to put in one group when spliting into two groups for bootstrap statistics.
            Other group will contain ((1 - percent_split) * total number of samples).
            Default is 0.5.
        p_value : float 
            p-value used to determine upper bounds of errors based based on the distribution 
            created by the splitting.
            Default is 0.95.
        num_boot : int
            Number of times sequences are split and statistic measured when estimating statistics through
            bootstrap.
            Default is 500.
        m_compare : int
            Number of steps to compare the step probabilities of the symbols.
        num_seq : int
            Number of sequences to generate.
        max_extra_states : int
            Maximum number of states to allow for each symbol.
            Default is 15.
        start_symbol : int
            Numerical symbol for the start state. Default is 1000.
        end_symbol : int
            Numerical symbol for the end state. Default is 1001.
        """
        prop_defaults = {
            'prob_prune': 0.01,
            'frac_in_prune': 0.01,
            'prob_small': 1e-3,
            'tolerance': 1e-3,
            'max_steps': 10000,
            'num_random_starts': 20,
            'percent_split': 0.5,
            'p_value': 0.95,
            'num_boot': 500,
            'm_compare': 30,
            'num_seq': 5000,
            'max_extra_states': 15,
            'start_symbol': 1000,
            'end_symbol': 1001,
        }

        props_for_other_methods = [
            'symbols',
            'symbols_int_map'
            'seqs_mapped',
            'repeat_syms',
            'max_repeats',
            'res_diff',
            'initial_state_model'
        ]

        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

        for prop_for_other_methods in props_for_other_methods:
            setattr(self, prop_for_other_methods, None)

    def _determine_symbols_and_max_repeats(self, sequences):
        symbols_and_max_repeats = determine_symbols_and_max_repeats(sequences)
        for key, val in symbols_and_max_repeats.items():
            setattr(self, key, val)

    def _prune(self):
        """prunes any transitions with probabilities less than prob_prune
        final step of fitting POMMA.
        """ 

    def fit(self, sequences):
        """

        Parameters
        ----------
        sequences : list
            List of lists, of type int or str.
            Sequences of ints where each int is a Symbol used to label a syllable in birdsong.

        Returns
        -------
        None
        """

        self._determine_symbols_and_max_repeats(sequences)


