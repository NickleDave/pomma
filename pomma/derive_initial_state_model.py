import logging


def derive_initial_state_model(max_repeats,
                               num_symbols,
                               max_extra_states=15,
                               start_symbol=1000,
                               end_symbol=1001,
                               num_random_starts=20
                               ):
    """derives initial state model using Expectation-Maximization (E-M) algorithm

    Parameters
    ----------
    max_extra_states : int
        Maximum number of states to allow for each symbol.
        Default is 15.
    start_symbol : int
        Numerical symbol for the start state. Default is 1000.
    end_symbol : int
        Numerical symbol for the end state. Default is 1001.
    max_repeats : dict
        where each key is a symbol and the corresponding value is
        the maximum number of consecutive repeats of that symbol
        found in any of the sequences
    num_symbols : int
        number of unique symbols, i.e., len(symbols)
    num_random_starts : int
        Number of random starts to derive the best model. Default is 20.    
    
    Returns
    -------

    """
    for num_extra_states in range(1, max_extra_states+1):
        logging.info(f'Trying model with {num_extra_states} extra_states.')

        state_symbols = [start_symbol, end_symbol]
        max_repeat_nums = [0, 0]
        for symbol in range(0,num_symbols):
            number_states = 1 + num_extra_states
            state_symbols.extend([symbol] * number_states)
            max_repeat_nums.extend([max_repeats[symbol]] * number_states)
        
        