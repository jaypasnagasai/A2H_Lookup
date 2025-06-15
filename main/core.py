import pandas as pd
import ast
import builtins
import zipfile
import os

def read_tsv(path, sep="\t"):
    df = pd.read_csv(path, sep=sep)
    for col in df.columns:
        df[col] = df[col].astype(str).str.upper()
    return df

def read_tsv_from_zip(zip_path, filename_in_zip):
    with zipfile.ZipFile(zip_path) as z:
        with z.open(filename_in_zip) as f:
            df = pd.read_csv(f, sep="\t")
            for col in df.columns:
                df[col] = df[col].astype(str).str.upper()
            return df

def load_datasets():
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
    data_diseases = read_tsv(os.path.join(data_path, "data_diseases.tsv"))
    data_drugs = read_tsv(os.path.join(data_path, "data_drugs.tsv"))
    data_nct = read_tsv(os.path.join(data_path, "data_nct.tsv"))
    data_pmc = read_tsv_from_zip(os.path.join(data_path, "data_pmc.zip"), "data_pmc.tsv")
    return data_diseases, data_drugs, data_pmc, data_nct

def run_query(query, data_diseases, data_drugs, pmc_df, nct_df):
    query = query.strip().upper()
    builtins.shared_input = query

    if query in data_diseases["mesh_id"].values or \
       query in data_diseases["mesh_term"].values or \
       any(query in [t.strip().upper() for t in ast.literal_eval(str(entry))]
           for entry in data_diseases["entry_terms"]):
        print("INPUT TYPE: DISEASE")
        exec(open("biolookup/src/lookup_diseases.py").read())
        exec(open("biolookup/src/lookup_link.py").read())

    elif query in data_drugs["drug_name"].values:
        print("INPUT TYPE: DRUG")
        exec(open("biolookup/src/lookup_drugs.py").read())
        exec(open("biolookup/src/lookup_link.py").read())

    elif query in pmc_df["pmcid"].values:
        print("INPUT TYPE: PRECLINICAL PAPER [PMCID]")
        exec(open("biolookup/src/lookup_pmc.py").read())

    elif query in nct_df["nctid"].values:
        print("INPUT TYPE: CLINICAL PAPER [NCTID]")
        exec(open("biolookup/src/lookup_nct.py").read())

    else:
        print("Input not found in any dataset.")
