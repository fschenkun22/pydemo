from fastapi import APIRouter
from pydantic import BaseModel


test = APIRouter()

# 这个类定义标准，put_item的数据格式必须符合这个标准
class Item(BaseModel):
    name: str


@test.get("/")
async def testfun1():
    return {"message": "Hello 这是testfun1"}


# 普通get传递参数
@test.get(
        "/normal_get",
        # fastAPI上面显示的参数说明
        summary="普通get传递参数",
        )
async def normal_get(
    name:str,
    age:int,
    # 性别 不是必须传，默认men
    jender:str = 'men'
    ):
    return {"message": f"数据被更新为： {name} --{age} --{jender}"}

# 更新严格限定的数据格式
@test.put(
        '/put_item',
        summary="普通put更新数据，数据格式必须符合Item标准",        
        )
async def put_item(item: Item):
    
    return item.name