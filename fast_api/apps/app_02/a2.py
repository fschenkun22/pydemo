from fastapi import APIRouter
app2 = APIRouter()

@app2.post("/")
async def a1fun1():
    return {"message": "Hello 这是a2fun1"}