from collections import namedtuple

# define the Mask class (as a namedtuple)
Mask = namedtuple("Mask", [
    "mask",   # string of # and _
    "tuple",  # tuple of indices of significant positions (#)
    "k",      # weight (number of #)
    "w",      # total width (len(mask))
    "m",      # minimizer length (if applicable; otherwise m=0)
    "is_contiguous",  # True iff w == k
    "has_minimizer",  # True iff is_contiguous and (m != 0) and m < k
    ])


def check_mask(mask, symmetric=True, k=0, w=0, m=0):
    if not isinstance(mask, str):
        raise TypeError(f"mask must be of type str, not {type(mask)}")
    if symmetric and not mask == mask[::-1]:
        raise ValueError(f"mask '{mask}'' is not symmetric")
    if not (mask[0] == '#' and mask[-1] == '#'):
        raise ValueError(f"first and last characters of mask '{mask}' must be '#'")
    if k > 0 and mask.count('#') != k:
        raise ValueError(f"mask '{mask}' does not have k={k} #s.")
    if w > 0 and len(mask) != w:
        raise ValueError(f"mask '{mask}' does not have width w={w}.")
    if m > 0 and not (k==w or k==0 or w==0):
        raise ValueError(f"Masks with minimizers {m=} must be contiguous.")
    if m > 0 and k > 0 and not (m < k):
        raise ValueError(f"Masks with minimizers {m=} must have m < k, but {k=}, {w=}.")

def contiguous_mask(k):
    return "".join("#" for i in range(k))


def mask_to_tuple(mask, symmetric=True):
    check_mask(mask, symmetric=symmetric)
    return tuple([i for i, c in enumerate(mask) if c == '#'])


def tuple_to_mask(tmask, symmetric=True):
    w = max(tmask) + 1
    k = len(tmask)
    mask = "".join(['#' if i in tmask else '_' for i in range(w)])
    check_mask(mask, symmetric=symmetric, k=k, w=w)
    return mask


def create_mask(form, m=0):
    m = 0 if m is None else m
    mask = dict(m=m)

    if isinstance(form, int):  # given k: contiguous k-mer
        mask["k"] = form
        mask["w"] = form
        mask["mask"] = mm = contiguous_mask(form)
        mask["tuple"] = mask_to_tuple(mm)
    elif isinstance(form, str):  # given string
        mask["mask"] = form
        mask["tuple"] = mask_to_tuple(form)
        mask["w"] = len(form)
        mask["k"] = len(mask["tuple"])
    elif isinstance(form, tuple):  # given tuple
        mask["tuple"] = form
        mask["mask"] = tuple_to_mask(mask["tuple"])
        mask["w"] = len(mask["mask"])
        mask["k"] = len(form)
    else:
        raise ValueError(f"Wrong input to create_mask: {form=}, {m=}")

    check_mask(mask["mask"], k=mask["k"], w=mask["w"], m=m)
    mask["is_contiguous"] = (mask["k"] == mask["w"])
    mask["has_minimizer"] = (m != 0)
    return Mask(**mask)
