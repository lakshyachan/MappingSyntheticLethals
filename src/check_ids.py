import requests
import pandas as pd

# Getting the table data directly from the webpage
# `df` will be a list with 7 dataframes inside. One for each <table> in the webpage
# 1 Download Files + 3 Lethal Reactions + 3 Lethal Genes = 7 Tables = 7 Dataframes in `df`
df = pd.read_html('https://ramanlab.github.io/CASTLE/Synthetic_Lethal/Klebsiella_pneumoniae_subsp_pneumoniae_MGH_78578.html')
df_ = df[5] # `5` because 6th table in the webpage is Double lethal genes

# Extracting the gene pairs in double lethals into individual arrays
gene1 = df_[1].values
gene2 = df_[2].values

scores = []

## Construct URL
# Documentation: https://string-db.org/help//api/#getting-the-string-network-interactions
string_api_url = "https://version-11-5.string-db.org/api"
output_format = "json"
method = "network"

request_url = "/".join([string_api_url, output_format, method])

for a, b in zip(gene1, gene2):
    """
    For each gene pair, get interaction scores and store the scores in the
    `scores` list.
    """
    try:
        params = {

            "identifiers" : "%0d".join([a, b]),
            "species": 272620 # Taxon ID for the org (from UniProt)

        }

        ## Call STRING and get output as JSON

        response = requests.post(request_url, data=params)
        resp = response.json()[0]
        
        # Append gene names and score to `scores` list
        scores.append([a, b, resp['score']])
        
    except Exception as e:
        # If error, store empty string in place of the score
        scores.append([a, b, ''])

# Save the gene names and corresponding scores as CSV file
fname = 'scores_pneumoniae.csv'
pd.DataFrame(scores, columns=['gene1', 'gene2', 'score']).to_csv(fname, index=False)