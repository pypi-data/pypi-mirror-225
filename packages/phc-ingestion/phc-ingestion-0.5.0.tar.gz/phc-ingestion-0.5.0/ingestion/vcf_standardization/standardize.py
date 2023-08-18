from ingestion.vcf_standardization.util.read_write import read_vcf, add_to_headers, write_vcf
from ingestion.vcf_standardization.Variant import check_formatting
from logging import Logger

# TO DO: Add optional VENDSIG processing for supported vendors


def standardize_vcf(infile: str, outfile: str, log: Logger):
    approved_chr_list = [str(i) for i in range(1, 23)] + ["X", "Y", "MT"]
    approved_chr_list = approved_chr_list + ["chr" + i for i in approved_chr_list]
    compression = False
    if infile.endswith(".gz"):
        compression = True

    line_count, headers, variants = read_vcf(infile, log)

    standardized_variants = []
    for variant in variants:

        # Ignore structural variants
        if not "SVTYPE" in variant:

            # Working variant
            wv = check_formatting(variant)
            if wv.chr in approved_chr_list:

                if "AD" in wv.frmt:
                    wv.ad_af_dp.update({"AD": wv.smpl[wv.frmt.index("AD")]})

                wv.standardize_allele_frequency(log)

                wv.standardize_depth(log)

                wv.standardize_allelic_depth(log)

                updated_variant = wv.reassemble_variant()

                standardized_variants.append(updated_variant)

    standardized_headers = add_to_headers(headers)

    write_vcf(standardized_headers, standardized_variants, outfile, compression, log)

    return line_count
