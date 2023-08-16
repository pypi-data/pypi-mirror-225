import akshare

from bigan_data.db.PostgresqlAdapter import PostgresqlAdapter
from bigan_data.model.akshare.AKShareStockInfoACodeName import AKShareStockInfoACodeName


def clean_akshare_stock_info_a_code_name(pg: PostgresqlAdapter, date: str):
    sql = "delete from akshare_stock_info_a_code_name"
    pg.execute(sql)
