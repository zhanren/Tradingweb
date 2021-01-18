import pandas as pd

from python import helper


class Data():
    def __init__(self, local=True, write_result=False):

        self.local = local
        self.write_result = write_result
        self.wb = helper.webull_dashboard()

        if self.local:
            self.wb = helper.webull_dashboard()

        self.orders = self.get_orders()
        self.pl_history = self.get_pl_history()
        self.trading_tickers = self.get_history_stock_ticker(self.orders)

        return

    def get_orders(self):

        if self.local:
            orders = pd.read_csv('test_order.csv')

        else:
            orders = self.wb.get_trading_history(self.wb.orders)

        if self.write_result:
            orders.to_csv('test_order.csv')

        return orders

    def get_pl_history(self, method='local', write_result=False):

        if self.local:
            pl_history = pd.read_csv('test_pl_history.csv', header=0)

        else:
            pl_history = self.wb.get_profit_loss_history()

        if self.write_result:
            pl_history.to_csv('test_pl_history.csv')

        return pl_history

    def get_history_stock_ticker(self, trading_history):

        trading_company = trading_history.drop_duplicates(['Stock symbol', 'ticker', 'Company']).filter(
            ['Stock symbol', 'ticker', 'Company'], axis=1)

        return trading_company
