import requests


def get_currency(currency: str):
    api_url = "http://www.nbrb.by/API/ExRates/Rates/"
    params = {
        "ParamMode": 2
    }
    response = requests.get(api_url + currency, params)
    if response.status_code == 200:
        data = response.json()
        return round(data["Cur_OfficialRate"] * data["Cur_Scale"], 2)
    else:
        raise ValueError("CURRENCY IS INCORRECT")
