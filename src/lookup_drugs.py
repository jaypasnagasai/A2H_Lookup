import pandas as pd
import builtins

# Use the shared input from main.py
query = builtins.shared_input

# Load the drug dataset
data_drugs = pd.read_csv("data/data_drugs.tsv", sep="\t")

# Normalize text
data_drugs["drug_name"] = data_drugs["drug_name"].astype(str).str.lower()

def display_drug_info(drug_query, df):
    drug_query = drug_query.strip().lower()
    
    # Filter matching rows
    matches = df[df['drug_name'] == drug_query]

    if matches.empty:
        return f"No matches found for: {drug_query}"
    
    # Variables for summary
    drug_name = drug_query
    num_diseases_linked = matches.shape[0]
    total_preclinical_count = matches['p_count'].sum()
    total_clinical_count = matches['c_count'].sum()

    # Build output
    output = []
    output.append("\nDRUG SUMMARY")
    output.append(f"Drug Name: {drug_name}")
    output.append(f"# of Diseases Linked: {num_diseases_linked}")
    output.append(f"Preclinical Count: {total_preclinical_count}")
    output.append(f"Clinical Count: {total_clinical_count}")

    output.append("\nDISEASE BREAKDOWN")
    for _, row in matches.iterrows():
        mesh_id = row['mesh_id']
        mesh_term = row['mesh_term']
        p_count = row['p_count']
        c_count = row['c_count']

        output.append(f"MeSH ID: {mesh_id}")
        output.append(f"MeSH Term: {mesh_term}")
        output.append(f"\tPreclinical Count: {p_count}")
        output.append(f"\tClinical Count: {c_count}")

    return "\n".join(output)

# Call the function and print the result
print(display_drug_info(query, data_drugs))
