from typing import Union

from fastapi import FastAPI
from tutorial import app03, app04, app05

app = FastAPI()

app.include_router(app03, prefix="/chapter03", tags=["chapter03"])
app.include_router(app04, prefix="/chapter04", tags=["chapter04"])
app.include_router(app05, prefix="/chapter05", tags=["chapter05"])


@app.get("/")
def read_root():
    print("Hello World")
    return {"Hello": "World111"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



# 主程序
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)

