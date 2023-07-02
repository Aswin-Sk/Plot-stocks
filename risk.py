from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
def riskcal(stock_data, months):
    end_date = date.today()
    start_date = end_date - relativedelta(months=months)
    data =  stock_data[(stock_data['Date'] >= pd.Timestamp(start_date)) & (stock_data['Date'] <= pd.Timestamp(end_date))]
    data=data['Close']
    data = data.pct_change().dropna()
    data = data.describe()
    data["mean"] *= 251
    data["std"] *= np.sqrt(251)
    std = data["std"] / data["mean"]
    std = std.item()
    print(std)
    if std < 0.1:
        return "low"
    elif std < 0.3:
        return "moderate"
    else:
        return "high"

def risk(stock_data):
    return {
        'risk_1_month': (riskcal(stock_data, 1)),
        'risk_6_months': (riskcal(stock_data, 6)),
        'risk_24_months': (riskcal(stock_data, 24))
    }