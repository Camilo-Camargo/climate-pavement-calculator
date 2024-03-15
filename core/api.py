from fastapi import FastAPI
from pydantic import BaseModel, conlist
from typing import Union

from climate_pavement import climate_pavements

app = FastAPI()


class ClimatePavimentReqDTO(BaseModel):
    mode: str
    precipitation_mm: conlist(Union[float, int], min_length=12, max_length=12)
    temp_celsius: conlist(Union[float, int], min_length=12, max_length=12)
    specific_gravity: Union[float, int]
    plasticity_index: Union[float, int]
    california_bearing_ratio: Union[float, int]
    maximum_dry_density: Union[float, int]
    optimum_moisture_content: Union[float, int]
    p200: Union[float, int]


@app.get('/')
async def index():
    return {"version": "0.0.1"}


@app.post("/climate-pavement-calculator")
async def climate_in_pavement_calculator(req: ClimatePavimentReqDTO):
    res = climate_pavements(req.dict())
    return res
