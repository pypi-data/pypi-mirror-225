# Overview

[![Testing](https://github.com/EBI-Metagenomics/combined-gene-caller/actions/workflows/test.yml/badge.svg)](https://github.com/EBI-Metagenomics/combined-gene-caller/actions/workflows/test.yml)
[![Docker Repository on Quay](https://quay.io/repository/microbiome-informatics/combined-gene-caller/status "Docker Repository on Quay")](https://quay.io/repository/microbiome-informatics/combined-gene-caller)

Combined gene caller for MGnify pipeline, to combine predictions of Prodigal and FragGeneScan.

-   Free software: Apache Software License 2.0

## Installation

```bash
pip install https://github.com/ebi-metagenomics/combined-gene-caller/archive/main.zip
```

## Usage

To use the project:

```bash
combined_gene_caller --help
usage: MGnify gene caller combiner. This script will merge the gene called by prodigal and fraggenescan (in any order) [-h] -n NAME [-k MASK] [-a PRODIGAL_OUT]
                                                                                                                       [-b PRODIGAL_FFN] [-c PRODIGAL_FAA] [-d FGS_OUT]
                                                                                                                       [-e FGS_FFN] [-f FGS_FAA]
                                                                                                                       [-p {prodigal_fgs,fgs_prodigal}] [-v] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  basename
  -k MASK, --mask MASK  Sequence mask file
  -a PRODIGAL_OUT, --prodigal-out PRODIGAL_OUT
                        Stats out prodigal
  -b PRODIGAL_FFN, --prodigal-ffn PRODIGAL_FFN
                        Stats ffn prodigal
  -c PRODIGAL_FAA, --prodigal-faa PRODIGAL_FAA
                        Stats faa prodigal
  -d FGS_OUT, --fgs-out FGS_OUT
                        Stats out FGS
  -e FGS_FFN, --fgs-ffn FGS_FFN
                        Stats ffn FGS
  -f FGS_FAA, --fgs-faa FGS_FAA
                        Stats faa FGS
  -p {prodigal_fgs,fgs_prodigal}, --caller-priority {prodigal_fgs,fgs_prodigal}
                        Caller priority.
  -v, --verbose         verbose output
  --version             show program's version number and exit
```

## Development

To run all the tests run:

    pytest
