import datetime

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from python import config
from python.Stock_history import get_stock_history
from python.component import hovertemplate, dbc_card
from python.helper import get_history_stock_ticker

####get all needed data###
orders = pd.read_csv('python/account_detail/historical_order.csv')
trading_tickers = get_history_stock_ticker(orders)
today = datetime.datetime.today()
yield_rate_df = pd.read_csv('python/account_detail/yield_rate.csv')
current_holding = pd.read_csv('python/account_detail/current_holding.csv')
current_holding_stock = \
current_holding[current_holding.Date == today.strftime('%Y-%m-%d')][current_holding.AssetType == 'STOCK'][
    ['Company', 'Cost Base', 'Price', 'Unrealized Profit Loss Rate (%)', 'Position Proportion (%)']]

app = dash.Dash(__name__)

main_drop_down = dbc.Select(
    id='stock_drop_down',
    className='dropdown',
    options=[
        {"label": "{}".format(stock), "value": "{}".format(stock)} for stock in trading_tickers['Stock symbol']
    ],
    value='NIO'
)

asset_type_check_list = dbc.RadioItems(
    id='asset_type_check_list',
    className='radioitem',
    options=[
        {"label": "Show only stock trade", "value": 'STOCK'},
        {"label": "Show only option trade", "value": 'OPTION'},
        {"label": "Show both stock and option trade", "value": 'ALL'}],
    value='STOCK'
)

calendar = dcc.DatePickerRange(
    id='date_picker_ranger',
    className='calendar',
    initial_visible_month=today.date(),
    start_date=today.date() - datetime.timedelta(days=365),
    end_date=today.date()
)

return_period_type = dbc.Select(
    id="return_period_select",
    className='selector',
    options=[
        {"label": "YTD", "value": "YTD"},
        {"label": "MTD", "value": "MTD"},
        {"label": "Max", "value": "Max"},
    ],
    value='YTD'
)

app.layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                html.H1(config.name, id='title'),
                width={'size': 11, 'offset': 0},
            )
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    [return_period_type,
                     dcc.Loading(dcc.Graph(id="yield_rate_scatter", className='scatter_plot'))],
                    width={'size': 4, 'offset': 1},
                ),
                dbc.Col(
                    dbc.Card(
                        dbc_card('My current position',
                                 [dbc.Table.from_dataframe(
                                     current_holding_stock, striped=True, bordered=True, hover=True, size='sm'),
                                     # dcc.Graph(id='position_pie_chart',
                                     #           className='pie_chart'),
                                 ]
                                 ),
                    ),
                    width={'size': 4, 'offset': 2},
                )
            ]
        ),
        dbc.Row(
            [dbc.Col(
                width={'size': 3, 'offset': 1},
                children=[
                    dbc.Row(
                        dbc.Card(
                            dbc_card('Top three picks All time',
                                     [html.H5('top 3 picks')]
                                     )))
                    ,
                    dbc.Row(
                        dbc.Card(
                            dbc_card('Top three picks this month',
                                     [
                                         html.H5('top 3 picks this month')
                                     ]
                                     )
                        ),
                    )
                ]
            ),
                dbc.Col(
                    width={'size': 6, 'offset': 1},
                    children=[
                        dbc.Row(
                            dbc.Col(
                                     [
                                         main_drop_down,
                                         asset_type_check_list,
                                         calendar,
                                         dcc.Loading(dcc.Graph(id="main_graph", hoverData={}))
                                     ]
                            )
                        )
                    ]
                ), ]
        )
    ]
)


# @app.callback(
#     Output('yield_rate_bar', 'figure'),
#     [Input('return_period_select', 'value')
#      ])
# def generate_yield_bar(return_type):
#     if return_type == 'Max':
#         date = '1900-01-01'
#     elif return_type == 'YTD':
#         date = str(today.year) + '-01-01'
#     elif return_type == 'MTD':
#         month = str(today.month)
#         if len(month) == 1:
#             month = '0' + month
#         date = str(today.year) + '-' + month + '-01'
#
#     yield_rate_df_temp = yield_rate_df[yield_rate_df.date >= date]
#
#     last_day = yield_rate_df_temp.iloc[-1]
#     first_day = yield_rate_df_temp.iloc[0]
#
#     my_portfolio_return = (last_day.yieldRate + 1) / (first_day.yieldRate + 1) - 1
#     dia_portfolio_return = (last_day.yield_rate_dia + 1) / (first_day.yield_rate_dia + 1) - 1
#     ixic_portfolio_return = (last_day.yield_rate_ixic + 1) / (first_day.yield_rate_ixic + 1) - 1
#     spy_portfolio_return = (last_day.yield_rate_spy + 1) / (first_day.yield_rate_spy + 1) - 1
#
#     name_list = ['My portfolio return', 'Dow&Jones return', 'Nasdaq return', 'S&P500 return']
#
#     fig = go.Figure(
#         data=[
#             go.Bar(
#                 x=name_list,
#                 y=[my_portfolio_return, dia_portfolio_return, ixic_portfolio_return, spy_portfolio_return]
#             )
#         ],
#     )
#
#     # bar chart fig config
#     fig.update_layout(
#         yaxis={
#             'tickformat': '.0%'
#         },
#         width=400,
#         height=300,
#         paper_bgcolor='#000',
#         plot_bgcolor='#000'
#     ),
#
#     return fig


@app.callback(
    Output('yield_rate_scatter', 'figure'),
    [Input('return_period_select', 'value')
     ])
def generate_yield_scatter(return_type):
    if return_type == 'Max':
        date = '1900-01-01'
    elif return_type == 'YTD':
        date = str(today.year) + '-01-01'
    elif return_type == 'MTD':
        month = str(today.month)
        if len(month) == 1:
            month = '0' + month
        date = str(today.year) + '-' + month + '-01'

    yield_rate_df_temp = yield_rate_df[yield_rate_df.date >= date]

    first_day = yield_rate_df_temp.iloc[0]

    for r in ['yieldRate', 'yield_rate_dia', 'yield_rate_ixic', 'yield_rate_spy']:
        yield_rate_df_temp[r] = (yield_rate_df_temp[r] + 1) / (first_day[r] + 1) - 1

    fig = go.Figure(
        data=[go.Scatter(
            x=yield_rate_df_temp.date,
            y=yield_rate_df_temp.yieldRate,
            mode='lines+markers',
            name='My portoflio return',
            marker=dict(
                color='#FEDE61',
                size=5),
            line=dict(
                width=3
            ),
            textfont=dict(
                color='gold',
                family='Poor Story'
            ))]
    )

    fig.add_trace(go.Scatter(
        x=yield_rate_df_temp.date,
        y=yield_rate_df_temp.yield_rate_dia,
        mode='lines+markers',
        name='Dow&Jones return',
        marker=dict(
            color='#20EBB4',
            size=2),
        line=dict(
            width=2
        ),
        textfont=dict(
            color='green'
        )
    ))

    fig.add_trace(go.Scatter(
        x=yield_rate_df_temp.date,
        y=yield_rate_df_temp.yield_rate_ixic,
        mode='lines+markers',
        name='Nasdaq return',
        marker=dict(
            color='#78E7F5',
            size=2),
        textfont=dict(
            color='blue'
        )
    ))

    fig.add_trace(go.Scatter(
        x=yield_rate_df_temp.date,
        y=yield_rate_df_temp.yield_rate_spy,
        mode='lines+markers',
        name='S&P500 return',
        marker=dict(
            color='#F51B74',
            size=2),
        textfont=dict(
            color='red'
        )
    ))

    #portfolio return fig layout
    fig.update_layout(
        yaxis={
            'tickformat': '.0%',
            'showgrid': False
        },
        xaxis={
            'showgrid': False
        },
        width=650,
        height=400,
        paper_bgcolor='#000',
        plot_bgcolor='#000',
        font_color='#fff'
    )

    return fig


#
#
# @app.callback(
#     Output('position_pie_chart', 'figure'),
#     [Input('date_picker_ranger', 'start_date'),
#      Input('date_picker_ranger', 'end_date')
#      ])
# def generate_position_pie(start_date, end_date):
#     fig = go.Figure(
#         data=[go.Pie(labels=current_holding_stock.Company, values=current_holding_stock.positionProportion, hole=0.4)]
#     )
#
#     return fig


@app.callback(
    Output('main_graph', 'figure'),
    [Input('stock_drop_down', 'value'),
     Input('date_picker_ranger', 'start_date'),
     Input('date_picker_ranger', 'end_date'),
     Input('asset_type_check_list', 'value')
     ])
def get_main_graph(stock, start_date, end_date, asset_type):
    candle_stick = get_stock_history(stock)

    fig = go.Figure(data=[go.Candlestick(x=candle_stick.time,
                                         open=candle_stick.open,
                                         high=candle_stick.high,
                                         low=candle_stick.low,
                                         close=candle_stick.close,
                                         name=stock + ' Price'
                                         )])

    if asset_type == 'ALL':
        trade_data = orders.loc[(orders['Stock symbol'] == stock) &
                                (pd.to_datetime(orders.Date) >= pd.to_datetime(start_date)) &
                                (pd.to_datetime(orders.Date) <= pd.to_datetime(end_date))]
    else:
        trade_data = orders.loc[(orders['Stock symbol'] == stock) &
                                (orders['Stock/Option'] == asset_type) &
                                (pd.to_datetime(orders.Date) >= pd.to_datetime(start_date)) &
                                (pd.to_datetime(orders.Date) <= pd.to_datetime(end_date))]

    if trade_data.empty:
        pass
    else:
        for index, trade in trade_data.iterrows():
            fig.add_trace(go.Scatter(
                x=[trade.Date],
                y=[trade.Price] if trade['Stock/Option'] == 'STOCK' else [trade['Strike Price']],
                mode='markers',
                hovertemplate=hovertemplate(trade),
                name='SHORT' if trade['long/short'] == 'short' else 'LONG',
                marker=dict(
                    color='blue' if trade['long/short'] == 'short' else 'gold',
                    symbol='triangle-down-open' if trade['long/short'] == 'short' else 'triangle-up-open',
                    size=8),
                textfont=dict(
                    color='blue' if trade['long/short'] == 'short' else 'gold'
                )
            ))

    fig.update_layout(paper_bgcolor='#000',
                      plot_bgcolor='#000',
                      width=800,
                      height=600,
                      xaxis={
                          'showgrid': False
                      },
                      yaxis={
                          'showgrid': False
                      },
                      font_color='#fff',
                      showlegend=False
                      ),

    fig.update_xaxes(rangebreaks=[
        dict(bounds=['sat', 'mon'])
    ])

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
