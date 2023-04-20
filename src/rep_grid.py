import pandas as pd
import numpy as np

df = pd.read_csv("etc/data/auto2.csv")
df["avgMPG+"] = (df[' CityMPG+'] + df[' HighwayMPG+'])/2
df = df.sort_values(by=['avgMPG+'], ascending=False)
print(df.head())

df.to_csv("etc/data/auto_2_repGrid.csv")