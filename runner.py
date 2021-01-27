import logging
from datetime import datetime, timedelta

import hydra
import pandas as pd
import webull

from python.helper import get_trading_history, get_current_holding, get_stock_performace


def hydra_init(
        config_path='conf',
        config_name='config',
        strict=None
):
    return hydra.main(config_name=config_name, config_path=config_path, strict=strict)


@hydra_init()
def main(cfg):
    if cfg.steps_to_run.download_data:
        today = datetime.today()
        date_end = today.strftime('%Y-%m-%d')
        date_start = (today - timedelta(365)).strftime('%Y-%m-%d')
        week_start = (today - timedelta(today.weekday())).strftime('%Y-%m-%d')
        month_start = (today - timedelta(today.day - 1)).strftime('%Y-%m-%d')

        wb = webull.webull()

        wb.login(cfg.account_info.phone_number, cfg.account_info.password)
        wb.secondary_login(cfg.account_info.secondary_pass)

        logging.info('Logging Success!')

        if cfg.download_steps.stock_performance.overall:
            logging.info('Download overall stock performance')
            get_stock_performace(wb.get_stock_performance(date_start, date_end)).to_csv(
                '../../../python/account_detail/overall_stock_performance.csv')

        if cfg.download_steps.stock_performance.monthly:
            logging.info('Download overall monthly performance')
            get_stock_performace(wb.get_stock_performance(month_start, date_end)).to_csv(
                '../../../python/account_detail/monthly_stock_performance.csv')

        if cfg.download_steps.stock_performance.weekly:
            logging.info('Download overall weekly performance')
            get_stock_performace(wb.get_stock_performance(week_start, date_end)).to_csv(
                '../../../python/account_detail/weekly_stock_performance.csv')

        if cfg.download_steps.profit_loss_history:
            logging.info('Download Profit Loss History')
            pd.DataFrame(wb.get_proft_loss_history()).to_csv('../../../python/account_detail/profit_loss_history.csv')

        if cfg.download_steps.trading_history:
            logging.info('Download Trading History')
            get_trading_history(wb.get_history_orders(date_start, date_end, status='FILLED', count=10000)).to_csv(
                '../../../python/account_detail/historical_order.csv')

        if cfg.download_steps.trading_history:
            logging.info('Download Net Liquidity')
            pd.DataFrame(wb.get_net_liquidity()).to_csv('../../../python/account_detail/net_liquidity_history.csv')

        if cfg.download_steps.yield_rate.my_portfolio:
            logging.info('Download Portfolio Performance')
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

        if cfg.download_steps.current_holding:
            logging.info('Download Current_holding')
            current_holding = wb.get_positions()
            current_holding = get_current_holding(current_holding).assign(Date=date_end)
            current_holding.to_csv('../../../python/account_detail/current_holding.csv')


if __name__ == '__main__':
    main()
