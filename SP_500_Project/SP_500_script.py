import pandas as pd
import numpy as np
import statsmodels.api as sm

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

if __name__ == "__main__":
    tickers = get_sp500_tickers()
    print(tickers[:10])