import akshare as ak
import baostock as bs

import pandas as pd
import requests

from cachetools import cached, TTLCache

from typing import Iterable, List

def get_stocks_series() -> pd.Series:
    spot = ak.stock_zh_a_spot_em()
    return spot["代码"]


@cached(TTLCache(maxsize=1, ttl=60 * 60 * 24))
def code_market_dict():
    url = "http://80.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "50000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:1 t:2,m:1 t:23",
        "fields": "f12",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if not data_json["data"]["diff"]:
        return dict()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df["market_id"] = 'sh'
    temp_df.columns = ["sh_code", "sh_id"]
    code_id_dict = dict(zip(temp_df["sh_code"], temp_df["sh_id"]))
    params = {
        "pn": "1",
        "pz": "50000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0 t:6,m:0 t:80",
        "fields": "f12",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if not data_json["data"]["diff"]:
        return dict()
    temp_df_sz = pd.DataFrame(data_json["data"]["diff"])
    temp_df_sz["sz_id"] = 'sz'
    code_id_dict.update(dict(zip(temp_df_sz["f12"], temp_df_sz["sz_id"])))
    params = {
        "pn": "1",
        "pz": "50000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0 t:81 s:2048",
        "fields": "f12",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if not data_json["data"]["diff"]:
        return dict()
    temp_df_sz = pd.DataFrame(data_json["data"]["diff"])
    temp_df_sz["bj_id"] = 'bj'
    code_id_dict.update(dict(zip(temp_df_sz["f12"], temp_df_sz["bj_id"])))
    return code_id_dict

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
        
    start_date = pd.to_datetime(start_date).strftime("%Y-%m-%d")
    end_date = pd.to_datetime(end_date).strftime("%Y-%m-%d")
        
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
    
    start_date = pd.to_datetime(start_date).strftime("%Y%m%d")
    end_date = pd.to_datetime(end_date).strftime("%Y%m%d")
    
    dfs = []
    for c in code:
        df = get_code_outstading_period(c, start_date, end_date)
        
        min_date = df["变动日期"].min()
        date_range = pd.date_range(min_date, end_date)
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
