import gzip
import re
import os


def read_vcf(infile, log):
    # Read in (gzipped or not) and return line_count, list of headers and list of variants
    log.info(f"Reading in {infile}")

    # Check if file exists. Log if it doesn't.
    if os.path.exists(infile) == False:
        raise RuntimeError(f'Given file path "{infile}" could not be located')

    # Check if it ends in either .vcf or .vcf.gz
    if infile.endswith(".gz"):
        with gzip.open(infile, "rt") as f:
            line_count, headers, variants = separate_headers_and_variants(f, log)

    elif infile.endswith(".vcf"):
        with open(infile, "rt") as f:
            line_count, headers, variants = separate_headers_and_variants(f, log)

    else:
        raise RuntimeError(f'Given file "{infile}" must be in vcf or vcf.gz format')

    return line_count, headers, variants


def separate_headers_and_variants(f, log):
    headers = []
    variants = []
    line_count = 0

    for line in f:
        line_count += 1
        record = re.sub(" ", "", line.rstrip("\r\n"))
        if record.startswith("#"):
            headers.append(record)
        else:
            variants.append(record)

    return line_count, headers, variants


def add_to_headers(headers: list) -> list:
    headers_to_add = [
        '##INFO=<ID=AF,Number=A,Type=Float,Description="Allele frequency, for each ALT allele, in the same order as listed">',
        '##FORMAT=<ID=AD,Number=.,Type=Integer,Description="Number of reads harboring allele (in order specified by GT)">',
        '##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read depth">',
        '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">',
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE",
    ]
    for new_header in headers_to_add:
        if new_header not in headers:
            headers.insert(-1, new_header)

    return headers[:-1]


def write_vcf(headers: list, variants: list, outfile: str, compression: bool, log):
    log.info(f"Writing standardized VCF to {outfile}")

    if compression == True:
        with gzip.open(outfile, "wt") as w:
            vcf_out = "\n".join(headers + variants) + "\n"
            w.write(vcf_out)
    else:
        with open(outfile, "wt") as w:
            vcf_out = "\n".join(headers + variants) + "\n"
            w.write(vcf_out)

    return vcf_out
