import os


def gc_bounds(*bounds):
    if len(bounds) == 1:
        low, high = 0, bounds[0]
    elif len(bounds) == 2:
        low, high = bounds
    else:
        print("Ошибка. Функция ожидает от 1 до 2 аргументов")
        return (0, 0)
    if 0 <= low <= high <= 100:
        return (low, high)
    else:
        print("Ошибка. ")
        return (0, 0)


def check_gc(seq, gc_bounds):
    low, high = gc_bounds
    if not seq:
        gc_content = 0.0
    else:
        gc_count = sum(1 for n in seq if n in ("G", "C", "c", "g"))
        gc_content = gc_count / len(seq) * 100
    return low <= gc_content <= high


def check_length(seq, *length_bounds):
    if len(length_bounds) == 0:
        llow, lhigh = 0, 2**32
    if len(length_bounds) == 1:
        llow, lhigh = 0, length_bounds[0]
    elif len(length_bounds) == 2:
        llow, lhigh = length_bounds
    else:
        print("Ошибка. Функция ожидает от 1 до 2 аргументов")
        return (0, 0)
    if 0 <= llow <= lhigh <= 100:
        return (llow, lhigh)
    else:
        print("Ошибка. ")
        return (0, 0)


def check_quality(qual, quality_threshold):
    if not qual:
        return quality_threshold <= 0
    avg = sum(ord(c) - 33 for c in qual) / len(qual)
    return avg >= quality_threshold


def pass_filters(seq, qual, gc_bounds, length_bounds, quality_threshold):
    return (
        check_length(seq, length_bounds)
        and check_gc(seq, gc_bounds)
        and check_quality(qual, quality_threshold)
    )


def read_one(f):
    header = f.readline()
    if not header:
        return None
    seq = f.readline().rstrip("\n")
    plus = f.readline().rstrip("\n")
    qual = f.readline().rstrip("\n")
    if not (seq and plus and qual):
        return None
    return header.rstrip("\n"), seq, plus, qual


def open_output(name):
    os.makedirs("filtered", exist_ok=True)
    return open(os.path.join("filtered", name), "w")
