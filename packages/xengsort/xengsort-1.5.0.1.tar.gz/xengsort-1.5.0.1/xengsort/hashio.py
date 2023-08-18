import zarr
from importlib import import_module

from .zarrutils import save_to_zgroup, load_from_zgroup
from .lowlevel import debug


def save_hash(outname, h, valueset, additional=dict()):
    valueinfo = dict(valueset=valueset.encode("ASCII"))
    save_to_zgroup(outname, 'valueinfo', **valueinfo)
    info = dict(hashtype=h.hashtype.encode("ASCII"), aligned=h.aligned,
        universe=h.universe, n=h.n, subtables=h.subtables, npages=h.npages, pagesize=h.pagesize,
        nfingerprints=h.nfingerprints, nvalues=h.nvalues,  maxwalk=h.maxwalk,
        hashfuncs=h.hashfuncs, shortcutbits=h.shortcutbits)
    info.update(additional)  # e.g. k, walkseed
    save_to_zgroup(outname, 'info', **info)
    save_to_zgroup(outname, 'data', hashtable=h.hashtable)


def load_hash(filename):
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    timestamp0, timestamp1, timestamp2 = debug.timestamp
    startload = timestamp0(msg=f"- Loading hash index '{filename}'.")
    valueinfo = load_from_zgroup(filename, 'valueinfo')
    valueset = valueinfo['valueset'].decode('ASCII')
    debugprint1(f"- Importing value set '{valueset}'.")
    valueset = valueset.split()
    vmodule = import_module("."+valueset[0], __package__)
    values = vmodule.initialize(*(valueset[1:]))
    update_value = values.update

    info = load_from_zgroup(filename, 'info')
    hashtype = info['hashtype'].decode("ASCII")
    subtables = info['subtables']
    aligned = bool(info['aligned'])
    universe = int(info['universe'])
    n = int(info['n'])
    shortcutbits = int(info['shortcutbits'])
    #npages = int(info['npages'])
    pagesize = int(info['pagesize'])
    #assert (npages-2)*pagesize < n <= npages*pagesize,\
    #    f"Error: npages={npages}, pagesize={pagesize}: {npages*pagesize} vs. {n}"
    nfingerprints = int(info['nfingerprints'])
    nvalues = int(info['nvalues'])
    assert nvalues == values.NVALUES, f"Error: inconsistent nvalues (info: {nvalues}; valueset: {values.NVALUES})"
    maxwalk = int(info['maxwalk'])
    ##print(f"# Hash functions: {info['hashfuncs']}")
    hashfuncs = info['hashfuncs'].decode("ASCII")
    debugprint1(f"- Hash functions: {hashfuncs}")

    debugprint1(f"- Building hash table of type '{hashtype}'...")
    hashmodule = "hash_" + hashtype
    m = import_module("."+hashmodule, __package__)
    h = m.build_hash(universe, n, subtables,
        pagesize, hashfuncs, nvalues, update_value,
        aligned=aligned, nfingerprints=nfingerprints,
        init=True, maxwalk=maxwalk, shortcutbits=shortcutbits)
    with zarr.open(filename, 'r') as fi:
        ht = fi['data/hashtable']
        ht.get_basic_selection(out=h.hashtable)
    timestamp1(startload, msg="- Time to load")
    return h, values, info
