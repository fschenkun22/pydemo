from datetime import datetime
from typing import Any
from pydantic import BaseModel, PositiveInt, StrictInt, field_validator


class User(BaseModel):
    id: Any
    name: str = 'John Doe'
    signup_ts: datetime = None
    random_data: Any

# 自定义验证器
    @field_validator('id')
    def id_must_be_positive(cls, v):
        assert v > 0, 'id must be positive 正数'
        return v
    


user = User(
    id= 1,
    name='John Doe',
    signup_ts='2017-06-01 12:22',
    random_data='123'
)

# 直接把模型导出为json
user_json = user.model_dump_json()
print(user_json)

# 直接把模型导出为dict
# user_dict = user.model_dump()

# print(user_dict)


# print(user)

#  如果有一个json字符串 直接可以转换成user
# json_str = '{"id": 2, "name": "John Doe2", "signup_ts": "2017-06-01 12:22"}'
# user2 = User.model_validate_json(json_str)
# print(user2)




