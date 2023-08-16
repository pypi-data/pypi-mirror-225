"""
 Copyright (c) 2022 Antonio Fernandez-Guerra

 Permission is hereby granted, free of charge, to any person obtaining a copy of
 this software and associated documentation files (the "Software"), to deal in
 the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
 the Software, and to permit persons to whom the Software is furnished to do so,
 subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 """

import logging
from track_duplicates.utils import (
    get_arguments,
    process_bam,
    read_tsv,
    process_blast,
    process_lca,
)
import pandas as pd
import pysam
import tqdm
from collections import defaultdict


log = logging.getLogger("my_logger")


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s ::: %(asctime)s ::: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    args = get_arguments()
    logging.getLogger("my_logger").setLevel(
        logging.DEBUG if args.debug else logging.INFO
    )

    if args.bam is None and args.blast is None and args.lca is None:
        log.error("Please provide a BAM/SAM/CRAM or BLAST file...")
        exit()

    log.info("Starting track_duplicates...")
    log.debug(f"Arguments: {args}")
    log.info("Reading duplicates file...")

    filename = args.duplicates_file
    dups = read_tsv(filename, file_type="dups")

    log.info(f"Read {len(dups):,} reads from duplicates file...")
    columns = ["reference", "unique_reads", "n_reads", "singletons", "duplicates"]
    if args.bam is not None:
        log.info("Processing BAM file...")
        bam_results = process_bam(
            filename=args.bam,
            dups=dups,
            threads=args.threads,
            min_read_ani=args.min_read_ani,
            sort_memory=args.sort_memory,
        )
        df = (
            pd.DataFrame(bam_results)
            .transpose()
            .rename_axis("reference")
            .reset_index()
            .fillna(0)
        )
        log.info("::: Saving results...")
        df[columns].to_csv(args.output, sep="\t", index=False)

    if args.blast is not None:
        log.info("Processing BLAST file...")
        blast_results = process_blast(filename=args.blast, dups=dups)
        # log.info(f"Read {len(blast_results):,} reads from BLAST file...")
        df = (
            pd.DataFrame(blast_results)
            .transpose()
            .rename_axis("reference")
            .reset_index()
            .fillna(0)
        )
        log.info("::: Saving results...")
        df[columns].to_csv(args.blast_output, sep="\t", index=False)
    if args.lca is not None:
        log.info("Processing LCA file...")
        lca_results = process_lca(filename=args.lca, dups=dups)
        df = (
            pd.DataFrame(lca_results)
            .transpose()
            .rename_axis("reference")
            .reset_index()
            .fillna(0)
        )
        log.info("::: Saving results...")
        df[columns].to_csv(args.lca_output, sep="\t", index=False)
    log.info("Done!")
    exit()


if __name__ == "__main__":
    main()
