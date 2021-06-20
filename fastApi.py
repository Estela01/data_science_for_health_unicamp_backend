from fastapi import FastAPI, Request
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import json

from functions import getAnomaliasbyCidades, getListAnomalias, getAnomaliasAllYears
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UnicornException(Exception):
    def __init__(self, name: str, status_code: int):
        self.name = name
        self.status_code = status_code


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.name}
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/getAnomalias/")
async def read_item(year: int = 2019, cid10: str = None):
    
    if year != -1 and (year < 2009 or year > 2019):
       raise UnicornException(name="Não foi encontrado dados para esse ano.", status_code=404)
            
    try:
        if year == -1:
            anomaliasAllYears = getAnomaliasAllYears(cid10)
            result = anomaliasAllYears.to_json(orient = "records")
            parsed = jsonable_encoder(result)
            return JSONResponse(content=parsed)
        
        anomaliasByCidades = getAnomaliasbyCidades(year, cid10)
        result = anomaliasByCidades.to_json(orient = "records")
        parsed = jsonable_encoder(result)
        return JSONResponse(content=parsed)
    except:
       raise UnicornException(name="Server Error", status_code= 500)

    
@app.get("/getListAnomalias/")
async def read_item():
    try:    
        lista = getListAnomalias()
        result = lista.to_json(orient = "records")
        parsed = jsonable_encoder(result)
        return JSONResponse(content=parsed)
    except:
       raise UnicornException(name="Server Error", status_code= 500)
    
@app.get("/getListYears/")
async def read_item():
    try:
        yearList = []
        for year in range(2009, 2020):
            yearList.append({"id": year, "label": "{}".format(year)})
        yearList.append({"id": -1, "label": "Todos"})
        return JSONResponse(content=yearList)
    except:
       raise UnicornException(name="Server Error", status_code= 500)

if __name__ == "__main__":
#     uvicorn.run("fastApi:app", host="127.0.0.1", port=3000, log_level="info") 
    uvicorn.run("fastApi:app", host="192.168.0.9", port=3000, log_level="info")