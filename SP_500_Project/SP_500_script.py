import pandas as pd
import numpy as np
import statsmodels.api as sm
from yahoo_fin import stock_info as si

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    sp500_table = tables[0]
    tickers = sp500_table['Symbol'].tolist()
    return tickers

def is_reliably_increasing(data):
    x = np.arrange(len(data))
    X = sm.add_constant(x)
    model = sm.OLS(data, X).fit()
    slope = model.params[1]
    p_value = model.pvalues[1]
    return (slope > 0 and p_value < 0.05)

def upward_sloping_financials(ticker):
    return all([
        is_reliably_increasing(fetch_financial_data(ticker, 'Free Cash Flow')),
        is_reliably_increasing(fetch_financial_data(ticker, 'Net Income')),
        is_reliably_increasing(fetch_financial_data(ticker, 'Revenue'))
    ])

def fetch_financial_data(ticker, quantity):
    if quantity == 'Free Cash Flow':
        cash_flow = si.get_cash_flow(ticker, yearly=True)
        return cash_flow.loc["totalCashFromOperatingActivities"] - cash_flow.loc["capitalExpenditures"]
    elif quantity == 'Net Income': 
        income_statement = si.get_income_statement(ticker, yearly=True)
        return income_statement.loc["netIncome"]
    elif quantity == 'Revenue': 
        income_statement = si.get_income_statement(ticker, yearly=True)
        revenue = income_statement.loc["totalRevenue"]
    else:
        raise ValueError(f"Invalid quantity '{quantity}'. Expected one of: 'Free Cash Flow', 'Net Income', 'Revenue'.")
        

if __name__ == "__main__":
    tickers = get_sp500_tickers()
    for ticker in tickers[:10]:
        if upward_sloping_financials(ticker):
            print(ticker)
        else:
            print(f"No dice for {ticker}")