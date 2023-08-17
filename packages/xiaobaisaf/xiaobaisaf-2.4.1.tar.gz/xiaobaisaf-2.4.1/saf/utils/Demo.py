#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/6/16 0:04
@File  : Demo.py
'''
import sqlalchemy
from typing import Union
from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, Table, exc
from sqlalchemy.orm import declarative_base, sessionmaker

# 创建 FastAPI 应用
app = FastAPI()

# 创建数据库连接
engine = create_engine('mysql+pymysql://tinyshop:123456@192.168.0.240:3306/tinyshop', echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 使用反射自动生成模型类
metadata = MetaData(bind=engine)
metadata.reflect()

for table_name in metadata.tables:
    class_name = table_name.capitalize()
    table = Table(table_name, metadata, autoload=True)

    try:
        # 动态创建模型类
        model_class = type(class_name, (Base,), {'__tablename__': table_name, '__table__': table})

        # 将模型类添加到全局作用域中
        globals()[class_name] = model_class
    except exc.ArgumentError:
        pass

# 所有条件查询接口
@app.get('/{table_name}')
def get_record(table_name: str, record_id: Union[int, None] = None):
    db = SessionLocal()
    table = metadata.tables[table_name]
    if record_id:
        record = db.query(table).filter(table.c.id == record_id).first()
        db.close()
        return record
    else:
        records = db.query(table).all()
        db.close()
        return records

@app.post('/{table_name}')
def create_record(table_name: str, data: dict):
    db = SessionLocal()
    table = metadata.tables[table_name]
    record = table.insert().values(**data)
    db.execute(record)
    db.commit()
    db.close()
    return {'message': 'Record created successfully'}

'''
def greet(name):
    print(f"Hello, {name}!")

# 动态创建函数
function_name = "greet_custom"
function_args = ["name"]
function_body = 'print(f"Custom greeting, {name}!")'
custom_greet = type(function_name, (object,), {
    "__doc__": "A custom greeting function",
    "__module__": "__main__",
    "__name__": function_name,
    "__annotations__": {},
    "__qualname__": function_name,
    "__defaults__": (),
    "__kwdefaults__": None,
    "__code__": compile(function_body, filename="<string>", mode="exec"),
})

# 调用动态创建的函数
custom_greet("John")

'''


# 运行 FastAPI 应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="saf.utils.Demo:app", host='0.0.0.0', port=8000, reload=True)