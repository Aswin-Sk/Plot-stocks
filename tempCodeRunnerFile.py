['longName']

    plot_data=plot.make_graph(stock_data, company_name, duration, predict, '1d')
    risk_output = risk.risk(stock_data=stock_data)

    return jsonify({'plot': plot_data, 'risk_output': risk_output})
