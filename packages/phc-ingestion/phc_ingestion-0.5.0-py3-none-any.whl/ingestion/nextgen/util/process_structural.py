import pandas as pd
from logging import Logger

from ingestion.shared_util.coords_to_genes import coords_to_genes
from ingestion.nextgen.util.variant_table import extract_variant_table
from ingestion.nextgen.util.interpretation import map_interpretation


def process_structural(sv_in_file: str, xml_in_file, root_path: str, prefix: str, log: Logger):
    structural_variant_table = extract_variant_table(
        xml_in_file=xml_in_file, variant_type="structural", log=log
    )

    structural_variant_path_name = f"{root_path}/{prefix}.structural.csv"
    sample_id = prefix

    with open(sv_in_file, "r") as f:
        variants = [line for line in f.readlines() if not line.startswith("#")]

    if not variants:
        log.info(f"No structural variants found in {sv_in_file}")
        structural_status = False
        return None, structural_status

    structural_variant_rows = []
    structural_status = True
    for variant in variants:
        working_variant = variant.strip().split("\t")

        chromosome1 = f"chr{working_variant[0]}"
        start_position1 = working_variant[1]

        if "MantaDEL" in working_variant[2] or "MantaDUP" in working_variant[2]:
            end_position1 = working_variant[7].split(";")[0].split("=")[1]
            chromosome2 = chromosome1
            start_position2 = start_position1
            end_position2 = end_position1
            effect = "deletion" if "MantaDEL" in working_variant[2] else "duplication"

            # Get genes from coordinates using center point of start and end positions
            gene1 = coords_to_genes(
                "GRCh38", chromosome1, int((int(start_position1) + int(end_position1)) / 2), log
            )
            gene2 = "N/A"

        else:
            alt = working_variant[4].strip("][TCGA").split(":")

            end_position1 = start_position1
            chromosome2 = f"chr{alt[0]}"
            start_position2 = alt[1]
            end_position2 = alt[1]
            effect = "translocation"

            # Get genes from coordinates using center point of start and end positions
            gene1 = coords_to_genes(
                "GRCh38", chromosome1, int((int(start_position1) + int(end_position1)) / 2), log
            )
            gene2 = coords_to_genes(
                "GRCh38", chromosome2, int((int(start_position2) + int(end_position2)) / 2), log
            )

        # Scrape interpretation
        interpretation = None
        if not structural_variant_table.empty:
            for index, row in structural_variant_table.iterrows():
                ref_gene1 = row["gene"].split(" ")[0].split("-")[0]
                ref_coord = row["gene"].split(" ")[1].split(";")[0].strip("(")

                if ref_gene1 == gene1 and ref_coord == f"{chromosome1}:{start_position1}":
                    interpretation = map_interpretation(row["info"], log)

        if not interpretation:
            interpretation = "unknown"

        # Hard-code
        sequence_type = "Somatic"
        in_frame = "Unknown"
        attributes = {}

        structural_variant_rows.append(
            f"{sample_id},{gene1},{gene2},{effect},{chromosome1},{start_position1},{end_position1},{chromosome2},{start_position2},{end_position2},{interpretation},{sequence_type},{in_frame},{attributes}\n"
        )

    log.info(f"Saving file to {structural_variant_path_name}")
    with open(structural_variant_path_name, "w+") as f:
        f.write(
            "sample_id,gene1,gene2,effect,chromosome1,start_position1,end_position1,chromosome2,start_position2,end_position2,interpretation,sequence_type,in-frame,attributes\n"
        )
        for sv_text_row in structural_variant_rows:
            f.write(sv_text_row)

    return structural_variant_path_name, structural_status
