
# trackDups: a tool to identify which taxa or function has read duplicates


[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/genomewalker/track-duplicates?include_prereleases&label=version)](https://github.com/genomewalker/track-duplicates/releases) [![track-duplicates](https://github.com/genomewalker/track-duplicates/workflows/trackDups_ci/badge.svg)](https://github.com/genomewalker/track-duplicates/actions) [![PyPI](https://img.shields.io/pypi/v/track-duplicates)](https://pypi.org/project/track-duplicates/) [![Conda](https://img.shields.io/conda/v/genomewalker/track-duplicates)](https://anaconda.org/genomewalker/track-duplicates)

A simple tool to extract reads from specific taxonomic groups BAM files

# Installation

We recommend having [**conda**](https://docs.conda.io/en/latest/) or [**mamba**](https://github.com/mamba-org/mamba) installed to manage the virtual environments

### Using pip

First, we create a conda virtual environment with:

```bash
wget https://raw.githubusercontent.com/genomewalker/track-duplicates/master/environment.yml
conda env create -f environment.yml
```

Then we proceed to install using pip:

```bash
pip install track-duplicates
```

### Using mamba

```bash
mamba install -c conda-forge -c bioconda -c genomewalker track-duplicates
```

### Install from source to use the development version

Using pip

```bash
pip install git+ssh://git@github.com/genomewalker/track-duplicates.git
```

By cloning in a dedicated conda environment

```bash
git clone https://github.com/genomewalker/track-duplicates.git
cd track-duplicates
conda env create -f environment.yml
conda activate track-duplicates
pip install -e .
```


# Usage

trackDups will take a BAM/SAM/CRAM or a blast-m8 like file and a TSV file with read duplicates to track those duplicates over references.

For a complete list of options:

```bash
$ trackDups --help 
usage: trackDups [-h] [-b FILE] [-B FILE] [-l FILE] -d FILE [-a FLOAT] [-m STR] [-t INT]
                 [--blast-output FILE] [--bam-output FILE] [--lca-output FILE] [--debug]
                 [--version]

A simple tool to track duplicates on taxonomic and functional references.

optional arguments:
  -h, --help            show this help message and exit

required arguments:
  -b FILE, --bam FILE   A BAM file sorted by queryname (default: None)
  -B FILE, --blast FILE
                        A BLAST file in tabular format (default: None)
  -l FILE, --lca FILE   A LCA file in tabular format produced by metaDMG (default: None)

optional arguments:
  -d FILE, --duplicates-file FILE
                        A TSV file with the reads and number of duplicates. (default: None)
  -a FLOAT, --min-read-ani FLOAT
                        Minimum read ANI to keep a read (default: 90.0)
  -m STR, --sort-memory STR
                        Set maximum memory per thread for sorting; suffix K/M/G recognized
                        (default: 1G)
  -t INT, --threads INT
                        Number of threads (default: 1)
  --blast-output FILE   Save a TSV file with the statistics for each reference (default:
                        blast-output.tsv.gz)
  --bam-output FILE     Save a TSV file with the statistics for each reference (default: bam-
                        output.tsv.gz)
  --lca-output FILE     Save a TSV file with the statistics for each taxa (default: lca-
                        output.tsv.gz)
  --debug               Print debug messages (default: False)
  --version             Print program version
```

One would run `trackDups` as:

```bash
trackDups -d mysample.counts.tsv.gz --bam mysample.bam --threads 8  -a 95
```
> **Note**: A read might be counted more than once if it is mapping to different locations in the same reference.
