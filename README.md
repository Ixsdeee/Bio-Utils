# Bio-Utils

A small collection of pure-Python utilities for working with biological files: FASTQ filtering, FASTA reformatting, and BLAST output parsing. Standard library only — no external dependencies.

## Project structure

    Bio-Utils/
    ├── main.py              # filter_fastq, convert_multiline_fasta_to_oneline, parse_blast_output
    ├── helpers/
    │   ├── fastq.py         # FASTQ helpers
    │   └── bio_files.py     # file helpers
    ├── data/                # example inputs
    └── filtered/            # output for filter_fastq (auto-created)

## Functions

### `filter_fastq(input_fastq, output_fastq, gc_bounds=(0, 100), length_bounds=(0, 2**32), quality_threshold=0)`

Filters a FASTQ file by GC content, length and average read quality. Reads one record at a time.

- `gc_bounds`, `length_bounds` — tuple or single number (single number = upper bound, lower = 0).
- `quality_threshold` — Phred+33 average quality threshold.
- Writes surviving reads to `filtered/<output_fastq>`.

```python
from main import filter_fastq

filter_fastq(
    "data/example_fastq.fastq",
    "strict.txt",
    gc_bounds=(20, 80),
    length_bounds=(50, 100),
    quality_threshold=30,
)
```
### `convert_multiline_fasta_to_oneline(input_fasta, output_fasta=None)`

Converts a multiline FASTA into "one line per sequence" format. If output_fasta is None, the name is generated as <base>_oneline<ext>.

```python
from main import convert_multiline_fasta_to_oneline

convert_multiline_fasta_to_oneline("data/seq.fasta", "data/seq_one_line.fasta")
```
###parse_blast_output(input_file, output_file)

Extracts the best-hit description per query from a BLAST txt report, deduplicates and writes them alphabetically to output_file.

```python
from main import parse_blast_output

parse_blast_output("data/example_blast_results.txt", "top_hits.txt")
```
## Requirements
Python 3.10+ (uses str | None annotations). Standard library only.


