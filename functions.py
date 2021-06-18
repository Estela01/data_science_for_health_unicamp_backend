import pandas as pd
import numpy as np

def getAnomaliasbyCidades(year):
    df = pd.read_csv("./sp_{}_clean.csv".format(year))

    cidades = df["CODMUNNASC"].unique()

    array_anomal_cidade = []

    for cidade in cidades:
        json = {"id" : cidade, "anomalias": df[df["CODMUNNASC"] == cidade ]["CODANOMAL"].to_numpy().tolist() }

        array_anomal_cidade.append(json)
    
    return pd.DataFrame(array_anomal_cidade)
