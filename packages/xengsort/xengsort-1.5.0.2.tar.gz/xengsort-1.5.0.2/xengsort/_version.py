VERSION = "1.5.0"
__version__ = VERSION

DESCRIPTION = f"xengsort {VERSION}: xenograft sorting of FASTQ reads into five categories: host, graft, both, neither, ambiguous"


LONG_DESCRIPTION = """
The xengsort tool is made for xenograft sorting of single-end or paired-end FASTQ reads.
The input reads are assumed to be a mixture of reads from (mainly) two organisms,
typically human (tumor) and mouse (normal tissue),
obtained from sequencing a human tumor that was implanted
into a mouse model to study its growth and evolution,
or its behavior under certain treatments.

Using a k-mer-based approach and an ultra-fast hash table,
xengsort separates (sorts) reads into five categories:
(1) host (mouse) reads,
(2) graft (human) reads,
(3) reads that could result from both species,
(4) reads that fit neither species,
(5) ambiguous reads, which contain conflicting information.

So the reads (or pairs) from a FASTQ file (or a pair of FASTQ files)
are split into five output files (or pairs of files).
Compared to other alignment-free tools, xengsort can be up to 4 times faster.
Compared to alignment-based tools, xengsort is faster by orders of magnitude.
"""
