from sqlalchemy import Column
from sqlmodel import Field, Session, SQLModel, create_engine, select


# Code - string 000001.SZ
# ExchangeID - string 合约市场代码
# InstrumentID - string 合约代码
# InstrumentName - string 合约名称
# ProductID - string 合约的品种ID(期货)
# ProductName - string 合约的品种名称(期货)
# CreateDate - str 上市日期(期货)
# OpenDate - str IPO日期(股票)
# ExpireDate - int 退市日或者到期日
# PreClose - float 前收盘价格
# SettlementPrice - float 前结算价格
# UpStopPrice - float 当日涨停价
# DownStopPrice - float 当日跌停价
# FloatVolume - float 流通股本
# TotalVolume - float 总股本
# LongMarginRatio - float 多头保证金率
# ShortMarginRatio - float 空头保证金率
# PriceTick - float 最小价格变动单位
# VolumeMultiple - int 合约乘数(对期货以外的品种，默认是1)
# MainContract - int 主力合约标记，1、2、3分别表示第一主力合约，第二主力合约，第三主力合约
# LastVolume - int 昨日持仓量
# InstrumentStatus - int 合约已停牌日期（停牌第一天值为0，第二天为1，以此类推。注意，正常交易的股票该值也是0） 获取股票停牌状态参考get_full_tick openInt字段
# IsTrading - bool 合约是否可交易
# IsRecent - bool 是否是近月合约
class Instrument(SQLModel, table=True):
    Code: str = Field(description="总代码, 000001.SZ", primary_key=True)
    ExchangeID: str = Field(description=" 合约市场代码")
    InstrumentID: str = Field(description=" 合约代码")
    InstrumentName: str = Field(description=" 合约名称")
    ProductID: str = Field(description=" 合约的品种ID(期货)")
    ProductName: str = Field(description=" 合约的品种名称(期货)")
    CreateDate: str = Field(description=" 上市日期(期货)")
    OpenDate: str = Field(description=" IPO日期(股票)")
    ExpireDate: int = Field(description=" 退市日或者到期日")
    PreClose: float = Field(description=" 前收盘价格")
    SettlementPrice: float = Field(description=" 前结算价格")
    UpStopPrice: float = Field(description=" 当日涨停价")
    DownStopPrice: float = Field(description=" 当日跌停价")
    FloatVolume: float = Field(description=" 流通股本")
    TotalVolume: float = Field(description=" 总股本")
    LongMarginRatio: float = Field(description=" 多头保证金率")
    ShortMarginRatio: float = Field(description=" 空头保证金率")
    PriceTick: float = Field(description=" 最小价格变动单位")
    VolumeMultiple: int = Field(description=" 合约乘数(对期货以外的品种，默认是1)")
    MainContract: int = Field(description=" 主力合约标记，1、2、3分别表示第一主力合约，第二主力合约，第三主力合约")
    LastVolume: int = Field(description=" 昨日持仓量")
    InstrumentStatus: int = Field(
        description=" 合约已停牌日期（停牌第一天值为0，第二天为1，以此类推。注意，正常交易的股票该值也是0） 获取股票停牌状态参考get_full_tick openInt字段")
    IsTrading: bool = Field(description=" 合约是否可交易")
    IsRecent: bool = Field(description=" 是否是近月合约")
