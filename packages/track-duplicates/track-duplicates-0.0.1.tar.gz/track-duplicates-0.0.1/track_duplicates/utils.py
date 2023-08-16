import argparse
import sys
import gzip
import os
import logging
import tqdm
from mimetypes import guess_type
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from os import devnull
from track_duplicates import __version__
import time
import json
from track_duplicates.defaults import mdmg_header, valid_ranks, filterBAM_header
from collections import defaultdict
from itertools import chain
import io
import mmap
from pathlib import Path
import pysam

log = logging.getLogger("my_logger")
log.setLevel(logging.INFO)
timestr = time.strftime("%Y%m%d-%H%M%S")


def is_debug():
    return logging.getLogger("my_logger").getEffectiveLevel() == logging.DEBUG


# From: https://note.nkmk.me/en/python-check-int-float/
def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


# function to check if the input value has K, M or G suffix in it
def check_suffix(val, parser, var):
    if var == "--scale":
        units = ["K", "M"]
    else:
        units = ["K", "M", "G"]
    unit = val[-1]
    value = int(val[:-1])

    if is_integer(value) & (unit in units) & (value > 0):
        if var == "--scale":
            if unit == "K":
                val = value * 1000
            elif unit == "M":
                val = value * 1000000
            elif unit == "G":
                val = value * 1000000000
            return val
        else:
            return val
    else:
        parser.error(
            "argument %s: Invalid value %s. Has to be an integer larger than 0 with the following suffix K, M or G"
            % (var, val)
        )


# From https://stackoverflow.com/a/59617044/15704171
def convert_list_to_str(lst):
    n = len(lst)
    if not n:
        return ""
    if n == 1:
        return lst[0]
    return ", ".join(lst[:-1]) + f" or {lst[-1]}"


def get_compression_type(filename):
    """
    Attempts to guess the compression (if any) on a file using the first few bytes.
    http://stackoverflow.com/questions/13044562
    """
    magic_dict = {
        "gz": (b"\x1f", b"\x8b", b"\x08"),
        "bz2": (b"\x42", b"\x5a", b"\x68"),
        "zip": (b"\x50", b"\x4b", b"\x03", b"\x04"),
    }
    max_len = max(len(x) for x in magic_dict)

    unknown_file = open(filename, "rb")
    file_start = unknown_file.read(max_len)
    unknown_file.close()
    compression_type = "plain"
    for file_type, magic_bytes in magic_dict.items():
        if file_start.startswith(magic_bytes):
            compression_type = file_type
    if compression_type == "bz2":
        sys.exit("Error: cannot use bzip2 format - use gzip instead")
        sys.exit("Error: cannot use zip format - use gzip instead")
    return compression_type


def get_open_func(filename):
    if get_compression_type(filename) == "gz":
        return gzip.open
    else:  # plain text
        return open


def check_values(val, minval, maxval, parser, var):
    value = float(val)
    if value < minval or value > maxval:
        parser.error(
            "argument %s: Invalid value %s. Range has to be between %s and %s!"
            % (
                var,
                value,
                minval,
                maxval,
            )
        )
    return value


# From: https://stackoverflow.com/a/11541450
def is_valid_file(parser, arg, var):
    if not os.path.exists(arg):
        parser.error("argument %s: The file %s does not exist!" % (var, arg))
    else:
        return arg


def is_valid_filter(parser, arg, var, type="metaDMG"):
    if type == "metaDMG":
        header = mdmg_header
    elif type == "filterBAM":
        header = filterBAM_header
    arg = json.loads(arg)
    # check if the dictionary keys are in the mdmg header list
    for key in arg.keys():
        if key not in header:
            parser.error(
                f"argument {var}: Invalid value {key}.\n"
                f"Valid values are: {convert_list_to_str(header)}"
            )

    return arg


def is_valid_rank(parser, arg, var):
    arg = json.loads(arg)
    for key in arg.keys():
        if key not in valid_ranks.keys():
            parser.error(
                f"argument {var}: Invalid value {key}.\n"
                f"Valid values are: {convert_list_to_str(valid_ranks)}"
            )
    return arg


def get_ranks(parser, ranks, var):
    valid_ranks = [
        "domain",
        "kingdom",
        "lineage",
        "phylum",
        "class",
        "order",
        "family",
        "genus",
        "species",
    ]
    ranks = ranks.split(",")
    # check if ranks are valid
    for rank in ranks:
        if rank not in valid_ranks:
            parser.error(
                f"argument {var}: Invalid value {rank}.\Rank has to be one of {convert_list_to_str(valid_ranks)}"
            )
        if rank == "all":
            ranks = valid_ranks[1:]
    return ranks


defaults = {
    "prefix": None,
    "sort_memory": "1G",
    "threads": 1,
    "chunk_size": None,
    "min_read_ani": 90.0,
    "blast_output": "blast-output.tsv.gz",
    "bam_output": "bam-output.tsv.gz",
    "lca_output": "lca-output.tsv.gz",
}

help_msg = {
    "bam": "A BAM file sorted by queryname",
    "blast": "A BLAST file in tabular format",
    "lca": "A LCA file in tabular format produced by metaDMG",
    "prefix": "Prefix used for the output files",
    "taxonomy_file": "A file containing the taxonomy of the BAM references in the format d__;p__;c__;o__;f__;g__;s__.",
    "duplicates_file": "A TSV file with the reads and number of duplicates.",
    "min_read_ani": "Minimum read ANI to keep a read",
    "sort_memory": "Set maximum memory per thread for sorting; suffix K/M/G recognized",
    "chunk_size": "Chunk size for parallel processing",
    "blast_output": "Save a TSV file with the statistics for each reference",
    "bam_output": "Save a TSV file with the statistics for each reference",
    "lca_output": "Save a TSV file with the statistics for each taxa",
    "threads": "Number of threads",
    "debug": "Print debug messages",
    "version": "Print program version",
}


def get_arguments(argv=None):
    parser = argparse.ArgumentParser(
        description="A simple tool to track duplicates on taxonomic and functional references.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # parent_parser = argparse.ArgumentParser(add_help=False)
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    required.add_argument(
        "-b",
        "--bam",
        type=lambda x: is_valid_file(parser, x, "--bam"),
        dest="bam",
        help=help_msg["bam"],
        required=False,
        metavar="FILE",
    )
    required.add_argument(
        "-B",
        "--blast",
        type=lambda x: is_valid_file(parser, x, "--blast"),
        dest="blast",
        help=help_msg["blast"],
        required=False,
        metavar="FILE",
    )
    required.add_argument(
        "-l",
        "--lca",
        type=lambda x: is_valid_file(parser, x, "--lca"),
        dest="lca",
        help=help_msg["lca"],
        required=False,
        metavar="FILE",
    )
    optional.add_argument(
        "-d",
        "--duplicates-file",
        required=True,
        type=lambda x: is_valid_file(parser, x, "---duplicate-file"),
        dest="duplicates_file",
        help=help_msg["duplicates_file"],
        metavar="FILE",
    )
    optional.add_argument(
        "-a",
        "--min-read-ani",
        type=lambda x: float(
            check_values(x, minval=0, maxval=100, parser=parser, var="--min-read-ani")
        ),
        metavar="FLOAT",
        default=defaults["min_read_ani"],
        dest="min_read_ani",
        help=help_msg["min_read_ani"],
    )
    optional.add_argument(
        "-m",
        "--sort-memory",
        type=lambda x: check_suffix(x, parser=parser, var="--sort-memory"),
        default=defaults["sort_memory"],
        dest="sort_memory",
        help=help_msg["sort_memory"],
        metavar="STR",
    )
    # optional.add_argument(
    #     "--chunk-size",
    #     type=lambda x: int(
    #         check_values(x, minval=1, maxval=100000, parser=parser, var="--chunk-size")
    #     ),
    #     default=defaults["chunk_size"],
    #     dest="chunk_size",
    #     help=help_msg["chunk_size"],
    #     metavar="INT",
    # )
    optional.add_argument(
        "-t",
        "--threads",
        type=lambda x: int(
            check_values(x, minval=1, maxval=1000, parser=parser, var="--threads")
        ),
        dest="threads",
        default=1,
        help=help_msg["threads"],
        metavar="INT",
    )
    optional.add_argument(
        "--blast-output",
        dest="blast_output",
        default=defaults["blast_output"],
        type=str,
        metavar="FILE",
        # nargs="?",
        # const="",
        required=False,
        help=help_msg["blast_output"],
    )
    optional.add_argument(
        "--bam-output",
        dest="output",
        default=defaults["bam_output"],
        type=str,
        metavar="FILE",
        # nargs="?",
        # const="",
        required=False,
        help=help_msg["bam_output"],
    )
    optional.add_argument(
        "--lca-output",
        dest="lca_output",
        default=defaults["lca_output"],
        type=str,
        metavar="FILE",
        # nargs="?",
        # const="",
        required=False,
        help=help_msg["lca_output"],
    )
    optional.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        help=help_msg["debug"],
    )
    optional.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + __version__,
        help=help_msg["version"],
    )
    args = parser.parse_args(None if sys.argv[1:] else ["-h"])
    return args


@contextmanager
def suppress_stdout():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, "w") as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


# From https://stackoverflow.com/a/61436083
def splitkeep(s, delimiter):
    split = s.split(delimiter)
    return [substr + delimiter for substr in split[:-1]] + [split[-1]]


def fast_flatten(input_list):
    return list(chain.from_iterable(input_list))


def initializer(init_data):
    global parms
    parms = init_data


# from https://stackoverflow.com/questions/53751050/python-multiprocessing-understanding-logic-behind-chunksize/54032744#54032744
def calc_chunksize(n_workers, len_iterable, factor=4):
    """Calculate chunksize argument for Pool-methods.

    Resembles source-code within `multiprocessing.pool.Pool._map_async`.
    """
    chunksize, extra = divmod(len_iterable, n_workers * factor)
    if extra:
        chunksize += 1
    return chunksize


def process_line_dups(line):
    return line.split("\t")[0:2]


def process_line_blast(line):
    line = line.split("\t")[0:2]
    line[0] = line[0].split("__")[0]
    return line


import re


def process_line_lca(line):
    # skip if it starts with #
    if line.startswith("#"):
        pass
    # split line
    l = line.split("\t")
    # cerate regex to parse
    pattern = r"(\S+):[ATCGN]+:\d+:\d+\S+"

    match = re.search(pattern, l[0])
    if match:
        read_id = match.group(1)
        return list([read_id, l[1]])
    else:
        pass


def read_tsv(filename, file_type="bam"):
    data = dict()

    if file_type == "dups":
        process_line = process_line_dups
    elif file_type == "blast":
        process_line = process_line_blast
    elif file_type == "lca":
        process_line = process_line_lca

    with open(filename, "rb") as f:
        encoding = guess_type(filename)[1]

        if encoding == "gzip":
            is_compressed = True
        else:
            is_compressed = False

        if is_compressed:
            decompressed_stream = gzip.open(f, "rt", encoding="utf-8")
            f.seek(0)
        else:
            decompressed_stream = io.TextIOWrapper(f, encoding="utf-8")
            f.seek(0)

        with tqdm.tqdm(
            unit="B", unit_scale=True, unit_divisor=1024, desc="Processed", leave=False
        ) as pbar:
            chunk_size = 8192  # Adjust the chunk size as needed
            remainder = ""
            while True:
                chunk = decompressed_stream.read(chunk_size)
                if not chunk:
                    break

                lines = (remainder + chunk).split("\n")
                remainder = lines.pop(-1)

                for line in lines:
                    row = process_line(line)

                    data[sys.intern(row[0])] = int(row[1])

                pbar.update(len(chunk))

        decompressed_stream.close()

        return data


def process_blast(filename, dups):
    process_line = process_line_blast
    seen = {}
    results = defaultdict(lambda: defaultdict(int))
    i = 0
    with open(filename, "rb") as f:
        encoding = guess_type(filename)[1]

        if encoding == "gzip":
            is_compressed = True
        else:
            is_compressed = False

        if is_compressed:
            decompressed_stream = gzip.open(f, "rt", encoding="utf-8")
            f.seek(0)
        else:
            decompressed_stream = io.TextIOWrapper(f, encoding="utf-8")
            f.seek(0)

        with tqdm.tqdm(
            unit="B", unit_scale=True, unit_divisor=1024, desc="Processed", leave=False
        ) as pbar:
            chunk_size = 8192  # Adjust the chunk size as needed
            remainder = ""
            while True:
                chunk = decompressed_stream.read(chunk_size)
                if not chunk:
                    break

                lines = (remainder + chunk).split("\n")
                remainder = lines.pop(-1)

                for line in lines:
                    i += 1
                    row = process_line(line)
                    qname = row[0]
                    reference_name = row[1]
                    comb = reference_name + qname
                    try:
                        dups[qname]
                        try:
                            seen[comb]
                            pass
                        except KeyError:
                            results[reference_name]["unique_reads"] += 1
                            counts = dups[qname]
                            if counts == 1:
                                results[reference_name]["singletons"] += 1
                                results[reference_name]["n_reads"] += 1
                            else:
                                results[reference_name]["n_reads"] += counts
                                results[reference_name]["duplicates"] += 1
                            seen[comb] = 1
                    except KeyError:
                        pass
                    # data[sys.intern(row[0])] = int(row[1])

                pbar.update(len(chunk))
        decompressed_stream.close()
        log.info(f"::: Found {i:,} alignments in BLAST file...")

        return results


def process_bam(filename, dups, threads, sort_memory="8G", min_read_ani=90):
    save = pysam.set_verbosity(0)
    bam = filename
    samfile = pysam.AlignmentFile(filename, "rb", threads=threads)

    # Check if BAM files is not sorted by coordinates, sort it by coordinates
    if not samfile.header["HD"]["SO"] == "queryname":
        log.info("BAM file is not sorted by coordinates, sorting it...")
        sorted_bam = bam.replace(".bam", ".td-sorted.bam")
        pysam.sort(
            "-n",
            "-@",
            str(threads),
            "-m",
            str(sort_memory),
            "-o",
            sorted_bam,
            bam,
        )
        bam = sorted_bam

        samfile.close()
        samfile = pysam.AlignmentFile(bam, "rb", threads=threads)

    pysam.set_verbosity(save)

    i = 0

    results = defaultdict(lambda: defaultdict(int))
    for aln in tqdm.tqdm(
        samfile.fetch(multiple_iterators=False, until_eof=True),
        desc="Processing alignments",
        leave=False,
        ncols=80,
        unit_scale=True,
        unit_divisor=1000,
        unit=" aln",
        disable=False,
    ):
        i += 1
        ani_read = (1 - ((aln.get_tag("NM") / aln.infer_query_length()))) * 100
        rname = aln.reference_name
        if ani_read >= min_read_ani:
            results[rname]["unique_reads"] += 1
            counts = dups[aln.qname]
            if counts == 1:
                results[rname]["singletons"] += 1
                results[rname]["n_reads"] += 1
            else:
                results[rname]["duplicates"] += 1
                results[rname]["n_reads"] += counts
    log.info(f"::: Found {i:,} alignments in BAM file...")
    return results


def process_lca(filename, dups):
    process_line = process_line_lca
    seen = {}
    results = defaultdict(lambda: defaultdict(int))
    i = 0
    with open(filename, "rb") as f:
        encoding = guess_type(filename)[1]

        if encoding == "gzip":
            is_compressed = True
        else:
            is_compressed = False

        if is_compressed:
            decompressed_stream = gzip.open(f, "rt", encoding="utf-8")
            f.seek(0)
        else:
            decompressed_stream = io.TextIOWrapper(f, encoding="utf-8")
            f.seek(0)

        with tqdm.tqdm(
            unit="B", unit_scale=True, unit_divisor=1024, desc="Processed", leave=False
        ) as pbar:
            chunk_size = 8192 * 10  # Adjust the chunk size as needed
            remainder = ""
            while True:
                chunk = decompressed_stream.read(chunk_size)
                if not chunk:
                    break

                lines = (remainder + chunk).split("\n")
                remainder = lines.pop(-1)

                for line in lines:
                    i += 1
                    row = process_line(line)
                    if row is None:
                        continue
                    qname = row[0]
                    reference_name = row[1]
                    comb = reference_name + qname
                    try:
                        dups[qname]
                        try:
                            seen[comb]
                            pass
                        except KeyError:
                            results[reference_name]["unique_reads"] += 1
                            counts = dups[qname]
                            if counts == 1:
                                results[reference_name]["singletons"] += 1
                                results[reference_name]["n_reads"] += 1
                            else:
                                results[reference_name]["n_reads"] += counts
                                results[reference_name]["duplicates"] += 1
                            seen[comb] = 1
                    except KeyError:
                        pass
                    # data[sys.intern(row[0])] = int(row[1])

                pbar.update(len(chunk))
        decompressed_stream.close()
        log.info(f"::: Found {i:,} alignments in BLAST file...")

        return results
