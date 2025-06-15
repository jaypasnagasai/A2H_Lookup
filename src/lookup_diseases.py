import pandas as pd
import re
import ast
import builtins

query = builtins.shared_input

# Load the disease dataset
data_diseases = pd.read_csv("data/data_diseases.tsv", sep="\t")

def display_mesh_info(input, df):
    query = input.strip().lower()

    def match_row(row):
        if str(row["mesh_id"]).lower() == query:
            return True
        if str(row["mesh_term"]).lower() == query:
            return True
        try:
            terms = ast.literal_eval(str(row["entry_terms"]))
            return query in [t.lower() for t in terms]
        except:
            return False

    match = df[df.apply(match_row, axis=1)]

    if match.empty:
        return f"No data found for: {input}"

    row = match.iloc[0]
    mesh_id = row["mesh_id"]
    mesh_term = row["mesh_term"]
    p_count = row["p_count"]
    c_count = row["c_count"]
    child_nodes = row["child_nodes"]
    drug_names = row["drug_names"]
    is_specific = row.get("is_specific", False)

    output = []
    output.append(f"\nMesh ID: {mesh_id}")
    output.append(f"Mesh Term: {mesh_term}")
    output.append(f"Type Of Disease: {'Specific' if is_specific else 'Non-Specific'}")

    output.append("PUBLICATION STATS")
    output.append(f"\tPreclinical Count: {p_count}")
    output.append(f"\tClinical Count: {c_count}")

    output.append("CHILD NODES")
    if pd.isna(child_nodes) or child_nodes.strip() == '':
        output.append("\tNone")
    else:
        matches = re.findall(r'([^\[\]]+)\s*\[p=(\d+),\s*c=(\d+)\]', child_nodes)
        for term, p, c in matches:
            output.append(f"\t{term.strip()}\n\t\tPreclinical Count: {p}\n\t\tClinical Count: {c}")

    output.append("DRUG")
    if pd.isna(drug_names) or drug_names.strip() == '':
        output.append("\tNone")
    else:
        try:
            drug_list = ast.literal_eval(drug_names)
            for entry in drug_list:
                drug_match = re.match(r"(.*?)\s*\(p_count\s*=\s*(\d+),\s*c_count\s*=\s*(\d+)\)", entry)
                if drug_match:
                    name = drug_match.group(1).strip()
                    p = drug_match.group(2)
                    c = drug_match.group(3)
                    output.append(f"\t{name}\n\t\tPreclinical Count: {p}\n\t\tClinical Count: {c}")
        except Exception as e:
            output.append(f"\tError parsing drug names: {e}")

    return "\n".join(output)

# Run and print result
print(display_mesh_info(query, data_diseases))