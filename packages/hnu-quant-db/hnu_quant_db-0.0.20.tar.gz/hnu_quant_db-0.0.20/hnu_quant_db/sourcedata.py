import akshare as ak
import pandas as pd

import baostock as bs

from cachetools import cached, TTLCache

from typing import Iterable, List

def get_stocks_series() -> pd.Series:
    spot = ak.stock_zh_a_spot_em()
    return spot["代码"]


@cached(TTLCache(maxsize=1, ttl=60 * 60 * 24))
def code_market_dict() -> dict:
    spot_xl_code = ak.stock_zh_a_spot()["代码"]

    result = pd.DataFrame()
    result["code"] = spot_xl_code.apply(lambda x: x[2:])
    result["market"] = spot_xl_code.apply(lambda x: x[:2])

    return result.set_index("code")["market"].to_dict()


def get_stock_hist(code: str, start_date="19800101") -> pd.DataFrame:
    stock_hist = ak.stock_zh_a_hist(code, "daily", start_date, "20301231")

    if stock_hist.empty:
        return stock_hist

    fhq = ak.stock_zh_a_hist(code, "daily", start_date, "20301231", "hfq")

    stock_hist["开盘_后复权"] = fhq["开盘"]
    stock_hist["收盘_后复权"] = fhq["收盘"]
    stock_hist["最高_后复权"] = fhq["最高"]
    stock_hist["最低_后复权"] = fhq["最低"]

    stock_hist["股票代码"] = code

    cols = [
        "股票代码",
        "日期",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "开盘_后复权",
        "收盘_后复权",
        "最高_后复权",
        "最低_后复权",
        "成交量",
        "成交额",
        "换手率",
    ]
    stock_hist = stock_hist[cols]
    stock_hist.columns = [
        "code",
        "date",
        "open",
        "close",
        "high",
        "low",
        "open_hfq",
        "close_hfq",
        "high_hfq",
        "low_hfq",
        "volume",
        "amount",
        "turnover_rate",
    ]
    return stock_hist


def get_indexs_series() -> pd.Series:
    spot = ak.stock_zh_index_spot()
    return spot["代码"]


def get_index_hist(code: str, start_date: str | None = None) -> pd.DataFrame:
    index_hist = ak.stock_zh_index_daily(code)

    if index_hist.empty:
        return index_hist

    if start_date:
        index_hist = index_hist[
            pd.to_datetime(index_hist["date"]) >= pd.to_datetime(start_date)
        ]

    index_hist["code"] = code

    cols = ["code", "date", "open", "close", "high", "low", "volume"]
    index_hist = index_hist[cols]

    return index_hist


def get_code_valuation_indices_baostock(
    code: str, start_date: str, end_date: str
) -> pd.DataFrame:
    
    code = code_market_dict()[code] + "." + code
    start_date = f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:]}"

    res = bs.query_history_k_data_plus(
        code,
        "date,peTTM,pbMRQ,psTTM,pcfNcfTTM",
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag="3",
    )

    return res.get_data()


def get_valuation_indices_baostock(
    code: Iterable[str] | str, start_date: str = "19800101", end_date: str = "20301231"
) -> pd.DataFrame:
    bs.login()
    
    if isinstance(code, str):
        code = [code]
        
    dfs = []
    
    for c in code:
        df = get_code_valuation_indices_baostock(c, start_date, end_date)
        df["code"] = c
        dfs.append(df)
    
    res = pd.concat(dfs, ignore_index=True)

    # set code to the first column
    cols = res.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    res = res[cols]
    
    bs.logout()
    
    return res

def get_code_outstading_period(code: str, start_date: str, end_date: str) -> pd.DataFrame:
    df = ak.stock_share_change_cninfo(
        symbol=code, start_date=start_date, end_date=end_date
    )
    return df[["变动日期", "已流通股份"]].drop_duplicates(subset=["已流通股份"], keep="first")

def get_outstanding_daily(code: Iterable[str] | str, start_date: str = "19800101", end_date: str = "20301231") -> pd.DataFrame:
    if isinstance(code, str):
        code = [code]
        
    dfs = []
    
    for c in code:
        df = get_code_outstading_period(c, start_date, end_date)
        
        min_date = df["变动日期"].min()
        date_range = pd.date_range(min_date, max_date)
        df = df.set_index("变动日期").reindex(date_range, method="ffill").reset_index()
        
        df["code"] = c
        
        dfs.append(df)

    res = pd.concat(dfs, ignore_index=True)

    # set code to the first column
    cols = res.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    res = res[cols]
    res.columns = ["code", "date", "outstanding_shares"]
    
    return res



# def get_outstanding_daily_xl(code: str, start_date: str = "19800101") -> pd.DataFrame:
#     """易封IP，限5秒调用一次"""
#     code = code + code_market_dict()[code]

#     hist = ak.stock_zh_a_daily(symbol=code, start_date=start_date, end_date="20301231")
#     pass

def __del__():
    bs.logout()

if __name__ == "__main__":
    pass
