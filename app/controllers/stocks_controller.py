from flask import jsonify
from app.mocks.mock_response import OVERVIEW, GLOBAL_QUOTE, TIME_SERIES_MONTHLY_ADJUSTED
from app.mocks.mock_stocks import STOCKS
from app.misc.key import API_KEY
from app.misc.watchlist_keys import WATCHLIST_PEA
from app.domain.stocks_domain import build_company_data, get_companies_data_from_file, save_companies_data
from app.models.companies import Company


def get_stock_data():
    overview_data = OVERVIEW
    global_quote_data = GLOBAL_QUOTE
    time_series_monthly_adjusted_data = TIME_SERIES_MONTHLY_ADJUSTED
    

    # print("stock_data", stock_data)
    response = {
        "overview": overview_data,
        "global_quote": global_quote_data,
        "time_series_monthly_adjusted": time_series_monthly_adjusted_data
    }
    return response

def load_companies_data():
    company_pea = WATCHLIST_PEA
    companies_data = []
    for ticker in company_pea:
        company = build_company_data(OVERVIEW, GLOBAL_QUOTE, TIME_SERIES_MONTHLY_ADJUSTED['Monthly Adjusted Time Series'])
        if company:
            companies_data.append(company)
        # url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}'
        # r = requests.get(url)
        # overview = r.json()
        
        # url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}'
        # r = requests.get(url)
        # global_quote = r.json()
        
        # url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={ticker}&apikey={API_KEY}'
        # r = requests.get(url)
        # time_series_monthly_adjusted = r.json()
        
    save_companies_data(companies_data)
    return companies_data, 200
    
    
    # url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={API_KEY}'
    # url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={API_KEY}'
    # url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&symbol={ticker}&apikey={API_KEY}'
    # r = requests.get(url)
    # stock_data = r.json()
    companies_data = build_companies_data()
    save_companies_data(companies_data)
    
def get_companies_data() -> list[Company]:
    companies_data = []
    companies_data = get_companies_data_from_file()
    return companies_data