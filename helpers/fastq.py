import os


def check_gc(seq: str, *gc_bounds: float) -> bool:
    """
    Check whether the GC content of a sequence falls within the given bounds.

    Arguments:
    seq: str — nucleotide sequence
    *gc_bounds: float — a single number (upper bound, lower bound is 0)
                        or two numbers (lower and upper bounds), in percent

    Returns bool: True if GC content (in %) is within [low, high].
    """
    if len(gc_bounds) == 0:
        low, high = 0, 100
    elif len(gc_bounds) == 1:
        low, high = 0, gc_bounds[0]
    elif len(gc_bounds) == 2:
        low, high = gc_bounds
    else:
        print("Error. The function expects 1 to 2 arguments")
        return False

    if not seq:
        gc_content = 0.0
    else:
        gc_count = sum(1 for n in seq if n in ("G", "C", "c", "g"))
        gc_content = gc_count / len(seq) * 100

    return low <= gc_content <= high


def check_length(seq: str, *length_bounds: int) -> bool:
    """
    Check whether the length of a sequence falls within the given bounds.

    Arguments:
    seq: str — nucleotide sequence
    *length_bounds: int — a single number (upper bound, lower bound is 0)
                          or two numbers (lower and upper bounds)

    Returns bool: True if len(seq) is within [low, high].
    """
    if len(length_bounds) == 0:
        llow, lhigh = 0, 2**32
    elif len(length_bounds) == 1:
        llow, lhigh = 0, length_bounds[0]
    elif len(length_bounds) == 2:
        llow, lhigh = length_bounds
    else:
        print("Error. The function expects 1 to 2 arguments")
        return False

    return llow <= len(seq) <= lhigh


def check_quality(qual: str, quality_threshold: float) -> bool:
    """
    Check that the average quality of a read is not below the threshold.

    Arguments:
    qual: str — quality string in Phred+33 encoding
    quality_threshold: float — threshold for average quality

    Returns bool: True if average quality >= quality_threshold.
    """
    if not qual:
        return quality_threshold <= 0
    avg = sum(ord(c) - 33 for c in qual) / len(qual)
    return avg >= quality_threshold


def pass_filters(
    seq: str,
    qual: str,
    gc_bounds,
    length_bounds,
    quality_threshold: float,
) -> bool:
    """
    Apply all filters to a read: length, GC content and quality.

    Arguments:
    seq: str — nucleotide sequence
    qual: str — quality string (Phred+33)
    gc_bounds: tuple | float — GC content interval in percent
    length_bounds: tuple | int — length interval
    quality_threshold: float — average quality threshold

    Returns bool: True if the read passes all filters.
    """
    return (
        check_length(seq, *length_bounds)
        and check_gc(seq, *gc_bounds)
        and check_quality(qual, quality_threshold)
    )


def read_one(f) -> tuple[str, str, str, str] | None:
    """
    Read a single FASTQ read (4 lines) from a file object.

    Arguments:
    f — open file object

    Returns a tuple (header, seq, plus, qual), or None if the end of the file
    is reached or the read is incomplete.
    """
    header = f.readline()
    if not header:
        return None
    seq = f.readline().rstrip("\n")
    plus = f.readline().rstrip("\n")
    qual = f.readline().rstrip("\n")
    if not (seq and plus and qual):
        return None
    return header.rstrip("\n"), seq, plus, qual


def open_output(name: str):
    """
    Open an output file named `name` inside the filtered/ directory
    (creating the directory if needed).

    Arguments:
    name: str — output file name

    Returns an opened file object in write mode.
    """
    os.makedirs("filtered", exist_ok=True)
    return open(os.path.join("filtered", name), "w")
