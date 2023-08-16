from sqlmodel import Field, SQLModel


class AKShareStockInfoACodeName(SQLModel, table=True):
    __tablename__ = "akshare_stock_info_a_code_name"
    code: str = Field(description="代码", primary_key=True)
    name: str = Field(description="名称")
