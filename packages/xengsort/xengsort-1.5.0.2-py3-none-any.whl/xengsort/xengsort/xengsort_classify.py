"""
xengsort_classify:
Xenograft classification
by Jens Zentgraf & Sven Rahmann, 2019--2023
"""

import io
import datetime
import os.path
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
from numba import njit, uint32, uint64

from ..hashio import load_hash
from ..kmers import compile_kmer_processor
from ..io.fastqio import fastq_chunks, fastq_chunks_paired
from ..io.fastaio import fasta_reads
from ..dnaencode import (
    quick_dna_to_2bits,
    twobits_to_dna_inplace,
    compile_twobit_to_codes,
    twobits_to_dna_inplace)
from ..lowlevel import debug



def compile_classify_read(tmask, rcmode, h, buckets):
    # tmask: mask in tuple form
    get_value = h.get_value
    get_pf1, get_pf2, get_pf3 = h.private.get_pf
    prefetch = h.private.prefetch_page
    get_subtable_subkey = h.private.get_subtable_subkey_from_key
    get_value_from_subtable_subkey = h.private.get_value_from_st_sk

    @njit(nogil=True,
        locals=dict(code=uint64, subkey=uint64, subtable=uint64, value=uint64))
    def count_values_subtables(ht, code, counts):
        subtable, subkey = get_subtable_subkey(code)
        if buckets == 1:
            prefetch(ht, subtable, get_pf2(subkey)[0])
        if buckets == 2:
            prefetch(ht, subtable, get_pf2(subkey)[0])
            prefetch(ht, subtable, get_pf3(subkey)[0])
        value = get_value_from_subtable_subkey(ht, subtable, subkey)  # value is 0 if code is not a key in the hash table
        counts[value] += 1
        return False  # we never fail!

    # because the supplied function 'count_values' has ONE extra parameter (counts),
    # the generated function process_kmers also gets ONE extra parameter (counts)!
    k, process_kmers = compile_kmer_processor(tmask, count_values_subtables, rcmode=rcmode)

    @njit(nogil=True)
    def classify_read(ht, seq, counts):
        process_kmers(ht, seq, 0, len(seq), counts)

    return classify_read


@njit(nogil=True)
def classify_majority(counts):
    # TODO: factor 99 ? ok for short reads
    # TODO: long term -> remove majority classification
    if counts[1] > 0:
        if counts[2] == 0:  # (no graft)
            return 0  # host
        # both counts[1] > 0 and counts[2] > 0
        if (counts[1] + counts[5]) > (counts[2] + counts[6])*99: # ambiguous host
            return 0
        if (counts[2] + counts[6]) > (counts[1] + counts[5])*99: # ambiguous graft
            return 1
        return 2
    # counts[1] == 0 (no host)
    if counts[2] > 0:
        return 1  # graft
    # no host, no graft
    if np.sum(counts[3:]) > counts[0]:
        return 3  # both
    return 4  # neither


@njit(nogil=True,  locals=dict(
    gscore=uint32, hscore=uint32, nkmers=uint32))
def classify_xengsort(counts):
    # counts = [neither, host, graft, both, NA, weakhost, weakgraft, both]
    # returns: 0=host, 1=graft, 2=ambiguous, 3=both, 4=neither.
    nkmers = 0
    for i in counts:
        nkmers += i  # apparently faster than np.sum(), re-check in 2024
    if nkmers == 0:
        return 2  # no k-mers -> ambiguous
    nothing = uint32(0)
    few = uint32(6)
    insubstantial = max(uint32(nkmers // 20), 1)
    Ag = uint32(3)
    Ah = uint32(3)
    Mh = uint32(max(uint32(nkmers // 4), 3))
    Mg = uint32(max(uint32(nkmers // 4), 3))
    Mb = uint32(max(uint32(nkmers // 5), 3))
    Mn = uint32(max(uint32((nkmers * 3) // 4 + 1),3))

    hscore = counts[1] + counts[5] // 2
    gscore = counts[2] + counts[6] // 2

    # no host
    if counts[1] + counts[5] == nothing: # no host
        if gscore >= Ag:
            return 1  # graft
        if counts[3] + counts[7] >= Mb: # both
            return 3  # both
        if counts[0] >= Mn: # neither (was: > nkmers*3 // 4)
            return 4  # neither
    # host, but no graft
    elif counts[2] + counts[6] == nothing: # no graft
        if hscore >= Ah:
            return 0  # host
        if counts[3] + counts[7] >= Mb: # both
            return 3  # both
        if counts[0] >= Mn: # neither
            return 4  # neither

    # some real graft, few weak host, no real host:
    if counts[2] >= few and counts[5] <= few and counts[1] == nothing:
        return 1  # graft
    # some real host, few weak graft, no real graft:
    if counts[1] >= few and counts[6] <= few and counts[2] == nothing:
        return 0  # host

    # substantial graft, insubstantial real host, a little weak host compared to graft:
    if counts[2] + counts[6] >= Mg and counts[1] <= insubstantial and counts[5] < gscore:
        return 1  # graft
    # substantial host, insubstantial real graft, a little weak graft compared to host:
    if counts[1] + counts[5] >= Mh and counts[2] <= insubstantial and counts[6] < hscore:
        return 0  # host
    if counts[3] + counts[7] >= Mb and gscore <= insubstantial and hscore <= insubstantial: # both
        return 3  # both
    if counts[0] >= Mn:
        return 4  # neither
    return 2  # ambiguous



def compile_classify_read_from_fastq(
        mode, tmask, rcmode, bits, path, h, threads, pairs,
        bufsize=2**23, chunkreads=(2**23)//200, quick=False,
        filt=False, count=False, prefetchlevel=0):
    # tmask: mask in tuple form (works for contiguous and gapped k-mers)

    if mode == "majority":
        debugprint0("- Using majority classification mode (naive)")
        classify = classify_majority
    elif mode == "xengsort":
        debugprint0("- Using xengsort classification mode (recommended)")
        classify = classify_xengsort
    else:
        raise ValueError(f"Unknown mode '{mode}'")

    classify_read = compile_classify_read(tmask, rcmode, h, prefetchlevel)
    _, twobit_to_code = compile_twobit_to_codes(tmask, rcmode)
    get_value = h.get_value
    k, w = len(tmask), tmask[-1] + 1

    @njit(nogil=True, locals=dict(
        third_kmer=uint64, third=uint64,
        thirdlast_kmer=uint64, thirdlast=uint64))
    def get_classification(ht, sq, kcount):
        quick_dna_to_2bits(sq)
        if quick:
            # get 2 k-mers (3rd and 3rd-last)
            third_kmer = twobit_to_code(sq, 2)
            thirdlast_kmer = twobit_to_code(sq, len(sq)-w-2)
            # look up values of both k-mers, ignore weak status (good thing?!)
            third = get_value(ht, third_kmer) & uint64(3)
            thirdlast = get_value(ht, thirdlast_kmer) & uint64(3)
            if third == thirdlast and third != 3 and third != 0:
                return (third - 1)  # 2 -> 1,  1 -> 0
        kcount[:] = 0
        classify_read(ht, sq, kcount)
        return classify(kcount)

    @njit(nogil=True, locals=dict(
            third_kmer1=uint64, third_sq1=uint64,
            third_kmer2=uint64, third_sq2=uint64,
            thirdlast_kmer1=uint64, thirdlast_sq1=uint64,
            thirdlast_kmer2=uint64, thirdlast_sq2=uint64))
    def get_paired_classification(ht, sq1, sq2, kcount):
        quick_dna_to_2bits(sq1)
        quick_dna_to_2bits(sq2)
        if quick:
            # get 4 k-mers (3rd and 3rd-last of both sequences)
            third_kmer1 = twobit_to_code(sq1, 2)
            thirdlast_kmer1 = twobit_to_code(sq1, len(sq1)-w-2)
            third_kmer2 = twobit_to_code(sq2, 2)
            thirdlast_kmer2 = twobit_to_code(sq2, len(sq2)-w-2)
            # look up values of all 4 k-mers, ignore weak status (good thing?!)
            third_sq1  = get_value(ht, third_kmer1) & uint64(3)
            thirdlast_sq1 = get_value(ht, thirdlast_kmer1) & uint64(3)
            third_sq2  = get_value(ht, third_kmer2) & uint64(3)
            thirdlast_sq2 = get_value(ht, thirdlast_kmer2) & uint64(3)
            if (third_sq1 == thirdlast_sq1 and third_sq1 == third_sq2 and third_sq1 == thirdlast_sq2) \
                and (third_sq1 != 3 and third_sq1 != 0):
                return (third_sq1 - 1)
        kcount[:] = 0
        classify_read(ht, sq1, kcount)  # adds to kcount
        classify_read(ht, sq2, kcount)  # adds to kcount
        return classify(kcount)

    @njit(nogil=True)
    def classify_kmers_chunkwise(buf, linemarks, ht):
        n = linemarks.shape[0]
        classifications = np.zeros(n, dtype=np.uint8)
        counts = np.zeros(8, dtype=np.uint32)
        for i in range(n):
            sq = buf[linemarks[i,0]:linemarks[i,1]]
            classifications[i] = get_classification(ht, sq, counts)
            twobits_to_dna_inplace(buf, linemarks[i,0], linemarks[i,1])
        return (classifications, linemarks)

    @njit(nogil=True)
    def classify_paired_kmers_chunkwise(buf, linemarks, buf1, linemarks1, ht):#, atsv, btsv, ntsv, htsv, gtsv):
        n = linemarks.shape[0]
        classifications = np.zeros(n, dtype=np.uint8)
        counts = np.zeros(8, dtype=np.uint32)
        for i in range(n):
            sq1 = buf[linemarks[i,0]:linemarks[i,1]]
            sq2 = buf1[linemarks1[i,0]:linemarks1[i,1]]
            classifications[i] = get_paired_classification(ht, sq1, sq2, counts)
            twobits_to_dna_inplace(buf, linemarks[i,0], linemarks[i,1])
            twobits_to_dna_inplace(buf1, linemarks1[i,0], linemarks1[i,1])
        return (classifications, linemarks, linemarks1)

    @njit(nogil=True)
    def get_borders(linemarks, threads):
        n = linemarks.shape[0]
        perthread = (n + (threads-1)) // threads
        borders = np.empty(threads+1, dtype=uint32)
        for i in range(threads):
            borders[i] = min(i*perthread, n)
        borders[threads] = n
        return borders

    class dummy_contextmgr():
        """a context manager that does nothing at all"""
        def __enter__(self):
            return self
        def __exit__(self, *exc):
            return False
        def write(*_):
            pass
        def flush(*_):
            pass

    @contextmanager
    def cond_contextmgr(name, suffix, buffsize, count, filt):
        # TODO: buffsize not used !!!
        if count and filt:
            raise ValueError("ERROR: cannot use both --count and --filter option at the same time.")
        if count:
            yield dummy_contextmgr()
        elif filt:
            if "graft" in suffix:
                yield io.BufferedWriter(io.FileIO(name + suffix, 'w'))
            else:
                yield dummy_contextmgr()
        else:
            yield io.BufferedWriter(io.FileIO(name + suffix, 'w'))


    def classify_read_from_fastq_paired(fastq, ht):
        # TODO: To work, both reads of a pair have to be exactly the same length,
        # i.e. the files have to be byte-synchronized!
        # This is not true, for example, if adapters have been removed.
        counts = [0, 0, 0, 0, 0]  # host, graft, amb., both, neither
        with  cond_contextmgr(path, "-host.1.fq", bufsize, count, filt) as host1, \
              cond_contextmgr(path, "-host.2.fq", bufsize, count, filt) as host2, \
              cond_contextmgr(path, "-graft.1.fq", bufsize, count, filt) as graft1, \
              cond_contextmgr(path, "-graft.2.fq", bufsize, count, filt) as graft2, \
              cond_contextmgr(path, "-ambiguous.1.fq", bufsize, count, filt) as ambiguous1, \
              cond_contextmgr(path, "-ambiguous.2.fq", bufsize, count, filt) as ambiguous2, \
              cond_contextmgr(path, "-both.1.fq", bufsize, count, filt) as both1, \
              cond_contextmgr(path, "-both.2.fq", bufsize, count, filt) as both2, \
              cond_contextmgr(path, "-neither.1.fq", bufsize, count, filt) as neither1, \
              cond_contextmgr(path, "-neither.2.fq", bufsize, count, filt) as neither2:
            streams = ((host1, host2), (graft1, graft2), (ambiguous1, ambiguous2), (both1, both2), (neither1, neither2))

            with ThreadPoolExecutor(max_workers=threads) as executor:
                for chunk in fastq_chunks_paired((fastq, pairs), bufsize=bufsize*threads, maxreads=chunkreads*threads):
                    # TODO: What is a chunk ?
                    c0, c1, c2, c3 = chunk  # what is c0, c1, c2, c3?
                    borders = get_borders(c1, threads)  # TODO: why not also c3?
                    futures = [ executor.submit(
                        classify_paired_kmers_chunkwise, c0, c1[borders[i]:borders[i+1]], c2, c3[borders[i]:borders[i+1]], ht)
                        for i in range(threads) ]

                    for fut in as_completed(futures):
                        (classifications, linemarks, linemarks2) = fut.result()
                        if count:
                            for seq in range(linemarks.shape[0]):
                                cl = classifications[seq]
                                counts[cl] += 1
                        elif filt:
                            for seq in range(linemarks.shape[0]):
                                cl = classifications[seq]
                                counts[cl] += 1
                                if cl == 1: # graft
                                    lms1, lms2 = linemarks[seq], linemarks2[seq]
                                    streams[cl][0].write(c0[lms1[2]:lms1[3]])
                                    streams[cl][1].write(c2[lms2[2]:lms2[3]])
                        else:
                            for seq in range(linemarks.shape[0]):
                                cl = classifications[seq]
                                counts[cl] += 1
                                lms1, lms2 = linemarks[seq], linemarks2[seq]
                                streams[cl][0].write(c0[lms1[2]:lms1[3]])
                                streams[cl][1].write(c2[lms2[2]:lms2[3]])
                # all chunks processed
            # ThreadPool closed
            for s in streams:
                s[0].flush()
                s[1].flush()
        return counts


    def classify_read_from_fastq_single(fastq, ht):
        counts = [0,0,0,0,0]
        with  cond_contextmgr(path, "-host.fq", bufsize, count, filt) as host, \
              cond_contextmgr(path, "-graft.fq", bufsize, count, filt) as graft, \
              cond_contextmgr(path, "-ambiguous.fq", bufsize, count, filt) as ambiguous, \
              cond_contextmgr(path, "-both.fq", bufsize, count, filt) as both, \
              cond_contextmgr(path, "-neither.fq", bufsize, count, filt) as neither:
            streams = (host, graft, ambiguous, both, neither)
            with ThreadPoolExecutor(max_workers=threads) as executor:
                for chunk in fastq_chunks(fastq, bufsize=bufsize*threads, maxreads=chunkreads*threads):
                    # TODO: What is a chunk ?
                    c0, c1 = chunk  # TODO: c0? c1?
                    borders = get_borders(c1, threads)
                    futures = [ executor.submit(
                        classify_kmers_chunkwise, c0, c1[borders[i]:borders[i+1]], ht)
                        for i in range(threads) ]
                    for fut in as_completed(futures):
                        (classifications, linemarks) = fut.result()
                        for seq in range(linemarks.shape[0]):
                            cl = classifications[seq]
                            assert 0 <= cl <= 4  # TODO: remove
                            counts[cl] += 1
                            lms = linemarks[seq]
                            streams[cl].write(c0[lms[2]:lms[3]])
                # all chunks processed
            # ThreadPool closed
            for s in streams:
                s.flush()
        return counts

    classify_read_from_fastq = (
        classify_read_from_fastq_paired if pairs \
        else classify_read_from_fastq_single)
    return classify_read_from_fastq


# TODO: FASTA classification currently not enabled;
# parameters are only optimized for short reads (100-150) given in FASTQ format
def compile_classify_read_from_fasta(mode, tmask, rcmode, bits, path, h):
    # tmask: mask tuple, works for contiguous and gapped k-mers
    if mode == "majority":
        classify = classify_majority
    elif mode == "xengsort":
        classify = classify_xengsort
    else:
        raise ValueError(f"Unknown mode {mode}")
    classify_read = compile_classify_read(tmask, rcmode, h)
    both = (rcmode == "both")

    # @jit
    def classify_read_from_fasta(fasta, h, skipvalue=0):
        filename, file_extension = os.path.splitext(fasta)
        if file_extension == ".gz":
            filename, file_extension = os.path.splitext(filename)
        TYPES = ['_host', '_graft', '_ambiguous', '_both', '_neither']
        files = []
        if path:
            filename = os.path.join(path, os.path.basename(filename))

        # open files
        for i in TYPES:
            files.append(open(filename + i + file_extension, "w+"))

        counts = np.zeros(8, dtype=np.uint32)
        for header, sq in fasta_reads(fasta):
            quick_dna_to_2bits(sq)
            counts[:] = 0
            classify_read(h, sq, counts)
            classification = classify(counts)
            twobits_to_dna_inplace(sq)
            str_counts = ",".join(str(i) for i in counts)
            header = ">" + header.decode("utf-8") + "counts: " + str_counts + "\n"
            files[classification].write(header)
            sq = sq.decode("utf-8") + "\n"
            files[classification].write(sq)

    return classify_read_from_fasta



def main(args):
    """main method for classifying reads"""
    global debugprint0, debugprint1, debugprint2
    global timestamp0, timestamp1, timestamp2
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    timestamp0, timestamp1, timestamp2 = debug.timestamp

    starttime = timestamp0(msg="\n# Xengsort classify")
    debugprint0("\n- (c) 2019-2023 by Sven Rahmann, Jens Zentgraf, Algorithmic Bioinformatics, Saarland University")
    debugprint0("- Licensed under the MIT License")

    # Load hash table (index)
    h, values, info = load_hash(args.index)
    bits = values.bits
    mask = info['mask']
    k, tmask = mask.k, mask.tuple
    rcmode = info.get('rcmode', values.RCMODE)
    if rcmode is None:  rcmode = values.RCMODE
    if not isinstance(rcmode, str):
        rcmode = rcmode.decode("ASCII")
    chunksize = int(args.chunksize * 2**20)
    chunkreads = args.chunkreads or (chunksize // 200)

    # classify reads from either FASTQ or FASTA files
    timestamp1(msg=f'- Begin classification')
    debugprint1(f"- mask: {k=}, w={tmask[-1]+1}, tuple={tmask}")

    # See if FASTQ was given
    if args.fastq:
        classify_read_from_fastq = compile_classify_read_from_fastq(
            args.classification, tmask, rcmode, bits,
            args.prefix, h, args.threads, args.pairs,
            bufsize=chunksize, chunkreads=chunkreads, quick=args.quick,
            filt=args.filter, count=args.count, prefetchlevel=args.prefetchlevel)
        counts = classify_read_from_fastq(args.fastq, h.hashtable)
        str_counts = "\t".join(str(i) for i in counts)
        print("\n## Classification Statistics")
        print("\n```")
        print("prefix\thost\tgraft\tambiguous\tboth\tneither")
        print(f"{args.prefix}\t{str_counts}")
        print("```\n")
    elif False: # args.fasta was removed
        # TODO: FASTA classification needs to be updated (threads? quick? filter? count?)
        classify_read_from_fasta = compile_classify_read_from_fasta(
            args.classification, tmask, rcmode, bits, args.prefix, h)
        classify_read_from_fasta(f, h.hashtable, bits)
    else:
        # neither --fastq nor --fasta given, nothing to do
        debugprint0("- Neither FASTA nor FASTQ files to classify. Nothing to do. Have a good day.")
        sys.exit(17)

    debugprint0("## Running time statistics\n")
    timestamp0(starttime, msg="- Running time in seconds")
    timestamp0(starttime, msg="- Running time in minutes", minutes=True)
    timestamp0(msg="- Done.")
