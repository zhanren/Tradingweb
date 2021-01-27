import pandas as pd

def get_trading_history(orders):
    trading_history = pd.DataFrame()

    for order in orders:
        action = order['action']
        type_ = order['comboTickerType'].upper()
        quantity = order['quantity']
        detail = order['orders'][0]
        if detail['statusStr'] != 'Filled':
            pass
        else:
            if type_ == 'STOCK':
                tradeID = detail['orderId']
                option_type = None
                Strike_price = None
                Expire_date = None
                price = detail['avgFilledPrice']
                filledTime = detail['filledTime']
                filledValue = detail['filledValue']
                stock = detail['ticker']
                symbol = stock['disSymbol']
                company = stock['tinyName']
                ticker = stock['tickerId']
            if type_ == 'OPTION':
                tradeID = detail['orderId']
                price = detail['avgFilledPrice']
                filledTime = detail['filledTime']
                filledValue = detail['filledValue']
                stock = detail['ticker']
                symbol = stock['disSymbol']
                company = stock['tinyName']
                option_type = detail['optionType']
                Strike_price = detail['optionExercisePrice']
                Expire_date = detail['optionExpireDate']
                ticker = stock['tickerId']

            current_line = pd.Series([tradeID,
                                      filledTime,
                                      symbol,
                                      company,
                                      price,
                                      quantity,
                                      filledValue,
                                      type_,
                                      Strike_price,
                                      option_type,
                                      action,
                                      Expire_date,
                                      ticker])

            trading_history = trading_history.append(
                current_line, ignore_index=True)

    trading_history = trading_history.rename(
        columns={
            0: 'trade Id',
            1: 'Time',
            2: 'Stock symbol',
            3: 'Company',
            4: 'Price',
            5: 'Quantity',
            6: 'Total Amount ($)',
            7: 'Stock/Option',
            8: 'Strike Price',
            9: 'Option type',
            10: 'Action',
            11: 'Option Expire Date',
            12: 'ticker'
        }
    )

    trading_history['long/short'] = [
        'long' if (type_ == 'STOCK' and action == 'BUY') or (
                type_ == 'OPTION' and option_type == 'call' and action == 'BUY') or (
                          type_ == 'OPTION' and option_type == 'put' and action == 'SELL')
        else 'short' for type_, action, option_type in
        zip(trading_history['Stock/Option'], trading_history['Action'], trading_history['Option type'])
    ]

    trading_history['Date'] = pd.to_datetime(trading_history['Time']).dt.date

    return trading_history


def get_history_stock_ticker(trading_history):
    trading_company = trading_history.drop_duplicates(['Stock symbol', 'ticker', 'Company']).filter(
        ['Stock symbol', 'ticker', 'Company'], axis=1)

    return trading_company


def get_current_holding(current_holding):
    position_df = pd.DataFrame()

    for stock in current_holding:
        info = stock['ticker']
        symbol = info['symbol']
        position = int(stock['position'])
        assetType = stock['assetType'].upper()
        totalcost = stock['cost']
        cost = round(float(stock['cost']) / position, 2)
        lastPrice = stock['lastPrice']
        marketValue = stock['marketValue']
        unrealizedProfitLossRate = str(round(float(stock['unrealizedProfitLossRate']) * 100, 1)) + '%'
        positionProportion = str(round(float(stock['positionProportion']) * 100, 1)) + '%'

        current_line = pd.Series([
            symbol,
            position,
            assetType,
            totalcost,
            cost,
            lastPrice,
            marketValue,
            unrealizedProfitLossRate,
            positionProportion
        ])

        position_df = position_df.append(
            current_line, ignore_index=True)

    position_df = position_df.rename(
        columns={
            0: 'Company',
            1: 'Position',
            2: 'AssetType',
            3: 'Total Cost',
            4: 'Cost Base',
            5: 'Price',
            6: 'MarketValue',
            7: 'Unrealized Profit Loss Rate (%)',
            8: 'Position Proportion (%)',
        }
    )

    position_df.sort_values('Total Cost', ascending=False, inplace=True)

    return position_df

def get_stock_performace(stocks):
    performance_df = pd.DataFrame()

    for stock in stocks['items']:
        profit = stock['totalProfitLoss']
        info = stock['ticker']
        symbol = info['symbol']
        name = info['tinyName']

        current_line = pd.Series([
            name,
            symbol,
            profit
        ])

        performance_df = performance_df.append(
            current_line, ignore_index=True)

    performance_df = performance_df.rename(
        columns={
            0: 'Company',
            1: 'Symbol',
            2: 'Profit'
        }
    )

    return performance_df
