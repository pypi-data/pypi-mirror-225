"""
xengsort_index:
Build index for host and graft reference genomes.
by Jens Zentgraf & Sven Rahmann, 2019--2023
"""

import sys
import os
from importlib import import_module

import numpy as np

from ..mathutils import print_histogram
from ..srhash import get_npages
from ..builders_subtables import parallel_build_from_fasta
from ..hashio import save_hash
from ..zarrutils import load_from_zgroup
from ..parameters import get_valueset_parameters, parse_parameters
from ..lowlevel import debug  # the global debugging functions
from .xengsort_weak import calculate_weak_set

DEFAULT_HASHTYPE = "s3c_fbcbvb"


# build index #########################################


def build_index_precomputed(args):
    """build index from precomputed kmers/values"""
    data = load_from_zgroup(args.precomputed, "data")
    codes = data["kmercodes"]
    choices = data["choices"]  # is this really necessary?
    valuearray = data["values"]

    valueinfo = load_from_zgroup(args.precomputed, "valueinfo")
    valueset = valueinfo['valueset'].decode('ASCII')
    valuestr = valueset  # needed as return value
    debugprint0(f"- Importing value set '{valueset}'...")
    valueset = valueset.split()
    if valueset[0].startswith('xengsort.'):
        valueset[0] = valueset[0][len('xengsort.'):]
    vmodule = import_module(".."+valueset[0], __package__)
    values = vmodule.initialize(*(valueset[1:]))
    update_value = values.update

    info = load_from_zgroup(args.precomputed, "info")["info"]
    hashtype = info['hashtype'].decode("ASCII")
    aligned = bool(info['aligned'])
    universe = int(info['universe'])
    n = int(info['n'])
    k = int(info['k'])
    nkmers = int(info['kmers'])
    rcmode = info['rcmode']
    npages = int(info['npages'])
    pagesize = int(info['pagesize'])
    nfingerprints = int(info['nfingerprints'])
    nvalues = int(info['nvalues'])
    assert nvalues == values.NVALUES, f"Error: inconsistent nvalues (info: {nvalues}; valueset: {values.NVALUES})"
    maxwalk = int(info['maxwalk'])
    hashfuncs = info['hashfuncs'].decode("ASCII")
    debugprint1(f"- Hash functions: {hashfuncs}")
    debugprint1(f"- Building hash table of type '{hashtype}'...")
    hashmodule = "hash_" + hashtype
    m = import_module(".."+hashmodule, __package__)
    h = m.build_hash(universe, n, pagesize,
        hashfuncs, nvalues, update_value,
        aligned=aligned, nfingerprints=nfingerprints,
        maxwalk=maxwalk, lbits=args.shortcutbits)
    (total, failed, walkstats) = build_from_dump(h, k, nkmers, codes, choices, valuearray)
    return (h, total, failed, walkstats, valuestr, k, rcmode)


def build_index_fasta(args):
    # obtain the parameters
    subtables = args.subtables
    if subtables is None:
        subtables = max(min(os.cpu_count() - 3, 9), 1)
    subtables = max(subtables - (1 - subtables % 2), 1)
    valueset = ['xenograft', '3']
    P = get_valueset_parameters(valueset, mask=args.mask,
        minimizersize=None, rcmode="max")
    (values, valuestr, rcmode, mask, parameters) = P
    k, tmask = mask.k, mask.tuple
    if not isinstance(k, int):
        debugprint0(f"- Error: k-mer size k not given; k={k}")
        sys.exit(1)
    debugprint1(f"- Imported value set '{valuestr}'.")
    debugprint2(f"- Dataset parameters: {parameters}")
    parameters = parse_parameters(parameters, args)
    debugprint2(f"- Updated parameters: {parameters}")
    (nobjects, hashtype, aligned, hashfuncs, pagesize, nfingerprints, fill) = parameters

    # create the hash table
    if hashtype == "default":
        hashtype = DEFAULT_HASHTYPE

    debugprint2(f"- Using hash type {hashtype}")
    hashmodule = import_module("..hash_" + hashtype, __package__)
    build_hash = hashmodule.build_hash
    universe = int(4**k)
    nvalues = values.NVALUES
    value_update = values.update
    n = get_npages(nobjects, pagesize, fill) * pagesize
    debugprint1(f"- Allocating hash table for {n} objects, functions '{hashfuncs}'...")
    h = build_hash(universe, n, subtables, pagesize,
        hashfuncs, nvalues, value_update,
        aligned=aligned, nfingerprints=nfingerprints,
        maxwalk=args.maxwalk, shortcutbits=args.shortcutbits)
    debugprint0(f"- Memory for hash table: {h.mem_bytes/(2**20):.3f} MB")
    debugprint1(f"- Info:  rcmode={rcmode}, walkseed={args.walkseed}")
    debugprint1(f'- Number of threads for computing weak k-mers: {args.weakthreads}')

    # fill the hash table; get some functions
    calc_shortcutbits = h.compute_shortcut_bits
    build = parallel_build_from_fasta
    # store all k-mers from host genome
    value_from_name = values.get_value_from_name_host
    (total_host, failed_host, walkstats_host) = build(
        args.host, tmask, h, value_from_name,
        rcmode=rcmode, walkseed=args.walkseed, maxfailures=args.maxfailures)
    if failed_host:
        return (h, total_host, failed_host, walkstats_host, valuestr, mask, rcmode)

    # store all k-mers from graft genome
    value_from_name = values.get_value_from_name_graft
    (total_graft, failed_graft, walkstats_graft) = build(
        args.graft, tmask, h, value_from_name,
        rcmode=rcmode, walkseed=args.walkseed, maxfailures=args.maxfailures)
    if failed_graft:
        return (h, total_graft, failed_graft, walkstats_graft, valuestr, mask, rcmode)

    # calculate shortcut bits
    if args.shortcutbits > 0:
        startshort = timestamp0(msg=f'- Calculating shortcut bits ({args.shortcutbits})...')
        calc_shortcutbits(h.hashtable)
        timestamp0(msg='- Done calculating shortcut bits.')
        timestamp0(startshort, msg="- Time for calculating shortcut bits")

    # calculate weak k-mers
    # the function does its own timestamp/debug output.
    time_start_weak = timestamp0(msg="\n- Computing weak k-mers...")
    nextchars = 3  # TODO:? parameterize via args?
    calculate_weak_set(
        h, k, args.groupprefixlength, nextchars,
        rcmode=rcmode, threads=args.weakthreads)
    timestamp0(time_start_weak, msg=f"- Total time for weak k-mers")

    total = total_host + total_graft
    failed = failed_host + failed_graft
    walkstats = walkstats_host + walkstats_graft
    return (h, total, failed, walkstats, valuestr, mask, rcmode)


# main #########################################

def main(args):
    """main method for indexing"""

    global debugprint0, debugprint1, debugprint2
    global timestamp0, timestamp1, timestamp2
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    timestamp0, timestamp1, timestamp2 = debug.timestamp

    starttime = timestamp0(msg="\n# Xengsort index")
    debugprint0("\n- (c) Algorithmic Bioinformatics, Saarland University")
    debugprint0("- (c) Sven Rahmann, Jens Zentgraf")
    debugprint0("- Licensed under the MIT License")

    (h, total, failed, walkstats, valueset, mask, rcmode) = build_index_fasta(args)
    ##k, tmask = mask.k, mask.tuple

    debugprint0()
    if failed == 0:
        timestamp0(msg=f"- SUCCESS, processed {total} k-mers; writing '{args.index}'.")
        save_hash(args.index, h, valueset,
            additional=dict(mask=mask, walkseed=args.walkseed, rcmode=rcmode))
        failed = False
    else:
        timestamp0(msg=f"- FAILED for {failed}/{total} processed k-mers. NOT WRITING '{args.index}'.")

    show_statistics = not args.nostatistics
    if show_statistics:
        timestamp1(msg="- Collecting statistics...")
        debugprint0()
        valuehist, fillhist, choicehist, shortcuthist = h.get_statistics(h.hashtable)
        print_histogram(np.sum(valuehist, axis=0), title="Value statistics", shorttitle="values", fractions="%")
        print_histogram(np.sum(fillhist, axis=0), title="Page fill statistics", shorttitle="fill", fractions="%", average=True, nonzerofrac=True)
        print_histogram(np.sum(choicehist, axis=0), title="Choice statistics", shorttitle="choice", fractions="%+", average="+")

    debugprint0("## Running time statistics\n")
    timestamp0(starttime, msg="- Running time in seconds")
    timestamp0(starttime, msg="- Running time in minutes", minutes=True)
    timestamp0(msg="- Done.")
    if failed:
        sys.exit(1)
