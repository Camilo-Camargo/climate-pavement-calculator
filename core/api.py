from fastapi import FastAPI, Request
from pydantic import BaseModel, conlist
from typing import Union, Optional
from climate_pavement import climate_pavements
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="static")


class ClimatePavimentReqDTO(BaseModel):
    mode: str
    precipitation_mm: conlist(Union[float, int], min_length=12, max_length=12)
    temp_celsius: conlist(Union[float, int], min_length=12, max_length=12)
    specific_gravity: Union[float, int]
    plasticity_index: Union[float, int]
    california_bearing_ratio: Union[float, int]
    maximum_dry_density: Union[float, int]
    optimum_moisture_content: Union[float, int]
    sieves_passing: Optional[conlist(
        Union[float, int], min_length=9, max_length=9)] = []
    p200: Union[float, int]


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get('/api')
async def version():
    return {"version": "0.0.1"}


@app.post("/api/climate-pavement-calculator")
async def climate_in_pavement_calculator(req: ClimatePavimentReqDTO):
    res = climate_pavements(req.dict())
    return res
