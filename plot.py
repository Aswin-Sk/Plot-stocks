import plotly.graph_objects as go
import pandas as pd
import predict
import json
from datetime import datetime, timedelta


def get_duration_label(duration):
    if duration[1] == 'm':
        return duration[0] + ' ' + "Month(s)"
    elif duration[1] == 'y':
        return duration[0] + ' ' + "Year(s)"
    return duration[0]


from datetime import timedelta

def create_graph(data, company_name, period, future_predictions=None):
    graph_data = []
    if future_predictions is not None:
        alpha = 0.2
        smoothed_data = predict.exponential_weighting(data['Close'], alpha).tolist()
        graph_data.append({
            'x': data['Date'].dt.strftime('%Y-%m-%d').tolist(),
            'y': smoothed_data,
            'type': 'scatter',
            'mode': 'lines+markers',
            'marker': {'color': 'red'},
            'name': 'Historical Data (Smooth)'
        })
    else:
        graph_data.append({
            'x': data['Date'].dt.strftime('%Y-%m-%d').tolist(),
            'y': data['Close'].tolist(),
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': 'Historical Data'
        })

    if future_predictions is not None:
        last_date = data['Date'].iloc[-1].to_pydatetime()
        future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=len(future_predictions), freq='D')
        future_dates_str = future_dates.strftime('%Y-%m-%d').tolist()
        graph_data.append({
            'x': [data['Date'].iloc[-1].strftime('%Y-%m-%d')] + future_dates_str,
            'y': [data['Close'].iloc[-1]] + future_predictions.flatten().tolist(),
            'type': 'scatter',
            'mode': 'lines+markers',
            'name': 'Future Predictions'
        })

    layout = {
        'width': 320,
        'height': 240,
        'title': company_name + " - Stock Price of past " + get_duration_label(period)
    }

    return {
        'data': graph_data,
        'layout': layout
    }


def make_graph(stock_data, company_name, span, needPredictions=False, interval='1d'):
    # Call the predict function to get future prices
    if needPredictions:
        future_prices = predict.predict(stock_data, "2y", future=20)  # Use your desired value for 'future'
        graph = create_graph(stock_data, company_name, span, future_predictions=future_prices)
    else:
        graph = create_graph(stock_data, company_name, span)

    return json.dumps(graph)
