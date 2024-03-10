from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field


test = APIRouter()

# 这个类定义标准，put_item的数据格式必须符合这个标准


class Item(BaseModel):
    name: str = 'default_name'
    age: int = 18
    # gender是必传参数，如果没有传错误信息应该提示gender是必传参数的中文
    gender: str = Field(..., title="性别", description="性别是必传参数",
                        error_messages={"required": "性别是必传参数"})


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
    name: str,
    age: int,
    # 性别 不是必须传，默认men
    jender: str = 'men'
):
    return {"message": f"数据被更新为： {name} --{age} --{jender}"}

# 更新严格限定的数据格式


# @test.put(
#     '/put_item',
#     summary="普通put更新数据，数据格式必须符合Item标准",
# )
# async def put_item(item: Item):

#     return item.name


# 测试默认参数
@test.get(
    "/default_param",
    summary="测试默认参数",
    responses={
        200: {"description": "成功返回数据"},
        404: {"description": "找不到数据"}
    },
)
async def default_param(item: Item = Depends()):
    #404错误
    if item.name == 'default_name':
        raise HTTPException(status_code=404, detail="错误处理---找不到数据")
    return item.dict()
