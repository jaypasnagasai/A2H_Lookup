from .core import load_datasets, run_query

def main():
    data_diseases, data_drugs, pmc_df, nct_df = load_datasets()
    while True:
        query = input("\nENTER [Q TO QUIT]: ").strip().upper()
        if query == "Q":
            print("Exiting.")
            break
        run_query(query, data_diseases, data_drugs, pmc_df, nct_df)
