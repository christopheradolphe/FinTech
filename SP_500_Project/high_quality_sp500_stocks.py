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

def conservative_debt_structure_check(ticker):
    debt_to_equity = fetch_financial_data(ticker, 'D/E')
    return debt_to_equity < 1.0

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
    elif quantity == "D/E": # Debt to Equity Ratio
        balance = ticker.balance_sheet
        total_liabilities = balance.loc["Total Debt"].dropna().values[0]
        equity = balance.loc["Stockholder's Equity"].dropna().values[0]
        return total_liabilities / equity
    
    elif quantity == "ROIC":
        balance = ticker.balance_sheet
        income = ticker.financials

        # Invested Capital Calculation
        total_assets = balance.loc["Total Assets"].dropna().values[0]
        cash_and_short_term_investments = balance.loc["Cash, Cash Equivalents & Short Term Investments"].dropna().values[0]
        long_term_investments = balance.loc["Investments & Advances"].dropna().values[0]
        non_interest_bearing_current_liabilities = balance.loc["Payables and Accrued Expenses"].dropna().values[0] + balance.loc["Other Current Liabilities"].dropna().values[0]
        invested_capital = total_assets - cash_and_short_term_investments - long_term_investments - non_interest_bearing_current_liabilities

        # NOPAT Calculation
        ebit = income.loc["EBIT"].dropna().values[0]
        tax_rate = income.loc["Tax Provision"].dropna().values[0] / income.loc["Pretax Income"].dropna().values[0]
        nopat = ebit * (1 - tax_rate)

        return nopat / invested_capital
    elif quantity == "WACC":
        return 0
    else:
        raise ValueError(f"Invalid quantity '{quantity}'.")
    
def high_roic_check(ticker):
    roic = fetch_financial_data(ticker, 'ROIC')
    return np.mean(roic) > 0.1
        
def company_vetting(ticker):
    upward_sloping_financials(ticker)
    conservative_debt_structure_check(ticker)

if __name__ == "__main__":
    tickers = get_sp500_tickers()
    count = 0
    for ticker in tickers:
        if upward_sloping_financials(ticker):
            print(ticker)
            count += 1

    print(f"Total percentage with upward sloping: {count / 500:.2%}")