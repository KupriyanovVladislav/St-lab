from flask import render_template, request
from main import app
from helpers import get_value_currency, fetch_data_from_file, update_currencies_file


@app.route('/', methods=['GET', 'PUT'])
def index():
    if request.method == 'PUT':
        update_currencies_file
    data = fetch_data_from_file()  # type: list
    currency_names = [obj.get("Cur_Abbreviation") for obj in data if obj.get("Cur_Abbreviation")]
    return render_template('index.html', currency_names=currency_names)
