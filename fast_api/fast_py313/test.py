from pydantic import BaseModel, EmailStr
from typing import List

class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    hobbies: List[str] = []

# 创建用户实例
user = User(name="Alice", age=25, email="alice@example.com", hobbies=["reading", "hiking"])

# 序列化为 JSON
print(user.model_dump_json())  # {"name": "Alice", "age": 25, "email": "alice@example.com", "hobbies": ["reading", "hiking"]}

# 验证错误示例
try:
    User(name="Bob", age="invalid", email="not-an-email")  # 触发验证错误
except ValueError as e:
    print(e)