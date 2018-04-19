from pomma.pommafitter import POMMAfitter

# list of lists to test
LOL = [
    [1,1,2,3],
    [1, 1, 1, 1, 2, 3],
    [1, 1, 2, 3],
]


def test_determine_symbols_and_max_repeats():
    pf = POMMAfitter()
    pf._determine_symbols_and_max_repeats(sequences=LOL)
    assert pf.symbols == {1,2,3}
    assert pf.seqs_mapped == LOL
    assert pf.max_repeats == {1:4, 2:1, 3:1}
    assert pf.repeat_symbols == [1]