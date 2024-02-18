from fastapi import APIRouter
app1 = APIRouter()

print('app1 is improted')

@app1.get("/")
async def a1fun1():
    return {"message": "Hello 这是a1fun1"}

@app1.post("/a1fun2")
async def a1fun2():
    return {"message": "Hello 这是a1fun2"}

@app1.put("/a1fun3")
async def a1fun3():
    return {"message": "Hello 这是a1fun3"}

@app1.delete("/a1fun4")
async def a1fun4():
    return {"message": "Hello 这是a1fun4"}

