#!/usr/bin/env python3
"""
Annotate one variant using the Ensembl VEP REST API (GRCh37).

Outputs: JSON (full API response) and CSV (easy to view table).

Usage:
    python3 vep_single_variant_demo.py

Example variant: chr1:3329040 A>C
"""

import csv
import json
import os
import requests

# ### Configuration ###
# GRCh37 VEP API (use grch37 for human genome build 37)
VEP_URL = "https://grch37.rest.ensembl.org/vep/human/region"

# One variant in VEP "region" format: "chr start end allele strand"
VARIANT = "1 3329040 3329040 A/C 1"

# Request headers
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# VEP parameters (similar to our vendor's previous format)
VEP_PARAMS = {
    "canonical": True,
    "merged": True,
    "ambiguous_hgvs": True,
    "numbers": True,
    "everything": True,
    "regulatory": True,
    "distance": 8000,
    "transcript_version": True,
    "hgvs": True,
}


def annotate_variant(variant_region):
    """
    Send a variant to the VEP API and return the annotated result.
    """
    payload = {
        "variants": [variant_region],
        **VEP_PARAMS,
    }

    response = requests.post(VEP_URL, headers=HEADERS, json=payload)

    # Check for errors
    response.raise_for_status()

    return response.json()


CSV_COLUMNS = [
    "Input",
    "Coordinate",
    "Gene",
    "Most_severe_consequence",
    "Impact",
    "Canonical_HGVS_Coding",
    "Canonical_HGVS_Protein",
    "Exon",
    "Transcript",
    "Biotype",
]


def result_to_row(result):
    """save CSV output from JSON"""
    transcripts = result.get("transcript_consequences", [])
    canonical = next((t for t in transcripts if t.get("canonical")), transcripts[0]) if transcripts else {}

    chrom = result.get("seq_region_name", "")
    start = result.get("start", "")
    end = result.get("end", "")
    coord = f"{chrom}:{start}-{end}" if chrom else ""

    return {
        "Input": result.get("input", ""),
        "Coordinate": coord,
        "Gene": canonical.get("gene_symbol", ""),
        "Most_severe_consequence": result.get("most_severe_consequence", ""),
        "Impact": canonical.get("impact", ""),
        "Canonical_HGVS_Coding": canonical.get("hgvsc", ""),
        "Canonical_HGVS_Protein": canonical.get("hgvsp", ""),
        "Exon": canonical.get("exon", ""),
        "Transcript": canonical.get("transcript_id", ""),
        "Biotype": canonical.get("biotype", ""),
    }


def write_json(results, path):
    """Save the entire API response as JSON"""
    with open(path, "w") as f:
        json.dump(results, f, indent=2)


def write_csv(results, path):
    """Save annotated variants as a CSV table."""
    rows = [result_to_row(r) for r in results]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main():
    # Output paths for an example 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "vep_response.json")
    csv_path = os.path.join(script_dir, "vep_variants.csv")

    results = annotate_variant(VARIANT)

    if not results:
        print("No results returned from VEP API.")
        return

    # save JSON outputs
    write_json(results, json_path)
    print(f"JSON saved to: {json_path}")

    # save CSV outputs
    write_csv(results, csv_path)
    print(f"CSV saved to: {csv_path}")
    print(f"  ({len(results)} variant(s))")
    print("\nDone.")


if __name__ == "__main__":
    main()
