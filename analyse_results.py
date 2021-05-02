import pandas as pd
import matplotlib as mp

df = pd.read_csv("/Users/jcurtis/DoneDeal_Scrapper/output.csv", index_col=0)

print(df.groupby(["year"]).count())