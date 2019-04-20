from flask import Flask
from helpers import update_currencies_file

update_currencies_file()

app = Flask(__name__)

from views import index
