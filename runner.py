from datetime import datetime, timedelta

import pandas as pd
import yaml
from webull import webull

from python.helper import get_trading_history, get_current_holding, get_stock_performace

if __name__ == '__main__':
    account_info = yaml.safe_load(open('account_info.yaml'))

    today = datetime.today()
    date_end = today.strftime('%Y-%m-%d')
    date_start = (today - timedelta(365)).strftime('%Y-%m-%d')
    week_start = (today - timedelta(today.weekday())).strftime('%Y-%m-%d')
    month_start = (today - timedelta(today.day - 1)).strftime('%Y-%m-%d')

    wb = webull()
    wb.login(account_info['phone_number'], account_info['password'])
    wb.secondary_login(account_info['secondary_pass'])

    monthly_stock_performance = wb.get_stock_performance(month_start, date_end)
    weekly_stock_performance = wb.get_stock_performance(week_start, date_end)
    overall_stock_performance = wb.get_stock_performance(date_start, date_end)

    get_stock_performace(monthly_stock_performance).to_csv('python/account_detail/monthly_stock_performance.csv')
    get_stock_performace(weekly_stock_performance).to_csv('python/account_detail/weekly_stock_performance.csv')
    get_stock_performace(overall_stock_performance).to_csv('python/account_detail/overall_stock_performance.csv')

    profit_loss_history = wb.get_proft_loss_history()
    pd.DataFrame(profit_loss_history).to_csv('python/account_detail/profit_loss_history.csv')

    orders = historical_orders = wb.get_history_orders(status='FILLED', count=10000)
    get_trading_history(orders).to_csv('python/account_detail/historical_order.csv')

    net_liquidity_history = wb.get_net_liquidity()
    pd.DataFrame(net_liquidity_history).to_csv('python/account_detail/net_liquidity_history.csv')

    yield_rate_dia = wb.get_yield_rate(date_start, index='DIA')
    yield_rate_ixic = wb.get_yield_rate(date_start, index='IXIC')
    yield_rate_spy = wb.get_yield_rate(date_start, index='SPY')

    yield_rate = pd.DataFrame(yield_rate_dia)
    yield_rate_ixic = pd.DataFrame(yield_rate_ixic)
    yield_rate_spy = pd.DataFrame(yield_rate_spy)

    yield_rate['yield_rate_dia'] = yield_rate.indexYieldRate
    yield_rate['yield_rate_ixic'] = yield_rate_ixic.indexYieldRate
    yield_rate['yield_rate_spy'] = yield_rate_spy.indexYieldRate

    yield_rate.to_csv('python/account_detail/yield_rate.csv')

    current_holding = wb.get_positions()
    get_current_holding(current_holding).to_csv('python/account_detail/current_holding.csv')
