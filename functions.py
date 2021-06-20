import pandas as pd
import numpy as np

cid = pd.read_csv("./CID10.csv")
dtAll = pd.DataFrame()
for year in range(2009, 2020):
    df = pd.read_csv("./sp_{}_clean.csv".format(year))
    dtAll = dtAll.append(df[['CODANOMAL', 'CODMUNNASC']])

def getAnomaliaDescription(cod):
    descricao = cid[cid["CID10"] == cod.strip().replace('X', '').replace('D', '') ]
    return descricao["DESCR"]

def frequency(my_list): 
    freq = {}
    dictionary = []
    for item in np.unique(np.array(my_list)):
        freq[item] = np.where(np.array(my_list)==item)[0].shape[0]
        dictionary.append({"cod": item, "quantidade":freq[item], "descricao": getAnomaliaDescription(item)})
    return dictionary

def anomaliaFetch(arrayAnomalias):
    completedArray = []
    for element in arrayAnomalias:
        anomaliasRaw = element.split('Q')
        for anomalia in anomaliasRaw:
            if(len(anomalia) > 0):
                anomalia = 'Q'+ anomalia
                completedArray.append(anomalia)
    anomaliasObjects = frequency(completedArray)
    return { "anomalias": anomaliasObjects , "total":  len(completedArray) }


def getAnomaliasbyCidades(year, cid10):
    df = pd.read_csv("./sp_{}_clean.csv".format(year))
    dtTemp = pd.DataFrame()
    if(cid10):
        df = df[df["CODANOMAL"].replace('X', '').replace('D', '').str.contains(cid10.strip() )]
        df["CODANOMAL"] = df["CODANOMAL"].replace(regex=r'.+', value=cid10.strip())
    cidades = df["CODMUNNASC"].unique()
    array_anomal_cidade = []
    for cidade in cidades:
        json =   {"id" : cidade}
        arrayAnomalias = df[df["CODMUNNASC"] == cidade ]["CODANOMAL"].to_numpy()
        infos = anomaliaFetch(arrayAnomalias)
        json.update(infos)
        array_anomal_cidade.append(json)
    return pd.DataFrame(array_anomal_cidade)

def getAnomaliasAllYears(cid10):
    dtTemp = dtAll
    if(cid10):
        dtTemp = dtTemp[dtTemp["CODANOMAL"].replace('X', '').replace('D', '').str.contains(cid10.strip())]
        dtTemp["CODANOMAL"] = dtTemp["CODANOMAL"].replace(regex=r'.+', value=cid10.strip())
    cidades = dtTemp["CODMUNNASC"].unique()
    array_anomal_cidade = []
    for cidade in cidades:
        json =   {"id" : cidade}
        arrayAnomalias = dtTemp[dtTemp["CODMUNNASC"] == cidade ]["CODANOMAL"].to_numpy()
        infos = anomaliaFetch(arrayAnomalias)
        json.update(infos)
        array_anomal_cidade.append(json)
    return pd.DataFrame(array_anomal_cidade)


def getListAnomalias():
    cidAnomalias =  cid[cid["CID10"].str.contains('Q')]
    cidAnomalias = cidAnomalias[["CID10","DESCR"]]
    return pd.DataFrame(cidAnomalias)