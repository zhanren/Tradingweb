def get_stock_history(stock, start_day=None, end_day=None, period='D', api_key='bvqgjjf48v6qg460kugg'):
    import finnhub
    import datetime
    import pandas as pd

    finhub_client = finnhub.Client(api_key=api_key)
    if end_day is None:
        end_day = int(datetime.datetime.today().timestamp())
    else:
        end_day = int(datetime.datetime.strptime(end_day, '%Y-%M-%d').timestamp())
    if start_day is None:
        start_day = int((datetime.datetime.today() - datetime.timedelta(days=365)).timestamp())
    else:
        start_day = int(datetime.datetime.strptime(start_day, '%Y-%M-%d').timestamp())

    res = finhub_client.stock_candles(stock, period, start_day, end_day)

    res_pd = pd.DataFrame(res)
    res_pd.t = pd.to_datetime(res_pd.t, unit='s')
    res_pd.columns = [
        'close',
        'high',
        'low',
        'open',
        's',
        'time',
        'volume'
    ]

    return res_pd
