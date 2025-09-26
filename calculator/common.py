from .settings import POLYGON_API_KEY, POLYGON_API_URL
import requests
from datetime import datetime


def get_dividends_from_date(
    ymd_from: str | datetime, 
    ymd_to: str | datetime, 
    ticker: str, 
    order: str = "desc", 
    sort: str = "ex_dividend_date",
):
    """
    Args:
        ymd_from (str | datetime): ex) "2020-01-01"
        ymd_to (str | datetime): ex) "2023-01-01"
        ticker (str): ex) "AAPL"
        order (str, optional): "asc" or "desc". Defaults to "desc".
        sort (str, optional): "ex_dividend_date" or "record_date". Defaults to "ex_dividend_date".
    Returns:
        list: dividends data from Polygon.io
    Raises:
        Exception: when API call fails
    """
    url = POLYGON_API_URL.format(vesion="v3", search_type="dividends")

    params = {
        "order": order,
        "from": ymd_from.strftime("%Y-%m-%d") if isinstance(ymd_from, datetime) else ymd_from,
        "to": ymd_to.strftime("%Y-%m-%d") if isinstance(ymd_to, datetime) else ymd_to,
        "sort": sort,
        "ticker": ticker,
        "apiKey": POLYGON_API_KEY,
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        else:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {e}")
