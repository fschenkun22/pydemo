from fastapi import FastAPI
import uvicorn
from apps.app_01.a1 import app1
from apps.app_02.a2 import app2
from apps.test_app.main import test

app = FastAPI()
app.include_router(app1,prefix="/app1的路由前缀",tags=["app1的路由标签"])
app.include_router(app2,prefix="/app2的路由前缀",tags=["app2的路由标签"])

app.include_router(test,prefix="/test",tags=["用来测试各种请求响应等"])

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080 ,debug=True,reload=True)