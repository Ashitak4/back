from . import api
from app.controllers.stocks_controller import get_stock_data, get_companies_data, load_companies_data

@api.route('/load_companies', methods=['POST'])
def load_companies():
    return load_companies_data()

@api.route('/stock/<ticker>', methods=['GET'])
def get_stock(ticker):
    return get_stock_data(ticker)

@api.route('/companies', methods=['GET'])
def get_companies():
    return get_companies_data()