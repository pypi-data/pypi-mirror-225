import akshare

from bigan_data.model.akshare.AKShareStockInfoACodeName import AKShareStockInfoACodeName
from bigan_data.model.akshare.AKShareStockZhAHist import AKShareStockZhAHist


def get_akshare_stock_info_a_code_name() -> list[AKShareStockInfoACodeName]:
    df = akshare.stock_info_a_code_name()
    df_list = df.to_dict('records')
    res_list = []
    for ak_dict in df_list:
        data = AKShareStockInfoACodeName.parse_obj(ak_dict)
        res_list.append(data)
    return res_list


def get_akshare_stock_zh_a_hist(code: str, start_date: str, end_date: str) -> list[AKShareStockZhAHist]:
    df = akshare.stock_zh_a_hist(symbol=code, period="daily", start_date=start_date,
                                 end_date=end_date,
                                 adjust="")
    df['code'] = code
    df['date'] = df['日期']
    df['open'] = df['开盘']
    df['close'] = df['收盘']
    df['high'] = df['最高']
    df['low'] = df['最低']
    df['volume'] = df['成交量']
    df['turnover'] = df['成交额']
    df['amplitude'] = df['振幅']
    df['percentChange'] = df['涨跌幅']
    df['change'] = df['涨跌额']
    df['turnoverRate'] = df['换手率']
    df_list = df.to_dict('records')
    res_list = []
    for ak_dict in df_list:
        ak_dict['date']=ak_dict['date'].strftime('%Y%m%d')
        data = AKShareStockZhAHist.parse_obj(ak_dict)
        res_list.append(data)
    return res_list
