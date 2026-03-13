# VEP REST API Demo

A demo script for annotating variants with the Ensembl VEP REST API.

## To run the demo

```bash
python3 vep_single_variant_demo.py
```

## What it does

1. Sends **one variant** (example here is `chr1:3329040 A>C`) to the GRCh37 VEP API using `vep/human/region`  
2. Receives the annotated JSON response
3. Prints key fields: gene, consequence, HGVS notation, impact
4. Saves the full JSON to `vep_response_example.json`
5. Parse the JSON to save it to a more user friendly csv file.  

## Format of input variant

```
# Format: "CHROM START END REF/ALT STRAND"
# Example SNV: 1 3329040 3329040 A/C 1
# Example indel: 1 3322113 3322112 -/CCGA 1
```

## API reference

- **Endpoint:** `https://grch37.rest.ensembl.org/vep/human/region`
- **Method:** POST
- **Body:** JSON with `variants` array and optional parameters
- **Docs:** https://rest.ensembl.org/documentation/info/vep_region_post
