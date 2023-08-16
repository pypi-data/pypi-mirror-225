import os
import time

import pandas as pd
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

DATABASE_URL = os.environ.get("DATABASE_URL")
CURRENT_SCHEMA = os.environ.get("CURRENT_SCHEMA")


class PostgresqlAdapter:
    database_url: str
    current_schema: str

    def __init__(self, database_url=DATABASE_URL, current_schema=CURRENT_SCHEMA):
        if database_url is None:
            database_url = "postgresql://postgres:postgres@localhost:5432/bigan_data"
        if current_schema is None:
            current_schema = "bigan_data"
        self.db = create_engine(database_url, connect_args={'options': '-csearch_path={}'.format(current_schema)},
                                pool_size=10,
                                pool_recycle=1600,
                                pool_pre_ping=True,
                                pool_use_lifo=True,
                                echo_pool=True,
                                max_overflow=5)
        self.conn = self.db.connect()
        SQLModel.metadata.create_all(self.db)

    def add_entities(self, entities: list):
        with Session(self.db) as session:
            for entity in entities:
                session.add(entity)
            session.commit()

    def log(self, msg):
        date = time.strftime('%Y.%m.%d %H:%M:%S ', time.localtime(time.time()))
        print(date + ': {}'.format(msg))

    def df_2_db(self, df, tb, is_create=False, index=False):
        if len(df) == 0:
            self.log("no data insert into table {}".format(tb))
            return
        if is_create is True:
            df.to_sql(tb, self.conn, if_exists='replace', index=index)
            self.log("init table {} successfully".format(tb))
        else:
            df.to_sql(tb, self.conn, if_exists='append', index=index)
            self.log("insert data into {} successfully".format(tb))

    #     sql = text("SELECT * FROM test.stock_all where ts_code=:code")
    #     params={'code': current_code}
    #     # 使用 params 进行参数传递
    #     data_df = ts.query_stock(sql, params)
    def db_2_df(self, sql, params):
        return pd.read_sql(sql, self.conn, params=params)

    def execute(self, sql):

        return self.conn.execute(sql)
