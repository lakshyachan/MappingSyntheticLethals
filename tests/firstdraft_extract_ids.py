import pandas as pd
import requests
from bs4 import BeautifulSoup

gene_data = pd.read_csv("/Users/lakshmichanemougam/Documents/IITM-Castle Project/external id/Escherichia coli 042.csv")
gene_data = gene_data.fillna('dummy')
gene_data['G:L'] = gene_data['G:L'].apply(lambda x: x.strip("'"))
base_url = "http://bigg.ucsd.edu/models/iEC042_1314/genes/"
gene_ids = list(gene_data['G:L'])
len(gene_ids)
gene_ids = list(filter(('dummy').__ne__, gene_ids))

### run this as for loop: inside 3 repetitive commands for sgd, dgd, tgd
full_url = base_url + gene_ids[0]
htmldoc = requests.get(full_url)
htmldoc.txt

soup = BeautifulSoup(htmldoc.text, 'html.parser')
soup.find_all('a')
gene_names = []
uniprot = []
interpro = []
goa = []
u = []
i = []
g = []

for link in soup.find_all('a'):
  if str(link.get('href')).startswith("http://identifiers"):
    url_parts = str(link.get('href')).split('/')
    if url_parts[-2] == 'uniprot':
      u.append(url_parts[-1])
    elif url_parts[-2] == 'interpro':
      i.append(url_parts[-1])
    elif url_parts[-2] == 'goa':
      g.append(url_parts[-1])

gene_names.append(gene_ids[0])
uniprot.append(','.join(u))
interpro.append(','.join(i))
goa.append(','.join(g))

mydf = pd.DataFrame(list(zip(gene_names,uniprot,interpro,goa)), columns=['gene_id','uniprot','interpro','goa'])
mydf.head()
### convert df to csv
