# -*- coding: utf-8 -*-


from enum import Enum
from fastapi import APIRouter

app03 = APIRouter()

@app03.get("/")
def read_root():
    print("Hello World")
    return {"Hello": "World"}

class CityName(str, Enum):
    beijing = "beijing"
    shanghai = "shanghai"
    guangzhou = "guangzhou"
    
@app03.get("/city/{city_name}")
def read_city(city_name: CityName):
    if city_name == CityName.beijing:
        return {"city": "Beijing", "country": "China"}
    elif city_name == CityName.shanghai:
        return {"city": "Shanghai", "country": "China"}
    elif city_name == CityName.guangzhou:
        return {"city": "Guangzhou", "country": "China"}
    else:
        return {"error": "City not found"}