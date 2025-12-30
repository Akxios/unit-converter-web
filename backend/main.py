from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path
from pydantic import BaseModel, Field

from backend.services.convertor import convert_temperature, convert_length, convert_weight

templates = Jinja2Templates(directory="frontend/templates")
app = FastAPI(title="Unit Converter API", description="API для конвертации единиц измерения")

app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConvertRequest(BaseModel):
    category: str = Field(
        ..., 
        description="Тип конверсии: temperature, weight или length",
        example="temperature"
    )
    value: float = Field(
        ..., 
        description="Значение для конвертации", 
        example=25.5
    )
    from_unit: str = Field(
        ..., 
        description="Исходная единица", 
        example="c"
    )
    to_unit: str = Field(
        ..., 
        description="Целевая единица", 
        example="k"
    )


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/units/{category}", summary="Список единиц")
async def get_units(category: str):
  """
  Возвращает список единиц для выбранной категории.

  - **category**: temperature, weight или length
  """
  data = {
    "temperature": ["c", "k", "f"],
    "weight": ["mg", "g", "kg", "oz", "lb"],
    "length": ["mm", "cm", "m", "km", "in", "ft", "yd", "mi"]
  }

  if category not in data:
    raise HTTPException(status_code=400, detail="Unsupported category")
  
  return {"units": data[category]}


@app.post("/convert", summary="Конвертация единиц")
async def convert(request: ConvertRequest):
  """
  Конвертирует значения одних единиц в другие.

  - **request.category**: тип конверсии (temperature, weight, length)
  - **request.value**: значение для конвертации
  - **request.from_unit**: исходная единица
  - **request.to_unit**: целевая единица
  """
  
  try:
    if request.category == "temperature":
      result = convert_temperature(value=request.value, from_unit=request.from_unit, to_unit=request.to_unit)
    elif request.category == "weight":
      result = convert_weight(value=request.value, from_unit=request.from_unit, to_unit=request.to_unit)
    elif request.category == "length":
      result = convert_length(value=request.value, from_unit=request.from_unit, to_unit=request.to_unit)
    else:
      raise ValueError("Unsupported category")

  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

  return {
    "category": request.category,
    "value": request.value,
    "from_unit": request.from_unit,
    "to_unit": request.to_unit,
    "result": result,
    "result_unit": request.to_unit
  }
