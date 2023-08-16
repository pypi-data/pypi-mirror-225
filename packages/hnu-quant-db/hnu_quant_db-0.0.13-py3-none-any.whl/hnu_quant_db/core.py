import sqlalchemy
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import pandas as pd

from typing import List, Iterable, Union


class Querier:
    def __init__(self, token: str):
        try:
            self.engine = sqlalchemy.create_engine(
                f"postgresql://client:{token}@azimememe.top:5432/hnu_quant"
            )
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            raise Exception("连接数据库失败。") from e

    def __del__(self):
        self.engine.dispose()

    def query(self, sql: str) -> pd.DataFrame:
        """输入SQL语句，返回查询结果的DataFrame

        Args:
            sql (str): 查询的SQL语句

        Returns:
            pd.DataFrame: 查询结果
        """
        with self.engine.connect() as conn:
            return pd.read_sql_query(text(sql), conn)

    def get_table_daily(
        self,
        table_name: str,
        columns: Union[Iterable[str], str, None] = None,
        code: Union[Iterable[str], str, None] = None,
        start: Union[str, None] = None,
        end: Union[str, None] = None,
    ) -> pd.DataFrame:
        if isinstance(columns, str):
            columns = [columns]
        
        TableHistDaily = sqlalchemy.Table(
            table_name, sqlalchemy.MetaData(), autoload_with=self.engine
        )

        with self.Session() as session:
            query = session.query(TableHistDaily)

            if columns is not None:
                query = query.with_entities(
                    *[getattr(TableHistDaily.c, col) for col in columns]
                )
            if code is not None:
                query = query.filter(TableHistDaily.c.code.in_(code))
            if start is not None:
                query = query.filter(TableHistDaily.c.date >= start)
            if end is not None:
                query = query.filter(TableHistDaily.c.date <= end)

            df = pd.read_sql_query(query.statement, session.bind)  # type: ignore
        
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        
        return df

    def get_stocks_daily(
        self,
        columns: Union[Iterable[str], str, None] = None,
        code: Union[Iterable[str], str, None] = None,
        start: Union[str, None] = None,
        end: Union[str, None] = None,
    ) -> pd.DataFrame:
        """获取股票历史日度数据

        Args:
            columns (Iterable[str] | str | None, optional): 需要查询的列名，如['code', 'date', 'close']，默认为None，表示查询所有列\n
            code (Iterable[str] | str | None, optional): 股票代码，可以为列表或字符串，如['000001', '000002']或'000001'，默认为None，表示查询所有股票\n
            start (str | None, optional): 开始日期，如'2020-01-01'，默认为None，表示从最早日期开始\n
            end (str | None, optional): 结束日期，如'2020-01-01'，默认为None，表示到最晚日期结束\n

        Returns:
            pd.DataFrame: 查询结果
        """
        return self.get_table_daily("stock_hist_daily", columns, code, start, end)

    def get_indexs_daily(
        self,
        columns: Union[Iterable[str], str, None] = None,
        code: Union[Iterable[str], str, None] = None,
        start: Union[str, None] = None,
        end: Union[str, None] = None,
    ) -> pd.DataFrame:
        """获取指数历史日度数据

        Args:
            columns (Iterable[str] | str | None, optional): 需要查询的列名，如['code', 'date', 'close']，默认为None，表示查询所有列\n
            code (Iterable[str] | str | None, optional): 指数代码，如'000001'，默认为None，表示查询所有指数\n
            start (str | None, optional): 开始日期，如'2020-01-01'，默认为None，表示从最早日期开始\n
            end (str | None, optional): 结束日期，如'2020-01-01'，默认为None，表示到最晚日期结束\n
            
        Returns:
            pd.DataFrame: 查询结果
        """
        return self.get_table_daily("index_hist_daily", columns, code, start, end)

    def get_table_pivot(
        self,
        table_name: str,
        value: str = "close",
        codes: Union[Iterable[str], str, None] = None,
        start: Union[str, None] = None,
        end: Union[str, None] = None,
    ) -> pd.DataFrame:
        df = self.get_table_daily(table_name, ["code", "date", value], codes, start, end)
        df = df.pivot(index="date", columns="code", values=value)
        return df
    
    def get_stocks_pivot(
        self,
        value: str = "close",
        codes: Union[Iterable[str], str, None] = None,
        start: Union[str, None] = None,
        end: Union[str, None] = None,
    ) -> pd.DataFrame:
        """获取股票历史日度数据的透视表
        
        Args:
            value (str, optional): 需要透视的列名，如'close'，默认为'close'\n
            codes (Iterable[str] | None, optional): 股票代码，可以为列表或字符串，如['000001', '000002']或'000001'，默认为None，表示查询所有股票\n
            start (str | None, optional): 开始日期，如'2020-01-01'，默认为None，表示从最早日期开始\n
            end (str | None, optional): 结束日期，如'2020-01-01'，默认为None，表示到最晚日期结束\n
            
        Returns:
            pd.DataFrame: 查询结果
        """
        
        return self.get_table_pivot("stock_hist_daily", value, codes, start, end)
    
    def get_indexs_pivot(
        self,
        value: str = "close",
        codes: Union[Iterable[str], str, None] = None,
        start: Union[str, None] = None,
        end: Union[str, None] = None,
    ) -> pd.DataFrame:
        """获取指数历史日度数据的透视表
        
        Args:
            value (str, optional): 需要透视的列名，如'close'，默认为'close'\n
            codes (Iterable[str] | str | None, optional): 指数代码，可以为列表或字符串，如['sh000001', 'sz399001']或'sh000001'，默认为None，表示查询所有指数\n
            start (str | None, optional): 开始日期，如'2020-01-01'，默认为None，表示从最早日期开始\n
            end (str | None, optional): 结束日期，如'2020-01-01'，默认为None，表示到最晚日期结束\n
            
        Returns:
            pd.DataFrame: 查询结果
        """
        return self.get_table_pivot("index_hist_daily", value, codes, start, end)
        
if __name__ == "__main__":
    with open("token") as f:
        token = f.read()
    querier = Querier(token=token)
    
    df = querier.get_stocks_daily(["code", "date", "close"], ["000001", "000002"], "2020-01-01", "2020-01-10")
    print(df)
    
    df = querier.get_stocks_pivot("close", ["000001", "000002"], "2020-01-01", "2020-01-10")
    print(df)
    
    df = querier.get_indexs_daily(["code", "date", "close"], ["sh000001", "sz399001"], "2020-01-01", "2020-01-10")
    print(df)
    
    df = querier.get_indexs_pivot("close", ["sh000001", "sz399001"], "2020-01-01", "2020-01-10")
    print(df)