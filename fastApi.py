from fastapi import FastAPI, Request
import uvicorn
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

import json

from functions import getAnomaliasbyCidades
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


app = FastAPI()


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
async def read_item(year: int = 2019):
    
    if year < 2009 or year > 2019:
       raise UnicornException(name="Não foi encontrado dados para esse ano.", status_code=404)
            
    try:    
        anomaliasByCidades = getAnomaliasbyCidades(year)
        result = anomaliasByCidades.to_json(orient = "records")
        parsed = jsonable_encoder(result)
        return JSONResponse(content=parsed)
    except:
       raise UnicornException(name="Server Error", status_code= 500)


if __name__ == "__main__":
    uvicorn.run("fastApi:app", host="192.168.0.9", port=5000, log_level="info")