import numpy as np
from xengsort.dnaencode import  quick_dna_to_2bits, twobits_to_dna_inplace

def test_dna_to_2bits_to_dna():
    dnastr = np.copy(np.frombuffer(b"ACGTacgtNuU", np.uint8))
    encoded = np.array([0, 1, 2, 3, 0, 1, 2, 3, 4, 3, 3])
    decoded = np.copy(np.frombuffer(b"ACGTACGTNTT", np.uint8))

    #check if AaCcGgTtUuN is correctly encoded and decoded
    quick_dna_to_2bits(dnastr)
    assert (dnastr == encoded).all()
    twobits_to_dna_inplace(dnastr)
    assert (dnastr == decoded).all()

def test_all_chars_to_2bit_to_dna():
    allchars = np.copy(np.frombuffer(b"BbDdEeFfHhIiJjKkLlMmNnOoPpQqRrSsVvWwXxYyZz", np.uint8))
    # check if all other letters are correctly encoded and decoded as N
    quick_dna_to_2bits(allchars)
    assert (allchars == 4).all()
    twobits_to_dna_inplace(allchars)
    assert (allchars == 78).all()