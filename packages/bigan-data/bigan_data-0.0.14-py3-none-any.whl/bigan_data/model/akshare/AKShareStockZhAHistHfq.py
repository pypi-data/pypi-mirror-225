from typing import Optional

from sqlmodel import Field, SQLModel


# 名称	类型	描述
# 日期	object	交易日
# 开盘	float64	开盘价
# 收盘	float64	收盘价
# 最高	float64	最高价
# 最低	float64	最低价
# 成交量	int64	注意单位: 手
# 成交额	float64	注意单位: 元
# 振幅	float64	注意单位: %
# 涨跌幅	float64	注意单位: %
# 涨跌额	float64	注意单位: 元
# 换手率	float64	注意单位: %
#
class AKShareStockZhAHistHfq(SQLModel, table=True):
    __tablename__ = "akshare_stock_zh_a_hist_hfq"
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(description="代码", index=True)
    date: str = Field(description="交易日")
    open: float = Field(description="开盘价")
    close: float = Field(description="收盘价")
    high: float = Field(description="最高价")
    low: float = Field(description="最低价")
    volume: int = Field(description="成交量	int64	注意单位: 手")
    turnover: float = Field(description="成交额	float64	注意单位: 元")
    amplitude: float = Field(description="振幅	float64	注意单位: %")
    percentChange: float = Field(description="涨跌幅	float64	注意单位: %")
    change: float = Field(description="涨跌额	float64	注意单位: 元")
    turnoverRate: float = Field(description="换手率	float64	注意单位: %")
