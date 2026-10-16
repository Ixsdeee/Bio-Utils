import os


def default_output_name(input_fasta: str) -> str:
    """
    Return the default output file name for a converted FASTA file.

    Arguments:
    input_fasta: str — path to the input FASTA file

    Returns str: file name of the form <base>_oneline<ext>, e.g. "seq_oneline.fasta".
    """
    base, ext = os.path.splitext(input_fasta)
    return f"{base}_oneline{ext or '.fasta'}"
