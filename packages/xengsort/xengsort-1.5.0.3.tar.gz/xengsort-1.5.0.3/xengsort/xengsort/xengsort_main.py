"""
xengsort_main.py
xengsort: xenograft indexing and classification
by Jens Zentgraf & Sven Rahmann, 2019--2023
"""

import argparse
from importlib import import_module  # dynamically import subcommand

from .._version import VERSION, DESCRIPTION
from ..parameters import set_threads
from ..lowlevel.debug import set_debugfunctions


def classify(p):
    #gf = p.add_mutually_exclusive_group(required=True)
    #gf.add_argument("--fasta", "-f", metavar="FASTA",
    #    help="FASTA file to classify")
    #gf.add_argument("--fastq", "-q", metavar="FASTQ",
    #    help="single or first paired-end FASTQ file to classify")
    p.add_argument("--fastq", "-q", metavar="FASTQ", required=True,
        help="single or first paired-end FASTQ file to classify")
    p.add_argument("--pairs", "-p", metavar="FASTQ",
        help="second paired-end FASTQ file (only together with --fastq)")
    p.add_argument("--index", metavar="ZARR", required=True,
        help="existing index (zarr folder)")
    p.add_argument("--out", "-o", "--prefix",
        dest="prefix", metavar="PREFIX",
        help="prefix for output files (directory and name prefix)")
    p.add_argument("--classification", "--mode", metavar="MODE",
        choices=("majority", "xengsort"), default="xengsort",
        help="classification mode ('majority', 'xengsort': default)")
    p.add_argument("--threads", "-T", "-j",
        metavar="INT", type=int, default=4,
        help="maximum number of worker threads for classification (default: 4)")
    p.add_argument("--quick", action="store_true",
        help="quick mode: Sample two k-mers per read. Immediately classify if they agree. If not, run standard classification.")
    gmode = p.add_mutually_exclusive_group(required=False)
    gmode.add_argument("--filter", action="store_true",
        help="only output the graft FASTQ file, not the other class FASTQ files")
    gmode.add_argument("--count", action="store_true",
        help="only count reads or read pairs for each class, do not output any FASTQ")
    p.add_argument("--prefetchlevel", "-P", metavar="INT", type=int, default=0, choices=(0,1,2),
        help="amount of prefetching: none (0, default); only second page (1); all pages (2)")
    p.add_argument("--chunksize", "-C", metavar="FLOAT_SIZE_MB",
        type=float, default=8.0,
        help="chunk size in MB [default: 8.0]; one chunk is allocated per thread.")
    p.add_argument("--chunkreads", "-R", metavar="INT", type=int,
        help="maximum number of reads per chunk per thread [SIZE_MB*(2**20) // 200]")


def index(p):
    p.add_argument("--index", metavar="INDEX_ZARR", required=True,
        help="name of the resulting index (.zarr output)")
    p.add_argument("--host", "-H", metavar="FASTA", nargs="+",
        help="reference FASTA file(s) for the host organism")
    p.add_argument("--graft", "-G", metavar="FASTA", nargs="+",
        help="reference FASTA file(s) for the graft organism")
    # TODO? support for a precomputed set of k-mers with values (dump)?

    p.add_argument("-n", "--nobjects", metavar="INT",
        type=int, required=True,
        help="number of k-mers to be stored in hash table (4_500_000_000 for mouse+human)")

    k_group = p.add_mutually_exclusive_group(required=False)
    k_group.add_argument('-k', '--kmersize', dest="mask", metavar="INT",
        type=int, default=27, help="k-mer size",)
    k_group.add_argument('--mask', metavar="MASK",
        help="gapped k-mer mask (quoted string like '#__##_##__#')")

    p.add_argument("--pagesize", "--bucketsize", "-p", "-b",
        metavar="INT", type=int, default=4,
        help="page size, i.e. number of elements on a page")
    p.add_argument("--fill",
        type=float, default=0.9, metavar="FLOAT",
        help="desired fill rate (< 1.0) of the hash table")
    p.add_argument("--subtables", type=int, metavar="INT",  # no default -> None!
        help="number of subtables used; subtables+1 threads are used")
    p.add_argument("--shortcutbits", "-S", metavar="INT",
        type=int, choices=(0,1,2), default=0,
        help="number of shortcut bits (0,1,2), default: 0")
    p.add_argument("--hashfunctions", "--functions", metavar="SPEC",
        help="hash functions: 'default', 'random', or 'func0:func1:func2:func3'")
    p.add_argument("--aligned", action="store_true",
        help="use power-of-two-bits-aligned pages (slightly faster, but larger)")
    p.add_argument("--nostatistics", "--nostats", action="store_true",
        help="do not compute or show index statistics at the end")
    p.add_argument("--weakthreads", "-W", metavar="INT", type=int,
        help="calculate weak kmers with the given number of threads")
    p.add_argument("--groupprefixlength", metavar="INT", type=int, default=1,
        help="calculate weak k-mers in groups with common prefix of this length [1]")
    p.add_argument("--maxwalk", metavar="INT", type=int, default=500,
        help="maximum length of random walk through hash table before failing [500]")
    p.add_argument("--maxfailures", metavar="INT", type=int, default=0,
        help="continue even after this many failures [default:0; forever:-1]")
    p.add_argument("--walkseed", type=int, metavar="INT", default=7,
        help="seed for random walks while inserting elements [7]")



##### main argument parser #############################

def get_argument_parser():
    """
    return an ArgumentParser object
    that describes the command line interface (CLI)
    of this application
    """
    p = argparse.ArgumentParser(
        description = DESCRIPTION,
        epilog = "(c) 2019-2023 by Algorithmic Bioinformatics, Saarland University. MIT License."
        )
    # global options
    p.add_argument("--version", action="version", version=VERSION,
        help="show version and exit")
    p.add_argument("--debug", "-D", action="count", default=0,
        help="output debugging information (repeat for more)")

    # add subcommands to parser
    subcommands = [
        ("index",
        "build index of two species' FASTA references (toplevel + cdna) for xenograft sorting",
        index,
        "xengsort_index", "main"),
        ("classify",
        "sort (or filter or count) FASTQ reads according to species of origin",
        classify,
        "xengsort_classify", "main"),
        ]
    sps = p.add_subparsers(
        description="The xengsort application supports the following commands. "
            "Run 'xengsort COMMAND --help' for detailed information on each command.",
        metavar="COMMAND", required=True, dest="subcommand")
    for (name, helptext, f_parser, module, f_main) in subcommands:
        if name.endswith('!'):
            name = name[:-1]
            chandler = 'resolve'
        else:
            chandler = 'error'
        sp = sps.add_parser(name, help=helptext,
            description=helptext, conflict_handler=chandler)
        sp.set_defaults(func=(module, f_main))
        f_parser(sp)
    return p


def main(args=None):
    p = get_argument_parser()
    pargs = p.parse_args() if args is None else p.parse_args(args)
    set_debugfunctions(debug=pargs.debug, timestamps=pargs.debug)
    set_threads(pargs, "threads")  # limit number of threads in numba/prange
    (module, f_main) = pargs.func
    m = import_module("."+module, __package__)
    mymain = getattr(m, f_main)
    mymain(pargs)
