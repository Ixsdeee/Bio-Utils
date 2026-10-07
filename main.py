from helpers.fastq import read_one, open_output, pass_filters


def filter_fastq(
    input_fastq,
    output_fastq,
    gc_bounds=(0, 100),
    length_bounds=(0, 2**32),
    quality_threshold=0,
):
    with open(input_fastq) as inp, open_output as out:
        while True:
            read = read_one(inp)
            if read is None:
                break
            header, seq, plus, qual = read
            if pass_filters(seq, qual, gc_bounds, length_bounds, quality_threshold):
                out.write(f"{header}\n{seq}\n{plus}\n{qual}\n")
