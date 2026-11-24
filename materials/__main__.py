"""显示资料清单，不生成业务判断。"""
import json
from . import validate
print(json.dumps({"资料格式":"有效","记录数":validate()},ensure_ascii=False,indent=2))
