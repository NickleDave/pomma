from pomma.determine_symbols_and_max_repeats import determine_symbols_and_max_repeats

# list of lists to test
LOL = [
    [1, 1, 2, 3],
    [1, 1, 1, 1, 2, 3],
    [1, 1, 2, 3],
]

LOL_mapped = [
    [0, 0, 1, 2],
    [0, 0, 0, 0, 1, 2],
    [0, 0, 1, 2],
]


def test_determine_symbols_and_max_repeats():
    symbols_and_max_repeats = determine_symbols_and_max_repeats(sequences=LOL)
    assert symbols_and_max_repeats['symbols'] == {1,2,3}
    assert symbols_and_max_repeats['seqs_mapped'] == LOL_mapped
    assert symbols_and_max_repeats['max_repeats'] == {1:4, 2:1, 3:1}
    assert symbols_and_max_repeats['repeat_symbols'] == [1]