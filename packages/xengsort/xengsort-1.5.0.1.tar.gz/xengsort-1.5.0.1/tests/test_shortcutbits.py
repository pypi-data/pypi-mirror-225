import pytest
from importlib import import_module

from xengsort.hash_s3c_fbcbvb import build_hash
from xengsort.builders_subtables import parallel_build_from_fasta
from xengsort.kmers import compile_kmer_iterator
from xengsort.io.fastaio import fasta_reads


#get value set
vimport = "values.xenograft"
vmodule = import_module("xengsort."+vimport, __package__)
values = vmodule.initialize(3)  


# Build hash table
def build_ht(k, n, st, b, lb):
    h = build_hash(int(4**k), n, st, b,
            "random", 7, values.update,
            aligned=False, nfingerprints=-1,
            maxwalk=5000, shortcutbits=lb)

    (total, failed, walkstats) = parallel_build_from_fasta(
            ["tests/data/random_100k.fa"],
            k, h, values.get_value_from_name_host,
            rcmode="max", walkseed=7, maxfailures=0,
            )
    assert not failed, "Error in build_ht"
    print("Calculating shortcut bits")
    h.compute_shortcut_bits(h.hashtable)
    print("Done calculating shortcut bits")
    return h


def check_shortcutbits(h, st, b, k, lb):
    get_signature_at = h.private.get_signature_at
    get_value_at = h.private.get_value_at
    get_shortcutbits_at = h.private.get_shortcutbits_at
    is_slot_empty_at = h.private.is_slot_empty_at
    get_subkey_choice_from_page_signature = h.private.get_subkey_choice_from_page_signature
    (h1, h2, h3) = h.private.get_pf
    table = h.hashtable
    if lb == 0: return
    for s in range(st):
        for page in range(h.npages): # iterate over all pages
            for slot in range(b): # iterate over all slots
                if is_slot_empty_at(table, s, page, slot):
                    continue
                sig = get_signature_at(table, s, page, slot)
                subkey, choice = get_subkey_choice_from_page_signature(page, sig)
                if choice == 1: continue
                if choice == 2:
                    if get_shortcutbits_at(table, s, h1(subkey)[0]) & 1 != 1:
                        print(get_shortcutbits_at(table, s, h1(subkey)[0]), "1")
                        assert False, "Wrong shortcut bit"
                elif choice == 3:
                    if lb == 1:
                        if get_shortcutbits_at(table, s, h1(subkey)[0]) & 1 != 1:
                            print(get_shortcutbits_at(table, s, h1(subkey)[0]), "1")
                            assert False, "Wrong shortcut bit"
                        if get_shortcutbits_at(table, s, h2(subkey)[0]) & 1 != 1:
                            print(get_shortcutbits_at(table, s, h2(subkey)[0]), "1")
                            assert False, "Wrong shortcut bit"
                    else:
                        if get_shortcutbits_at(table, s, h1(subkey)[0]) & 2 != 2:
                            print(get_shortcutbits_at(table, s, h1(subkey)[0]), "2")
                            assert False, "Wrong shortcut bit"
                        if get_shortcutbits_at(table, s, h2(subkey)[0]) & 2 != 2:
                            print(get_shortcutbits_at(table, s, h2(subkey)[0]), "2")
                            assert False, "Wrong shortcut bit"

def check_get_value(h, b, k, lb):
    k, kmers = compile_kmer_iterator(k, "max")
    h.get_value
    for seq in fasta_reads("tests/data/random_100k.fa", True):
        for kmer in kmers(seq, 0, len(seq)):
            value = get_value(h.hashtable, kmer)
            assert value >= 0, f"Value {value}"


@pytest.mark.parametrize("st", [3])  # subtables
@pytest.mark.parametrize("b", [4])  # bucket size
@pytest.mark.parametrize("k", [23]) # k-mer size
@pytest.mark.parametrize("scb", [0, 1, 2])  # number of shortcut bits
def test_shortcutbits(st, b, k, scb):
    h = build_ht(k, 110_000, st, b, scb)
    check_shortcutbits(h, st, b, k, scb)
    check_get_value(h, b, k, scb)
