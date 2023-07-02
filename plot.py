import plotly.graph_objects as go
import plotly.utils
import yfinance as yf
import numpy as np
import pandas as pd
import tensorflow as tf
import predict
import json
def get_duration_label(duration):
    if duration[1] == 'm':
        return duration[0] + ' ' + "Month(s)"
    elif duration[1] == 'y':
        return duration[0] + ' ' + "Year(s)"
    return duration[0]

def create_graph(data, company_name, period, future_predictions=None):
    fig = go.Figure()

    if future_predictions is not None:
        # Smooth curve for historical data
        alpha = 0.2  # Adjust the alpha parameter as needed
        smoothed_data = predict.exponential_weighting(data['Close'], alpha)
        fig.add_trace(go.Scatter(x=data['Date'], y=smoothed_data, name='Historical Data (Smooth)'))
    else:
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Historical Data'))

    if future_predictions is not None:
        future_dates = pd.date_range(start=data['Date'].iloc[-1] + pd.DateOffset(days=1), periods=len(future_predictions), freq='D').strftime('%Y-%m-%d').tolist()
        fig.add_trace(go.Scatter(x=future_dates, y=future_predictions.flatten(), name='Future Predictions'))

    fig.update_layout(
        title=company_name + " - Stock Price of past " + get_duration_label(period),
        xaxis_title='Date',
        yaxis_title='Price (in USD)',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='white'),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    return fig


def plot_graph(fig):
    fig.show()
def make_graph(stock_data,company_name,span, needPredictions=False, interval='1d'):
    

    # Call the predict function to get future prices
    if needPredictions:
        future_prices = predict.predict(stock_data,"2y", future=20)  # Use your desired value for 'future'
        fig = create_graph(stock_data, company_name, span, future_predictions=future_prices)
    else:
        fig = create_graph(stock_data, company_name, span)
    plot_graph(fig)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

