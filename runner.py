from datetime import datetime, timedelta

import hydra
import pandas as pd
import webull
from omegaconf import OmegaConf

from python.helper import get_trading_history, get_current_holding, get_stock_performace


def hydra_init(
        config_path='settings',
        config_name='config',
        strict=None
):
    return hydra.main(config_name=config_name, config_path=config_path, strict=strict)


@hydra_init()
def main(cfg):
    print(OmegaConf.to_yaml(cfg))
    if cfg.download_data:
        today = datetime.today()
        date_end = today.strftime('%Y-%m-%d')
        date_start = (today - timedelta(365)).strftime('%Y-%m-%d')
        week_start = (today - timedelta(today.weekday())).strftime('%Y-%m-%d')
        month_start = (today - timedelta(today.day - 1)).strftime('%Y-%m-%d')

        wb = webull.webull()

        wb.login(cfg.phone_number, cfg.password)
        wb.secondary_login(cfg.secondary_pass)

        monthly_stock_performance = wb.get_stock_performance(month_start, date_end)
        weekly_stock_performance = wb.get_stock_performance(week_start, date_end)
        overall_stock_performance = wb.get_stock_performance(date_start, date_end)

        get_stock_performace(monthly_stock_performance).to_csv(
            '../../../python/account_detail/monthly_stock_performance.csv')
        get_stock_performace(weekly_stock_performance).to_csv(
            '../../../python/account_detail/weekly_stock_performance.csv')
        get_stock_performace(overall_stock_performance).to_csv(
            '../../../python/account_detail/overall_stock_performance.csv')

        profit_loss_history = wb.get_proft_loss_history()
        pd.DataFrame(profit_loss_history).to_csv('../../../python/account_detail/profit_loss_history.csv')

        orders = wb.get_history_orders(date_start, date_end, status='FILLED', count=10000)
        get_trading_history(orders).to_csv('../../../python/account_detail/historical_order.csv')

        net_liquidity_history = wb.get_net_liquidity()
        pd.DataFrame(net_liquidity_history).to_csv('../../../python/account_detail/net_liquidity_history.csv')

        yield_rate_dia = wb.get_yield_rate(date_start, index='DIA')
        yield_rate_ixic = wb.get_yield_rate(date_start, index='IXIC')
        yield_rate_spy = wb.get_yield_rate(date_start, index='SPY')

        yield_rate = pd.DataFrame(yield_rate_dia)
        yield_rate_ixic = pd.DataFrame(yield_rate_ixic)
        yield_rate_spy = pd.DataFrame(yield_rate_spy)

        yield_rate['yield_rate_dia'] = yield_rate.indexYieldRate
        yield_rate['yield_rate_ixic'] = yield_rate_ixic.indexYieldRate
        yield_rate['yield_rate_spy'] = yield_rate_spy.indexYieldRate

        yield_rate.to_csv('../../../python/account_detail/yield_rate.csv')

        current_holding = wb.get_positions()
        current_holding = get_current_holding(current_holding).assign(Date=date_end)
        current_holding.to_csv('../../../python/account_detail/current_holding.csv', header=False, mode='a')


if __name__ == '__main__':
    main()
