import dash_bootstrap_components as dbc

dbc.themes

def hovertemplate(trade):
    if trade['Stock/Option'] == 'STOCK':

        template = ('<b>Asset Type: </b>' + trade['Stock/Option'] +
                    "<br>Price: " + str(trade['Price']) +
                    "<br>Quantity: " + str(trade['Quantity']) +
                    '<br>Total Amount ($): ' + str(trade['Total Amount ($)']) +
                    '<br>Action: ' + str(trade['Action']))

    elif trade['Stock/Option'] == 'OPTION':

        template = ('<b>Asset Type: </b>' + trade['Stock/Option'] +
                    "<br>Price: " + str(trade['Price']) +
                    "<br>Quantity: " + str(trade['Quantity']) +
                    '<br>Total Amount ($): ' + str(trade['Total Amount ($)']) +
                    '<br>Action: ' + str(trade['Action']) +
                    '<br>' +
                    '<b>Option detail: </b>' +
                    '<br>Option type: ' + trade['Option type'] +
                    '<br>Strick Price: ' + str(trade['Strike Price']) +
                    '<br>Option Expire Date: ' + trade['Option Expire Date'])

    return template


def dbc_card(title, content):
    card_content = [
        dbc.CardHeader(title),
        dbc.CardBody(
            content
        ),
    ]

    return card_content

# dbc.Card(
# dbc_card('My Portfolio Return Bar; bar_plot',
# [dcc.Graph(id='yield_rate_bar', className='bar_plot')]),
# color='primary',
# outline=True),