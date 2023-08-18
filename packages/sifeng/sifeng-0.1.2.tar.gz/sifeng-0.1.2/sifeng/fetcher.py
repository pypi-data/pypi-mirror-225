import warnings
warnings.simplefilter("ignore", category=UserWarning)
import grequests
import requests
import pandas as pd
import json
import math

base_url = "https://service-cemns23n-1300348397.sh.apigw.tencentcs.com/"

def query_size(api, **kwargs):
    api_map = {
        "/stock/basic_info": (0, "basic_info"),
        "/stock/kline_day": (2, "kline_day"),
        "/stock/indicator_day": (2, "indicator_day")
    }
    kwargs = kwargs.copy()
    kwargs["table_type"] = api_map[api][0]
    kwargs["table_name"] = api_map[api][1]
    response = requests.request("GET", base_url + "stock/table_count", params=kwargs, timeout=20.0)
    response_json = json.loads(response.text)
    return response_json["result"]

def query(api, fields="*", workers=8, **kwargs):
    """
        Query the distant server and retrieve information.
    """
    if api == "ping":
        response = requests.request("GET", base_url + api, params=kwargs, timeout=20.0)
        return json.loads(response.text)["response"]
    api_map = {
        "/stock/basic_info": ["stock_code", "list_status", "st_flag", "list_date", "industry", "sector", "area", "stock_name"],
        "/stock/kline_day": ["stock_code", "trade_date", "open", "high", "low", "close", "vol", "amount", "adj_factor"],
        "/stock/indicator_day": ["trade_date", "stock_code", "turnover_rate", "turnover_rate_free", "volume_ratio", "pe", "pe_ttm", "pb", "ps", "ps_ttm", "dv_ratio", "dv_ttm", "total_share", "float_share", "free_share", "total_mv", "circ_mv"]
    }
    if "limit" in kwargs.keys() or "offset" in kwargs.keys():
        kwargs["fields"] = api_map[api] if fields == "*" else fields
        response = requests.request("GET", base_url + api, params=kwargs, timeout=20.0)
        response_json = json.loads(response.text)
        if response.status_code != 200:
            raise Exception(response_json["response"])
        else:
            return pd.DataFrame(data=response_json["result"], columns=kwargs["fields"])
    else:
        def handler(request, exception):
            raise Exception(f"Request failed: {exception}")
        def dict_update(dictx, limit, offset):
            dictx["limit"] = limit
            dictx["offset"] = offset
            return dictx
        table_size = query_size(api=api, **kwargs)
        kwargs["fields"] = api_map[api] if fields == "*" else fields
        query = [grequests.request("GET", base_url + api, params=dict_update(kwargs, limit=10000, offset=_ * 10000), timeout=20.0) for _ in range(0, math.ceil(table_size / 10000), 1)]
        try:
            responses = grequests.map(query, size=workers, exception_handler=handler)
        except Exception as excptn:
            return f"{excptn}"
        else:
            result = pd.DataFrame(columns=kwargs["fields"])
            for response in responses:
                response_json = json.loads(response.text)
                if response.status_code != 200:
                    raise Exception(response_json["response"])
                result = pd.concat([result, pd.DataFrame(data=response_json["result"], columns=kwargs["fields"])], axis=0)
            return result
