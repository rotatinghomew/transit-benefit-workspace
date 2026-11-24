"""合成业务资料的读取与格式检查。"""
from pathlib import Path
import json

def read_bundle(root=None):
    root=Path(root or Path(__file__).resolve().parents[1])
    schema=json.loads((root/"data/schema.json").read_text(encoding="utf-8"))
    tables={name:[json.loads(line) for line in (root/"data"/(name+".jsonl")).read_text(encoding="utf-8").splitlines() if line.strip()] for name in schema["tables"]}
    return schema,tables

def validate(root=None):
    schema,tables=read_bundle(root)
    for name,definition in schema["tables"].items():
        seen=set()
        for row in tables[name]:
            if set(row)!=set(definition["fields"]):raise ValueError(f"{name}字段与协议不符")
            if row["id"] in seen:raise ValueError(f"{name}编号重复")
            seen.add(row["id"])
            for key,rule in definition["fields"].items():
                value=row[key];kind=rule["type"]
                if value is None and kind.startswith("nullable_"):continue
                kind=kind.removeprefix("nullable_")
                valid={"string":isinstance(value,str),"number":isinstance(value,(int,float)) and not isinstance(value,bool),"boolean":isinstance(value,bool),"array":isinstance(value,list)}
                if not valid[kind]:raise ValueError(f"{name}.{key}类型不符")
        for key,target in definition.get("references",{}).items():
            allowed={row["id"] for row in tables[target]}
            for row in tables[name]:
                if row[key] not in (None,"") and row[key] not in allowed:raise ValueError(f"{name}.{key}引用不存在")
    return {name:len(values) for name,values in tables.items()}
