import pandas as pd
import ast
import builtins

query = builtins.shared_input

# Load datasets
pc_df = pd.read_csv("data/data_pmc.tsv", sep="\t")
nct_df = pd.read_csv("data/data_nct.tsv", sep="\t")

def parse_terms(x):
    try:
        terms = ast.literal_eval(x)
        return [str(t).upper() for t in terms]
    except:
        return []

def format_output(pmcid, pmc_title, nctid, nct_title, status):
    return (
        f"{pmcid} | {nctid}\n\n"
        f"PRECLINICAL INFO\n"
        f" PMCID: {pmcid}\n"
        f"  TITLE: {pmc_title if pmc_title else 'Not Available'}\n"
        f"  LINK: https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/\n\n"
        f"CLINICAL INFO\n"
        f" NCTID: {nctid}\n"
        f"  TITLE: {nct_title if nct_title else 'Not Available'}\n"
        f"  LINK: https://clinicaltrials.gov/study/{nctid}\n"
        f"  STATUS: {status if status else 'Not Available'}\n"
    )

def display_linked_pairs(input, pc_df, nct_df):
    query = input.strip().upper()

    # Normalize
    for col in ["mesh_id", "mesh_term", "drug_name"]:
        pc_df[col] = pc_df[col].astype(str).str.upper()

    pc_df["entry_terms"] = pc_df["entry_terms"].astype(str).apply(parse_terms)
    pc_df["pmcid"] = pc_df["pmcid"].astype(str).str.upper()
    pc_df["pmc_title"] = pc_df.get("pmc_title", "")

    nct_df["nctid"] = nct_df["nctid"].astype(str).str.upper()
    nct_title_map = dict(zip(nct_df["nctid"], nct_df["nct_title"]))
    nct_status_map = dict(zip(nct_df["nctid"], nct_df["status"]))

    matches = pc_df[
        (pc_df["mesh_id"] == query) |
        (pc_df["mesh_term"] == query) |
        (pc_df["drug_name"] == query) |
        (pc_df["entry_terms"].apply(lambda terms: query in terms))
    ]

    if matches.empty:
        return "No matches found."

    output = []
    seen = set()

    for _, row in matches.iterrows():
        pmcid = row["pmcid"]
        pmc_title = row.get("pmc_title", "")
        try:
            nctids = ast.literal_eval(str(row["matched_clinical_studies"]))
        except:
            nctids = []

        for nctid in nctids:
            pair = (pmcid, nctid)
            if pair in seen:
                continue
            seen.add(pair)
            output.append(format_output(
                pmcid,
                pmc_title,
                nctid,
                nct_title_map.get(nctid, ""),
                nct_status_map.get(nctid, "")
            ))

    output.append(f"Total unique linked pairs: {len(seen)}")
    return "\n".join(output)

# Run and print result
print(display_linked_pairs(query, pc_df, nct_df))