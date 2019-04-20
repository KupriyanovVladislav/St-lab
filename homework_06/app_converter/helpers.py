import requests
import json


def update_currencies_file():
    data = fetch_currency_rates()  # type: dict
    return dump_json(data) if data else False


def dump_json(data: dict, file_path="currencies.json") -> bool:
    """
    Returns True in case of success
    Returns False otherwise
    """
    ok = True
    try:
        with open(file_path, 'w') as currencies_file:
            json.dump(data, currencies_file, indent=4)
    except IOError as ex:
        print(f"dump_json(): {ex}")
        ok = False

    return ok


def get_value_currency(currency: str):
    api_url = "http://www.nbrb.by/API/ExRates/Rates/"
    params = {
        "ParamMode": 2,
    }
    response = requests.get(api_url + currency, params)
    if response.status_code == 200:
        data = response.json()
        return round(data["Cur_OfficialRate"] * data["Cur_Scale"], 2)
    else:
        raise ValueError("CURRENCY IS INCORRECT")


def fetch_currency_rates(url="http://www.nbrb.by/API/ExRates/Rates?Periodicity=0") -> dict:
    """
    Used to fetch data by URL.
    """
    data = {}
    response = requests.get(url)
    if response.status_code == 200:
        data = get_json(response)
    return data


def get_json(data):
    data_json = {}
    try:
        data_json = data.json()
    except ZeroDivisionError as ex:
        print(f"get_json(): {ex}")
    return data_json


def fetch_data_from_file(file_path="currencies.json") -> list:
    data = []

    try:
        with open(file_path, "r") as fh:
            data = json.load(fh)
    except IOError as ex:
        print(f"load_json: {ex}")

    return data
