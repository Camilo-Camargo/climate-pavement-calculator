from fastapi import FastAPI
from pydantic import BaseModel, conlist

from climate_pavement import climate_pavements

app = FastAPI()


class ClimatePavimentReqDTO(BaseModel):
    mode: str
    precipitation_mm: conlist(float, min_length=12, max_length=12)
    temp_celsius: conlist(float, min_length=12, max_length=12)
    specific_gravity: float
    plasticity_index: float
    california_bearing_ratio: float
    maximum_dry_density: float
    optimum_moisture_content: float
    p200: float


@app.get('/')
async def index():
    return {"version": "0.0.1"}


@app.post("/climate-pavement-calculator")
async def climate_in_pavement_calculator(req: ClimatePavimentReqDTO):
    res = climate_pavements(req.dict())
    return res
