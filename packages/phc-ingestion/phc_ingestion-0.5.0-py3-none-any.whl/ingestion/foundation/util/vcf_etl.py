import gzip
import xmltodict
from natsort import natsorted
from logging import Logger
import re
import os
import errno


def vcf_etl(in_vcf: str, out_vcf: str, base_xml_name: str, xml_file: str, log: Logger) -> int:
    headers = []
    vars = []

    # Get xml short variant entries for scraping vendsig
    xml_short_vars = get_xml_short_vars(xml_file, log)

    if not os.path.exists(os.path.dirname(out_vcf)):
        try:
            os.makedirs(os.path.dirname(out_vcf))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    with open(in_vcf) as f:
        lines = f.readlines()
        line_count = len(lines)
        if line_count == 0:
            return line_count
        else:
            for line in lines:
                if line.startswith("#"):
                    headers.append(line)
                else:
                    vars.append(line)

            sorted_vars = natsorted(vars)

            with gzip.open(f"{out_vcf}.gz", "wt") as w:
                for header in headers:
                    if "=af," in header:
                        header = header.replace("=af", "=AF")

                    if "#CHROM" in header:
                        w.write('##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">\n')
                        w.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
                        w.write(
                            '##FORMAT=<ID=AD,Number=.,Type=Integer,Description="Number of reads harboring allele (in order specified by GT)">\n'
                        )
                        w.write(
                            '##INFO=<ID=VENDSIG,Number=1,Type=String,Description="Vendor Significance">\n'
                        )
                        header = header.strip("\n") + "\tFORMAT\t" + base_xml_name + "\n"

                    w.write(header)

                for var in sorted_vars:
                    var = var.replace("af=", "AF=")
                    var = transform_scientific_notation_in_af(var)
                    untouched_var = "\t".join(var.split("\t")[0:7])
                    new_vcf_info = add_vendsig_to_info(var, xml_short_vars)
                    af_match = re.search(r"AF=(\d*\.?\d*)", var)
                    if not af_match:
                        raise RuntimeError("Failed to find AF for var")
                    af = float(af_match.group(1))
                    depth_match = re.search(r"depth=(\d*\.?\d*)", var)
                    if not depth_match:
                        raise RuntimeError("Failed to find depth for var")
                    depth = int(depth_match.group(1))
                    alt_depth = int(round(depth * af))
                    ref_depth = depth - alt_depth
                    ad = f"{ref_depth},{alt_depth}"
                    gt = "1/1" if af > 0.9 else "0/1"
                    vcf_format = "GT:DP:AD"
                    sample = ":".join([gt, str(depth), ad])
                    var = untouched_var + f"\t{new_vcf_info}\t{vcf_format}\t{sample}\n"
                    w.write(var)

            return line_count


def get_xml_short_vars(xml_file: str, log) -> dict:
    with open(xml_file) as fd:
        xml_dict = xmltodict.parse(fd.read())
    try:
        xml_short_vars = xml_dict["rr:ResultsReport"]["rr:ResultsPayload"]["variant-report"][
            "short-variants"
        ]["short-variant"]
    except TypeError:
        log.info("No short variants found in xml")
        return {}
    return xml_short_vars


def map_vendsig(vendsig: str) -> str:
    if vendsig in ["known"]:
        return "VENDSIG=Pathogenic"
    elif vendsig in ["likely"]:
        return "VENDSIG=Likely pathogenic"
    elif vendsig in ["unknown"]:
        return "VENDSIG=Uncertain significance"
    else:
        return "VENDSIG=Unknown"


def add_vendsig_to_info(var: str, xml_short_vars: dict) -> str:
    split_var = var.split("\t")
    # get 'chr:pos' from var
    var_position = f"{split_var[0]}:{split_var[1]}"

    # Info section -> dict, get depth
    info_dict = {x.split("=")[0]: x.split("=")[1] for x in split_var[7].split(";") if "=" in x}
    var_depth = info_dict["depth"]

    # dictionary comprehension to get the short_var in xml_short_vars that matches the transcript_name
    if xml_short_vars == {}:
        vendsig = "Unknown"
    else:
        if isinstance(xml_short_vars, dict):
            xml_short_vars = [xml_short_vars]

        matched_xml_var = [
            short_var
            for short_var in xml_short_vars
            if short_var.get("@position", "") == var_position
            and short_var.get("@depth", "") == var_depth
        ]
        if not matched_xml_var:
            vendsig = "Unknown"
        else:
            vendsig = matched_xml_var[0]["@status"]

    mapped_vendsig = map_vendsig(vendsig)
    new_vcf_info = f"{split_var[7].strip()};{mapped_vendsig}"
    return new_vcf_info


def transform_scientific_notation_in_af(var: str) -> str:
    var_split = var.split("\t")
    var_info = var_split[-1]
    var_info_split = var_info.split(";")
    var_info_list = [x for x in var_info_split if x.startswith("AF=")]

    # No AF= in line so lets return as is and move on
    if len(var_info_list) != 1:
        return var
    var_info_af = var_info_list[0]
    af_split = var_info_af.split("=")
    af_original_value = af_split[1]
    af_float_value = float(af_original_value)
    var = var.replace(af_original_value, str(af_float_value))
    return var
