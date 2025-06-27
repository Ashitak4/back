from datetime import date, datetime, timedelta
import json
import os
from typing import Union
from flask import jsonify
from app.mocks.mock_response import OVERVIEW, GLOBAL_QUOTE, TIME_SERIES_MONTHLY_ADJUSTED
from app.mocks.mock_stocks import STOCKS
from app.models.companies import Company
from dataclasses import asdict

def build_company_data(company_info: any, global_quote: any, time_series: any) -> Union[Company, None]:
    company = None
    try:
        price = float(global_quote['Global Quote']['05. price'])
        high_price = float(company_info['52WeekHigh'])

        # Compute % drop from 52-week high
        drop_from_high = f"{((price - high_price) / high_price) * 100:.2f}%"
        price_history_10y = get_last_10_years_price_history(time_series)
        company = Company(
            ticker=company_info['Symbol'],
            name=company_info['Name'],
            market_cap=company_info['MarketCapitalization'],
            currency=company_info['Currency'],
            price=global_quote['Global Quote']['05. price'],
            high_price=company_info['52WeekHigh'],
            drop_from_high=drop_from_high,
            pe=str(company_info['PERatio']),
            daily_change=global_quote['Global Quote']['10. change percent'],
            eps=str(company_info['EPS']),
            sector=company_info['Sector'],
            moat='-',
            price_history=price_history_10y
        )
    except KeyError as e:
        print(f"KeyError: {e} - Missing data in company_info or global_quote")
        return None
    except Exception as e:
        print(f"An error occurred while building company data: {e}")
        return None
    return company

def get_last_10_years_price_history(time_series: dict) -> list[float]:
    ten_years_ago = datetime.today().replace(day=1) - timedelta(days=365 * 10)
    return [
        float(data["5. adjusted close"])
        for date_str, data in sorted(time_series.items())
        if datetime.strptime(date_str, "%Y-%m-%d") >= ten_years_ago
    ]


def save_companies_data(companies: list[Company], folder='data'):
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Get today's date as a string
    today = date.today().isoformat()  # e.g., '2025-06-27'

    # Construct file path
    filename = f"{today}.json"
    filepath = os.path.join(folder, filename)

    # Save data as JSON
    json_ready_companies = [asdict(company) for company in companies]

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(json_ready_companies, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved company data to {filepath}")
    
def get_companies_data_from_file(folder='data') -> list[Company]:
    # Get today's date as a string
    today = date.today().isoformat()  # e.g., '2025-06-27'

    # Construct file path
    filename = f"{today}.json"
    filepath = os.path.join(folder, filename)

    if not os.path.exists(filepath):
        print(f"File {filepath} does not exist.")
        return []

    with open(filepath, 'r', encoding='utf-8') as f:
        companies_data = json.load(f)

    return [Company(**data) for data in companies_data]