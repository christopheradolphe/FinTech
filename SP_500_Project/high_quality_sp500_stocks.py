import pandas as pd
import numpy as np
import statsmodels.api as sm
import yfinance as yf

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    sp500_table = tables[0]
    tickers = sp500_table['Symbol'].tolist()
    return tickers

def is_reliably_increasing(data):
    x = np.arange(len(data))
    X = sm.add_constant(x)
    model = sm.OLS(data, X).fit()
    slope = model.params[1]
    p_value = model.pvalues[1]
    return (slope > 0) and (p_value < 0.1)

def upward_sloping_financials(ticker):
    return all([
        is_reliably_increasing(fetch_financial_data(ticker, 'Free Cash Flow')),
        is_reliably_increasing(fetch_financial_data(ticker, 'Net Income')),
        is_reliably_increasing(fetch_financial_data(ticker, 'Revenue'))
    ])

def fetch_financial_data(ticker, quantity):
    ticker = yf.Ticker(ticker)
    if quantity == 'Free Cash Flow':
        cashflow = ticker.cashflow
        return cashflow.loc["Free Cash Flow"].dropna().values[::-1]
    elif quantity == 'Net Income': 
        income = ticker.financials
        return income.loc["Net Income"].dropna().values[::-1]
    elif quantity == 'Revenue': 
        income = ticker.financials
        return income.loc["Total Revenue"].dropna().values[::-1]
    elif quantity == "Debt-to_Equity":
        balance = yf.Ticker(ticker).balance_sheet
        total_liabilities = balance.loc["Total Debt"].dropna().values[0]
        equity = balance.loc["Stockholder's Equity"].dropna().values[0]
        return total_liabilities / equity
    else:
        raise ValueError(f"Invalid quantity '{quantity}'. Expected one of: 'Free Cash Flow', 'Net Income', 'Revenue'.")
        

if __name__ == "__main__":
    tickers = get_sp500_tickers()
    count = 0
    for ticker in tickers:
        if upward_sloping_financials(ticker):
            print(ticker)
            count += 1

    print(f"Total percentage with upward sloping: {count / 500:.2%}")