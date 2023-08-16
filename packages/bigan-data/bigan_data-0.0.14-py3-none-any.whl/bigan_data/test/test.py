from datetime import datetime

import akshare as ak

from bigan_data.db.PostgresqlAdapter import PostgresqlAdapter
from bigan_data.model.AKShareSyncModel import get_akshare_stock_info_a_code_name, get_akshare_stock_zh_a_hist
from bigan_data.model.AKShareSyncModelClean import clean_akshare_stock_info_a_code_name

if __name__ == '__main__':
    print("test")
    start_date = "20230101"
    today = datetime.today().strftime('%Y%m%d')
    print(today)
    pg = PostgresqlAdapter()
    clean_akshare_stock_info_a_code_name(pg, today)
    stocks = get_akshare_stock_info_a_code_name()
    #pg.add_entities(stocks)
    for stock in stocks:
        stock_zh_a_hist = get_akshare_stock_zh_a_hist(stock.code, start_date, today)
        print(stock_zh_a_hist)
        pg.add_entities(stock_zh_a_hist)
