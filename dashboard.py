import dash
import dash_bootstrap_components as dbc
import pandas as pd

orders = pd.read_csv('python/test_order.csv')
pl_history = pd.read_csv('python/test_pl_history.csv')

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

if __name__ == '__main__':
    app.run_server(debug=True)
