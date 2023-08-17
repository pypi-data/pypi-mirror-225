#! /usr/bin/env python
'''
@Author: xiaobaiTser
@email : 807447312@qq.com
@Time  : 2023/8/17 10:53
@File  : dbMonitor.py
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

# 所有条件新增接口
create_apis_code = ''

# 所有条件删除接口
delete_apis_code = ''

# 所有条件更新接口
update_apis_code = ''

# 所有条件查询接口
query_apis_code = ''


for table_name in metadata.tables:
    class_name = table_name.capitalize()
    table = Table(table_name, metadata, autoload=True)

    try:
        # 动态创建模型类
        model_class = type(class_name, (Base,), {'__tablename__': table_name, '__table__': table})

        # 将模型类添加到全局作用域中
        globals()[class_name] = model_class

        create_apis_code += f'\n'
        create_apis_code += f'@app.post(\'/{table_name}\')\n'
        create_apis_code += f'def create_record(table_name: str, data: dict):\n'
        create_apis_code += f'    db = SessionLocal()\n'
        create_apis_code += f'    table = metadata.tables[table_name]\n'
        create_apis_code += f'    record = table.insert().values(**data)\n'
        create_apis_code += f'    db.execute(record)\n'
        create_apis_code += f'    db.commit()\n'
        create_apis_code += f'    db.close()\n'

        delete_apis_code += f'\n'
        delete_apis_code += f'@app.delete(\'/{table_name}\')\n'
        delete_apis_code += f'def delete_record(table_name: str):\n'
        delete_apis_code += f'    db = SessionLocal()\n'
        delete_apis_code += f'    table = metadata.tables[table_name]\n'
        delete_apis_code += f'    record = table.delete()\n'
        delete_apis_code += f'    db.execute(record)\n'
        delete_apis_code += f'    db.commit()\n'
        delete_apis_code += f'    db.close()\n'

        update_apis_code += f'\n'
        update_apis_code += f'@app.put(\'/{table_name}\')\n'
        update_apis_code += f'def update_record(table_name: str, data: dict):\n'
        update_apis_code += f'    db = SessionLocal()\n'
        update_apis_code += f'    table = metadata.tables[table_name]\n'
        update_apis_code += f'    record = table.update().values(**data)\n'
        update_apis_code += f'    db.execute(record)\n'
        update_apis_code += f'    db.commit()\n'
        update_apis_code += f'    db.close()\n'

        query_apis_code += f'\n'
        query_apis_code += f'@app.get(\'/{table_name}\')\n'
        query_apis_code += f'def get_record(table_name: str, record_id: Union[int, None] = None):\n'
        query_apis_code += f'    db = SessionLocal()\n'
        query_apis_code += f'    table = metadata.tables[table_name]\n'
        query_apis_code += f'    if record_id:\n'
        query_apis_code += f'        record = db.query(table).filter(table.c.id == record_id).first()\n'
        query_apis_code += f'        db.close()\n'
        query_apis_code += f'        return record\n'
        query_apis_code += f'    else:\n'
        query_apis_code += f'        records = db.query(table).all()\n'
        query_apis_code += f'        db.close()\n'
        query_apis_code += f'        return records\n'

    except exc.ArgumentError:
        pass

compile(create_apis_code, '<string>', 'exec')
compile(delete_apis_code, '<string>', 'exec')
compile(update_apis_code, '<string>', 'exec')
compile(query_apis_code, '<string>', 'exec')

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app="saf.utils.dbMonitor:app", host='0.0.0.0', port=8000, reload=True)
