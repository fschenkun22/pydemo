from fastapi import FastAPI
import uvicorn
from apps.app_01.a1 import app1
from apps.app_02.a2 import app2
from apps.test_app.main import test
from fastapi.responses import FileResponse
from typing import Union
# 枚举类型
from enum import Enum

# 请求体
from pydantic import BaseModel

app = FastAPI()
app.include_router(app1, prefix="/app1的路由前缀", tags=["app1的路由标签"])
app.include_router(app2, prefix="/app2的路由前缀", tags=["app2的路由标签"])
app.include_router(test, prefix="/test", tags=["用来测试各种请求响应等"])


@app.get("/items/me")
async def read_me():
    return {"items": "me"}


@app.get("/items/{item_id}")
async def readitem(item_id: int):
    print(item_id)
    return {"item_id": item_id}


class Model_name(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
    chen = "chen"


@app.get("/models/{model_name}")
async def get_model(model_name: Model_name):
    if model_name == Model_name.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return FileResponse(file_path)

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {
    "item_name": "Baz"}, {"item_name": "Baz"}, {"item_name": "asddasdf"}]


@app.get("/items/")
async def read_item(limit: int = 3, skip: int = 0, q: str = None):
    print(skip, limit, q)
    print(fake_items_db[skip: skip + limit])
    return fake_items_db[skip: skip + limit]

# 请求体


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str): 
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        print(q+'被更新')
        result.update({"q": q})
        print(result)
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, debug=True, reload=True)
