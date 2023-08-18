"""
hash_s3c_fbcbvb:
a hash table with subtables and three choices,
page layout is (low) ... [shortcutbits][slot]+ ... (high),
where slot is  (low) ... [signature value] ...     (high),
where signature is (low) [fingerprint choice] .....(high).
signature as bitmask: ccffffffffffffff (choice is at HIGH bits!)

This layout allows fast access because bits are separated.
It is memory-efficient if the number of values is a power of 2,
or just a little less.
"""

import numpy as np
from numpy.random import randint
from numba import njit, uint64, int64, uint32, int32, boolean
from math import log

from .mathutils import bitsfor, xbitsfor, nextpower
from .lowlevel.bitarray import bitarray
from .lowlevel.intbitarray import intbitarray
from .subtable_hashfunctions import get_hashfunctions, build_get_sub_subkey_from_key, parse_names
from .srhash import (
    create_SRHash,
    check_bits,
    get_npages,
    get_nfingerprints,
    compile_get_subkey_from_page_signature,
    compile_get_subkey_choice_from_page_signature,
    compile_get_statistics,
    )
from .lowlevel import debug  # the global debugging functions



def build_hash(universe, n, subtables, pagesize,
        hashfuncs, nvalues, update_value, *,
        aligned=False, nfingerprints=-1, init=True,
        maxwalk=500, shortcutbits=0, prefetch=False):
    """
    Allocate an array and compile access methods for a hash table.
    Return an SRHash object with the hash information.
    """

    # Get debug printing functions
    debugprint0, debugprint1, debugprint2 = debug.debugprint
    ##timestamp0, timestamp1, timestamp2 = debug.timestamp

    # Basic properties
    hashtype = "s3c_fbcbvb"
    choices = 3
    base = 1
    npages = get_npages(n//subtables, pagesize)
    sub_universe = universe//(4**(int(log(subtables,4))))
    nfingerprints = get_nfingerprints(nfingerprints, sub_universe, npages)
    fprbits, ffprbits = xbitsfor(nfingerprints)
    choicebits = bitsfor(choices)
    sigbits = fprbits + choicebits
    valuebits = bitsfor(nvalues)
    check_bits(sigbits, "signataure")
    check_bits(valuebits, "value")
    if shortcutbits < 0 or shortcutbits > 2:
        debugprint0(f"- Warning: illegal number {shortcutbits=}; using 0.")
        shortcutbits = 0

    fprmask = uint64(2**fprbits - 1)
    choicemask = uint64(2**choicebits - 1)
    sigmask = uint64(2**sigbits - 1)  # fpr + choice, no values
    slotbits = sigbits + valuebits  # sigbits: bitsfor(fpr x choice)
    neededbits = slotbits * pagesize + shortcutbits  # specific
    pagesizebits = nextpower(neededbits)  if aligned else neededbits
    subtablebits = int(npages * pagesizebits)
    subtablebits = (subtablebits // 512 + 1) * 512
    tablebits = subtablebits * subtables

    fprloss = pagesize * npages * (fprbits-ffprbits) / 2**23  # in MB

    # allocate the underlying array
    if init == True:
        hasharray = bitarray(tablebits, alignment=64)  # (#bits, #bytes)
        debugprint2(f"- Allocated {hasharray.array.dtype} hash table of shape {hasharray.array.shape}.")
    else:
        hasharray = bitarray(0)
        debugprint2(f"- Nothing allocated.")
    hashtable = hasharray.array  # the raw bit array
    get_bits_at = hasharray.get  # (array, startbit, nbits=1)
    set_bits_at = hasharray.set  # (array, startbit, value , nbits=1)
    hprefetch = hasharray.prefetch

    if hashfuncs == "random":
        firsthashfunc = parse_names(hashfuncs, 1)[0]
    else:
        firsthashfunc, hashfuncs = hashfuncs.split(":", 1)
    get_subtable_subkey_from_key, get_key_from_subtable_subkey = build_get_sub_subkey_from_key(firsthashfunc, universe, subtables)
    
    hashfuncs, get_pf, get_subkey, get_subtable_page_fpr, get_key_from_subtale_page_fpr = get_hashfunctions(
            firsthashfunc, hashfuncs, choices, universe, npages, subtables)

    debugprint1(
        f"- Fingerprintbits: {ffprbits} -> {fprbits}; loss={fprloss:.1f} MB\n"
        f"- npages={npages}, slots={pagesize*npages}, n={n} per subtable\n"
        f"- Bits per slot: {slotbits}; per page: {neededbits} -> {pagesizebits}\n"
        f"- Subtable bits: {subtablebits};  MB: {subtablebits/2**23:.1f};  GB: {subtablebits/2**33:.3f}\n"
        f"- Table bits: {tablebits};  MB: {tablebits/2**23:.1f};  GB: {tablebits/2**33:.3f}\n"
        f"- Shortcutbits: {shortcutbits}\n"
        f"- Final hash functions: {hashfuncs}",
    )
    get_ps = tuple([ compile_getps_from_getpf(get_pf[c], c+1, fprbits)
            for c in range(choices) ])
    get_pf1, get_pf2, get_pf3 = get_pf
    get_ps1, get_ps2, get_ps3 = get_ps
    get_key1, get_key2, get_key3 = get_subkey

    @njit(nogil=True, inline='always', locals=dict(
        page=int64, startbit=uint64))
    def prefetch_page(table, subtable, page):
        startbit = subtable * subtablebits + page * pagesizebits
        hprefetch(table, startbit)

    # Define private low-level hash table accssor methods
    @njit(nogil=True, locals=dict(
            page=int64, startbit=int64, v=uint64))
    def get_shortcutbits_at(table, subtable, page):
        """Return the shortcut bits at the given page."""
        if shortcutbits == 0:
            return uint64(3)
        startbit = subtable * subtablebits + page * pagesizebits
        v = get_bits_at(table, startbit, shortcutbits)
        return v

    @njit(nogil=True,  locals=dict(
            page=int64, slot=uint64, startbit=int64, v=uint64))
    def get_value_at(table, subtable, page, slot):
        """Return the value at the given page and slot."""
        if valuebits == 0: return 0
        startbit = subtable * subtablebits + page * pagesizebits + slot * slotbits + shortcutbits + sigbits
        v = get_bits_at(table, startbit, valuebits)
        return v

    @njit(nogil=True, locals=dict(
            page=int64, slot=uint64, startbit=int64, c=uint64))
    def get_choicebits_at(table, subtable, page, slot):
        """Return the choice at the given page and slot; choices start with 1."""
        startbit = subtable * subtablebits + page * pagesizebits + slot * slotbits + shortcutbits + fprbits
        c = get_bits_at(table, startbit, choicebits)
        return c

    @njit(nogil=True,  locals=dict(
            page=int64, slot=uint64, startbit=int64, sig=uint64))
    def get_signature_at(table, subtable, page, slot):
        """Return the signature (choice, fingerprint) at the given page and slot."""
        startbit = subtable * subtablebits + page * pagesizebits + slot * slotbits + shortcutbits
        sig = get_bits_at(table, startbit, sigbits)
        return sig

    @njit(nogil=True, locals=dict(
            page=int64, slot=uint64, startbit=int64, sig=uint64, v=uint64))
    def get_item_at(table, subtable, page, slot):
        """Return the signature (choice, fingerprint) and value at the given page and slot."""
        startbit = subtable * subtablebits + page * pagesizebits + slot * slotbits + shortcutbits
        sig = get_bits_at(table, startbit, sigbits)
        if valuebits > 0:
            v = get_bits_at(table, startbit+sigbits, valuebits)
            return (sig, v)
        return (sig, uint64(0))

    @njit(nogil=True, inline='always', locals=dict(
            sig=uint64, c=uint64, fpr=uint64))
    def signature_to_choice_fingerprint(sig):
        """Return (choice, fingerprint) from signature"""
        fpr = sig & fprmask
        c = (sig >> uint64(fprbits)) & choicemask
        return (c, fpr)

    @njit(nogil=True, inline='always', locals=dict(
            sig=uint64, choice=uint64, fpr=uint64))
    def signature_from_choice_fingerprint(choice, fpr):
        """Return signature from (choice, fingerprints)"""
        sig = (choice << uint64(fprbits)) | fpr
        return sig

    @njit(nogil=True, locals=dict(
            page=int64, bit=uint64, startbit=uint64))
    def set_shortcutbit_at(table, subtable, page, bit):
        """Set the shortcut bits at the given page."""
        if shortcutbits == 0: return
        # assert 1 <= bit <= shortcutbits
        startbit = subtable * subtablebits + page * pagesizebits + bit - 1
        set_bits_at(table, startbit, 1, 1)  # set exactly one bit to 1

    @njit(nogil=True, locals=dict(
            page=int64, slot=int64, sig=uint64))
    def set_signature_at(table, subtable, page, slot, sig):
        """Set the signature at the given page and slot."""
        startbit = subtable * subtablebits + page * pagesizebits + slot * slotbits + shortcutbits
        set_bits_at(table, startbit, sig, sigbits)
    
    @njit(nogil=True, locals=dict(
            page=int64, slot=int64, value=int64))
    def set_value_at(table, subtable, page, slot, value):
        if valuebits == 0: return
        """Set the value at the given page and slot."""
        startbit = subtable * subtablebits + page * pagesizebits + slot * slotbits + sigbits + shortcutbits
        set_bits_at(table, startbit, value, valuebits)

    @njit(nogil=True, locals=dict(
            page=int64, slot=int64, sig=uint64, value=uint64))
    def set_item_at(table, subtable, page, slot, sig, value):
        startbit = subtable * subtablebits + page * pagesizebits + slot * slotbits + shortcutbits
        set_bits_at(table, startbit, sig, sigbits)
        if valuebits == 0: return
        set_bits_at(table, startbit+sigbits, value, valuebits)


    # define the is_slot_empty_at function
    @njit(nogil=True, inline='always', locals=dict(b=boolean))
    def is_slot_empty_at(table, subtable, page, slot):
        """Return whether a given slot is empty (check by choice)"""
        c = get_choicebits_at(table, subtable, page, slot)
        b = (c == 0)
        return b

    # define the get_subkey_from_page_signature function
    get_subkey_from_page_signature = compile_get_subkey_from_page_signature(
        get_subkey, signature_to_choice_fingerprint, base=base)
    get_subkey_choice_from_page_signature = compile_get_subkey_choice_from_page_signature(
        get_subkey, signature_to_choice_fingerprint, base=base)

    # define the _find_signature_at function
    @njit(nogil=True, inline="always", locals=dict(
            page=uint64, fpr=uint64, choice=uint64,
            query=uint64, slot=int64, v=uint64, s=uint64))
    def _find_signature_at(table, subtable, page, query):
        """
        Attempt to locate signature on a page,
        assuming choice == 0 indicates an empty space.
        Return (int64, uint64):
        Return (slot, value) if the signature 'query' was found,
            where 0 <= slot < pagesize.
        Return (-1, fill) if the signature was not found,
            where fill >= 0 is the number of slots already filled.
        """
        for slot in range(pagesize):
            s = get_signature_at(table, subtable, page, slot)
            if s == query:
                v = get_value_at(table, subtable, page, slot)
                return (slot, v)
            c, _ = signature_to_choice_fingerprint(s)
            if c == 0:
                return (int64(-1), uint64(slot))  # free slot, only valid if tight!
        return (int64(-1), uint64(pagesize))

    # define the update/store/overwrite functions

    update, update_ssk \
        = compile_update_by_randomwalk(pagesize,
            get_ps, _find_signature_at,
            get_item_at, set_item_at, set_value_at,
            get_subkey_from_page_signature,
            get_subtable_subkey_from_key,
            prefetch_page,
            update_value=update_value, overwrite=False,
            allow_new=True, allow_existing=True,
            maxwalk=maxwalk, prefetch=prefetch)

    update_existing, update_existing_ssk \
        = compile_update_by_randomwalk(pagesize,
            get_ps, _find_signature_at,
            get_item_at, set_item_at, set_value_at,
            get_subkey_from_page_signature,
            get_subtable_subkey_from_key,
            prefetch_page,
            update_value=update_value, overwrite=False,
            allow_new=False, allow_existing=True,
            maxwalk=maxwalk, prefetch=prefetch)

    store_new, store_new_ssk \
        = compile_update_by_randomwalk(pagesize,
            get_ps, _find_signature_at,
            get_item_at, set_item_at, set_value_at,
            get_subkey_from_page_signature,
            get_subtable_subkey_from_key,
            prefetch_page,
            update_value=None, overwrite=True,
            allow_new=True, allow_existing=False,
            maxwalk=maxwalk, prefetch=prefetch)

    overwrite, overwrite_ssk \
        = compile_update_by_randomwalk(pagesize,
            get_ps, _find_signature_at,
            get_item_at, set_item_at, set_value_at,
            get_subkey_from_page_signature,
            get_subtable_subkey_from_key,
            prefetch_page,
            update_value=update_value, overwrite=True,
            allow_new=True, allow_existing=True,
            maxwalk=maxwalk, prefetch=prefetch)

    overwrite_existing, overwrite_existing_ssk \
        = compile_update_by_randomwalk(pagesize,
            get_ps, _find_signature_at,
            get_item_at, set_item_at, set_value_at,
            get_subkey_from_page_signature,
            get_subtable_subkey_from_key,
            prefetch_page,
            update_value=update_value, overwrite=True,
            allow_new=False, allow_existing=True,
            maxwalk=maxwalk, prefetch=prefetch)


    # define the "reading" functions find_index, get_value, etc.

    @njit(nogil=True, locals=dict(
            key=uint64, default=uint64, NOTFOUND=uint64,
            page1=uint64, sig1=uint64, slot1=int64, val1=uint64,
            page2=uint64, sig2=uint64, slot2=int64, val2=uint64,
            page3=uint64, sig3=uint64, slot3=int64, val3=uint64,
            pagebits=uint32, check2=uint32, check3=uint32))
    def find_index(table, subtable, key, default=uint64(-1)):
        """
        Return uint64: the linear table index the given key,
        or the default if the key is not present.
        """
        NOTFOUND = uint64(default)
        page1, sig1 = get_ps1(key)
        (slot1, val1) = _find_signature_at(table, subtable, page1, sig1)
        if slot1 >= 0: return uint64(uint64(page1 * pagesize) + slot1)
        if val1 < pagesize: return NOTFOUND
        # test for shortcut
        pagebits = get_shortcutbits_at(table, subtable, page1)  # returns all bits set if bits==0
        if not pagebits: return NOTFOUND
        check2 = pagebits & 1
        check3 = pagebits & 2 if shortcutbits >= 2 else 1

        if check2:
            page2, sig2 = get_ps2(key)
            (slot2, val2) = _find_signature_at(table, subtable, page2, sig2)
            if slot2 >= 0: return uint64(uint64(page2 * pagesize) + slot2)
            if val2 < pagesize: return NOTFOUND
            # test for shortcuts
            if shortcutbits != 0:
                pagebits = get_shortcutbits_at(table, subtable, page2)
                if shortcutbits == 1:
                    check3 = pagebits  # 1 or 0
                else:
                    check3 &= pagebits & 2

        # try the third choice only if necessary
        if not check3: return NOTFOUND
        page3, sig3 = get_ps3(key)
        (slot3, val3) = _find_signature_at(table, subtable, page3, sig3)
        if slot3 >= 0: return uint64(uint64(page3 * pagesize) + slot3)
        return NOTFOUND


    @njit(nogil=True, locals=dict(
            subkey=uint64, subtable=uint64, default=uint64, NOTFOUND=uint64,
            page1=uint64, sig1=uint64, slot1=int64, val1=uint64,
            page2=uint64, sig2=uint64, slot2=int64, val2=uint64,
            page3=uint64, sig3=uint64, slot3=int64, val3=uint64,
            pagebits=uint32, check2=uint32, check3=uint32))
    def get_value_from_st_sk(table, subtable, subkey, default=uint64(0)):
        """
        Return uint64: the value for the given subkey,
        or the default if the subkey is not present.
        """
        NOTFOUND = uint64(default)
        page1, sig1 = get_ps1(subkey)
        (slot1, val1) = _find_signature_at(table, subtable, page1, sig1)
        if slot1 >= 0: return val1
        if val1 < pagesize: return NOTFOUND
        # test for shortcut
        pagebits = get_shortcutbits_at(table, subtable, page1)  # returns all bits set if bits==0
        if not pagebits: return NOTFOUND
        check2 = pagebits & 1
        check3 = pagebits & 2 if shortcutbits >= 2 else 1

        if check2:
            page2, sig2 = get_ps2(subkey)
            (slot2, val2) = _find_signature_at(table, subtable, page2, sig2)
            if slot2 >= 0: return val2
            if val2 < pagesize: return NOTFOUND
            # test for shortcuts
            if shortcutbits != 0:
                pagebits = get_shortcutbits_at(table, subtable, page2)
                if shortcutbits == 1:
                    check3 = pagebits  # 1 or 0
                else:
                    check3 &= pagebits & 2

        # try the third choice only if necessary
        if not check3: return NOTFOUND
        page3, sig3 = get_ps3(subkey)
        (slot3, val3) = _find_signature_at(table, subtable, page3, sig3)
        if slot3 >= 0: return val3
        return NOTFOUND


    @njit(nogil=True, locals=dict(
            subkey=uint64, subtable=uint64, default=uint64,
            page1=uint64, sig1=uint64, slot1=int64, val1=uint64,
            page2=uint64, sig2=uint64, slot2=int64, val2=uint64,
            page3=uint64, sig3=uint64, slot3=int64, val3=uint64,
            pagebits=uint32, check2=uint32, check3=uint32))
    def get_value_and_choice_from_st_sk(table, subtable, subkey, default=uint64(0)):
        """
        Return (value, choice) for given subkey,
        where value is uint64 and choice is in {1,2,3} if subkey was found,
        but value=default and choice=0 if subkey was not found.
        """
        NOTFOUND = (uint64(default), uint32(0))
        page1, sig1 = get_ps1(subkey)
        (slot1, val1) = _find_signature_at(table, subtable, page1, sig1)
        if slot1 >= 0: return (val1, uint32(1))
        if val1 < pagesize: return NOTFOUND
        # test for shortcut
        pagebits = get_shortcutbits_at(table, subtable, page1)  # returns all bits set if bits==0
        if not pagebits: return NOTFOUND
        check2 = pagebits & 1
        check3 = pagebits & 2 if shortcutbits >= 2 else 1

        if check2:
            page2, sig2 = get_ps2(subkey)
            (slot2, val2) = _find_signature_at(table, subtable, page2, sig2)
            if slot2 >= 0: return (val2, uint32(2))
            if val2 < pagesize: return NOTFOUND
            # test for shortcuts
            if shortcutbits != 0:
                pagebits = get_shortcutbits_at(table, subtable, page2)
                if shortcutbits == 1:
                    check3 = pagebits  # 1 or 0
                else:
                    check3 &= pagebits & 2

        # try the third choice only if necessary
        if not check3: return NOTFOUND
        page3, sig3 = get_ps3(subkey)
        (slot3, val3) = _find_signature_at(table, subtable, page3, sig3)
        if slot3 >= 0: return (val3, uint32(3))
        return NOTFOUND

    @njit(nogil=True)
    def get_value_and_choice(table, key):
        st, sk = get_subtable_subkey_from_key(key)
        return get_value_and_choice_from_st_sk(table, st, sk)

    @njit(nogil=True)
    def get_value(table, key):
        st, sk = get_subtable_subkey_from_key(key)
        return get_value_from_st_sk(table, st, sk)


    @njit(nogil=True, locals=dict(
            page=uint64, slot=int64, v=uint64, sig=uint64, c=uint64,
            f=uint64, key=uint64, p=uint64, s=int64, fill=uint64))
    def is_tight(ht):
        """
        Return (0,0) if hash is tight, or problem (key, choice).
        In the latter case, it means that there is an empty slot
        for key 'key' on page choice 'choice', although key is
        stored at a higher choice.
        """
        for page in range(npages):
            for slot in range(pagesize):
                sig = get_signature_at(ht, page, slot)
                (c, f) = signature_to_choice_fingerprint(sig)  # should be in 0,1,2,3.
                if c <= 1: continue
                # c >= 2
                key = get_key2(page, f)
                p, s = get_ps1(key)
                (slot, val) = _find_signature_at(ht, p, s)
                if slot >= 0 or val != pagesize:
                    return (uint64(key), 1)  # empty slot on 1st choice
                if c >= 3:
                    key = get_key3(page, f)
                    p, s = get_ps2(key)
                    (slot, val) = _find_signature_at(ht, p, s)
                    if slot >= 0 or val != pagesize:
                        return (uint64(key), 2)  # empty slot on 2nd choice
                if c >= 4:
                    return (uint64(key), 9)  # should never happen, c=1,2,3.
        # all done, no problems
        return (0, 0)


    @njit(nogil=True, locals=dict(counter=uint64))
    def count_items(ht, filter_func):
        """
        ht: uint64[:]  # the hash table
        filter_func(key: uint64, value: uint64) -> bool  # function
        Return number of items satisfying the filter function (uint64).
        """
        counter = 0
        for st in range(subtables):
            for p in range(npages):
                for s in range(pagesize):
                    if is_slot_empty_at(ht, st, p, s):  continue
                    sig = get_signature_at(ht, st, p, s)
                    value = get_value_at(ht, st, p, s)
                    subkey = get_subkey_from_page_signature(p, sig)
                    key = get_key_from_subtable_subkey(st, subkey)
                    if filter_func(key, value):
                        counter += 1
        return counter

    @njit(nogil=True, locals=dict(pos=uint64))
    def get_items(ht, filter_func, buffer):
        """
        ht: uint64[:]  # the hash table
        filter_func(key: uint64, value: uint64) -> bool  # function
        buffer: uint64[:]  # buffer for keys
        Return number of items satisfying the filter function (uint64).
        Copy keys satisfying filter_func into buffer until it is full.
        (Additional keys are not copied, but counted.)
        """
        B = buffer.size
        pos = 0
        for st in range(subtables):
            for p in range(npages):
                for s in range(pagesize):
                    if is_slot_empty_at(ht, st, p, s):  continue
                    sig = get_signature_at(ht, st, p, s)
                    value = get_value_at(ht, st, p, s)
                    subkey = get_subkey_from_page_signature(p, sig)
                    key = get_key_from_subtable_subkey(st, subkey)
                    if filter_func(key, value):
                        if pos < B:
                            buffer[pos] = key
                        pos += 1
        return pos


    # define the occupancy computation function
    get_statistics = compile_get_statistics("c", subtables,
        choices, npages, pagesize, nvalues, shortcutbits,
        get_value_at, get_signature_at,
        signature_to_choice_fingerprint, get_shortcutbits_at)


    # define the compute_shortcut_bits fuction,
    # depending on the number of shortcutbits
    if shortcutbits == 0:
        @njit
        def compute_shortcut_bits(table):
            pass
    elif shortcutbits == 1:
        @njit
        def compute_shortcut_bits(table):
            for subtable in range(subtables):
                for page in range(npages):
                    for slot in range(pagesize):
                        if is_slot_empty_at(table, subtable, page, slot):
                            continue
                        key, c = get_subkey_choice_from_page_signature(
                            page, get_signature_at(table, subtable, page, slot))
                        assert c >= 1
                        if c == 1: continue  # first choice: nothing to do
                        # treat c >= 2
                        firstpage, _ = get_pf1(key)
                        set_shortcutbit_at(table, subtable, firstpage, 1)
                        if c >= 3:
                            secpage, _ = get_pf2(key)
                            set_shortcutbit_at(table, subtable, secpage, 1)
    elif shortcutbits == 2:
        @njit
        def compute_shortcut_bits(table):
            for subtable in range(subtables):
                for page in range(npages):
                    for slot in range(pagesize):
                        if is_slot_empty_at(table, subtable, page, slot):
                            continue
                        key, c = get_subkey_choice_from_page_signature(
                            page, get_signature_at(table, subtable, page, slot))
                        assert c >= 1
                        if c == 1:
                            continue
                        if c == 2:
                            firstpage, _ = get_pf1(key)
                            set_shortcutbit_at(table, subtable, firstpage, 1)
                            continue
                        # now c == 3:
                        firstpage, _ = get_pf1(key)
                        set_shortcutbit_at(table, subtable, firstpage, 2)
                        secpage, _ = get_pf2(key)
                        set_shortcutbit_at(table, subtable, secpage, 2)
    else:
        raise ValueError(f"illegal number of shortcutbits: {shortcutbits}")

    # all methods are defined; return the hash object
    return create_SRHash(locals())


#######################################################################


def compile_getps_from_getpf(get_pfx, choice, fprbits):
    @njit(nogil=True, inline='always', locals=dict(
            p=uint64, f=uint64, sig=uint64))
    def get_psx(code):
        (p, f) = get_pfx(code)
        sig = uint64((choice << uint64(fprbits)) | f)
        return (p, sig)
    return get_psx


def compile_update_by_randomwalk(pagesize,
            get_ps, _find_signature_at,
            get_item_at, set_item_at,
            set_value_at,
            get_subkey_from_page_signature,
            get_subtable_subkey_from_key,
            prefetch_page,
            *,
            update_value=None, overwrite=False,
            allow_new=False, allow_existing=False,
            maxwalk=1000, prefetch=False):
    """return a function that stores or modifies an item"""
    choices = len(get_ps)
    assert choices == 3
    (get_ps1, get_ps2, get_ps3) = get_ps
    LOCATIONS = choices * pagesize
    if LOCATIONS < 2:
        raise ValueError(f"ERROR: Invalid combination of pagesize={pagesize} * choices={choices}")
    if (update_value is None or overwrite) and allow_existing:
        update_value = njit(
            nogil=True, locals=dict(old=uint64, new=uint64)
            )(lambda old, new: new)
    if not allow_existing:
        update_value = njit(
            nogil=True, locals=dict(old=uint64, new=uint64)
            )(lambda old, new: old)

    @njit(nogil=True, locals=dict(
            subkey=uint64, value=uint64, v=uint64,
            page1=uint64, sig1=uint64, slot1=int64, val1=uint64,
            page2=uint64, sig2=uint64, slot2=int64, val2=uint64,
            page3=uint64, sig3=uint64, slot3=int64, val3=uint64,
            fc=uint64, fpr=uint64, c=uint64, page=uint64,
            oldpage=uint64, lastlocation=uint64, steps=uint64,
            xsig=uint64, xval=uint64))
    def update_ssk(table, subtable, subkey, value):
        """
        Attempt to store given subkey with given value in hash table.
        If the subkey exists, the existing value may be updated or overwritten,
        or nothing may happen, depending on how this function was compiled.
        If the subkey does not exist, it is stored with the provided value,
        or nothing may happen, depending on how this function was compiled.

        Returns (status: int32, result: uint64).

        status: if status == 0, the subkey was not found,
            and, if allow_new=True, it could not be inserted either.
            If (status & 127 =: c) != 0, the subkey exists or was inserted w/ choice c.
            If (status & 128 != 0), the subkey was aleady present.

        result: If the subkey was already present (status & 128 != 0),
            then result is the new value that was stored.
            Otherwise (if status & 128 == 0), result is the walk length needed 
            to store the new (subkey, value) pair.
        """
        oldpage = uint64(-1)
        lastlocation = uint64(-1)
        steps = 0
        while steps <= maxwalk:
            page1, sig1 = get_ps1(subkey)
            if prefetch:
                page2, sig2 = get_ps2(subkey)
                prefetch_page(table, page2)
            steps += (page1 != oldpage)
            (slot1, val1) = _find_signature_at(table, subtable, page1, sig1)
            if slot1 != -1:  # found on page1/choice1
                v = update_value(val1, value)
                if v != val1: set_value_at(table, subtable, page1, slot1, v)
                return (int32(128|1), v)
            elif val1 < pagesize:  # not found, but space available at slot val1
                if allow_new:
                    set_item_at(table, subtable, page1, val1, sig1, value)
                    return (int32(1), steps)
                return (int32(0), steps)
            
            if prefetch:
                page3, sig3 = get_ps3(subkey)
                prefetch_page(table, page3)
            else:
                page2, sig2 = get_ps2(subkey)
            steps += (page2 != oldpage)
            (slot2, val2) = _find_signature_at(table, subtable, page2, sig2)
            if slot2 != -1:  # found on page2/choice2
                v = update_value(val2, value)
                if v != val2: set_value_at(table, subtable, page2, slot2, v)
                return (int32(128|2), v)
            elif val2 < pagesize:  # not found, but space available at slot val2
                if allow_new:
                    set_item_at(table, subtable, page2, val2, sig2, value)
                    return (int32(2), steps)
                return (int32(0), steps)
            
            if not prefetch:
                page3, sig3 = get_ps3(subkey)
            steps += (page3 != oldpage)
            (slot3, val3) = _find_signature_at(table, subtable, page3, sig3)
            if slot3 != -1:  # found on page3/choice3
                v = update_value(val3, value)
                if v != val3: set_value_at(table, subtable, page3, slot3, v)
                return (int32(128|3), v)
            elif val3 < pagesize:  # not found, but space available at slot val3
                if allow_new:
                    set_item_at(table, subtable, page3, val3, sig3, value)
                    return (int32(3), steps)
                return (int32(0), steps)
            
            # We get here iff all pages are full.
            if not allow_new:
                return (int32(0), steps)

            # Pick a random location; 
            # store item there and continue with evicted item.
            location = randint(LOCATIONS)
            while location == lastlocation:
                location = randint(LOCATIONS)
            lastlocation = location
            slot = location // choices
            c = location % choices
            page = (page1, page2, page3)[c]
            sig = (sig1, sig2, sig3)[c]
            #if c == 0:
            #    page = page1; sig = sig1
            #elif c == 1:
            #    page = page2; sig = sig2
            #else:  # c == 2
            #    page = page3; sig = sig3
            oldpage = page
            xsig, xval = get_item_at(table, subtable, page, slot)
            set_item_at(table, subtable, page, slot, sig, value)
            subkey = get_subkey_from_page_signature(page, xsig)
            value = xval
            # loop again
        # maxwalk step exceeded; some item was kicked out :(
        return (int32(0), steps)

    @njit(nogil=True, locals=dict(
            subtable=uint64, subkey=uint64))
    def update(table, key, value):
        subtable, subkey = get_subtable_subkey_from_key(key)
        return update_ssk(table, subtable, subkey, value)

    return update, update_ssk


#######################################################################
## Module-level functions
#######################################################################
## define the fill_from_dump function

def fill_from_arrays(h, k, nkmers, codes, tables, achoices, values):
    npages = h.npages
    pagesize = h.pagesize
    (get_pf1, get_pf2, get_pf3) = h.private.get_pf
    set_signature_at = h.private.set_signature_at
    set_value_at = h.private.set_value_at
    is_slot_empty_at = h.private.is_slot_empty_at
    signature_from_choice_fingerprint = h.private.signature_from_choice_fingerprint
    choices = intbitarray(nkmers, 2, init=achoices)
    acodes = codes.array
    avalues = values.array
    atable = tables.array
    get_code = codes.get
    get_value = values.get
    get_choice = choices.get
    get_table = tables.get

    @njit
    def _insert_elements(ht):
        total = 0
        for i in range(nkmers):
            total += 1
            code = get_code(acodes, i)
            table = get_table(atable, i)
            value = get_value(avalues, i)
            choice = uint64(get_choice(achoices, i))
            assert choice >= 1
            if choice == 1:
                page, fpr = get_pf1(code)
            elif choice == 2:
                page, fpr = get_pf2(code)
            elif choice == 3:
                page, fpr = get_pf3(code)
            else:
                assert False
            for slot in range(pagesize):
                if is_slot_empty_at(ht, table, page, slot): break
            else:
                assert False
            sig =  signature_from_choice_fingerprint(choice, fpr)
            set_signature_at(ht, table, page, slot, sig)
            set_value_at(ht, table, page, slot, value)
        return total

    total = _insert_elements(h.hashtable)
    walklength = np.zeros(h.maxwalk+5, dtype=np.uint64)
    walklength[0] = total
    return (total, 0, walklength)
