import pandas as pd
import builtins

query = builtins.shared_input

# Load the PMC data
df = pd.read_csv("data/data_pmc.tsv", sep="\t")

def display_pmc_info(input, df):
    query_pmcid = input.strip().upper()
    matches = df[df["pmcid"].str.upper() == query_pmcid]

    if matches.empty:
        return f"No entry found for {query_pmcid}"

    output = [f"\nPMCID: {query_pmcid}"]

    # --- PMC NAME & LINK ---
    pmc_title = matches["pmc_title"].iloc[0] if "pmc_title" in matches else "N/A"
    pmc_link = matches["pmc_link"].iloc[0] if "pmc_link" in matches else "N/A"
    output.append(f"NAME: {pmc_title}")
    output.append(f"LINK: {pmc_link}\n")

    # --- DISEASE SECTION ---
    output.append("DISEASE")
    disease_seen = set()
    for _, row in matches.iterrows():
        term = str(row["mesh_term"])
        mesh_id = str(row["mesh_id"])
        if (term, mesh_id) not in disease_seen:
            output.append(term)
            output.append(f"\t{mesh_id}")
            disease_seen.add((term, mesh_id))

    # --- DRUG TERMS ---
    output.append("\nDRUG TERMS")
    for drug in matches["drug_name"].dropna().unique():
        output.append(f"\t{drug}")

    # --- CLINICAL COUNT ---
    output.append("\nCLINICAL COUNT")
    for drug in matches["drug_name"].dropna().unique():
        count = matches[matches["drug_name"] == drug]["clinical_count"].iloc[0]
        output.append(f"{drug}\n\t{count}")

    # --- MATCHED CLINICAL STUDIES ---
    output.append("\nMATCHED CLINICAL STUDIES")
    for drug in matches["drug_name"].dropna().unique():
        output.append(drug)
        rows = matches[matches["drug_name"] == drug]
        studies = rows["matched_clinical_studies"].dropna().tolist()
        if studies:
            nct_ids = set()
            for study_list in studies:
                try:
                    items = eval(study_list) if study_list.startswith("[") else [study_list]
                    for item in items:
                        nct_ids.add(item)
                except Exception:
                    continue
            for nct in sorted(nct_ids):
                output.append(f"\t{nct}")
        else:
            output.append("\tN/A")

    return "\n".join(output)

# Run and print result
print(display_pmc_info(query, df))