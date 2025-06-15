import pandas as pd
import ast
import builtins

query = builtins.shared_input

# Load the datasets
pc_df = pd.read_csv("data/data_pmc.tsv", sep="\t")
nct_df = pd.read_csv("data/data_nct.tsv", sep="\t")

def display_nct_related_info(input, pc_df, nct_df):
    query_nctid = input.strip().upper()
    output = [f"\nNCTID: {query_nctid}"]

    # Helper function to check if the given NCTID appears in the list
    def contains_nctid(val):
        try:
            studies = ast.literal_eval(str(val))
            return query_nctid in studies
        except:
            return False

    # Filter preclinical rows that reference this NCTID
    matches = pc_df[pc_df['matched_clinical_studies'].apply(contains_nctid)]

    if matches.empty:
        return "No data found."
    
    # Fetch study metadata
    nct_row = nct_df[nct_df['nctid'] == query_nctid]
    if not nct_row.empty:
        title = nct_row.iloc[0].get('nct_title', 'Not Available')
        link = nct_row.iloc[0].get('nct_link', f"https://clinicaltrials.gov/study/{query_nctid}")
        status = nct_row.iloc[0].get('status', 'Not Available')
        output.append("\nCLINICAL STUDY DETAILS")
        output.append(f"Title : {title}")
        output.append(f"Link  : {link}")
        output.append(f"Status: {status}")
    else:
        output.append("\nNo study metadata found in nct.tsv.")

    # Iterate through related preclinical articles
    seen = set()
    for _, row in matches.iterrows():
        pmcid = row.get('pmcid')
        mesh_id = row.get('mesh_id')
        mesh_term = row.get('mesh_term')
        key = (pmcid, mesh_id, mesh_term)

        if key in seen:
            continue
        seen.add(key)

        candidates = pc_df[pc_df['pmcid'] == pmcid]
        non_null_drugs = candidates['drug_name'].dropna().unique()
        drug_display = non_null_drugs[0] if len(non_null_drugs) > 0 else "N/A"

        pmc_title = row.get('pmc_title', 'Not Available')
        pmc_link = row.get('pmc_link', f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/")

        output.append("\nRELATED PMC ARTICLE")
        output.append(f"DRUG               : {drug_display}")
        output.append(f"MATCHED PMCID      : {pmcid}")
        output.append(f"MATCHED PMCID TITLE: {pmc_title}")
        output.append(f"MATCHED PMCID LINK : {pmc_link}")
        output.append(f"DISEASE MESH ID    : {mesh_id}")
        output.append(f"DISEASE MESH TERM  : {mesh_term}")

        related_studies = row.get('matched_clinical_studies', '')
        if related_studies and related_studies != "[]":
            output.append("\nRELATED CLINICAL STUDIES")
            try:
                for study in ast.literal_eval(related_studies):
                    output.append(f"  {study}")
            except:
                output.append(f"  {related_studies}")

    return "\n".join(output)

# Call and print
print(display_nct_related_info(query, pc_df, nct_df))