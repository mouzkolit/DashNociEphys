from physioweb.models import GeneMapHuman
import pandas as pd

def run():
    csv = pd.read_csv("genemap.csv")
    GeneMapHuman.objects.all().delete()
    for i in csv.itertuples():
        row = i[1:]
        mapping = GeneMapHuman(ensembl = row[0],
                               gene_symbol = row[1],
                               biotype = row[2])
        mapping.save()

