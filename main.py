from flask import Flask, request, jsonify
from flask_cors import CORS
import plot
import risk
import yfinance as yf
from twisted.internet import reactor
from twisted.web import proxy, server

app = Flask(__name__)
CORS(app)

@app.route('/api/main', methods=['POST'])
def main():
    data = request.get_json()
    
    company_name = data.get('company_name')
    stock_data = data.get('stock_data', None)
    predict = data.get('predict', False)
    duration = data.get('duration', '2y')
    print(company_name,predict)
    if stock_data is None:
        stock_data = yf.download(company_name, period=duration, interval='1d')

    stock_data.reset_index(inplace=True)
    company_name = yf.Ticker(company_name).info['longName']

    plot_data=plot.make_graph(stock_data, company_name, duration, predict, '1d')
    risk_output = risk.risk(stock_data=stock_data)

    return jsonify({'plot': plot_data, 'risk_output': risk_output})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

# Twisted reverse proxy server
reverse_proxy_resource = proxy.ReverseProxyResource('localhost', 5000)
site = server.Site(reverse_proxy_resource)
reactor.listenTCP(3000, site)
reactor.run()
